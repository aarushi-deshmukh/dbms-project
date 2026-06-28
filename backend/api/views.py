from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from .models import Buyer, Seller, Product, Cart, CartItem, Wishlist
from .serializers import (
    ProductSerializer,
    SignInSerializer,
    BuyerSignupSerializer,
    SellerSignupSerializer,
)
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger('api')

@api_view(['GET'])
def products(request):
    items = Product.objects.all()
    serializer = ProductSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ScopedRateThrottle])
def signin(request):
    request.throttle_scope = 'signin'
    serializer = SignInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    account_type = serializer.validated_data['account_type']

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        logger.warning('Signin failed: email not found %s', email)
        return Response({'success': False, 'message': 'User not found', 'data': None, 'error': 'User not found', 'code': 'user_not_found'}, status=status.HTTP_404_NOT_FOUND)

    if not check_password(password, user.password):
        logger.warning('Signin failed: invalid password for %s', email)
        return Response({'success': False, 'message': 'Invalid password', 'data': None, 'error': 'Invalid password', 'code': 'invalid_credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if account_type == 'Buyer':
        if not Buyer.objects.filter(user=user).exists():
            return Response({'success': False, 'message': 'Buyer account not found', 'data': None, 'error': 'Buyer account not found', 'code': 'account_not_found'}, status=status.HTTP_404_NOT_FOUND)
    elif account_type == 'Seller':
        if not Seller.objects.filter(user=user).exists():
            return Response({'success': False, 'message': 'Seller account not found', 'data': None, 'error': 'Seller account not found', 'code': 'account_not_found'}, status=status.HTTP_404_NOT_FOUND)

    refresh = RefreshToken.for_user(user)
    # Keep the legacy wrapper but also expose tokens and account_type at top-level
    return Response({
        'success': True,
        'message': 'Signed in successfully',
        'user_id': user.id,
        'email': user.email,
        'account_type': account_type,
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'data': {
            'user_id': user.id,
            'email': user.email,
            'account_type': account_type,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        },
        'error': None,
        'code': 'signed_in',
    })

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ScopedRateThrottle])
def signup_buyer(request):
    request.throttle_scope = 'signup'
    serializer = BuyerSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    validated = serializer.validated_data

    user = User.objects.create_user(
        username=validated['username'],
        email=validated['email'],
        password=validated['password'],
        first_name=validated['first_name'],
        last_name=validated['last_name'],
    )

    Buyer.objects.create(
        user=user,
        age=validated['age'],
        phone_number=validated['phone_number'],
        address=validated['address'],
        city=validated['city'],
        country=validated['country'],
        pincode=validated['pincode'],
    )

    return Response({
        'success': True,
        'message': 'Buyer account created successfully',
        'data': {'user_id': user.id, 'email': user.email},
        'error': None,
        'code': 'buyer_created',
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ScopedRateThrottle])
def signup_seller(request):
    request.throttle_scope = 'signup'
    serializer = SellerSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    validated = serializer.validated_data

    user = User.objects.create_user(
        username=validated['email'],
        email=validated['email'],
        password=validated['password'],
    )

    Seller.objects.create(
        user=user,
        company_name=validated['company_name'],
        contact_number=validated['contact_number'],
        address=validated['address'],
        city=validated['city'],
        country=validated['country'],
        pincode=validated['pincode'],
    )

    return Response({
        'success': True,
        'message': 'Seller account created successfully',
        'data': {'user_id': user.id, 'email': user.email},
        'error': None,
        'code': 'seller_created',
    }, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    # Frontend expects an array as the response body for products
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    data = request.data
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    buyer = Buyer.objects.get(user=request.user)
    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(buyer=buyer)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    return Response({
        'success': True,
        'message': 'Added to cart',
        'data': None,
        'error': None,
        'code': 'cart_item_added',
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    buyer = Buyer.objects.get(user=request.user)
    cart = Cart.objects.filter(buyer=buyer).first()
    if not cart:
        return Response({'items': []})

    items = CartItem.objects.filter(cart=cart)
    data = [
        {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'image': item.product.image.url if item.product.image else None,
            'brand': item.product.seller.company_name if item.product.seller else None,
        }
        for item in items
    ]

    # Frontend expects `res.data.items`
    return Response({'items': data})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):

    data = request.data
    product_id = data.get("product_id")

    buyer = Buyer.objects.get(user=request.user)

    product = Product.objects.get(id=product_id)

    Wishlist.objects.get_or_create(
        buyer=buyer,
        product=product
    )

    # preserve simple message shape for existing callers
    return Response({"message": "Added to wishlist"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    buyer = Buyer.objects.get(user=request.user)
    items = Wishlist.objects.filter(buyer=buyer)

    data = [
        {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'image': item.product.image.url if item.product.image else None,
        }
        for item in items
    ]
    # Frontend expects `res.data.items`
    return Response({'items': data})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, product_id):

    try:
        buyer = Buyer.objects.get(user=request.user)

        cart = Cart.objects.get(buyer=buyer)

        cart_item = CartItem.objects.get(
            cart=cart,
            product_id=product_id
        )

        cart_item.delete()

        return Response({"message": "Item removed from cart"})

    except CartItem.DoesNotExist:
        return Response(
            {"error": "Item not found in cart"},
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, product_id):

    try:
        buyer = Buyer.objects.get(user=request.user)

        wishlist_item = Wishlist.objects.get(
            buyer=buyer,
            product_id=product_id
        )

        wishlist_item.delete()

        return Response({"message": "Item removed from wishlist"})

    except Wishlist.DoesNotExist:
        return Response(
            {"error": "Item not found in wishlist"},
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):

    user = request.user

    # check if buyer
    if Buyer.objects.filter(user=user).exists():
        buyer = Buyer.objects.get(user=user)

        return Response({
            "account_type": "buyer",
            "name": user.first_name + " " + user.last_name,
            "email": user.email,
            "phone": buyer.phone_number,
            "address": buyer.address,
            "city": buyer.city,
            "country": buyer.country,
            "pincode": buyer.pincode,
            "age": buyer.age
        })

    # check if seller
    elif Seller.objects.filter(user=user).exists():
        seller = Seller.objects.get(user=user)

        return Response({
            "account_type": "seller",
            "company_name": seller.company_name,
            "email": user.email,
            "phone": seller.contact_number,
            "address": seller.address,
            "city": seller.city,
            "country": seller.country,
            "pincode": seller.pincode
        })

    return Response({"error": "Profile not found"}, status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_product(request):

    try:
        # ✅ get seller (IMPORTANT)
        seller = Seller.objects.get(user=request.user)

        product = Product.objects.create(
            seller=seller,
            name=request.data.get("name"),
            description=request.data.get("description"),
            price=request.data.get("price"),
            stock=request.data.get("quantity"),
            category=request.data.get("category"),
            image=request.FILES.get("image")
        )

        return Response({
            "success": True,
            "product_id": product.id
        })

    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(["GET"])
def get_product(request, id):
    try:
        product = Product.objects.get(id=id)

        return Response({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "quantity": product.stock,
            "category": product.category,
            "image": product.image.url if product.image else None,
            "brand": product.seller.company_name if product.seller else None
        })

    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
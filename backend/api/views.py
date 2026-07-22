from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from .models import Buyer, Seller, Product, Cart, CartItem, Wishlist
from .serializers import (
    ProductSerializer,
    SignInSerializer,
    BuyerSignupSerializer,
    SellerSignupSerializer,
    ShippingAddressSerializer,
    OrderSerializer,
    CheckoutSerializer,
    SellerOrderItemSerializer,
)
from .permissions import IsBuyer, IsSeller
from . import services
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger('api')

@api_view(['GET'])
def products(request):
    items = Product.objects.all().select_related('seller')
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
    products = Product.objects.all().select_related('seller')
    serializer = ProductSerializer(products, many=True)
    # Frontend expects an array as the response body for products
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsBuyer])
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
@permission_classes([IsAuthenticated, IsBuyer])
def get_cart(request):
    buyer = Buyer.objects.get(user=request.user)
    cart = Cart.objects.filter(buyer=buyer).first()
    if not cart:
        return Response({'items': []})

    items = CartItem.objects.filter(cart=cart).select_related('product__seller')
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
@permission_classes([IsAuthenticated, IsBuyer])
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
@permission_classes([IsAuthenticated, IsBuyer])
def get_wishlist(request):
    buyer = Buyer.objects.get(user=request.user)
    items = Wishlist.objects.filter(buyer=buyer).select_related('product')

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
@permission_classes([IsAuthenticated, IsBuyer])
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
@permission_classes([IsAuthenticated, IsBuyer])
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
@permission_classes([IsAuthenticated, IsSeller])
def add_product(request):
    try:
        seller = Seller.objects.get(user=request.user)

        serializer = ProductCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(seller=seller)
            return Response({
                "success": True,
                "product_id": serializer.instance.id
            })

        return Response(serializer.errors, status=400)

    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=400)

@api_view(["GET"])
def get_product(request, id):
    try:
        product = Product.objects.select_related('seller').get(id=id)

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


# ── Phase 3: Shipping Addresses ───────────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsBuyer])
def shipping_addresses(request):
    """List all shipping addresses for the authenticated buyer, or create a new one."""
    if request.method == 'GET':
        qs = services.get_shipping_addresses(request.user)
        serializer = ShippingAddressSerializer(qs, many=True)
        return Response({'success': True, 'data': serializer.data, 'error': None})

    # POST
    serializer = ShippingAddressSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    address = services.create_shipping_address(request.user, serializer.validated_data)
    return Response(
        {'success': True, 'data': ShippingAddressSerializer(address).data, 'error': None},
        status=status.HTTP_201_CREATED,
    )


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsBuyer])
def shipping_address_detail(request, address_id):
    """Update or delete a specific shipping address owned by the authenticated buyer."""
    if request.method == 'DELETE':
        services.delete_shipping_address(request.user, address_id)
        return Response({'success': True, 'message': 'Address deleted.', 'error': None})

    # PUT
    serializer = ShippingAddressSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    address = services.update_shipping_address(request.user, address_id, serializer.validated_data)
    return Response({'success': True, 'data': ShippingAddressSerializer(address).data, 'error': None})


# ── Phase 3: Checkout & Orders ────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsBuyer])
def place_order(request):
    """
    POST /api/place-order/
    Converts the buyer's active cart into a confirmed order (atomic).
    Body (all optional):
      { "shipping_address_id": <int|null>, "notes": "<str>" }
    """
    serializer = CheckoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        order = services.place_order_from_cart(
            user=request.user,
            shipping_address_id=serializer.validated_data.get('shipping_address_id'),
            notes=serializer.validated_data.get('notes'),
        )
    except ValidationError as exc:
        return Response(
            {'success': False, 'message': exc.detail, 'data': None, 'error': str(exc.detail), 'code': 'checkout_failed'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            'success': True,
            'message': 'Order placed successfully.',
            'data': OrderSerializer(order).data,
            'error': None,
            'code': 'order_placed',
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBuyer])
def order_history(request):
    """GET /api/orders/ — Returns the authenticated buyer's full order history."""
    orders = services.get_buyer_orders(request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response({'success': True, 'data': serializer.data, 'error': None})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsBuyer])
def cancel_order_view(request, order_id):
    """
    POST /api/orders/<order_id>/cancel/
    Cancels a pending or confirmed order and restores stock.
    """
    try:
        order = services.cancel_order(request.user, order_id)
    except ValidationError as exc:
        return Response(
            {'success': False, 'message': exc.detail, 'data': None, 'error': str(exc.detail), 'code': 'cancel_failed'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response({
        'success': True,
        'message': 'Order cancelled successfully.',
        'data': OrderSerializer(order).data,
        'error': None,
        'code': 'order_cancelled',
    })


# ── Phase 3: Product Deletion ─────────────────────────────────────────────────

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSeller])
def delete_product(request, product_id):
    """
    DELETE /api/products/<product_id>/
    Standard ID-based product deletion. The seller must own the product.
    Phase 5 migration target — this is the permanent endpoint.
    """
    try:
        services.delete_seller_product(request.user, product_id)
    except PermissionDenied as exc:
        return Response(
            {'success': False, 'message': str(exc.detail), 'error': str(exc.detail), 'code': 'permission_denied'},
            status=status.HTTP_403_FORBIDDEN,
        )

    return Response({
        'success': True,
        'message': 'Product deleted successfully.',
        'error': None,
        'code': 'product_deleted',
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsSeller])
def remove_product_legacy(request, name, brand):
    """
    DELETE /api/remove-product/<name>/<brand>/
    Legacy compatibility endpoint. Resolves name+brand to a product ID,
    validates seller ownership, then delegates to the same core deletion logic.

    COMPATIBILITY LAYER — do not extend. Migrate the frontend to
    DELETE /api/products/<id>/ in Phase 5 and then remove this view.
    """
    try:
        services.resolve_and_delete_product_by_name_brand(request.user, name, brand)
    except NotFound as exc:
        return Response(
            {'success': False, 'message': str(exc.detail), 'error': str(exc.detail), 'code': 'not_found'},
            status=status.HTTP_404_NOT_FOUND,
        )
    except PermissionDenied as exc:
        return Response(
            {'success': False, 'message': str(exc.detail), 'error': str(exc.detail), 'code': 'permission_denied'},
            status=status.HTTP_403_FORBIDDEN,
        )

    return Response({
        'success': True,
        'message': 'Product deleted successfully.',
        'error': None,
        'code': 'product_deleted',
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSeller])
def seller_products(request):
    """
    GET /api/seller/products/
    Returns products owned by the authenticated seller. Thin controller.
    """
    products_qs = services.get_seller_products(request.user)
    serializer = ProductSerializer(products_qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSeller])
def seller_orders(request):
    """
    GET /api/seller/orders/
    Returns fulfillment items for orders containing the seller's products. Thin controller.
    """
    order_items_qs = services.get_seller_orders(request.user)
    serializer = SellerOrderItemSerializer(order_items_qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSeller])
def seller_stats(request):
    """
    GET /api/seller/stats/
    Returns calculated portfolio analytics for the seller. Thin controller.
    """
    stats_data = services.get_seller_stats(request.user)
    return Response(stats_data)

from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .models import Buyer, Seller, Product, Cart, CartItem, Wishlist
from django.contrib.auth.models import User


def authenticate_user(email, password, account_type):
    user = get_object_or_404(User, email=email)
    if not check_password(password, user.password):
        raise ValueError('invalid_password')

    if account_type == 'Buyer' and not Buyer.objects.filter(user=user).exists():
        raise ValueError('buyer_not_found')

    if account_type == 'Seller' and not Seller.objects.filter(user=user).exists():
        raise ValueError('seller_not_found')

    return user


def create_buyer_account(validated_data):
    user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
    )
    Buyer.objects.create(
        user=user,
        age=validated_data['age'],
        phone_number=validated_data['phone_number'],
        address=validated_data['address'],
        city=validated_data['city'],
        country=validated_data['country'],
        pincode=validated_data['pincode'],
    )
    return user


def create_seller_account(validated_data):
    user = User.objects.create_user(
        username=validated_data['email'],
        email=validated_data['email'],
        password=validated_data['password'],
    )
    Seller.objects.create(
        user=user,
        company_name=validated_data['company_name'],
        contact_number=validated_data['contact_number'],
        address=validated_data['address'],
        city=validated_data['city'],
        country=validated_data['country'],
        pincode=validated_data['pincode'],
    )
    return user


def list_products():
    return Product.objects.all()


def get_product_detail(product_id):
    return get_object_or_404(Product, id=product_id)


def get_cart_items(user):
    buyer = get_object_or_404(Buyer, user=user)
    cart = Cart.objects.filter(buyer=buyer).first()
    if not cart:
        return []

    return [
        {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'image': item.product.image.url if item.product.image else None,
        }
        for item in CartItem.objects.filter(cart=cart)
    ]


def add_to_cart_item(user, product_id, quantity):
    buyer = get_object_or_404(Buyer, user=user)
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(buyer=buyer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()
    return cart_item


def remove_cart_item(user, product_id):
    buyer = get_object_or_404(Buyer, user=user)
    cart = get_object_or_404(Cart, buyer=buyer)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    return True


def get_wishlist_items(user):
    buyer = get_object_or_404(Buyer, user=user)
    return [
        {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'image': item.product.image.url if item.product.image else None,
        }
        for item in Wishlist.objects.filter(buyer=buyer)
    ]


def add_to_wishlist_item(user, product_id):
    buyer = get_object_or_404(Buyer, user=user)
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(buyer=buyer, product=product)
    return product


def remove_wishlist_item(user, product_id):
    buyer = get_object_or_404(Buyer, user=user)
    wishlist_item = get_object_or_404(Wishlist, buyer=buyer, product_id=product_id)
    wishlist_item.delete()
    return True


def get_profile_for_user(user):
    if Buyer.objects.filter(user=user).exists():
        buyer = Buyer.objects.get(user=user)
        return {
            'account_type': 'buyer',
            'name': f'{user.first_name} {user.last_name}',
            'email': user.email,
            'phone': buyer.phone_number,
            'address': buyer.address,
            'city': buyer.city,
            'country': buyer.country,
            'pincode': buyer.pincode,
            'age': buyer.age,
        }

    if Seller.objects.filter(user=user).exists():
        seller = Seller.objects.get(user=user)
        return {
            'account_type': 'seller',
            'company_name': seller.company_name,
            'email': user.email,
            'phone': seller.contact_number,
            'address': seller.address,
            'city': seller.city,
            'country': seller.country,
            'pincode': seller.pincode,
        }

    return None


def create_product_for_seller(user, validated_data):
    seller = get_object_or_404(Seller, user=user)
    product = Product.objects.create(seller=seller, **validated_data)
    return product

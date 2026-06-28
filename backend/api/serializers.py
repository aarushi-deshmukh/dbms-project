from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Product, Buyer, Seller, CartItem, Wishlist


class ProductSerializer(serializers.ModelSerializer):
    seller_company_name = serializers.CharField(source='seller.company_name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category',
            'image',
            'created_at',
            'seller_company_name',
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'stock',
            'category',
            'image',
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'product_id',
            'name',
            'price',
            'quantity',
            'image',
        ]

    def get_image(self, obj):
        return obj.product.image.url if obj.product.image else None


class WishlistItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = [
            'product_id',
            'name',
            'price',
            'image',
        ]

    def get_image(self, obj):
        return obj.product.image.url if obj.product.image else None


class ProfileSerializer(serializers.Serializer):
    account_type = serializers.CharField()
    email = serializers.EmailField()
    name = serializers.CharField(required=False)
    company_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    address = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()
    pincode = serializers.CharField()
    age = serializers.IntegerField(required=False)


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    account_type = serializers.ChoiceField(choices=['Buyer', 'Seller'])


class BuyerSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    age = serializers.IntegerField(min_value=0)
    phone_number = serializers.CharField(max_length=15)
    address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    pincode = serializers.CharField(max_length=10)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists.')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')

        if password_confirmation and password != password_confirmation:
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match.'})

        validate_password(password)
        return attrs


class SellerSignupSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True, required=False)
    contact_number = serializers.CharField(max_length=15)
    address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    pincode = serializers.CharField(max_length=10)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists.')
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')

        if password_confirmation and password != password_confirmation:
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match.'})

        validate_password(password)
        return attrs

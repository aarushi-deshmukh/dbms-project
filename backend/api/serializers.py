from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Product, Buyer, Seller, CartItem, Wishlist, ShippingAddress, Order, OrderItem


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
            'brand',
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


# ── Phase 3: Shipping, Orders & Checkout ─────────────────────────────────────

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            'id',
            'recipient_name',
            'phone_number',
            'address',
            'city',
            'state',
            'country',
            'pincode',
            'is_default',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializes an individual item within an order.
    Captures product name and the unit price locked at order-creation time.
    """
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product_id',
            'product_name',
            'product_image',
            'quantity',
            'unit_price',
            'total_price',
        ]

    def get_product_image(self, obj):
        return obj.product.image.url if obj.product.image else None


class OrderSerializer(serializers.ModelSerializer):
    """Full order representation including nested line items."""
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'status',
            'total_amount',
            'tax_amount',
            'shipping_cost',
            'notes',
            'shipping_address',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']


class CheckoutSerializer(serializers.Serializer):
    """
    Validates the request body for POST /api/place-order/.
    All fields are optional to maintain frontend compatibility:
    the service layer will fall back to the buyer's default address
    or auto-generate one from their profile if not provided.
    """
    shipping_address_id = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=500)


class SellerOrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for order items containing products belonging to a seller.
    Exposes order details, buyer email/name, and unit/total pricing.
    """
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    status = serializers.CharField(source='order.status', read_only=True)
    buyer_name = serializers.SerializerMethodField()
    buyer_email = serializers.EmailField(source='order.buyer.user.email', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    created_at = serializers.DateTimeField(source='order.created_at', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'order_number',
            'status',
            'buyer_name',
            'buyer_email',
            'product_name',
            'quantity',
            'unit_price',
            'total_price',
            'created_at',
        ]

    def get_buyer_name(self, obj):
        buyer_user = obj.order.buyer.user
        name = f"{buyer_user.first_name} {buyer_user.last_name}".strip()
        return name if name else buyer_user.username


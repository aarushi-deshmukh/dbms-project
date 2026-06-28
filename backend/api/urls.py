from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # AUTH
    path("signin/", views.signin),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/buyer/", views.signup_buyer),
    path("signup/seller/", views.signup_seller),
    path("profile/", views.profile),

    # PRODUCTS
    path("products/", views.get_products),
    path("add-product/", views.add_product),
    path("details/<int:id>/", views.get_product),

    # CART
    path("cart/", views.get_cart),
    path("cart/add/", views.add_to_cart),
    path("cart/remove/<int:product_id>/", views.remove_from_cart),

    # WISHLIST
    path("wishlist/", views.get_wishlist),
    path("wishlist/add/", views.add_to_wishlist),
    path("wishlist/remove/<int:product_id>/", views.remove_from_wishlist),

    # ── Phase 3: Shipping Addresses ───────────────────────────────────────────
    path("shipping-addresses/", views.shipping_addresses),
    path("shipping-addresses/<int:address_id>/", views.shipping_address_detail),

    # ── Phase 3: Checkout & Orders ────────────────────────────────────────────
    path("place-order/", views.place_order),
    path("orders/", views.order_history),
    path("orders/<int:order_id>/cancel/", views.cancel_order_view),

    # ── Phase 3: Product Deletion ─────────────────────────────────────────────
    # Standard ID-based endpoint (Phase 5 frontend migration target)
    path("products/<int:product_id>/", views.delete_product),
    # Legacy compatibility — preserves existing frontend DELETE calls
    path("remove-product/<str:name>/<str:brand>/", views.remove_product_legacy),

    # ── Phase 3: New Secure Seller Endpoints ──────────────────────────────────
    path("seller/products/", views.seller_products),
    path("seller/orders/", views.seller_orders),
    path("seller/stats/", views.seller_stats),

]
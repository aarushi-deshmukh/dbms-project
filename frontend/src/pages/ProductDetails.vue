<template>
  <div class="page-wrapper">
    <div v-if="product" class="product-container">

      <!-- Left: Image -->
      <div class="product-img-holder">
        <img :src="product.image || 'https://via.placeholder.com/500x500'" :alt="product.name" />
      </div>

      <!-- Right: Details -->
      <div class="product-details">
        <div class="meta-row">
          <span class="category-badge">{{ product.category }}</span>
          <span class="brand-tag">{{ product.brand }}</span>
        </div>

        <h1 class="product-title">{{ product.name }}</h1>

        <div class="product-price">₹{{ product.price }}</div>

        <div class="stock-row">
          <span class="stock-dot" :class="product.stock > 0 ? 'dot--green' : 'dot--red'"></span>
          <span class="stock-label">{{ product.stock > 0 ? `${product.stock} in stock` : 'Out of stock' }}</span>
        </div>

        <p class="product-description">{{ product.description }}</p>

        <div class="button-group">
          <button class="btn-cart" @click="addToCart(product.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
            Add to Cart
          </button>
          <button class="btn-wishlist" @click="addToWishlist(product.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
            Save for Later
          </button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-else class="loading">
      <div class="loading-spinner"></div>
      <p>Loading product...</p>
    </div>
  </div>
</template>

<script>
import api from '@/api'
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useCartStore } from "@/stores/cart";
import { useWishlistStore } from "@/stores/wishlist";

export default {
  setup() {
    const route = useRoute();
    const product = ref(null);
    const cartStore = useCartStore();
    const wishlistStore = useWishlistStore();

    const fetchProduct = async () => {
      const id = route.params.id;

      try {
        const res = await api.get(`details/${id}/`);
        product.value = res.data;
      } catch (err) {
        console.error('Error loading product:', err);
      }
    };

    const addToCart = async () => {
      if (!product.value) return;
      try {
        await cartStore.addItem(product.value.id, 1);
        alert("Added to cart");
      } catch (err) {
        console.error('Add to cart error:', err);
      }
    };

    const addToWishlist = async () => {
      if (!product.value) return;
      try {
        await wishlistStore.addItem(product.value.id);
        alert("Added to wishlist");
      } catch (err) {
        console.error('Add to wishlist error:', err);
      }
    };

    onMounted(fetchProduct);

    return {
      product,
      addToCart,
      addToWishlist
    };
  }
};
</script>

<style scoped>
* { box-sizing: border-box; }

.page-wrapper {
  margin-top: 70px;
  padding: 48px;
  background-color: #fafafa;
  min-height: calc(100vh - 70px);
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

/* ── Product layout ──────────────────────────────────────── */
.product-container {
  display: flex;
  gap: 48px;
  max-width: 1100px;
  width: 100%;
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 16px;
  overflow: hidden;
}

/* ── Image ───────────────────────────────────────────────── */
.product-img-holder {
  flex: 0 0 480px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 500px;
  overflow: hidden;
}

.product-img-holder img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ── Details ─────────────────────────────────────────────── */
.product-details {
  flex: 1;
  padding: 40px 40px 40px 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
  justify-content: center;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-badge {
  display: inline-block;
  padding: 3px 10px;
  background: #f5f5f5;
  color: #555;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.brand-tag {
  font-size: 12px;
  color: #a3a3a3;
  font-weight: 500;
}

.product-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.3;
}

.product-price {
  font-size: 26px;
  font-weight: 800;
  color: #1a1a1a;
}

.stock-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stock-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot--green { background: #16a34a; }
.dot--red { background: #dc2626; }

.stock-label {
  font-size: 13px;
  color: #737373;
  font-weight: 500;
}

.product-description {
  font-size: 14px;
  color: #555;
  line-height: 1.7;
  margin: 0;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

/* ── Buttons ─────────────────────────────────────────────── */
.button-group {
  display: flex;
  gap: 12px;
  padding-top: 8px;
}

.btn-cart,
.btn-wishlist {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
}

.btn-cart {
  background: #1a1a1a;
  color: #ffffff;
  flex: 1;
}
.btn-cart:hover { background: #000; transform: translateY(-1px); }

.btn-wishlist {
  background: #ffffff;
  color: #1a1a1a;
  border: 1px solid #d4d4d4;
  flex: 1;
}
.btn-wishlist:hover { background: #fafafa; border-color: #a3a3a3; }

/* ── Loading ─────────────────────────────────────────────── */
.loading {
  display: flex; flex-direction: column; align-items: center;
  gap: 16px; padding: 80px; color: #737373;
}
.loading-spinner {
  width: 40px; height: 40px;
  border: 3px solid #f0f0f0; border-top-color: #1a1a1a;
  border-radius: 50%; animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 860px) {
  .page-wrapper { padding: 24px 16px; }
  .product-container { flex-direction: column; gap: 0; }
  .product-img-holder { flex: none; height: 320px; min-height: unset; }
  .product-details { padding: 24px; }
}

@media (max-width: 480px) {
  .product-title { font-size: 22px; }
  .button-group { flex-direction: column; }
}
</style>
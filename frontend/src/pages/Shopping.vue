<template>
  <div class="dashboard">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1>Discover Amazing Products</h1>
        <p>Shop the latest trends with exclusive deals</p>
      </div>
    </section>

    <!-- Products Section -->
    <section class="products-section">
      <div class="section-header">
        <h2 class="section-title">Featured Products</h2>
        <div class="filter-chips">
          <button :class="['chip', { active: selectedCategory === 'all' }]" @click="filterCategory('all')">
            All
          </button>
          <button v-for="category in categories" :key="category"
            :class="['chip', { active: selectedCategory === category }]" @click="filterCategory(category)">
            {{ category }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading products...</p>
      </div>

      <div v-else-if="error" class="error">{{ error }}</div>

      <div class="product-grid" v-else>
        <div class="product-card" v-for="product in filteredProducts" :key="product.id"
          @click="goToDetails(product.id)">
          <div class="image-zone">
            <img :src="product.image" :alt="product.name" class="product-img" />
            <button class="wishlist-btn" @click.stop="addToWishlist(product)" :class="{ active: product.saved }">
              <svg viewBox="0 0 24 24">
                <path
                  d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
              </svg>
            </button>
            <span class="category-tag">{{ product.category }}</span>
          </div>

          <div class="card-body">
            <div class="product-brand">{{ product.brand }}</div>
            <h3 class="product-name">{{ product.name }}</h3>

            <div class="divider"></div>

            <div class="price-row">
              <span class="price">₹{{ product.price }}</span>
              <span class="stock-badge" :class="{ low: product.quantity < 10 }">
                {{ product.quantity }} in stock
              </span>
            </div>

            <div class="qty-row">
              <span class="qty-label">Qty</span>
              <div class="qty-control">
                <button class="qty-btn" @click.stop="changeQty(product, -1)">−</button>
                <span class="qty-num">{{ product.userQuantity }}</span>
                <button class="qty-btn" @click.stop="changeQty(product, 1)">+</button>
              </div>
            </div>

            <button class="add-btn" @click.stop="addToCart(product)" :disabled="product.added">
              <svg v-if="!product.added" viewBox="0 0 24 24">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
              <svg v-else viewBox="0 0 24 24">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>{{ product.added ? 'Added to Cart' : 'Add to Cart' }}</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->

  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { fetchProducts as getProducts, fetchCart, addToCart as addCartItem, fetchWishlist, addWishlistItem as addWishItem } from "@/services";

export default {
  setup() {
    const router = useRouter();
    const products = ref([]);
    const searchQuery = ref("");
    const loading = ref(true);
    const error = ref(null);
    const cartTotal = ref(0);
    const wishlistTotal = ref(0);
    const selectedCategory = ref("all");
    const categories = ref([]);

    const displayCategories = [
      { name: "Electronics", image: "/categories/electronics.jpg" },
      { name: "Make-up", image: "/categories/makeup.jpg" },
      { name: "Clothes", image: "/categories/clothes.jpg" },
      { name: "Shoes", image: "/categories/shoes.jpg" },
      { name: "Accessories", image: "/categories/accessories.jpg" },
      { name: "Books", image: "/categories/books.jpg" },
      { name: "Home Appliances", image: "/categories/home-appliances.jpg" }
    ];

    const fetchProducts = async () => {
      try {
        const data = await getProducts();

        products.value = data.map(p => ({
          ...p,
          userQuantity: 1,
          added: false,
          saved: false
        }));

        categories.value = [...new Set(products.value.map(p => p.category))];

      } catch {
        error.value = "Failed to fetch products";
      } finally {
        loading.value = false;
      }
    };
    const changeQty = (product, delta) => {
      if (product.added) return;
      product.userQuantity = Math.max(1, Math.min(product.quantity, product.userQuantity + delta));
    };

    const addToCart = async (product) => {
      try {
        await addCartItem(product.id, product.userQuantity || 1);

        product.added = true;

        // refresh count properly
        const cartItems = await fetchCart();
        cartTotal.value = cartItems.length;

      } catch (err) {
        console.error("Failed to add to cart:", err);
      }
    };

    const addToWishlist = async (product) => {
      try {
        await addWishItem(product.id);

        product.saved = true;

        const wishlistItems = await fetchWishlist();
        wishlistTotal.value = wishlistItems.length;

      } catch (err) {
        console.error("Failed to add to wishlist:", err);
      }
    };

    const goToDetails = (id) => {
      router.push(`/details/${id}`);
    };

    const filterCategory = (category) => {
      selectedCategory.value = category;
    };

    const filteredProducts = computed(() => {
      return products.value.filter(p => {
        const matchName = p.name.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchCategory = selectedCategory.value === "all" || p.category === selectedCategory.value;
        return matchName && matchCategory;
      });
    });

    onMounted(() => {
      fetchProducts();
    });

    return {
      filterCategory,
      goToDetails,
      addToCart,
      addToWishlist,
      changeQty,
      selectedCategory,
      categories,
      loading,
      error,
      filteredProducts
    };
  }
};
</script>

<style scoped>
/* ── Palette ── */
:root {
  --cream: #F5F0E8;
  --parchment: #EDE4D3;
  --sand: #D4C4A8;
  --caramel: #B8996E;
  --mocha: #8B6B45;
  --espresso: #5C3D2E;
  --dark: #2C1A0E;
  --warm-white: #FAF7F2;
  --blush: #E8DDD0;
}

/* ── Base ── */
.dashboard {
  min-height: 100vh;
  background: var(--warm-white);
  padding-top: 70px;
}

/* ── Hero ── */
.hero-section {
  background: linear-gradient(135deg, #8B6B45 0%, #5C3D2E 100%);
  color: white;
  padding: 80px 24px;
  text-align: center;
  margin-bottom: 48px;
}

.hero-content h1 {
  font-size: 3rem;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--warm-white);
}

.hero-content p {
  font-size: 1.2rem;
  opacity: 0.85;
  font-weight: 300;
}

/* ── Products Section ── */
.products-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px 60px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  font-weight: 600;
  color: var(--dark);
}

/* Filter Chips */
.filter-chips {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.chip {
  padding: 7px 18px;
  border: 1.5px solid var(--sand);
  background: var(--cream);
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.25s ease;
  font-size: 0.9rem;
  font-weight: 400;
  color: white;
  font-family: 'Jost', sans-serif;
}

.chip:hover {
  border-color: var(--caramel);
  color: var(--espresso);
}

.chip.active {
  background: var(--espresso);
  color: var(--parchment);
  border-color: var(--espresso);
}

/* Loading / Error */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  gap: 16px;
  color: var(--mocha);
}

.spinner {
  width: 44px;
  height: 44px;
  border: 3px solid var(--sand);
  border-top-color: var(--espresso);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error {
  text-align: center;
  padding: 60px 20px;
  color: var(--espresso);
  font-size: 1.1rem;
}

/* ── Product Grid ── */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 28px;
}

/* ── Product Card ── */
.product-card {
  background: var(--cream);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--sand);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(92, 61, 46, 0.12);
}

/* Image Zone */
.image-zone {
  position: relative;
  width: 100%;
  height: 280px;
  overflow: hidden;
  background: var(--parchment);
  cursor: pointer;
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.image-zone:hover .product-img {
  transform: scale(1.05);
}

.wishlist-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(250, 247, 242, 0.92);
  border: 1px solid var(--sand);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.25s ease;
}

.wishlist-btn:hover {
  border-color: var(--caramel);
  transform: scale(1.1);
}

.wishlist-btn svg {
  width: 16px;
  height: 16px;
  fill: none;
  stroke: var(--mocha);
  stroke-width: 1.8;
  transition: all 0.25s ease;
}

.wishlist-btn.active svg {
  fill: var(--mocha);
  stroke: var(--mocha);
}

.category-tag {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: rgba(92, 61, 46, 0.82);
  color: var(--parchment);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 5px 12px;
  border-radius: 20px;
  font-family: 'Jost', sans-serif;
}

/* Card Body */
.card-body {
  padding: 20px 20px 22px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.product-brand {
  font-size: 10px;
  font-weight: 400;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--mocha);
  opacity: 0.75;
  margin-bottom: 5px;
}

.product-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--dark);
  line-height: 1.35;
  cursor: pointer;
  transition: color 0.2s;
  margin-bottom: 0;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-name:hover {
  color: var(--espresso);
}

.divider {
  height: 1px;
  background: var(--blush);
  margin: 14px 0;
}

.price-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 14px;
}

.price {
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--espresso);
}

.stock-badge {
  font-size: 11px;
  font-weight: 400;
  color: var(--mocha);
  background: var(--parchment);
  border: 1px solid var(--sand);
  padding: 3px 10px;
  border-radius: 20px;
}

.stock-badge.low {
  color: #8B5E3C;
  background: #F5EBD9;
  border-color: #D4A574;
}

/* Qty Control */
.qty-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.qty-label {
  font-size: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--mocha);
  opacity: 0.7;
  flex-shrink: 0;
}

.qty-control {
  display: flex;
  align-items: center;
  background: var(--parchment);
  border: 1px solid var(--sand);
  border-radius: 8px;
  overflow: hidden;
}

.qty-btn {
  width: 32px;
  height: 32px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--espresso);
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  font-family: 'Jost', sans-serif;
}

.qty-btn:hover {
  background: var(--sand);
}

.qty-num {
  width: 36px;
  text-align: center;
  font-size: 14px;
  font-weight: 500;
  color: var(--dark);
  border-left: 1px solid var(--sand);
  border-right: 1px solid var(--sand);
  line-height: 32px;
}

/* Add to Cart Button */
.add-btn {
  width: 100%;
  padding: 12px;
  background: var(--espresso);
  color: var(--parchment);
  border: none;
  border-radius: 10px;
  font-family: 'Jost', sans-serif;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  transition: all 0.3s ease;
  margin-top: auto;
}

.add-btn:hover:not(:disabled) {
  background: var(--dark);
  transform: translateY(-1px);
}

.add-btn:disabled {
  background: var(--caramel);
  cursor: not-allowed;
  opacity: 0.95;
  transform: none;
}

.add-btn svg {
  width: 15px;
  height: 15px;
  stroke: currentColor;
  fill: none;
  stroke-width: 2;
  flex-shrink: 0;
}



/* ── Responsive ── */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }

  .hero-content p {
    font-size: 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 18px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .categories-title {
    font-size: 1.75rem;
  }
}
</style>
<script setup>
import { computed } from "vue"
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authStore = useAuthStore()

const userType = computed(() => authStore.userType)
const showCategoryDropdown = ref(false)
const searchQuery = ref("")

const categories = ref([
  { label: 'All Products', value: 'all' },
  { label: 'Electronics', value: 'Electronics' },
  { label: 'Clothing', value: 'Clothing' },
  { label: 'Shoes', value: 'Shoes' },
  { label: 'Accessories', value: 'Accessories' },
  { label: 'Books', value: 'Books' },
  { label: 'Home Appliances', value: 'Home-Appliances' }
])

function toggleCategories() {
  showCategoryDropdown.value = !showCategoryDropdown.value
}

function selectCategory(category) {
  console.log("Selected category:", category)
  showCategoryDropdown.value = false
}

function goHome() {
  router.push("/")
}

function logout(){
  authStore.logout()
  router.push("/signin")
}
</script>

<template>
<nav class="navbar">

  <!-- LEFT -->
  <div class="nav-left">
    <div class="logo" @click="goHome">PARS</div>

    <!-- Categories only for buyers -->
    <div v-if="userType === 'buyer'" class="categories-wrapper">
      <div @click="toggleCategories" class="categories-btn">
        Categories
        <span class="dropdown-icon" :class="{ rotated: showCategoryDropdown }">▾</span>
      </div>

      <div v-if="showCategoryDropdown" class="category-dropdown">
        <div
          v-for="cat in categories"
          :key="cat.value"
          @click="selectCategory(cat.value)"
          class="category-item"
        >
          {{ cat.label }}
        </div>
      </div>
    </div>
  </div>


  <!-- SEARCH -->
  <div class="search-wrapper">
    <input
      v-model="searchQuery"
      placeholder="Search products..."
      class="search-bar"
    />
  </div>


  <!-- RIGHT -->
  <div class="nav-right">

    <!-- GUEST -->
    <div v-if="!userType" class="guest-links">
      <router-link to="/signin" class="btn-outline">Sign In</router-link>
      <router-link to="/signup" class="btn-solid">Sign Up</router-link>
    </div>

    <!-- BUYER -->
    <ul v-if="userType === 'buyer'" class="nav-links">
      <li @click="$router.push('/history')">History</li>
      <li @click="$router.push('/wishlist')">Wishlist</li>
      <li @click="$router.push('/cart')">Cart</li>
      <li @click="$router.push('/profile')">Profile</li>
    </ul>

    <!-- SELLER -->
    <ul v-if="userType === 'seller'" class="nav-links">
      <li @click="$router.push('/add-product')">Add Products</li>
      <li @click="$router.push('/my-products')">My Products</li>
      <li @click="$router.push('/analysis')">Analysis</li>
      <li @click="$router.push('/profile')">Profile</li>
    </ul>

  </div>

</nav>
</template>

<style scoped>
.btn-outline, .btn-solid {
  padding: 10px 24px;
  border-radius: 24px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #1a1a1a;
  text-decoration: none;
}

.btn-outline {
  background: transparent;
  color: #1a1a1a;
}

.btn-outline:hover {
  background: #f5f5f5;
}

.btn-solid {
  background: #1a1a1a;
  color: #fff;
}

.btn-solid:hover {
  background: #333;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  padding: 16px 40px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  height: 70px;
  box-sizing: border-box;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-right {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  cursor: pointer;
  color: #1a1a1a;
  letter-spacing: 1px;
}

/* Guest Links */
.guest-links {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Categories Dropdown */
.categories-wrapper {
  position: relative;
}

.categories-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: background-color 0.2s;
  font-weight: 500;
  color: #333;
  user-select: none;
}

.categories-btn:hover {
  background-color: #f5f5f5;
}

.dropdown-icon {
  transition: transform 0.3s ease;
  display: inline-block;
}

.dropdown-icon.rotated {
  transform: rotate(180deg);
}

.category-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  background: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 8px;
  border-radius: 12px;
  min-width: 200px;
  z-index: 1100;
  border: 1px solid #e5e5e5;
}

.category-item {
  padding: 12px 16px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s;
  font-weight: 500;
  color: #333;
}

.category-item:hover {
  background-color: #f5f5f5;
}

/* Search Bar */
.search-wrapper {
  flex: 1;
  max-width: 500px;
  margin: 0 32px;
}

.search-bar {
  width: 100%;
  padding: 10px 20px;
  border: 2px solid #e5e5e5;
  border-radius: 24px;
  font-size: 0.95rem;
  outline: none;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.search-bar:focus {
  border-color: #1a1a1a;
  box-shadow: 0 0 0 3px rgba(26, 26, 26, 0.1);
}

.search-bar::placeholder {
  color: #aaa;
}

/* Nav Links */
.nav-links {
  list-style: none;
  display: flex;
  gap: 30px;
  color: #1a1a1a;
  cursor: pointer;
  margin: 0;
  padding: 0;
  align-items: center;
}

.nav-links li {
  transition: color 0.2s;
  position: relative;
  font-weight: 500;
  font-size: 0.95rem;
}

.nav-links li:hover {
  color: #666;
}

.logout-link {
  color: #888 !important;
}

.logout-link:hover {
  color: #e00 !important;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .navbar {
    padding: 16px 24px;
  }

  .nav-left {
    gap: 16px;
  }

  .search-wrapper {
    max-width: 400px;
    margin: 0 24px;
  }

  .nav-links {
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .navbar {
    flex-wrap: wrap;
    padding: 12px 20px;
    height: auto;
  }

  .nav-left {
    width: 100%;
    justify-content: space-between;
    margin-bottom: 12px;
  }

  .search-wrapper {
    width: 100%;
    max-width: 100%;
    margin: 0;
    order: 3;
  }

  .nav-right {
    width: 100%;
    margin-top: 12px;
  }

  .nav-links {
    width: 100%;
    justify-content: space-between;
    gap: 12px;
    font-size: 0.85rem;
  }

  .category-dropdown {
    max-height: 300px;
    overflow-y: auto;
  }
}
</style>
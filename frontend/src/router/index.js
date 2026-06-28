import { createRouter, createWebHistory } from "vue-router"

import MainLayout from "@/layouts/MainLayout.vue"
import AuthLayout from "@/layouts/AuthLayout.vue"

import SignIn from "@/pages/Auth/SignIn.vue"
import SignUp from "@/pages/Auth/SignUp.vue"

import Home from "@/pages/Dashboard.vue"
import Shopping from "@/pages/Shopping.vue"
import Profile from '@/pages/Profile.vue'
import ProductDetails from '@/pages/ProductDetails.vue'

import Cart from '@/pages/Buyer/Cart.vue'
import Wishlist from '@/pages/Buyer/Wishlist.vue'
import History from '@/pages/Buyer/History.vue' 

import MyProducts from '@/pages/Seller/MyProducts.vue'
import AddProducts from '@/pages/Seller/AddProducts.vue'
import Analysis from '@/pages/Seller/Analysis.vue'

const routes = [

  {
    path: "/",
    component: MainLayout,
    children: [
      // Shared urls
      { path: '', component: Home },
      { path: 'shopping', component: Shopping },
      { path: 'details/:id', component: ProductDetails },
      { path: 'profile', component: Profile },

      // Buyer
      { path: 'cart', component: Cart },
      { path: 'history', component: History },
      { path: 'wishlist', component: Wishlist },

      // Seller
      { path: 'add-product', component: AddProducts },
      { path: 'my-products', component: MyProducts },
      { path: 'analysis', component: Analysis },
    ]
  },

  {
    path: "/",
    component: AuthLayout,
    children: [
      { path: "signin", component: SignIn },
      { path: "signup", component: SignUp }
    ]
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access")
  const userType = localStorage.getItem("user_type") // 'buyer' or 'seller'

  const authPages = ["/signin", "/signup"]
  const isAuthPage = authPages.includes(to.path)

  // Protected buyer paths
  const buyerPaths = ["/cart", "/history", "/wishlist"]
  const isBuyerPath = buyerPaths.includes(to.path)

  // Protected seller paths
  const sellerPaths = ["/add-product", "/my-products", "/analysis"]
  const isSellerPath = sellerPaths.includes(to.path)

  if (!token) {
    // Unauthenticated
    if (isBuyerPath || isSellerPath || to.path === "/profile") {
      next("/signin")
    } else {
      next()
    }
  } else {
    // Authenticated
    if (isAuthPage) {
      next(userType === "seller" ? "/my-products" : "/")
    } else if (isBuyerPath && userType !== "buyer") {
      next("/my-products") // Redirect unauthorized sellers to seller dashboard
    } else if (isSellerPath && userType !== "seller") {
      next("/") // Redirect unauthorized buyers to buyer dashboard
    } else {
      next()
    }
  }
})

export default router
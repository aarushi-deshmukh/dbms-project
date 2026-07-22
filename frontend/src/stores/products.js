import { defineStore } from "pinia";
import api from "@/api";

export const useProductsStore = defineStore("products", {
  state: () => ({
    products: [],
    sellerProducts: [],
    stats: {},
    loading: false,
    error: null,
  }),
  actions: {
    async fetchProducts() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("products/");
        this.products = res.data;
        return this.products;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async fetchSellerProducts() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("seller/products/");
        this.sellerProducts = res.data;
        return this.sellerProducts;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async fetchSellerStats() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("seller/stats/");
        this.stats = res.data;
        return this.stats;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async addProduct(formData) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.post("add-product/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async updateProduct(productId, formData) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.patch(`products/${productId}/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        // Replace the updated product in the local list
        const updated = res.data?.data || res.data;
        const idx = this.sellerProducts.findIndex((p) => p.id === productId);
        if (idx !== -1 && updated) {
          this.sellerProducts[idx] = { ...this.sellerProducts[idx], ...updated };
        }
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async deleteProduct(productId) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.delete(`products/${productId}/`);
        this.sellerProducts = this.sellerProducts.filter((p) => p.id !== productId);
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async deleteProductLegacy(name, brand) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.delete(`remove-product/${name}/${brand}/`);
        this.sellerProducts = this.sellerProducts.filter(
          (p) => !(p.name === name && p.brand === brand)
        );
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});

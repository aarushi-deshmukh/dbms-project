<template>
  <div class="page-wrapper">
    <div class="page-header">
      <div class="page-header-text">
        <h1>My Products</h1>
        <p class="subtitle">Manage and track your product inventory</p>
      </div>
      <button @click="goToAddProducts" class="btn-add-product">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Add Product
      </button>
    </div>

    <div class="page-body">
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>Loading products...</p>
      </div>

      <div v-else-if="filteredProducts.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
        </svg>
        <h3>No products found</h3>
        <p>Start by adding your first product</p>
        <button @click="goToAddProducts" class="btn-add-first">Add Your First Product</button>
      </div>

      <div v-else class="product-grid">
        <div class="product-card" v-for="product in filteredProducts" :key="product.id">
          <!-- Image -->
          <div class="card-image">
            <img
              v-if="product.image"
              :src="product.image"
              :alt="product.name"
              @error="e => e.target.style.display='none'"
            />
            <div v-else class="img-placeholder">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
            </div>
          </div>

          <!-- Info -->
          <div class="card-body">
            <span class="card-category">{{ product.category }}</span>
            <h3 class="card-name">{{ product.name }}</h3>
            <p class="card-brand">{{ product.brand || product.seller_company_name || '' }}</p>

            <div class="card-details">
              <div class="detail-row">
                <span class="detail-label">Price</span>
                <span class="detail-value">₹{{ formatPrice(product.price) }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Quantity</span>
                <span class="detail-value" :class="product.stock <= 10 ? 'qty--low' : ''">
                  {{ product.stock }}
                </span>
              </div>
            </div>

            <div class="card-actions">
              <button class="btn-edit" @click="openEditModal(product)">Edit</button>
              <button class="btn-delete" @click="confirmRemoveProduct(product)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-content" @click.stop>
        <h3>Delete Product</h3>
        <p>Are you sure you want to delete <strong>{{ productToDelete?.name }}</strong>?</p>
        <div class="modal-actions">
          <button @click="showDeleteModal = false" class="btn-modal-cancel">Cancel</button>
          <button @click="removeProduct" class="btn-modal-delete" :disabled="loading">
            {{ loading ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Product Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content modal-edit" @click.stop>
        <div class="modal-header">
          <h3>Edit Product</h3>
          <button class="btn-modal-close" @click="closeEditModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveEditProduct" class="edit-form">
          <!-- Image upload -->
          <div class="form-group">
            <label>Product Image</label>
            <div class="edit-image-preview" v-if="editImagePreview || editProduct.image">
              <img :src="editImagePreview || editProduct.image" alt="Preview" />
              <button type="button" class="btn-remove-img" @click="removeEditImage">Remove</button>
            </div>
            <input type="file" ref="editFileInput" @change="handleEditImageSelect" accept="image/*" style="display:none" />
            <button type="button" class="btn-upload-img" @click="$refs.editFileInput.click()">
              {{ editImagePreview || editProduct.image ? 'Change Image' : 'Upload Image' }}
            </button>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Product Name <span class="required">*</span></label>
              <input type="text" v-model="editProduct.name" required />
            </div>
            <div class="form-group">
              <label>Price (₹) <span class="required">*</span></label>
              <input type="number" v-model="editProduct.price" step="0.01" min="0" required />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Category</label>
              <select v-model="editProduct.category">
                <option value="">Select Category</option>
                <option value="clothing">Clothing</option>
                <option value="shoes">Shoes</option>
                <option value="accessories">Accessories</option>
                <option value="books">Books</option>
                <option value="home-appliances">Home Appliances</option>
                <option value="electronics">Electronics</option>
              </select>
            </div>
            <div class="form-group">
              <label>Quantity <span class="required">*</span></label>
              <input type="number" v-model="editProduct.stock" min="0" required />
            </div>
          </div>

          <div class="form-group">
            <label>Description <span class="required">*</span></label>
            <textarea v-model="editProduct.description" rows="3" required></textarea>
          </div>

          <div v-if="editError" class="edit-error">{{ editError }}</div>

          <div class="modal-actions">
            <button type="button" @click="closeEditModal" class="btn-modal-cancel">Cancel</button>
            <button type="submit" class="btn-modal-save" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useProductsStore } from "@/stores/products";
import { useRouter } from "vue-router";

export default {
  setup() {
    const productsStore = useProductsStore();
    const searchQuery = ref("");
    const selectedCategory = ref("all");
    const showDeleteModal = ref(false);
    const productToDelete = ref(null);
    const showEditModal = ref(false);
    const editProduct = ref({});
    const editImageFile = ref(null);
    const editImagePreview = ref(null);
    const editFileInput = ref(null);
    const editError = ref(null);
    const saving = ref(false);
    const router = useRouter();

    const fetchProducts = async () => {
      try {
        await productsStore.fetchSellerProducts();
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    const confirmRemoveProduct = (product) => {
      productToDelete.value = product;
      showDeleteModal.value = true;
    };

    const removeProduct = async () => {
      try {
        const product = productToDelete.value;
        // Prefer the ID-based endpoint; fall back to legacy if ID is missing
        if (product.id) {
          await productsStore.deleteProduct(product.id);
        } else {
          await productsStore.deleteProductLegacy(product.name, product.brand);
        }
        showDeleteModal.value = false;
        productToDelete.value = null;
      } catch (error) {
        console.error("Error removing product:", error);
        alert("Failed to delete product. Please try again.");
      }
    };

    // ── Edit helpers ───────────────────────────────────────────────────────
    const openEditModal = (product) => {
      editProduct.value = {
        id: product.id,
        name: product.name,
        description: product.description,
        price: product.price,
        stock: product.stock,
        category: product.category || '',
        image: product.image || null,
      };
      editImageFile.value = null;
      editImagePreview.value = null;
      editError.value = null;
      showEditModal.value = true;
    };

    const closeEditModal = () => {
      showEditModal.value = false;
      editImageFile.value = null;
      editImagePreview.value = null;
      editError.value = null;
    };

    const handleEditImageSelect = (e) => {
      const file = e.target.files[0];
      if (!file) return;
      if (file.size > 5 * 1024 * 1024) {
        alert('Image must be under 5MB');
        return;
      }
      editImageFile.value = file;
      const reader = new FileReader();
      reader.onload = (ev) => { editImagePreview.value = ev.target.result; };
      reader.readAsDataURL(file);
    };

    const removeEditImage = () => {
      editImageFile.value = null;
      editImagePreview.value = null;
      editProduct.value.image = null;
      if (editFileInput.value) editFileInput.value.value = '';
    };

    const saveEditProduct = async () => {
      saving.value = true;
      editError.value = null;
      try {
        const formData = new FormData();
        formData.append('name', editProduct.value.name);
        formData.append('description', editProduct.value.description);
        formData.append('price', editProduct.value.price);
        formData.append('stock', editProduct.value.stock);
        if (editProduct.value.category) {
          formData.append('category', editProduct.value.category);
        }
        if (editImageFile.value) {
          formData.append('image', editImageFile.value);
        }

        await productsStore.updateProduct(editProduct.value.id, formData);
        closeEditModal();
        // Refresh to get latest data (including Cloudinary URL if image changed)
        await productsStore.fetchSellerProducts();
      } catch (err) {
        editError.value = err.response?.data?.message || err.message || 'Failed to update product.';
      } finally {
        saving.value = false;
      }
    };

    const formatPrice = (price) => parseFloat(price).toFixed(2);

    onMounted(fetchProducts);

    const products = computed(() => productsStore.sellerProducts);

    const filteredProducts = computed(() =>
      products.value.filter(product => {
        const brand = product.brand || product.seller_company_name || '';
        const matchCategory = selectedCategory.value === "all" ||
          (product.category || '').toLowerCase() === selectedCategory.value.toLowerCase();
        const matchSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          brand.toLowerCase().includes(searchQuery.value.toLowerCase());
        return matchCategory && matchSearch;
      })
    );

    const goToAddProducts = () => router.push("/add-product");

    return {
      products, searchQuery, selectedCategory,
      loading: computed(() => productsStore.loading),
      showDeleteModal, productToDelete, filteredProducts,
      goToAddProducts, confirmRemoveProduct, removeProduct,
      showEditModal, editProduct, editImagePreview, editFileInput,
      editError, saving,
      openEditModal, closeEditModal, handleEditImageSelect,
      removeEditImage, saveEditProduct, formatPrice,
    };
  }
};
</script>

<style scoped>
* { box-sizing: border-box; }

.page-wrapper {
  margin-top: 70px;
  padding: 40px 48px;
  background-color: #ffffff;
  min-height: calc(100vh - 70px);
  display: flex;
  flex-direction: column;
}

/* ── Header ──────────────────────────────────────────────── */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 32px;
  gap: 16px;
  flex-shrink: 0;
}

.page-header-text { display: flex; flex-direction: column; gap: 4px; }
.page-header h1 { font-size: 26px; font-weight: 700; margin: 0; color: #1a1a1a; line-height: 1.2; }
.subtitle { font-size: 13px; color: #737373; margin: 0; }

.btn-add-product {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background-color: #1a1a1a;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  transition: background-color 0.2s ease, transform 0.15s ease;
}
.btn-add-product:hover { background-color: #000; transform: translateY(-1px); }

/* ── Body ────────────────────────────────────────────────── */
.page-body { flex: 1; }

/* ── Loading ─────────────────────────────────────────────── */
.loading {
  display: flex; flex-direction: column; align-items: center;
  gap: 16px; padding: 80px 20px; color: #737373; text-align: center;
}
.loading-spinner {
  width: 40px; height: 40px;
  border: 3px solid #f0f0f0; border-top-color: #1a1a1a;
  border-radius: 50%; animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Empty state ─────────────────────────────────────────── */
.empty-state {
  display: flex; flex-direction: column; align-items: center;
  gap: 14px; padding: 80px 20px; text-align: center;
}
.empty-state svg { stroke: #d4d4d4; }
.empty-state h3 { font-size: 18px; font-weight: 600; color: #1a1a1a; margin: 0; }
.empty-state p { font-size: 14px; color: #737373; margin: 0; }

.btn-add-first {
  margin-top: 8px; padding: 10px 24px;
  background: #1a1a1a; color: #ffffff;
  border: none; border-radius: 8px;
  font-size: 14px; font-weight: 500; cursor: pointer;
  transition: background-color 0.2s ease;
}
.btn-add-first:hover { background: #000; }

/* ── Product grid ────────────────────────────────────────── */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* ── Product card ────────────────────────────────────────── */
.product-card {
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.product-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.09);
  transform: translateY(-3px);
}

/* Image */
.card-image {
  width: 100%;
  height: 220px;
  background-color: #f5f5f5;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.img-placeholder { display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; }
.img-placeholder svg { stroke: #d4d4d4; }

/* Body */
.card-body {
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.card-category {
  font-size: 10px;
  font-weight: 700;
  color: #a3a3a3;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-name {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.3;
}

.card-brand {
  font-size: 12px;
  color: #a3a3a3;
  margin: 0 0 8px 0;
}

/* Details */
.card-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 14px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label { font-size: 13px; color: #737373; }
.detail-value { font-size: 13px; font-weight: 700; color: #1a1a1a; }
.qty--low { color: #dc2626; }

/* Actions */
.card-actions {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

.btn-edit, .btn-delete {
  flex: 1;
  padding: 9px 0;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.15s ease;
}

.btn-edit {
  background: #1a1a1a;
  color: #ffffff;
}
.btn-edit:hover { background: #000; transform: translateY(-1px); }

.btn-delete {
  background: transparent;
  color: #dc2626;
  border: 1px solid #dc2626;
}
.btn-delete:hover { background: #dc2626; color: #ffffff; }

/* ── Modal shared ─────────────────────────────────────────── */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex; align-items: center; justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: #ffffff;
  border-radius: 12px;
  padding: 28px 32px;
  max-width: 420px; width: 90%;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.18);
}

.modal-content h3 { font-size: 18px; font-weight: 600; color: #1a1a1a; margin: 0 0 10px 0; }
.modal-content p { font-size: 14px; color: #737373; margin: 0 0 24px 0; line-height: 1.6; }
.modal-content p strong { color: #1a1a1a; }

.modal-actions { display: flex; gap: 10px; justify-content: flex-end; }

.btn-modal-cancel, .btn-modal-delete, .btn-modal-save {
  padding: 9px 22px; border-radius: 8px;
  font-size: 14px; font-weight: 500; cursor: pointer;
  transition: all 0.15s ease; border: none;
}

.btn-modal-cancel { background: #ffffff; color: #1a1a1a; border: 1px solid #d4d4d4; }
.btn-modal-cancel:hover { background: #f5f5f5; }
.btn-modal-delete { background: #dc2626; color: #ffffff; }
.btn-modal-delete:hover:not(:disabled) { background: #b91c1c; }
.btn-modal-delete:disabled { background: #a3a3a3; cursor: not-allowed; }
.btn-modal-save { background: #1a1a1a; color: #ffffff; }
.btn-modal-save:hover:not(:disabled) { background: #000; }
.btn-modal-save:disabled { background: #a3a3a3; cursor: not-allowed; }

/* ── Edit Modal ──────────────────────────────────────────── */
.modal-edit {
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.modal-header h3 { margin: 0; }

.btn-modal-close {
  background: none; border: none; cursor: pointer;
  padding: 4px; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.15s;
}
.btn-modal-close:hover { background: #f0f0f0; }
.btn-modal-close svg { stroke: #737373; }

.edit-form { display: flex; flex-direction: column; gap: 16px; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 12px; font-weight: 600; color: #1a1a1a; }
.required { color: #dc2626; }

.form-group input,
.form-group select,
.form-group textarea {
  padding: 8px 12px;
  border: 1px solid #d4d4d4;
  border-radius: 7px;
  font-size: 13px;
  font-family: inherit;
  width: 100%;
  transition: border-color 0.2s;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #737373;
  box-shadow: 0 0 0 3px rgba(115,115,115,0.1);
}
.form-group textarea { resize: vertical; min-height: 80px; }

.edit-image-preview {
  position: relative;
  width: 100%;
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e5e5;
}
.edit-image-preview img { width: 100%; height: 100%; object-fit: cover; }
.btn-remove-img {
  position: absolute; top: 8px; right: 8px;
  background: rgba(0,0,0,0.6); color: #fff;
  border: none; border-radius: 6px; padding: 4px 10px;
  font-size: 11px; cursor: pointer;
}
.btn-remove-img:hover { background: rgba(0,0,0,0.85); }

.btn-upload-img {
  padding: 8px 16px;
  border: 1px dashed #d4d4d4;
  border-radius: 7px;
  background: #fafafa;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  color: #1a1a1a;
  transition: border-color 0.2s, background 0.2s;
}
.btn-upload-img:hover { border-color: #737373; background: #f0f0f0; }

.edit-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  border-radius: 7px;
  padding: 10px 14px;
  font-size: 13px;
}

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 968px) {
  .page-wrapper { padding: 28px 20px; }
  .page-header { flex-direction: column; align-items: flex-start; }
  .btn-add-product { width: 100%; justify-content: center; }
  .product-grid { grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
}

@media (max-width: 480px) {
  .page-wrapper { padding: 20px 14px; }
  .page-header h1 { font-size: 22px; }
  .product-grid { grid-template-columns: 1fr 1fr; gap: 12px; }
  .card-image { height: 160px; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
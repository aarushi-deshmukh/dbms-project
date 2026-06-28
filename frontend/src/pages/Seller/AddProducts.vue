<template>
  <div class="page-wrapper">
    <div class="page-header">
      <h1>Add New Product</h1>
      <p class="subtitle">Fill in the details to add a product to your inventory</p>
    </div>

    <div class="card">
      <form @submit.prevent="addProduct" class="product-form">

        <!-- Left: image upload -->
        <div class="image-col">
          <p class="image-col-label">Product Image</p>
          <div
            class="image-upload-box"
            @click="triggerFileInput"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            :class="{ dragging: isDragging }"
          >
            <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/*" style="display:none">

            <div v-if="!imagePreview" class="upload-placeholder">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
              <p class="upload-text">Click to upload<br>or drag and drop</p>
              <p class="upload-hint">PNG, JPG or JPEG<br>(max. 5MB)</p>
            </div>

            <div v-else class="image-preview">
              <img :src="imagePreview" alt="Product preview">
              <button @click.stop="removeImage" class="remove-image-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          </div>

          <div class="tips">
            <p class="tips-title">Tips for a great listing</p>
            <ul>
              <li>Use clear, high-quality images</li>
              <li>Write detailed descriptions</li>
              <li>Set competitive prices</li>
              <li>Keep inventory updated</li>
            </ul>
          </div>
        </div>

        <!-- Right: fields -->
        <div class="fields-col">
          <div class="form-row">
            <div class="form-group">
              <label>Product Name <span class="required">*</span></label>
              <input type="text" v-model="newProduct.name" placeholder="Enter product name" required>
            </div>
            <div class="form-group">
              <label>Price <span class="required">*</span></label>
              <div class="input-prefix-wrap">
                <span class="input-prefix">₹</span>
                <input type="number" v-model="newProduct.price" placeholder="0.00" step="0.01" required>
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Category <span class="required">*</span></label>
              <select v-model="newProduct.category" required>
                <option value="" disabled>Select Category</option>
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
              <input type="number" v-model="newProduct.quantity" placeholder="0" min="0" required>
            </div>
          </div>

          <div class="form-group">
            <label>Description <span class="required">*</span></label>
            <textarea v-model="newProduct.description" placeholder="Describe your product in detail..." rows="4" required></textarea>
          </div>

          <div class="form-actions">
            <button type="button" @click="goToMyProducts" class="btn-cancel">Cancel</button>
            <button type="submit" class="btn-publish" :disabled="isPublishing">{{ publishMessage }}</button>
          </div>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useProductsStore } from '@/stores/products';

export default {
  setup() {
    const router = useRouter();
    const productsStore = useProductsStore();

    const publishMessage = ref('Publish Product');
    const isPublishing = ref(false);
    const imagePreview = ref(null);
    const isDragging = ref(false);
    const fileInput = ref(null);
    const newProduct = ref({ name: '', price: '', category: '', quantity: '', description: '', image: null });

    const triggerFileInput = () => fileInput.value.click();
    const handleFileSelect = (e) => { const f = e.target.files[0]; if (f) processFile(f); };
    const handleDrop = (e) => { isDragging.value = false; const f = e.dataTransfer.files[0]; if (f && f.type.startsWith('image/')) processFile(f); };

    const processFile = (file) => {
      if (file.size > 5 * 1024 * 1024) { alert('File size must be less than 5MB'); return; }
      newProduct.value.image = file;
      const reader = new FileReader();
      reader.onload = (e) => { imagePreview.value = e.target.result; };
      reader.readAsDataURL(file);
    };

    const removeImage = () => {
      imagePreview.value = null;
      newProduct.value.image = null;
      if (fileInput.value) fileInput.value.value = '';
    };

    const addProduct = async () => {
      isPublishing.value = true;
      publishMessage.value = 'Publishing...';
      try {
        const formData = new FormData();
        formData.append('name', newProduct.value.name);
        formData.append('price', newProduct.value.price);
        formData.append('category', newProduct.value.category);
        formData.append('stock', newProduct.value.quantity); // Map quantity to stock
        formData.append('description', newProduct.value.description);
        if (newProduct.value.image) {
          formData.append('image', newProduct.value.image);
        }

        await productsStore.addProduct(formData);
        publishMessage.value = 'Published!';
        setTimeout(() => { router.push('/my-products'); }, 1000);
      } catch (err) {
        console.error(err);
        publishMessage.value = 'Publish Product';
        isPublishing.value = false;
        alert('Failed to publish product. Please try again.');
      }
    };

    const goToMyProducts = () => { router.push('/my-products'); };

    return { publishMessage, isPublishing, newProduct, imagePreview, isDragging, fileInput, triggerFileInput, handleFileSelect, handleDrop, removeImage, addProduct, goToMyProducts };
  }
};
</script>

<style scoped>
* { box-sizing: border-box; }

.page-wrapper {
  margin-top: 70px;
  padding: 40px 48px;
  background-color: #fafafa;
  min-height: calc(100vh - 70px);
  display: flex;
  flex-direction: column;
}

.page-header { flex-shrink: 0; margin-bottom: 24px; }
.page-header h1 { font-size: 26px; font-weight: 700; margin: 0 0 4px 0; color: #1a1a1a; }
.subtitle { font-size: 13px; color: #737373; margin: 0; }

/* Single card */
.card {
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  overflow: hidden;
}

.product-form {
  display: flex;
  flex-direction: row;
  align-items: stretch;
}

/* ── Left: image col (fixed width, slightly shaded) ──────── */
.image-col {
  width: 280px;
  flex-shrink: 0;
  padding: 28px 24px;
  background-color: #f7f7f7;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.image-col-label { font-size: 13px; font-weight: 600; color: #1a1a1a; margin: 0; }

.image-upload-box {
  flex: 1;
  min-height: 220px;
  border: 2px dashed #d4d4d4;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
  background-color: #ffffff;
}

.image-upload-box:hover { border-color: #a3a3a3; background-color: #f5f5f5; }
.image-upload-box.dragging { border-color: #737373; background-color: #f0f0f0; }

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 16px;
  gap: 8px;
}

.upload-placeholder svg { stroke: #d4d4d4; }
.upload-text { font-size: 12px; font-weight: 500; color: #1a1a1a; margin: 0; line-height: 1.5; }
.upload-hint { font-size: 11px; color: #a3a3a3; margin: 0; line-height: 1.5; }

.image-preview { width: 100%; height: 100%; position: absolute; inset: 0; }
.image-preview img { width: 100%; height: 100%; object-fit: cover; }

.remove-image-btn {
  position: absolute;
  top: 8px; right: 8px;
  width: 26px; height: 26px;
  background: rgba(0,0,0,0.6);
  border: none; border-radius: 6px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.2s;
}
.remove-image-btn:hover { background: rgba(0,0,0,0.85); }
.remove-image-btn svg { stroke: #ffffff; }

/* Tips */
.tips { border-top: 1px solid #e5e5e5; padding-top: 16px; }
.tips-title { font-size: 12px; font-weight: 700; color: #1a1a1a; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 0.4px; }
.tips ul { list-style: none; padding: 0; margin: 0; }
.tips li { padding: 6px 0 6px 18px; color: #737373; font-size: 12px; border-bottom: 1px solid #efefef; position: relative; }
.tips li:last-child { border-bottom: none; }
.tips li::before { content: '✓'; position: absolute; left: 0; color: #1a1a1a; font-weight: 700; font-size: 11px; }

/* ── Right: fields col ───────────────────────────────────── */
.fields-col {
  flex: 1 1 0;
  min-width: 0;
  padding: 28px 32px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 12px; font-weight: 600; color: #1a1a1a; }
.required { color: #dc2626; }

.form-group input,
.form-group select,
.form-group textarea {
  padding: 9px 12px;
  border: 1px solid #d4d4d4;
  border-radius: 7px;
  font-size: 13px;
  font-family: inherit;
  background: #ffffff;
  color: #1a1a1a;
  width: 100%;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input::placeholder,
.form-group textarea::placeholder { color: #a3a3a3; }

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #737373;
  box-shadow: 0 0 0 3px rgba(115,115,115,0.1);
}

.form-group textarea { resize: vertical; min-height: 100px; line-height: 1.5; }

.input-prefix-wrap { position: relative; display: flex; align-items: center; }
.input-prefix { position: absolute; left: 11px; font-size: 13px; color: #737373; pointer-events: none; }
.input-prefix-wrap input { padding-left: 24px; }

.form-group select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 11px center;
  padding-right: 32px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  margin-top: auto;
}

.btn-cancel, .btn-publish {
  padding: 9px 22px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-cancel { background: #ffffff; color: #1a1a1a; border: 1px solid #d4d4d4; }
.btn-cancel:hover { background: #fafafa; border-color: #a3a3a3; }
.btn-publish { background: #1a1a1a; color: #ffffff; min-width: 130px; }
.btn-publish:hover:not(:disabled) { background: #000; }
.btn-publish:disabled { background: #a3a3a3; cursor: not-allowed; }

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 860px) {
  .product-form { flex-direction: column; }
  .image-col { width: 100%; min-height: 0; }
  .image-upload-box { min-height: 180px; flex: none; height: 180px; }
}

@media (max-width: 560px) {
  .page-wrapper { padding: 20px 14px; }
  .fields-col { padding: 20px 16px; }
  .image-col { padding: 20px 16px; }
  .form-row { grid-template-columns: 1fr; }
  .form-actions { flex-direction: column-reverse; }
  .btn-publish, .btn-cancel { width: 100%; text-align: center; }
}
</style>
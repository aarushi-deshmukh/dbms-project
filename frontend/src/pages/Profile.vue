<template>
  <div>
    <div class="container">
      <aside class="sidebar">
        <div class="profile-section">
          <div class="profile-image">
            <svg xmlns="http://www.w3.org/2000/svg" width="56" height="56" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div class="profile-info">
            <span class="profile-name">
              {{ accountType === 'seller' ? userProfile.company_name : userProfile.name }}
            </span>
            <span class="mail-id">{{ userProfile.email || 'user@email.com' }}</span>
          </div>
        </div>

        <nav class="sidebar-nav">
          <ul class="sidebar-links">
            <li class="nav-item" :class="{ active: activeTab === 'profile' }" @click="activeTab = 'profile'">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span>My Profile</span>
            </li>
            <li class="nav-item" :class="{ active: activeTab === 'edit' }" @click="activeTab = 'edit'">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
              <span>Edit Profile</span>
            </li>
            <li class="nav-item" :class="{ active: activeTab === 'help' }" @click="activeTab = 'help'">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
              <span>Help &amp; Support</span>
            </li>
          </ul>

          <div class="logout-section">
            <button @click="showDeleteModal = true" class="btn-delete-account">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6l-1 14H6L5 6"></path>
                <path d="M10 11v6M14 11v6"></path>
                <path d="M9 6V4h6v2"></path>
              </svg>
              <span>Delete Account</span>
            </button>
            <button @click="logout" class="logout-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              <span>Logout</span>
            </button>
          </div>
        </nav>
      </aside>

      <main class="content">
        <!-- My Profile Tab -->
        <div v-if="activeTab === 'profile'" class="tab-content">
          <div class="page-header">
            <h1>Profile Information</h1>
            <p class="subtitle">View your personal details</p>
          </div>

          <div class="details-container">
            <div v-if="loading" class="loading">
              <div class="loading-spinner"></div>
              <p>Loading profile...</p>
            </div>

            <div v-else class="info-grid">
              <div class="info-card" v-for="(value, key) in filteredProfile" :key="key">
                <span class="info-label">{{ formatLabel(key) }}</span>
                <span class="info-value">{{ value }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Edit Profile Tab -->
        <div v-if="activeTab === 'edit'" class="tab-content">
          <div class="page-header">
            <h1>Edit Profile</h1>
            <p class="subtitle">Update your personal information</p>
          </div>

          <div class="details-container">
            <div v-if="editSuccess" class="alert-success">✓ Profile updated successfully.</div>
            <div v-if="editError" class="alert-error">{{ editError }}</div>

            <form class="edit-form" @submit.prevent="saveProfile">
              <!-- Buyer fields -->
              <template v-if="accountType === 'buyer'">
                <div class="form-row">
                  <div class="form-group">
                    <label>First Name</label>
                    <input type="text" v-model="editForm.first_name" />
                  </div>
                  <div class="form-group">
                    <label>Last Name</label>
                    <input type="text" v-model="editForm.last_name" />
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Phone</label>
                    <input type="tel" v-model="editForm.phone_number" />
                  </div>
                  <div class="form-group">
                    <label>Age</label>
                    <input type="number" v-model="editForm.age" min="0" />
                  </div>
                </div>
              </template>

              <!-- Seller fields -->
              <template v-if="accountType === 'seller'">
                <div class="form-row">
                  <div class="form-group">
                    <label>Company Name</label>
                    <input type="text" v-model="editForm.company_name" />
                  </div>
                  <div class="form-group">
                    <label>Contact Number</label>
                    <input type="tel" v-model="editForm.contact_number" />
                  </div>
                </div>
              </template>

              <!-- Shared address fields -->
              <div class="form-group">
                <label>Address</label>
                <textarea v-model="editForm.address" rows="2"></textarea>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>City</label>
                  <input type="text" v-model="editForm.city" />
                </div>
                <div class="form-group">
                  <label>Country</label>
                  <input type="text" v-model="editForm.country" />
                </div>
              </div>
              <div class="form-group half">
                <label>Pincode</label>
                <input type="text" v-model="editForm.pincode" />
              </div>

              <div class="form-actions">
                <button type="button" class="btn-secondary" @click="resetEditForm">Cancel</button>
                <button type="submit" class="btn-primary" :disabled="saving">
                  {{ saving ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Help Tab -->
        <div v-if="activeTab === 'help'" class="tab-content">
          <div class="page-header">
            <h1>Help &amp; Support</h1>
            <p class="subtitle">Get assistance with your account</p>
          </div>

          <div class="details-container">
            <div class="help-section">
              <div class="help-item">
                <h3>Contact Support</h3>
                <p>Email: support@example.com</p>
                <p>Phone: +1 234 567 8900</p>
              </div>
              <div class="help-item">
                <h3>FAQs</h3>
                <p>Find answers to commonly asked questions</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Delete Account Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-box" @click.stop>
        <h3>Delete Account</h3>
        <p>This will <strong>permanently delete</strong> your account and all associated data. This action cannot be undone.</p>
        <div class="modal-actions">
          <button @click="showDeleteModal = false" class="btn-secondary">Cancel</button>
          <button @click="deleteAccount" class="btn-danger" :disabled="deleting">
            {{ deleting ? 'Deleting...' : 'Yes, Delete My Account' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useProfileStore } from "@/stores/profile";
import { useAuthStore } from "@/stores/auth";

export default {
  data() {
    return {
      activeTab: 'profile',
      userProfile: {
        name: '',
        email: '',
        phone: '',
        address: '',
        company_name: '',
        city: '',
        country: '',
        pincode: '',
        age: '',
      },
      editForm: {},
      editSuccess: false,
      editError: null,
      saving: false,
      showDeleteModal: false,
      deleting: false,
    };
  },
  computed: {
    loading() {
      return useProfileStore().loading;
    },
    accountType() {
      return this.userProfile.account_type || localStorage.getItem("user_type");
    },
    filteredProfile() {
      if (this.accountType === "buyer") {
        return {
          Name: this.userProfile.name,
          Email: this.userProfile.email,
          Phone: this.userProfile.phone,
          Address: this.userProfile.address,
          City: this.userProfile.city,
          Country: this.userProfile.country,
          Pincode: this.userProfile.pincode,
          Age: this.userProfile.age,
        };
      } else {
        return {
          "Company Name": this.userProfile.company_name,
          Email: this.userProfile.email,
          Phone: this.userProfile.phone,
          Address: this.userProfile.address,
          City: this.userProfile.city,
          Country: this.userProfile.country,
          Pincode: this.userProfile.pincode,
        };
      }
    },
  },
  methods: {
    async fetchProfile() {
      try {
        const profileStore = useProfileStore();
        const data = await profileStore.fetchProfile();
        this.userProfile = { ...data };
        this.buildEditForm(data);
      } catch (error) {
        console.error("Failed to load profile:", error);
      }
    },

    buildEditForm(data) {
      if (this.accountType === 'buyer' || data?.account_type === 'buyer') {
        const nameParts = (data.name || '').split(' ');
        this.editForm = {
          first_name: nameParts[0] || '',
          last_name: nameParts.slice(1).join(' ') || '',
          phone_number: data.phone || '',
          address: data.address || '',
          city: data.city || '',
          country: data.country || '',
          pincode: data.pincode || '',
          age: data.age || '',
        };
      } else {
        this.editForm = {
          company_name: data.company_name || '',
          contact_number: data.phone || '',
          address: data.address || '',
          city: data.city || '',
          country: data.country || '',
          pincode: data.pincode || '',
        };
      }
    },

    resetEditForm() {
      this.buildEditForm(this.userProfile);
      this.editSuccess = false;
      this.editError = null;
    },

    async saveProfile() {
      this.saving = true;
      this.editSuccess = false;
      this.editError = null;
      try {
        const profileStore = useProfileStore();
        // Only send non-empty fields
        const payload = Object.fromEntries(
          Object.entries(this.editForm).filter(([, v]) => v !== '' && v !== null && v !== undefined)
        );
        await profileStore.updateProfile(payload);
        // Refresh local state
        const data = profileStore.profile;
        if (data) {
          this.userProfile = { ...data };
          this.buildEditForm(data);
        }
        this.editSuccess = true;
      } catch (err) {
        this.editError = err.response?.data?.message || err.message || 'Failed to update profile.';
      } finally {
        this.saving = false;
      }
    },

    async deleteAccount() {
      this.deleting = true;
      try {
        const profileStore = useProfileStore();
        await profileStore.deleteAccount();
        // Also clear auth store state
        const authStore = useAuthStore();
        if (authStore.logout) authStore.logout();
        this.$router.push("/signin");
      } catch (err) {
        alert(err.response?.data?.message || err.message || 'Failed to delete account.');
      } finally {
        this.deleting = false;
        this.showDeleteModal = false;
      }
    },

    formatLabel(key) {
      return key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1');
    },

    logout() {
      const authStore = useAuthStore();
      authStore.logout();
      this.$router.push("/signin");
    },
  },
  mounted() {
    this.fetchProfile();
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background-color: #ffffff;
}

.container {
  display: flex;
  min-height: calc(100vh - 70px);
  margin-top: 70px;
  background-color: #ffffff;
}

/* Sidebar */
.sidebar {
  width: 300px;
  background-color: white;
  padding: 10px 24px 20px;
  display: flex;
  flex-direction: column;
  position: fixed;
  overflow-y: auto;
  border-right: 1px solid #e8e8e0;
  height: calc(100vh - 70px);
}

.profile-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 32px;
  border-bottom: 1px solid #e8e8e0;
}

.profile-image {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #f5f5f0 0%, #e8e8e0 100%);
  color: #1a1a1a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  border: 3px solid #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.profile-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.profile-name {
  font-size: 19px;
  font-weight: 600;
  color: #1a1a1a;
  letter-spacing: -0.3px;
}

.mail-id {
  font-size: 14px;
  color: #6b6b6b;
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.sidebar-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.2s ease;
  font-size: 15px;
  color: #3a3a3a;
  font-weight: 500;
  background-color: transparent;
}

.nav-item svg {
  flex-shrink: 0;
}

.nav-item:hover {
  background-color: #f5f5f0;
  transform: translateX(4px);
}

.nav-item.active {
  background-color: #1a1a1a;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.nav-item.active svg {
  stroke: #ffffff;
}

.logout-section {
  padding-top: 24px;
  border-top: 1px solid #e8e8e0;
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.btn-delete-account {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 12px 16px;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.2s ease;
  font-size: 14px;
  color: #dc2626;
  font-weight: 500;
  background-color: transparent;
  border: 1px solid #fecaca;
}
.btn-delete-account svg { stroke: #dc2626; }
.btn-delete-account:hover { background-color: #fef2f2; border-color: #dc2626; }

.logout-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 14px 16px;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.2s ease;
  font-size: 15px;
  color: #8b4513;
  font-weight: 500;
  background-color: transparent;
  border: 1px solid #e8e8e0;
}

.logout-btn svg {
  flex-shrink: 0;
  stroke: #8b4513;
}

.logout-btn:hover {
  background-color: #fff5f0;
  border-color: #8b4513;
  transform: translateX(4px);
}

/* Main Content */
.content {
  margin-left: 300px;
  flex: 1;
  padding: 20px 64px;
  background-color: #ffffff;
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #1a1a1a;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 15px;
  color: #6b6b6b;
  margin: 0;
}

.details-container {
  background: #ffffff;
  border: 1px solid #e8e8e0;
  border-radius: 16px;
  padding: 20px;
  max-width: 900px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.loading {
  text-align: center;
  padding: 60px;
  color: #6b6b6b;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f5f5f0;
  border-top-color: #1a1a1a;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.info-grid {
  display: grid;
  gap: 0;
}

.info-card {
  display: flex;
  justify-content: space-between;
  padding: 24px 0;
  border-bottom: 1px solid #f5f5f0;
  align-items: flex-start;
  transition: all 0.2s ease;
}

.info-card:last-child {
  border-bottom: none;
}

.info-card:hover {
  background-color: #fafaf8;
  padding-left: 16px;
  padding-right: 16px;
  margin-left: -16px;
  margin-right: -16px;
  border-radius: 8px;
}

.info-label {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 15px;
  min-width: 160px;
  letter-spacing: -0.2px;
}

.info-value {
  color: #4a4a4a;
  font-size: 15px;
  text-align: right;
  line-height: 1.6;
}

/* Edit Form */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.half {
  max-width: 240px;
}

.form-group label {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 14px;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 12px 16px;
  border: 1px solid #e8e8e0;
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
  transition: all 0.2s ease;
  width: 100%;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #1a1a1a;
  box-shadow: 0 0 0 3px rgba(26, 26, 26, 0.1);
}

.form-group textarea { resize: vertical; min-height: 80px; }

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 8px;
}

/* Alerts */
.alert-success {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 14px;
  margin-bottom: 16px;
}
.alert-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 14px;
  margin-bottom: 16px;
}

/* Buttons */
.btn-primary,
.btn-secondary,
.btn-danger {
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-primary {
  background-color: #1a1a1a;
  color: #ffffff;
}
.btn-primary:hover:not(:disabled) {
  background-color: #000000;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.btn-primary:disabled { background: #a3a3a3; cursor: not-allowed; }

.btn-secondary {
  background-color: transparent;
  color: #1a1a1a;
  border: 1px solid #e8e8e0;
}
.btn-secondary:hover { background-color: #f5f5f0; }

.btn-danger {
  background-color: #dc2626;
  color: #ffffff;
}
.btn-danger:hover:not(:disabled) { background-color: #b91c1c; }
.btn-danger:disabled { background: #a3a3a3; cursor: not-allowed; }

/* Delete Modal */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex; align-items: center; justify-content: center;
  z-index: 2000;
}
.modal-box {
  background: #ffffff;
  border-radius: 12px;
  padding: 32px;
  max-width: 440px; width: 90%;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.18);
}
.modal-box h3 { font-size: 18px; font-weight: 600; color: #1a1a1a; margin: 0 0 12px 0; }
.modal-box p { font-size: 14px; color: #6b6b6b; margin: 0 0 28px 0; line-height: 1.6; }
.modal-box p strong { color: #dc2626; }
.modal-actions { display: flex; gap: 12px; justify-content: flex-end; }

/* Help Section */
.help-section {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.help-item h3 {
  font-size: 18px;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.help-item p {
  color: #4a4a4a;
  font-size: 15px;
  margin: 4px 0;
}

/* Responsive */
@media (max-width: 968px) {
  .sidebar { width: 260px; }
  .content { margin-left: 260px; padding: 40px 32px; }
}

@media (max-width: 768px) {
  .container { flex-direction: column; }
  .sidebar {
    width: 100%; position: relative;
    height: auto; padding: 32px 24px;
    border-right: none; border-bottom: 1px solid #e8e8e0;
  }
  .content { margin-left: 0; padding: 32px 24px; }
  .details-container { padding: 32px 24px; }
  .page-header h1 { font-size: 28px; }
  .info-card { flex-direction: column; gap: 8px; }
  .info-value { text-align: left; }
  .form-row { grid-template-columns: 1fr; }
  .form-actions { flex-direction: column; }
  .btn-primary, .btn-secondary, .btn-danger { width: 100%; }
}
</style>
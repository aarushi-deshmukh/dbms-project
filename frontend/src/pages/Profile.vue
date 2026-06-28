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
              <span>Help & Support</span>
            </li>
          </ul>

          <div class="logout-section">
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
            <form class="edit-form">
              <div class="form-group" v-if="accountType === 'buyer'">
                <label>Full Name</label>
                <input type="text" v-model="userProfile.name">
              </div>

              <div class="form-group" v-if="accountType === 'seller'">
                <label>Company Name</label>
                <input type="text" v-model="userProfile.company_name">
              </div>

              <div class="form-group">
                <label>Email</label>
                <input type="email" v-model="userProfile.email">
              </div>

              <div class="form-group">
                <label>Phone</label>
                <input type="tel" v-model="userProfile.phone">
              </div>

              <div class="form-group">
                <label>Address</label>
                <textarea v-model="userProfile.address"></textarea>
              </div>
              <div class="form-actions">
                <button type="button" class="btn-secondary">Cancel</button>
                <button type="submit" class="btn-primary">Save Changes</button>
              </div>
            </form>
          </div>
        </div>

        <!-- Help Tab -->
        <div v-if="activeTab === 'help'" class="tab-content">
          <div class="page-header">
            <h1>Help & Support</h1>
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
        address: ''
      }
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
          Age: this.userProfile.age
        };
      } else {
        return {
          "Company Name": this.userProfile.company_name,
          Email: this.userProfile.email,
          Phone: this.userProfile.phone,
          Address: this.userProfile.address,
          City: this.userProfile.city,
          Country: this.userProfile.country,
          Pincode: this.userProfile.pincode
        };
      }
    }
  },
  methods: {
    async fetchProfile() {
      try {
        const profileStore = useProfileStore();
        const data = await profileStore.fetchProfile();
        this.userProfile = { ...data };
      } catch (error) {
        console.error("Failed to load profile:", error);
      }
    },

    formatLabel(key) {
      return key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1');
    },
    logout() {
      const authStore = useAuthStore();
      authStore.logout();
      this.$router.push("/signin");
    }
  },
  mounted() {
    this.fetchProfile();
  }
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
  background-color: #ffffff;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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
}

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
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  to {
    transform: rotate(360deg);
  }
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
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #1a1a1a;
  font-size: 14px;
}

.form-group input,
.form-group textarea {
  padding: 12px 16px;
  border: 1px solid #e8e8e0;
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #1a1a1a;
  box-shadow: 0 0 0 3px rgba(26, 26, 26, 0.1);
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 16px;
}

.btn-primary,
.btn-secondary {
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

.btn-primary:hover {
  background-color: #000000;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  background-color: transparent;
  color: #1a1a1a;
  border: 1px solid #e8e8e0;
}

.btn-secondary:hover {
  background-color: #f5f5f0;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6b6b6b;
}

.empty-state svg {
  margin-bottom: 24px;
  stroke: #d0d0d0;
}

.empty-state h3 {
  font-size: 20px;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.empty-state p {
  font-size: 15px;
  margin: 0;
}

/* Settings */
.settings-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.settings-section h3 {
  font-size: 18px;
  color: #1a1a1a;
  margin: 0 0 16px 0;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #f5f5f0;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-item strong {
  display: block;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.setting-item p {
  color: #6b6b6b;
  font-size: 14px;
  margin: 0;
}

/* Toggle Switch */
.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e8e8e0;
  transition: 0.3s;
  border-radius: 26px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked+.slider {
  background-color: #1a1a1a;
}

input:checked+.slider:before {
  transform: translateX(22px);
}

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
  .sidebar {
    width: 260px;
  }

  .content {
    margin-left: 260px;
    padding: 40px 32px;
  }
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    position: relative;
    height: auto;
    padding: 32px 24px;
    border-right: none;
    border-bottom: 1px solid #e8e8e0;
  }

  .content {
    margin-left: 0;
    padding: 32px 24px;
  }

  .details-container {
    padding: 32px 24px;
  }

  .page-header h1 {
    font-size: 28px;
  }

  .info-card {
    flex-direction: column;
    gap: 8px;
  }

  .info-value {
    text-align: left;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>
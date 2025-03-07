<template>
  <div class="container">
    <div class="left-side">
      <div class="tabs">
        <router-link :to="'/signup'" :class="{ active: activeTab === 'signup' }" @click="activeTab = 'signup'">Sign-Up</router-link>
        <router-link :to="'/signin'" :class="{ active: activeTab === 'signin' }" @click="activeTab = 'signin'">Sign-In</router-link>
      </div>
    </div>

    <div class="right-side">
      <form @submit.prevent="submitForm">
        <h1>Sign-Up</h1>

        <div class="row">
          <div class="input-group">
            <label for="firstname">First Name</label>
            <input type="text" id="firstname" v-model="first_name" required />
          </div>

          <div class="input-group">
            <label for="lastname">Last Name</label>
            <input type="text" id="lastname" v-model="last_name" required />
          </div>
        </div>

        <div class="row">
          <div class="input-group">
            <label for="username">Username</label>
            <input type="text" id="username" v-model="username" required />
          </div>

          <div class="input-group">
            <label for="age">Age</label>
            <input type="number" id="age" v-model="age" required />
          </div>
        </div>

        <div class="input-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>

        <div class="input-group">
          <label for="phonenumber">Phone Number</label>
          <input type="text" id="phonenumber" v-model="phone_number" required />
        </div>

        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <button type="submit" :disabled="loading">Sign Up</button>
        <p v-if="message" class="success">{{ message }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      first_name: "",
      last_name: "",
      username: "",
      email: "",
      password: "",
      age: "",
      phone_number: "",
      message: "",
      error: "",
      loading: false
    };
  },
  methods: {
    async submitForm() {
      this.loading = true;
      this.message = "";
      this.error = "";

      try {
        const response = await axios.post("http://127.0.0.1:8000/api/signup/", {
          first_name: this.first_name,
          last_name: this.last_name,
          username: this.username,
          email: this.email,
          password: this.password,
          age: this.age,
          phone_number: this.phone_number
        });

        this.message = response.data.message;
      } catch (error) {
        this.error = error.response?.data?.error || "Something went wrong!";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style>
.container {
  display: flex;
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
}

.left-side {
  width: 50%;
  background-color: rgb(62, 123, 39);
  color: rgb(239, 227, 194);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 20px;
  position: relative;
}

.tabs {
  position: absolute;
  top: 30px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: flex-start;
}

.tabs a {
  color: rgb(239, 227, 194);
  text-decoration: none;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  padding: 12px 20px;
  border-radius: 5px;
  transition: background 0.3s, transform 0.2s;
  width: 100%;
}

.tabs a:hover,
.tabs a.active {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(5px);
}

.right-side {
  width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
}

form {
  background: white;
  color: rgb(93, 135, 54);
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 350px;
  display: flex;
  flex-direction: column;
  text-align: center;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 26px;
  font-weight: bold;
  font-style: italic;
}

/* Row for Firstname & Lastname, and Username & Age */
.row {
  display: flex;
  gap: 10px;
}

.input-group {
  flex: 1;
  margin-bottom: 15px;
}

label {
  font-size: 14px;
  margin-bottom: 5px;
  display: block;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

button {
  width: 100%;
  padding: 10px;
  background: rgb(62, 123, 39);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:disabled {
  background: #ccc;
}

.success {
  color: green;
  text-align: center;
  margin-top: 10px;
}

.error {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>

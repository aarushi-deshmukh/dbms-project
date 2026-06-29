# PARS – E-Commerce Marketplace Platform

PARS is a **full-stack e-commerce marketplace** built using **Django and Vue.js** that enables buyers and sellers to interact within a secure online platform.

The system supports **role-based authentication, product management, shopping carts, wishlists, and seller dashboards**, providing a complete marketplace experience.

The goal of this platform is to help **small businesses manage products and reach customers online through a simple and responsive web interface.**

---

# UI / UX

PARS provides **two different interfaces depending on the account type**.

* **Buyer Interface** – for customers browsing and purchasing products
* **Seller Interface** – for vendors managing their products

---

# Buyer Interface

<img src="https://github.com/user-attachments/assets/9fa87306-d32f-4da6-a498-3300837ba70d" width="100%">

Buyer features include:

* Browse available products
* Filter products by category
* Add items to cart
* Save products to wishlist
* View and manage shopping cart

---

# Seller Interface

<img src="https://github.com/user-attachments/assets/75489ca1-636b-431d-b962-6f6e3ce9f2a8" width="100%">

Seller features include:

* Add new products
* Manage product listings
* Track product inventory
* View products added to the marketplace

---

# Shopping Experience

<img src="https://github.com/user-attachments/assets/47972a26-b707-4308-89e4-25c43e8e0475" width="100%">

Buyers can:

* Add products to cart
* Move items between cart and wishlist
* Update item quantities
* Complete purchases through a streamlined checkout process

---

# Features

## Authentication System

* Role-based authentication (**Buyer / Seller**)
* Secure login using **JWT authentication**
* Separate dashboards for buyers and sellers

---

## Product Management

* Sellers can **add, update, and manage products**

* Products include:

  * Name
  * Description
  * Price
  * Stock
  * Category
  * Product image

* Inventory tracking per product

---

## Shopping Cart

* Add products to cart
* Update quantities dynamically
* Persistent cart for each buyer

---

## Wishlist

* Save products for later purchase
* Move items between wishlist and cart

---

## Buyer Dashboard

Buyers can:

* Browse all products
* Filter products by category
* Manage cart and wishlist
* View product details

---

## Seller Dashboard

Sellers can:

* Add new products
* Manage existing product listings
* Update product inventory

---

# Tech Stack

## Frontend

* **Vue.js 3**
* **Vue Router**
* **Axios**
* Responsive UI using modern CSS

---

## Backend

* **Django**
* **Django REST-style APIs**
* **JWT Authentication (SimpleJWT)**

---

## Database

* **Neon PostgreSQL**
* Configured through `DATABASE_URL`
* Requires SSL for managed Neon connections

Database entities include:

* User
* Buyer
* Seller
* Product
* Cart
* CartItem
* Wishlist

For local development, create `backend/.env` from `backend/.env.example` and set
`DATABASE_URL` to the Neon connection string. Do not commit `.env` or database
credentials.

---

# Project Architecture

```
frontend/
 ├── components
 ├── pages
 │    ├── Buyer
 │    └── Seller
 ├── router
 └── api.js

backend/
 ├── api
 │    ├── models.py
 │    ├── views.py
 │    ├── serializers.py
 │    └── urls.py
 └── backend
      └── settings.py
```

Architecture follows a **Vue SPA + Django API pattern**:

* Vue handles UI and routing
* Django provides API endpoints
* Axios connects frontend to backend

---

# Database Design

Main entities:

* **User**
* **Buyer**
* **Seller**
* **Product**
* **Cart**
* **CartItem**
* **Wishlist**

Relationships:

```
User
 ├── Buyer
 │     ├── Cart
 │     │     └── CartItem → Product
 │     └── Wishlist → Product
 │
 └── Seller
        └── Product
```

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/aarushi-deshmukh/ecommerce-website.git
cd ecommerce-website
```

---

# Backend Setup

```bash
cd backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Required backend environment variables:

```env
DATABASE_URL=postgresql://username:password@host.neon.tech/dbname?sslmode=require
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Before deploying, verify the PostgreSQL schema against Neon:

```bash
python manage.py migrate --noinput
python manage.py verify_postgres_schema
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

# Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# API Endpoints

| Endpoint                     | Method | Description               |
| ---------------------------- | ------ | ------------------------- |
| `/api/signin/`               | POST   | User login                |
| `/api/products/`             | GET    | Fetch all products        |
| `/api/cart/`                 | GET    | Get buyer cart            |
| `/api/cart/add/`             | POST   | Add product to cart       |
| `/api/cart/remove/<id>/`     | DELETE | Remove item from cart     |
| `/api/wishlist/`             | GET    | Fetch wishlist items      |
| `/api/wishlist/add/`         | POST   | Add product to wishlist   |
| `/api/wishlist/remove/<id>/` | DELETE | Remove item from wishlist |

---

# Impact

This platform demonstrates how small businesses can:

* Digitally manage their product catalog
* Provide customers with an online shopping experience
* Track products and inventory efficiently

The project showcases **full-stack development using Django APIs and a Vue SPA frontend.**

* **Architecture diagram**
* **Demo GIF / animated walkthrough** (very impressive visually).

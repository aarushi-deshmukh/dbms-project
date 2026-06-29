import requests
import os
import sys
import time

BASE = os.environ.get('API_BASE', 'http://127.0.0.1:8000/api/')
RUN_ID = os.environ.get('REGRESSION_RUN_ID', str(int(time.time())))

# Helper
def ok(resp, expected_status=200):
    assert resp.status_code == expected_status, f"Expected {expected_status}, got {resp.status_code}: {resp.text}"


def token_from(resp):
    data = resp.json()
    access = data.get('access') or data.get('data', {}).get('access')
    refresh = data.get('refresh') or data.get('data', {}).get('refresh')
    assert access and refresh, 'missing tokens'
    return access, refresh


def main():
    print('Starting regression tests against', BASE)

    # 1) Signup buyer
    buyer = {
        'username': f'testbuyer_{RUN_ID}',
        'email': f'testbuyer_{RUN_ID}@example.com',
        'password': 'Str0ngPass!23',
        'password_confirmation': 'Str0ngPass!23',
        'first_name': 'Test',
        'last_name': 'Buyer',
        'age': 30,
        'phone_number': '1234567890',
        'address': '123 Test St',
        'city': 'Testville',
        'country': 'Testland',
        'pincode': '12345',
    }

    r = requests.post(BASE + 'signup/buyer/', json=buyer)
    print('signup buyer', r.status_code, r.text[:200])
    ok(r, expected_status=201)

    # 2) Signup seller
    seller = {
        'email': f'testseller_{RUN_ID}@example.com',
        'password': 'Str0ngPass!23',
        'password_confirmation': 'Str0ngPass!23',
        'company_name': 'Test Corp',
        'contact_number': '0987654321',
        'address': '1 Seller Rd',
        'city': 'Sellertown',
        'country': 'Testland',
        'pincode': '54321',
    }

    r = requests.post(BASE + 'signup/seller/', json=seller)
    print('signup seller', r.status_code, r.text[:200])
    ok(r, expected_status=201)

    # 3) Signin buyer
    signin = {'email': buyer['email'], 'password': buyer['password'], 'account_type': 'Buyer'}
    r = requests.post(BASE + 'signin/', json=signin)
    print('signin buyer', r.status_code, r.text[:200])
    ok(r, expected_status=200)
    data = r.json()
    access, refresh = token_from(r)

    headers = {'Authorization': f'Bearer {access}'}
    assert requests.get(BASE + 'profile/', headers=headers).status_code == 200, 'JWT authentication failed'

    # 3b) Signin seller
    r = requests.post(BASE + 'signin/', json={'email': seller['email'], 'password': seller['password'], 'account_type': 'Seller'})
    print('signin seller', r.status_code, r.text[:200])
    ok(r, expected_status=200)
    saccess, _ = token_from(r)
    headers_s = {'Authorization': f'Bearer {saccess}'}

    # 4) Get products (should return array)
    r = requests.get(BASE + 'products/')
    print('products', r.status_code, type(r.json()))
    ok(r, expected_status=200)
    assert isinstance(r.json(), list), 'products should be list'

    # 5) Product details (if no products exist, create one as seller)
    products = r.json()
    if not products:
        # Create product as seller
        form = {'name': 'Regression Product', 'description': 'desc', 'price': '9.99', 'quantity': 10, 'category': 'TEST'}
        r3 = requests.post(BASE + 'add-product/', data=form, headers=headers_s)
        print('add-product', r3.status_code, r3.text[:200])
        ok(r3)
        r = requests.get(BASE + 'products/')
        products = r.json()

    # Create dedicated products for this run so checkout and deletion are deterministic.
    order_product_form = {
        'name': f'Regression Order Product {RUN_ID}',
        'description': 'checkout regression product',
        'price': '19.99',
        'quantity': 10,
        'category': 'REGRESSION',
    }
    r = requests.post(BASE + 'add-product/', data=order_product_form, headers=headers_s)
    print('add order product', r.status_code, r.text[:200])
    ok(r)
    order_pid = r.json().get('product_id')
    assert order_pid, 'missing order product id'

    delete_product_form = {
        'name': f'Regression Delete Product {RUN_ID}',
        'description': 'delete regression product',
        'price': '5.00',
        'quantity': 3,
        'category': 'REGRESSION',
    }
    r = requests.post(BASE + 'add-product/', data=delete_product_form, headers=headers_s)
    print('add delete product', r.status_code, r.text[:200])
    ok(r)
    delete_pid = r.json().get('product_id')
    assert delete_pid, 'missing delete product id'

    pid = order_pid
    r = requests.get(BASE + f'details/{pid}/')
    print('details', r.status_code, r.text[:200])
    ok(r)
    # frontend expects object at res.data

    # 6) Add to cart as buyer
    r = requests.post(BASE + 'cart/add/', json={'product_id': pid, 'quantity': 2}, headers=headers)
    print('add to cart', r.status_code, r.text[:200])
    ok(r)

    # 7) Get cart
    r = requests.get(BASE + 'cart/', headers=headers)
    print('get cart', r.status_code, r.text[:200])
    ok(r)
    cart = r.json()
    assert isinstance(cart.get('items'), list), 'cart.items must be list'

    # 8) Add to wishlist
    r = requests.post(BASE + 'wishlist/add/', json={'product_id': pid}, headers=headers)
    print('add wishlist', r.status_code, r.text[:200])
    ok(r)

    # 9) Get wishlist
    r = requests.get(BASE + 'wishlist/', headers=headers)
    print('get wishlist', r.status_code, r.text[:200])
    ok(r)
    wl = r.json()
    assert isinstance(wl.get('items'), list), 'wishlist.items must be list'

    # 10) Profile
    r = requests.get(BASE + 'profile/', headers=headers)
    print('profile', r.status_code, r.text[:200])
    ok(r)

    # 11) Shipping address lifecycle
    shipping = {
        'recipient_name': 'Regression Buyer',
        'phone_number': '1234567890',
        'address': '456 Ship St',
        'city': 'Shipville',
        'state': 'TS',
        'country': 'Testland',
        'pincode': '67890',
        'is_default': True,
    }
    r = requests.post(BASE + 'shipping-addresses/', json=shipping, headers=headers)
    print('create shipping', r.status_code, r.text[:200])
    ok(r, expected_status=201)
    address_id = r.json().get('data', {}).get('id')
    assert address_id, 'missing shipping address id'

    r = requests.get(BASE + 'shipping-addresses/', headers=headers)
    print('list shipping', r.status_code, r.text[:200])
    ok(r)
    assert any(item.get('id') == address_id for item in r.json().get('data', [])), 'shipping address missing from list'

    # 12) Checkout and buyer orders
    r = requests.post(BASE + 'place-order/', json={'shipping_address_id': address_id, 'notes': 'regression order'}, headers=headers)
    print('checkout', r.status_code, r.text[:200])
    ok(r, expected_status=201)
    order = r.json().get('data', {})
    order_id = order.get('id')
    assert order_id and order.get('items'), 'missing order data'

    r = requests.get(BASE + 'orders/', headers=headers)
    print('buyer orders', r.status_code, r.text[:200])
    ok(r)
    assert any(item.get('id') == order_id for item in r.json().get('data', [])), 'order missing from buyer history'

    # 13) Seller products, orders, analytics
    r = requests.get(BASE + 'seller/products/', headers=headers_s)
    print('seller products', r.status_code, r.text[:200])
    ok(r)
    seller_product_ids = {item.get('id') for item in r.json()}
    assert order_pid in seller_product_ids and delete_pid in seller_product_ids, 'seller products missing created products'

    r = requests.get(BASE + 'seller/orders/', headers=headers_s)
    print('seller orders', r.status_code, r.text[:200])
    ok(r)
    assert any(item.get('order_number') == order.get('order_number') for item in r.json()), 'seller order missing'

    r = requests.get(BASE + 'seller/stats/', headers=headers_s)
    print('seller stats', r.status_code, r.text[:200])
    ok(r)
    stats = r.json()
    assert stats.get('totalProducts', 0) >= 2, 'seller analytics totalProducts invalid'
    assert 'byCategory' in stats and 'topByValue' in stats, 'seller analytics missing breakdowns'

    # 14) Product deletion
    r = requests.delete(BASE + f'products/{delete_pid}/', headers=headers_s)
    print('delete product', r.status_code, r.text[:200])
    ok(r)

    r = requests.get(BASE + f'details/{delete_pid}/')
    print('deleted product details', r.status_code, r.text[:200])
    ok(r, expected_status=404)

    print('All regression checks passed')


if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print('TEST FAILURE:', e)
        sys.exit(1)
    except Exception as e:
        print('ERROR:', e)
        sys.exit(2)

import requests
import os
import sys

BASE = os.environ.get('API_BASE', 'http://127.0.0.1:8000/api/')

# Helper
def ok(resp, expected_status=200):
    assert resp.status_code == expected_status, f"Expected {expected_status}, got {resp.status_code}: {resp.text}"


def main():
    print('Starting regression tests against', BASE)

    # 1) Signup buyer
    buyer = {
        'username': 'testbuyer',
        'email': 'testbuyer@example.com',
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
        'email': 'testseller@example.com',
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
    access = data.get('access') or data.get('data', {}).get('access')
    refresh = data.get('refresh') or data.get('data', {}).get('refresh')
    assert access and refresh, 'missing tokens'

    headers = {'Authorization': f'Bearer {access}'}

    # 4) Get products (should return array)
    r = requests.get(BASE + 'products/')
    print('products', r.status_code, type(r.json()))
    ok(r, expected_status=200)
    assert isinstance(r.json(), list), 'products should be list'

    # 5) Product details (if no products exist, create one as seller)
    products = r.json()
    if not products:
        # Create product as seller
        r2 = requests.post(BASE + 'signin/', json={'email': seller['email'], 'password': seller['password'], 'account_type': 'Seller'})
        ok(r2)
        sdata = r2.json()
        saccess = sdata.get('access') or sdata.get('data', {}).get('access')
        headers_s = {'Authorization': f'Bearer {saccess}'}
        form = {'name': 'Regression Product', 'description': 'desc', 'price': '9.99', 'quantity': 10, 'category': 'TEST'}
        r3 = requests.post(BASE + 'add-product/', data=form, headers=headers_s)
        print('add-product', r3.status_code, r3.text[:200])
        ok(r3)
        r = requests.get(BASE + 'products/')
        products = r.json()

    pid = products[0].get('id')
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

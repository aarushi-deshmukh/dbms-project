from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            age = data.get("age")
            phone_number = data.get("phone_number")

            if not all([first_name, last_name, username, email, password, age, phone_number]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            hashed_password = make_password(password)

            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM api_customuser WHERE username = %s OR email = %s", [username, email])
                existing_user = cursor.fetchone()[0]

                if existing_user > 0:
                    return JsonResponse({"error": "Username or email already exists"}, status=400)

                cursor.execute(
                    """
                    INSERT INTO api_customuser (first_name, last_name, username, email, password, age, phone_number, is_active, is_staff, is_superuser)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 1, 0, 0)
                    """,
                    [first_name, last_name, username, email, hashed_password, age, phone_number]
                )

            return JsonResponse({"message": "User registered successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

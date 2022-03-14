import json
import sys

from django.contrib.auth.models import User

ADMIN_DATA_PATH="/admin.json"

with open(ADMIN_DATA_PATH) as admin_json_file:
    admin_info = json.load(admin_json_file)
    username = admin_info["username"]
    password = admin_info["password"]
    email = admin_info["email"]

print(f"Successfully read admin data from {ADMIN_DATA_PATH=}", file=sys.stderr)

admin = User(
    username=username,
    email=email,
    is_active=True,
    is_staff=True,
    is_superuser=True,
)

admin.set_password(password)
try:
    admin.save()
    print("Created brand new admin account!", file=sys.stderr)
except:
    print("Such user already exists, trying to change data", file=sys.stderr)
    admin = User.objects.get(username=username)
    admin.set_password(password)
    admin.email = email
    admin.is_superuser=True
    admin.is_staff=True
    admin.save()

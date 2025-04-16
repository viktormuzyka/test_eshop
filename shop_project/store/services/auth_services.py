from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from store.models import User

def register_user(username, email, password):
    return User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )

def login_user(username, password):
    return authenticate(username=username, password=password)

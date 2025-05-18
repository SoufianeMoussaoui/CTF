# conftest.py
import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def admin_user():
    User = get_user_model()
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass'
    )

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


from CTF.models import (
    CustomeUser,
    Category, 
    Challenge, 
    Hint, 
    ChallengeFile,
)


@pytest.fixture
def category():
    return Category.objects.create(
        name="Web Exploitation",
        description="Web-based security challenges"
    )

@pytest.fixture
def challenge(category):
    return Challenge.objects.create(
        title="SQL Injection 101",
        description="Find the flag using SQL injection",
        flags="CTF{sql_injection_master}",
        point_val=100,
        difficulty="medium",
        categorie=category
    )

@pytest.fixture
def hint(challenge):
    return Hint.objects.create(
        challenge=challenge,
        description="Look at the login form",
        cost=10
    )

@pytest.fixture
def user():
    return CustomeUser.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword',
        points=50
    )

@pytest.fixture
def admin_user():
    return CustomeUser.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword'
    )

@pytest.fixture
def challenge_file(challenge):
    file = SimpleUploadedFile(
        "challenge.txt",
        b"This is a test file content",
        content_type="text/plain"
    )
    return ChallengeFile.objects.create(
        challenge=challenge,
        file=file,
        name="challenge.txt",
        size=len("This is a test file content")
    )

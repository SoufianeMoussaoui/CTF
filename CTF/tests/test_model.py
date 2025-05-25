import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from CTF.models import (
    Category, 
    Challenge, 
    Hint, 
    Solve, 
    Submission, 
    ChallengeFile,
    HintUnlock
)



class UserModelTest(TestCase):
    def test_user_creation(self, user):
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.points == 50
        assert user.is_active is True

    def test_user_str_method(self, user):
        assert str(user) == "testuser"


class CategoryModelTest(TestCase):
    def test_category_creation(self, category):
        assert category.name == "Web Exploitation"
        assert category.slug == "web-exploitation"
        assert "Web-based" in category.description

    def test_category_str_method(self, category):
        assert str(category) == "Web Exploitation"
    
    def test_auto_slug_generation(self):
        category = Category.objects.create(
            name="Binary Exploitation",
            description="Binary-based challenges"
        )
        assert category.slug == "binary-exploitation"
        
    def test_custom_slug(self):
        category = Category.objects.create(
            name="Forensics Challenges",
            slug="forensics",
            description="Digital forensics challenges"
        )
        assert category.slug == "forensics"


class ChallengeModelTest(TestCase):
    def test_challenge_creation(self, challenge, category):
        assert challenge.title == "SQL Injection 101"
        assert challenge.point_val == 100
        assert challenge.difficulty == "medium"
        assert challenge.categorie == category

    def test_challenge_str_method(self, challenge):
        assert str(challenge) == "SQL Injection 101"


class HintModelTest(TestCase):
    def test_hint_creation(self, hint, challenge):
        assert hint.challenge == challenge
        assert hint.description == "Look at the login form"
        assert hint.cost == 10

    def test_hint_str_method(self, hint):
        assert str(hint) == "Hint for SQL Injection 101"



class SolveModelTest(TestCase):
    def test_solve_creation(self, user, challenge):
        solve = Solve.objects.create(
            user=user,
            challenge=challenge
        )
        assert solve.user == user
        assert solve.challenge == challenge
        assert (timezone.now() - solve.solved_at) < timedelta(seconds=10)

    def test_solve_str_method(self, user, challenge):
        solve = Solve.objects.create(
            user=user,
            challenge=challenge
        )
        assert str(solve) == "testuser solved SQL Injection 101"
    


class SubmissionModelTest(TestCase):
    def test_submission_creation(self, user, challenge):
        submission = Submission.objects.create(
            user=user,
            challenge=challenge
        )
        assert submission.user == user
        assert submission.challenge == challenge
        assert (timezone.now() - submission.end_time) < timedelta(seconds=10)

    def test_submission_str_method(self, user, challenge):
        submission = Submission.objects.create(
            user=user,
            challenge=challenge
        )
        assert str(submission) == "testuser - SQL Injection 101 Submission"


class HintUnlockModelTest(TestCase):
    def test_hint_unlock_creation(self, user, hint):
        hint_unlock = HintUnlock.objects.create(
            user=user,
            hint=hint
        )
        assert hint_unlock.user == user
        assert hint_unlock.hint == hint
        assert (timezone.now() - hint_unlock.unlocked_at) < timedelta(seconds=10)

    def test_unique_together_constraint(self, user, hint):
        HintUnlock.objects.create(
            user=user,
            hint=hint
        )
        with pytest.raises(Exception):
            HintUnlock.objects.create(
                user=user,
                hint=hint
            )
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from CTF.models import (
    Solve, 
    HintUnlock
)




class FlagSubmissionTest(TestCase):
    def test_correct_flag_submission(self, client, user, challenge):
        
        client.force_login(user)
        response = client.post(reverse('submit_flag'), {
            'challenge_id': challenge.id,
            'flag': 'CTF{sql_injection_master}'
        })
        
        assert response.status_code == 200
        assert Solve.objects.filter(user=user, challenge=challenge).exists()
        user.refresh_from_db()
        assert user.points == 150 

    def test_incorrect_flag_submission(self, client, user, challenge):
        
        client.force_login(user)
        initial_points = user.points
        
        response = client.post(reverse('submit_flag'), {
            'challenge_id': challenge.id,
            'flag': 'CTF{wrong_flag}'
        })

        assert response.status_code == 400
        assert not Solve.objects.filter(user=user, challenge=challenge).exists()
        user.refresh_from_db()
        assert user.points == initial_points


class HintUnlockTest(TestCase):
    def test_unlock_hint(self, client, user, hint):
        client.force_login(user)
        
        initial_points = user.points
        
        response = client.post(reverse('unlock_hint'), {
            'hint_id': hint.id
        })
        
        assert response.status_code == 200
        assert HintUnlock.objects.filter(user=user, hint=hint).exists()
        user.refresh_from_db()
        assert user.points == initial_points - hint.cost

   
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, null=True) 
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
 
class Challenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('expert', 'Expert'),
    ]
    
    
    title = models.CharField(max_length=50)
    description = models.TextField()
    flags = models.CharField(max_length=250)
    point_val = models.IntegerField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, 
                                  choices=DIFFICULTY_CHOICES, 
                                  default='medium')
    categorie = models.ForeignKey(Category, 
                                  related_name='challenges', 
                                  on_delete=models.CASCADE)


    def __str__(self):
        return self.title


    


class Hint(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    description = models.TextField()
    cost = models.IntegerField(default=0)

    def __str__(self):
        return f"Hint for {self.challenge.title}"
 




class CustomeUser(AbstractUser):
    email = models.EmailField(max_length=100)
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username



class Notification(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    url = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Solve(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    solved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'challenge')
    
    def __str__(self):
        return f"{self.user.username} solved {self.challenge.title}"





class Submission(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    end_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'challenge') 

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} Submission"





class ChallengeFile(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='challenges/')
    name = models.CharField(max_length=255)
    size = models.IntegerField()  # Size in bytes
    
    def __str__(self):
        return self.name
    



class HintUnlock(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    hint = models.ForeignKey(Hint, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'hint')
    
    def __str__(self):
        return f"{self.user.username} unlocked hint for {self.hint.challenge.title}"


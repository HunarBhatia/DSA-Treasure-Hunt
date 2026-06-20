from django.db import models
from accounts.models import User

PATTERN_CHOICES = [
    (1, 'Hashmaps'),
    (2, 'Binary Search'),
    (3, 'Recursion'),
    (4, 'Linked Lists'),
    (5, 'Graphs'),
]
DIFFICULTY_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
]

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=200)
    category = models.IntegerField(choices=PATTERN_CHOICES)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    expected_answer = models.TextField()

class ParticipantProgress(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    problem=models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_level=models.IntegerField()
    status=models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

class Submission(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    problem=models.ForeignKey(Problem, on_delete=models.CASCADE)
    submitted_answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_correct=models.BooleanField(default=False)
    
class EventConfig(models.Model):
    started_at=models.DateTimeField()
    ending_time=models.DateTimeField()
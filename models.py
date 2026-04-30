from django.db import models

class Pet(models.Model):
    ANIMAL_TYPES = [('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('other', 'Other')]
    STATUS_CHOICES = [('available', 'Available'), ('pending', 'Pending'), ('adopted', 'Adopted')]

    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=20, choices=ANIMAL_TYPES)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    medical_history = models.TextField(blank=True)
    photo = models.ImageField(upload_to='pet_photos/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    posted_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='listed_pets')
    created_at = models.DateTimeField(auto_now_add=True)

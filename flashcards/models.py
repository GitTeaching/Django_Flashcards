from django.db import models
from django.contrib.auth.models import User


# FlashCard Model
class FlashCard(models.Model):
	category = models.CharField(max_length=50)
	front = models.TextField()
	back = models.TextField()
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.IntegerField(default=0)
	known = models.IntegerField(default=0)

	def __str__(self):
		return self.front

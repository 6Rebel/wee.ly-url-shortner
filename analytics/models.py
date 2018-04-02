from django.db import models

# Create your models here.
from urlshortner.models import weeURL

class ClickEventManager(models.Manager):
	def create_event(self, wee_instance):
		if isinstance(wee_instance, weeURL):
			obj, created = self.get_or_create(wee_url=wee_instance)
			obj.count += 1
			obj.save()
			return obj.count
		return None

class ClickEvent(models.Model):
	wee_url	 	= models.OneToOneField(weeURL)
	count 		= models.IntegerField(default=0)
	updated 	= models.DateTimeField(auto_now=True) #everytime the model is saved
	timestamp 	= models.DateTimeField(auto_now_add=True)#when model was created
	
	objects = ClickEventManager() 

	def __str__(self):
		return "{i}".format(i=self.count)

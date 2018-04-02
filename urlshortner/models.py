from django.db import models
from django.conf import settings

from django.core.urlresolvers import reverse
# from django_hosts.resolvers import reverse
# Create your models here.
from .utils import code_generator, create_shortcode
from .validators import validate_url
import re

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 10)

# manager is used here for just preventing from errors
class weeURLManager(models.Manager):
	def all(self, *args, **kwargs):
		qs_main = super(weeURLManager, self).all(*args, **kwargs)
		qs = qs_main.filter(active=True)
		return qs

	def refresh_shortcodes(self, items=None):
		# print(items)
		qs = weeURL.objects.filter(id__gte=1)
		if items is not None and isinstance(items, int):
			qs = qs.order_by('-id')[:items]
		new_codes = 0
		for q in qs:
			q.shortcode = create_shortcode(q)
			print(q.id)
			q.save()
			new_codes += 1
		return "New codes made: {i}".format(i=new_codes)

class weeURL(models.Model):
	url 		= models.CharField(max_length=220, unique=True, validators=[validate_url])
	shortcode 	= models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
	active		= models.BooleanField(default=True)
	
	objects = weeURLManager()

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == "":
			self.shortcode = create_shortcode(self)
		if not "http" in self.url:
			self.url = "http://" + self.url
		# if re.match('^http(s)?://', self.url) is None:
		# 	self.url = 'http://'+self.url; 	
		super(weeURL, self).save(*args, **kwargs)
		
	def __str__(self):
		return str(self.url) + "    " + self.shortcode

	def __unicode__(self):
		return str(self.url)

	def get_short_url(self):
		# for host
		# url_path = reverse("scode", kwargs={'shortcode': self.shortcode}, host='www', scheme='http', port='8000')
		# print(scode)
		url_path = reverse("scode", kwargs={'shortcode': self.shortcode})
		return "http://www.wee.ly/" + url_path
 
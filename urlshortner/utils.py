#utility functions defines here
import random
import string

from django.conf import settings

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 4)

# from urlshortner.models import weeURL
# string.ascii_lowercase + string.digits
# def code_generator(size=6, chars='abcdefghijklmnopqrstuvwxyz123456789'):

def code_generator(size=SHORTCODE_MIN, chars= string.ascii_lowercase + string.digits):	
	# new_code = ''
	# for _ in range(size):
	# 	new_code += random.choice(chars)
	# return new_code
	return ''.join(random.choice(chars) for _ in range(size))

def create_shortcode(instance, size=SHORTCODE_MIN):
	new_code = code_generator(size=size)
	Klass = instance.__class__
	qs_exists = Klass.objects.filter(shortcode=new_code).exists()
	if qs_exists:
		return create_shortcode(size=size)
	return new_code
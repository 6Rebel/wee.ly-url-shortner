from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

def validate_url(value):
	# return URLValidator(value)

	url_validator = URLValidator()
	reg_val = value
	if "http" in reg_val:
		new_value = reg_val
	else:
		new_value = "http://" + value
	try:
		url_validator(new_value)
	except:
		raise ValidationError("Invalid url For this field")
	# print(value_2_url)
	return new_value

# def validate_dot_com(value):
# 	if not "com" in value:
# 		raise ValidationError("This is not valid because of no .com")
# 	return value

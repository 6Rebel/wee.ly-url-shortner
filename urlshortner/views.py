from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404,redirect
from django.views import View

from analytics.models import ClickEvent
from .forms import SubmitUrlForm
from .models import weeURL
# Create your views here.

# Class Based View CBV

class HomeView(View):
	def get(self, request, *args, **kwargs):
		the_form = SubmitUrlForm()
		bg_image = 'https://static01.nyt.com/images/2017/06/13/well/mfrl_beach/mfrl_beach-superJumbo.gif'
		# bg_image = 'urlshortner/back.gif'
		context = {
			"title": "Wee.ly",
			"form": the_form,
			"bg_image": bg_image
		}
		return render(request, "urlshortner/base.html", context)

	def post(self, request, *args, **kwargs):
		form = SubmitUrlForm(request.POST)
		context = {
			"title": "Wee.ly",
			"form": form
		}
		template = "urlshortner/base.html"
		if form.is_valid():
			# print(form.cleaned_data.get("url"))
			new_url= form.cleaned_data.get("url")
			# if not "http" in new_url and not "www" in new_url:
			# 	new_url = "http://www." + new_url
			# if not "www" in new_url:
			# 	new_url = "www." + new_url
			if not "http" in new_url:
				new_url = "http://" + new_url
			obj, created = weeURL.objects.get_or_create(url=new_url)
			bg_image = 'https://static01.nyt.com/images/2017/06/13/well/mfrl_beach/mfrl_beach-superJumbo.gif'	
			context = {
				"title": "Wee.ly",
				"object": obj,
				"created": created,
				"bg_image": bg_image
			}
			if created:
				template = "urlshortner/success.html"
			else:
				template = "urlshortner/already-exists.html"
		return render(request, template, context)

class URLRedirectView(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		qs = weeURL.objects.filter(shortcode=shortcode)
		if qs.count() != 1 and not qs.exists():
			raise Http404
		obj = qs.first()
		print(ClickEvent.objects.create_event(obj))
		return HttpResponseRedirect(obj.url)







# Function Based View FBV
# def wee_redirect_view(request, shortcode=None, *args, **kwargs):
# 	obj = get_object_or_404(weeURL, shortcode=shortcode)
# 	# do something
# 	return HttpResponseRedirect(obj.url)
# def home_view_fbv(request, *args, **kwargs):
# 	if request.method == "POST":
# 		print(request.POST)
# 	return render(request, "shortner/home.html", {})

'''# print(request.user)
	# print(request.user.is_authenticated())
	print('method is \n')
	print(request.method)
	# obj = weeURL.objects.get(shortcode=shortcode)
	obj = get_object_or_404(weeURL, shortcode=shortcode)
	# obj_url = obj.url
	# try:
	# 	obj = weeURL.objects.get(shortcode=shortcode)
	# except:
	# 	obj = weeURL.objects.all().first()

	# obj_url = None
	# qs = weeURL.objects.filter(shortcode_iexact=shortcode.upper())
	# if qs.exists() and qs.count() == 1:
	# 	obj = qs.first()
	# 	obj_url = obj.url
'''
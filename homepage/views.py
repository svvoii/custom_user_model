from django.shortcuts import render


def home_view(request, *args, **kwargs):
	context = {} # ..for illustration purposes, this is how you pass data to the template
	return render(request, "homepage/home.html", context)

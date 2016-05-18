from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .models import Url
from .forms import UrlForm


def index(request):
    if request.method == 'POST':
        return add(request)
    return render_to_response('index.html', {'form': UrlForm()}, context_instance=RequestContext(request))


def add(request):
    form = UrlForm(request.POST)
    if form.is_valid():
        random_user = User.objects.order_by('?').first()
        original_url = form.cleaned_data.get('url')
        url, created = Url.objects.get_or_create(original_url=original_url, defaults={'author': random_user})
        if created:
            url.trim()
            url.save()
        return HttpResponseRedirect('/!' + url.short_url)
    else:
        return render_to_response('index.html', {'form': form}, context_instance=RequestContext(request))


def redirect(request, url):
    url = get_object_or_404(Url, short_url=url)
    return HttpResponseRedirect(url.original_url)


def details(request, url):
    url = get_object_or_404(Url, short_url=url)
    return render_to_response('details.html', {'url': url, 'user': url.author},
                              context_instance=RequestContext(request))

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import Http404, HttpResponseRedirect

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_backends

from accounts.forms import RegistrationForm, LoginForm

def _backend_hackend(request, user):
    backend = get_backends()[0]
    user.backend = '%s.%s' % (backend.__module__,
        backend.__class__.__name__)
    auth_login(request, user)

def login(request):
    login_form = LoginForm()
    register_form = RegistrationForm()
    
    next = request.REQUEST.get('next', settings.LOGIN_REDIRECT_URL)
    # Special case next urls that will lead us into redirect loops
    if next == settings.LOGIN_URL:
        next = settings.LOGIN_REDIRECT_URL
    
    if 'kind' in request.POST:
        if request.POST['kind'] == 'register':
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                _backend_hackend(request, register_form.save())
                return HttpResponseRedirect(next)
        elif request.POST['kind'] == 'login':
            login_form = LoginForm(request.POST)
            if login_form.is_valid() and login_form.user:
                _backend_hackend(request, login_form.user)
                return HttpResponseRedirect(next)
    context = {
        'login_form': login_form,
        'register_form': register_form,
        'next': next,
    }
    return render_to_response('accounts/login.html', context,
        context_instance=RequestContext(request))

def logout(request):
    next = request.REQUEST.get('next', settings.LOGIN_REDIRECT_URL)
    auth_logout(request)
    return HttpResponseRedirect(next)
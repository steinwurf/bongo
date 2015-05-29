#! /usr/bin/env python
# encoding: utf-8

"""Handle requests."""
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.template import RequestContext


def index(request):
    return render_to_response(
        'index.html', {}, context_instance=RequestContext(request))


def about(request):
    return render_to_response(
        'about.html', {}, context_instance=RequestContext(request))


def logout(request):
    auth_logout(request)
    return redirect('/')

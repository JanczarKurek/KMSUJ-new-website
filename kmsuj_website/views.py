from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
import unicodedata
from django.contrib import messages
from django.utils.safestring import mark_safe

from kmsuj_website.forms import PageForm
from .models import Page
import bleach
from django_bleach.utils import get_bleach_default_options

def get_context(request):
    context = {}

    pages = Page.objects.all()

    context['pages'] = pages

    return context

def index_view(request):
    context = get_context(request)
    title = "KMS UJ"
    is_index = True

    context['title'] = title
    context['is_index'] = is_index

    return render(request, 'index.html', context)

def page_view(request, name):
    context = get_context(request)
    page = get_object_or_404(Page,name=name)
    title = page.title
    can_edit = request.user.is_superuser

    bleach_args = get_bleach_default_options().copy()
    page_content = mark_safe(bleach.clean(page.content, **bleach_args))


    context['title'] = title
    context['page'] = page
    context['can_edit'] = can_edit
    context['page_content'] = page_content

    return render(request, 'simple_page.html', context)

def page_edit_view(request, name=None):
    context = get_context(request)    
    new = (name is None)
    if new:
        page = None
        title = 'Nowa podstrona'
        has_permissions = request.user.is_superuser
    else :
        page = get_object_or_404(Page, name=name)
        title = page.title
        has_permissions = request.user.is_superuser
    
    if not has_permissions:
        return HttpResponseForbidden()

    if request.method == 'POST' :
        form = PageForm(request.user, request.POST, instance=page)

        if request.POST.get('delete'):
            print("Deleting ...")
            Page.objects.filter(name=name).delete()
            return redirect('index')

        if form.is_valid():
            new_page = form.save(commit=False)
            new_page.name = unicodedata.normalize('NFKD', new_page.title).encode('ascii', 'ignore').decode('ascii').lower()
            new_page.save()
            form.save_m2m()
            messages.info(request, 'Zapisano.', extra_tags='auto-dismiss')
            return redirect('page', form.instance.name)
    else:
        form = PageForm(request.user, instance=page)

    context['title'] = title
    context['page'] = page
    context['form'] = form

    return render(request, 'page_edit.html', context)

def page_delete_view(request, name=None):

    has_permissions = request.user.is_superuser

    if not has_permissions:
        return HttpResponseForbidden()

    if request.method == 'DELETE':
        print(request)

    return redirect('index')

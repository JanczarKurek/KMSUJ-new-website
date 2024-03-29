from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
import unicodedata
from django.contrib import messages
from django.utils.safestring import mark_safe

from kmsuj_website.forms import PageForm, BilingualPageForm
from .models import Page, BilingualPage
import bleach
from bleach.css_sanitizer import CSSSanitizer

from .settings import BLEACH_ALLOWED_TAGS, BLEACH_ALLOWED_ATTRIBUTES, BLEACH_ALLOWED_STYLES, BLEACH_STRIP_TAGS, BLEACH_STRIP_COMMENTS

class AdditionalLink:
    def __init__(self, link = '', title = ''):
        self.link = link
        self.title = title

def get_bleach_options():
    bleach_args = {
        "tags": BLEACH_ALLOWED_TAGS,
        "attributes": BLEACH_ALLOWED_ATTRIBUTES,
        "strip": BLEACH_STRIP_TAGS,
        "strip_comments": BLEACH_STRIP_COMMENTS,
        "css_sanitizer": CSSSanitizer(allowed_css_properties=BLEACH_ALLOWED_STYLES),
    }
    
    return bleach_args

def get_context(request, site = 'KMSUJ', language = 'en'):
    context = {}
    context['language'] = language
    additional_links = []
    dropdown_links = []
    header_footer_colors = 'header-footer-colors-' + site
    main_nav_tab = ''
    if site == 'WORKSHOP':
        main_pages = BilingualPage.objects.filter(category='main').order_by('order').all()
        if language == 'pl':
            main_nav_tab = 'Informacje'
        else :
            main_nav_tab = 'Information'
        if BilingualPage.objects.filter(name='contact').all().count() > 0:
            context['contact'] = True
        prefix = site + '/'

    else :
        main_pages = Page.objects.filter(site=site, category="main").order_by('order').all()
        if site == 'KMSUJ':
            sub_pages = Page.objects.filter(site=site, category="traditions").order_by('order').all()
            context['sub_pages'] = sub_pages
            main_nav_tab = 'Koło'
            prefix = ''
            additional_links.append(AdditionalLink("http://kmsuj.im.uj.edu.pl/biblioteka/katalog.php", "Biblioteka"))
            dropdown_links.append(AdditionalLink("/ossm", "Ogólnopolska Sesja Studentów Matematyki"))     
            dropdown_links.append(AdditionalLink("/workshop", "Międzynarodowe Warsztaty dla Młodych Matematyków"))       
        else:
            prefix = site + '/'

        if site == 'OSSM':
            main_nav_tab = 'Informacje'

        if Page.objects.filter(site=site, name="kontakt").all().count() or Page.objects.filter(site=site, name="kontakt_o").all().count() :
            context['contact'] = True
    
    context['main_pages'] = main_pages
    context['site'] = site
    context['main_nav_tab'] = main_nav_tab
    context['prefix'] = prefix
    context['additional_links'] = additional_links
    context['header_footer_colors'] = header_footer_colors
    context['dropdown_links'] = dropdown_links
    context['language'] = language

    return context

def index_view(request):
    context = get_context(request)

    context['title'] = "KMS UJ"
    context['is_index'] = True

    return render(request, 'index.html', context)

def ossm_index_view(request):
    context = get_context(request, "OSSM")

    context['title'] = "OSSM"
    context['is_index'] = True

    return render(request, 'ossm_index.html', context)

def workshop_index_view(request, lang='en'):
    context = get_context(request, "WORKSHOP", lang)

    if lang == 'PL':
        context['title'] = "Międzynarodowe Warsztaty dla Młodych Matematyków"
    else :
        context['title'] = "International Workshop for Young Mathematicians"

    context['is_index'] = True

    return render(request, 'workshop_index.html', context)

def page_view_base(request, site, name, language ='en'):
    context = get_context(request, site, language)

    if site == 'WORKSHOP':
        page = get_object_or_404(BilingualPage, name=name)
        title = page.title
        title_polish = page.title_polish
        bleach_args = get_bleach_options()
        page_content = mark_safe(bleach.clean(page.content, **bleach_args))
        page_content_polish= mark_safe(bleach.clean(page.content_polish, **bleach_args))
        context['title_polish'] = title_polish
        context['page_content_polish'] = page_content_polish

    else:
        page = get_object_or_404(Page,name=name, site=site)
        title = page.title
        bleach_args = get_bleach_options()
        page_content = mark_safe(bleach.clean(page.content, **bleach_args))
    
    can_edit = request.user.is_superuser


    if name.startswith('kontakt') or name.startswith('contact'):
        context['is_contact'] = True

    context['title'] = title
    context['page'] = page
    context['can_edit'] = can_edit
    context['page_content'] = page_content
    context['is_index'] = False

    return context

def page_view(request, name):
    context = page_view_base(request, "KMSUJ", name)
    return render(request, 'simple_page.html', context)

def ossm_page_view(request, name):
    context = page_view_base(request, "OSSM", name)
    return render(request, 'ossm_simple_page.html', context)

def workshop_page_view(request, name, lang='en'):
    context = page_view_base(request, "WORKSHOP", name, lang)
    return render(request, 'workshop_simple_page.html', context)

def page_edit_view_base(request, site, name=None):
    context = get_context(request, site)    
    new = (name is None)
    print(site)
    if new:
        page = None
        title = 'Nowa podstrona'
        has_permissions = request.user.is_superuser
    else :
        if site == 'WORKSHOP':
            page = get_object_or_404(BilingualPage, name=name)
        else :
            page = get_object_or_404(Page, name=name, site=site)
        title = page.title
        has_permissions = request.user.is_superuser
    
    if not has_permissions:
        return HttpResponseForbidden()

    if request.method == 'POST' :
        if site == 'WORKSHOP':
            form = BilingualPageForm(request.user, request.POST, instance=page)
        else:
            form = PageForm(request.user, request.POST, instance=page)

        if request.POST.get('delete'):
            print("Deleting ...")
            if site == 'OSSM':
                Page.objects.filter(name=name).delete()
                return redirect('ossm_index')
            elif site == 'WORKSHOP':
                BilingualPage.objects.filter(name=name).delete()
                return redirect('workshop_index')
            else:
                Page.objects.filter(name=name).delete()
                return redirect('index')

        if form.is_valid():
            new_page = form.save(commit=False)
            new_page.name = unicodedata.normalize('NFKD', new_page.title).encode('ascii', 'ignore').decode('ascii').lower().replace(' ', '_')
            new_page.save()
            form.save_m2m()
            messages.info(request, 'Zapisano.', extra_tags='auto-dismiss')
            if site == 'OSSM':
                return redirect('ossm_page', form.instance.name)
            elif site == 'WORKSHOP':
                return redirect('workshop_page', form.instance.name)
            else:
                return redirect('page', form.instance.name)   
    else:
        if site == 'WORKSHOP':
            form = BilingualPageForm(request.user, instance=page)
        else:
            form = PageForm(request.user, instance=page)

    context['title'] = title
    context['page'] = page
    context['form'] = form
    if site == 'OSSM':
        return render(request, 'ossm_page_edit.html', context)
    elif site == 'WORKSHOP':
        return render(request, 'workshop_page_edit.html', context)
    else:
        return render(request, 'page_edit.html', context)


def page_edit_view(request, name=None):
    return page_edit_view_base(request, 'KMSUJ', name)

def ossm_page_edit_view(request, name=None):
    return page_edit_view_base(request, 'OSSM', name)

def workshop_page_edit_view(request, name=None, lang='en'):
    return page_edit_view_base(request, 'WORKSHOP', name)

def page_delete_view_base(request, site, name=None):

    has_permissions = request.user.is_superuser

    if not has_permissions:
        return HttpResponseForbidden()

    if request.method == 'DELETE':
        print(request)
    if site == 'OSSM':
        return redirect('ossm_index')
    elif site == 'WORKSHOP':
        return redirect('workshop_index')
    else:
        return redirect('index')

def page_delete_view(request, name=None):
    return page_delete_view_base(request, "KMSUJ", name)

def ossm_page_delete_view(request, name=None):
    return page_delete_view_base(request,"OSSM", name)

def workshop_page_delete_view(request, name=None, lang='en'):
    return page_delete_view_base(request,"WORKSHOP", name)
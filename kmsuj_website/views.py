from django.shortcuts import render

def get_context(request):
    context = {}
    return context

def index_view(request):
    context = {}

    title = "KMS UJ"
    
    context['title'] = title

    return render(request, 'index.html', context)
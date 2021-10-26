from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import Providers
from .forms import ProvidersForm


def index(request):
    template_name = 'providers/list_providers.html'
    providers = Providers.objects.all()
    context = {
        'providers': providers
    }
    return render(request, template_name, context)


def add_providers(request):
    template_name = 'providers/form_providers.html'
    if request.method == 'POST':
        form = ProvidersForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ProvidersForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


def edit_providers(request, id):
    template_name = 'providers/form_providers.html'
    provider = get_object_or_404(Providers, id=id)
    if request.method == 'POST':
        form = ProvidersForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/providers/')
    else:
        form = ProvidersForm(instance=provider)
    context = {
        'form': form,
        'id': id
    }
    return render(request, template_name, context)


def delete_providers(request, id):
    template_name = 'providers/confirm_delete.html'
    provider = get_object_or_404(Providers, id=id)
    if request.POST.get('c_delete'):
        if 'Sim' in request.POST.get('c_delete'):
            provider.delete()
        return HttpResponseRedirect('/providers/')
    context = {
        'provider': provider
    }
    return render(request, template_name, context)

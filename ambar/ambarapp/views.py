from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactForm
from .models import Service, Route


def home(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'home.html', {'services': services})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(
                request,
                'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.',
            )
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    other_services = Service.objects.filter(is_active=True).exclude(pk=service.pk)
    return render(request, 'service_detail.html', {
        'service': service,
        'other_services': other_services,
    })


def route_detail(request, slug):
    route = get_object_or_404(Route, slug=slug, is_active=True)
    other_routes = Route.objects.filter(is_active=True).exclude(pk=route.pk)
    return render(request, 'route_detail.html', {
        'route': route,
        'other_routes': other_routes,
    })


def about(request):
    return render(request, 'about.html')

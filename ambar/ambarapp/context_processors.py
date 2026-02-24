from .models import Service, Route


def header_data(request):
    """
    Tüm sayfalarda header dropdown menülerine
    hizmet ve güzergah verilerini sağlar.
    """
    return {
        'header_services': Service.objects.filter(is_active=True),
        'header_routes':   Route.objects.filter(is_active=True).order_by('order'),
    }

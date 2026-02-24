from django.contrib import admin
from .models import Service, Route


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['title', 'icon', 'is_active']
    list_editable = ['is_active']
    list_filter   = ['is_active', 'icon']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'icon', 'is_active'],
            'description': 'Temel bilgiler. Slug alanını boş bırakırsanız başlıktan otomatik oluşturulur.',
        }),
        ('İçerik & SEO', {
            'fields': ['description', 'detail_content', 'image'],
        }),
    ]


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display  = ['__str__', 'duration', 'frequency', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['origin', 'destination']
    prepopulated_fields = {'slug': ('origin', 'destination')}
    fieldsets = [
        (None, {
            'fields': ['origin', 'destination', 'slug', 'duration', 'frequency', 'order', 'is_active'],
        }),
        ('İçerik & SEO', {
            'fields': ['description', 'detail_content', 'image'],
        }),
    ]

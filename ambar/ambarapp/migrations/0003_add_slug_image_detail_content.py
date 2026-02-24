from django.db import migrations, models
from django.utils.text import slugify


def make_unique_slug(base_slug, used_slugs):
    """Eğer slug zaten kullanılıyorsa sonuna -2, -3 ekle."""
    slug = base_slug
    counter = 2
    while slug in used_slugs:
        slug = f'{base_slug}-{counter}'
        counter += 1
    used_slugs.add(slug)
    return slug


def populate_slugs(apps, schema_editor):
    Service = apps.get_model('ambarapp', 'Service')
    Route = apps.get_model('ambarapp', 'Route')

    used_service_slugs = set()
    for service in Service.objects.all().order_by('id'):
        base = slugify(service.title, allow_unicode=False) or f'hizmet-{service.pk}'
        service.slug = make_unique_slug(base, used_service_slugs)
        service.save(update_fields=['slug'])

    used_route_slugs = set()
    for route in Route.objects.all().order_by('id'):
        base = slugify(f'{route.origin}-{route.destination}', allow_unicode=False) or f'guzergah-{route.pk}'
        route.slug = make_unique_slug(base, used_route_slugs)
        route.save(update_fields=['slug'])


def clear_slugs(apps, schema_editor):
    apps.get_model('ambarapp', 'Service').objects.all().update(slug=None)
    apps.get_model('ambarapp', 'Route').objects.all().update(slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ('ambarapp', '0002_seed_initial_data'),
    ]

    operations = [
        # detail_content ve image alanları
        migrations.AddField(
            model_name='route',
            name='detail_content',
            field=models.TextField(blank=True, help_text='Detay sayfasında gösterilecek uzun açıklama metni', verbose_name='Detay İçeriği'),
        ),
        migrations.AddField(
            model_name='route',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='routes/', verbose_name='Fotoğraf', help_text='Detay sayfasında gösterilecek fotoğraf'),
        ),
        migrations.AddField(
            model_name='service',
            name='detail_content',
            field=models.TextField(blank=True, help_text='Detay sayfasında gösterilecek uzun açıklama metni', verbose_name='Detay İçeriği'),
        ),
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Fotoğraf', help_text='Detay sayfasında gösterilecek fotoğraf'),
        ),
        # slug alanlarını null'a izin vererek ekle (unique index henüz yok)
        migrations.AddField(
            model_name='service',
            name='slug',
            field=models.SlugField(blank=True, null=True, max_length=220, verbose_name='URL (Slug)'),
        ),
        migrations.AddField(
            model_name='route',
            name='slug',
            field=models.SlugField(blank=True, null=True, max_length=220, verbose_name='URL (Slug)'),
        ),
        # Mevcut kayıtlara slug doldur
        migrations.RunPython(populate_slugs, clear_slugs),
        # Unique index'i doğrudan SQL ile ekle (AlterField/_remake_table sorununu atla)
        migrations.RunSQL(
            sql='CREATE UNIQUE INDEX ambarapp_service_slug_idx ON ambarapp_service (slug);',
            reverse_sql='DROP INDEX IF EXISTS ambarapp_service_slug_idx;',
        ),
        migrations.RunSQL(
            sql='CREATE UNIQUE INDEX ambarapp_route_slug_idx ON ambarapp_route (slug);',
            reverse_sql='DROP INDEX IF EXISTS ambarapp_route_slug_idx;',
        ),
        # description verbose_name güncelle
        migrations.AlterField(
            model_name='route',
            name='description',
            field=models.TextField(blank=True, verbose_name='Kısa Açıklama'),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(verbose_name='Kısa Açıklama'),
        ),
    ]

from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    ICON_CHOICES = [
        ('truck',    'Kamyon'),
        ('arrow',    'Ok'),
        ('building', 'Bina'),
        ('package',  'Paket'),
    ]

    title = models.CharField(max_length=200, verbose_name='Başlık')
    slug  = models.SlugField(max_length=220, unique=True, blank=True, null=True, verbose_name='URL (Slug)',
                             help_text='Boş bırakın, otomatik oluşturulur')
    icon  = models.CharField(
        max_length=50, choices=ICON_CHOICES, default='truck', verbose_name='İkon',
    )
    description = models.TextField(
        verbose_name='Kısa Açıklama',
        help_text='Kartlarda ve meta description\'da kullanılır (1-2 cümle)',
    )
    detail_content = models.TextField(
        blank=True,
        verbose_name='İçerik',
        help_text='Detay sayfasında gösterilecek SEO içeriği. Paragraflar arası boş satır bırakın.',
    )
    image = models.ImageField(
        upload_to='services/', blank=True, null=True,
        verbose_name='Fotoğraf',
        help_text='Önerilen boyut: 1200×800 px',
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        ordering            = ['pk']
        verbose_name        = 'Hizmet'
        verbose_name_plural = 'Hizmetler'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('service_detail', kwargs={'slug': self.slug})


class Route(models.Model):
    origin      = models.CharField(max_length=100, verbose_name='Kalkış Şehri')
    destination = models.CharField(max_length=100, verbose_name='Varış Şehri')
    slug        = models.SlugField(max_length=220, unique=True, blank=True, null=True, verbose_name='URL (Slug)',
                                   help_text='Boş bırakın, otomatik oluşturulur')
    description = models.TextField(blank=True, verbose_name='Kısa Açıklama')
    detail_content = models.TextField(
        blank=True,
        verbose_name='Detay İçeriği',
        help_text='Detay sayfasında gösterilecek uzun açıklama metni',
    )
    image = models.ImageField(
        upload_to='routes/',
        blank=True,
        null=True,
        verbose_name='Fotoğraf',
        help_text='Detay sayfasında gösterilecek fotoğraf',
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Tahmini Süre',
        help_text='Örn: 10-12 saat',
    )
    frequency = models.CharField(
        max_length=100,
        default='Günlük sefer',
        verbose_name='Sefer Sıklığı',
    )
    order     = models.PositiveSmallIntegerField(default=0, verbose_name='Sıra')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Güzergah'
        verbose_name_plural = 'Güzergahlar'

    def __str__(self):
        return f'{self.origin} – {self.destination}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.origin}-{self.destination}', allow_unicode=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('route_detail', kwargs={'slug': self.slug})

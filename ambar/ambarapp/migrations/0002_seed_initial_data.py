from django.db import migrations


SERVICES = [
    {
        'title': 'Parça Yük Taşımacılığı',
        'description': (
            'Ankara - Antalya hattında günlük sefer düzenleyen araçlarımızla '
            'ekonomik parça yük taşımacılığı yapıyoruz.'
        ),
        'icon': 'truck',
        'features': 'Ekonomik maliyet\nGünlük seferler\nAdresten alım\nKapıdan kapıya teslimat',
        'order': 1,
    },
    {
        'title': 'Şehirler Arası Nakliyat',
        'description': (
            'En hızlı ve güvenli şehirlerarası teslimat çözümü. '
            "Türkiye'nin 81 iline lojistik hizmet sunuyoruz."
        ),
        'icon': 'arrow',
        'features': '81 il kapsama alanı\nSigortalı taşıma\nCanlı takip imkânı\nHızlı teslimat',
        'order': 2,
    },
    {
        'title': 'Ambar Hizmeti',
        'description': (
            "Antalya'daki güvenli ambarımızda yükünüzü saklıyoruz. "
            'Yük konsolidasyonu ile maliyetleri düşürüyoruz.'
        ),
        'icon': 'building',
        'features': 'Güvenli depo\nYük konsolidasyonu\nGeniş dağıtım ağı\n7/24 güvenlik',
        'order': 3,
    },
]

ROUTES = [
    {
        'origin': 'Ankara',
        'destination': 'Antalya',
        'description': 'Günlük seferlerle güvenli ve hızlı taşımacılık.',
        'duration': '10-12 saat',
        'frequency': 'Günlük sefer',
        'order': 1,
    },
    {
        'origin': 'İstanbul',
        'destination': 'Antalya',
        'description': 'İstanbul - Antalya hattında düzenli sefer hizmeti.',
        'duration': '12-14 saat',
        'frequency': 'Günlük sefer',
        'order': 2,
    },
    {
        'origin': 'İzmir',
        'destination': 'Antalya',
        'description': 'İzmir - Antalya güzergahında hızlı ve emniyetli taşıma.',
        'duration': '8-10 saat',
        'frequency': 'Günlük sefer',
        'order': 3,
    },
]


def seed_data(apps, schema_editor):
    Service = apps.get_model('ambarapp', 'Service')
    Route   = apps.get_model('ambarapp', 'Route')

    for data in SERVICES:
        Service.objects.create(**data)

    for data in ROUTES:
        Route.objects.create(**data)


def remove_seed_data(apps, schema_editor):
    apps.get_model('ambarapp', 'Service').objects.all().delete()
    apps.get_model('ambarapp', 'Route').objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('ambarapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, remove_seed_data),
    ]

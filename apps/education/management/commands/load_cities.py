import csv
import os
from django.core.management.base import BaseCommand
from apps.education.models import City, Region

# python manage.py load_cities apps/education/csv/cities_kz_full.csv

class Command(BaseCommand):
    help = "Загружает города Казахстана с названиями на русском и казахском из CSV-файла"

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help="Путь к CSV-файлу с городами"
        )

    def handle(self, *args, **options):
        file_path = options['file_path']

        # Проверяем, существует ли файл
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Файл не найден: {file_path}"))
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Пропускаем заголовки

            for row in reader:
                if len(row) != 4:
                    self.stdout.write(self.style.WARNING(f"Пропущена строка (неверный формат): {row}"))
                    continue

                name_ru, name_kk, region_name_ru, region_name_kk = row
                region, _ = Region.objects.get_or_create(name=region_name_ru, name_kk=region_name_kk)
                City.objects.get_or_create(name_ru=name_ru, name_kk=name_kk, region=region)

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))

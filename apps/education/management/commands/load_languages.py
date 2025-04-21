import csv
import os
from django.core.management.base import BaseCommand
from apps.education.models import Language

# python manage.py load_languages  apps/education/csv/languages_kz.csv


class Command(BaseCommand):
    help = "Загружает языки обучения с названиями на русском и казахском из CSV-файла"

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help="Путь к CSV-файлу с языками обучения"
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
                if len(row) != 2:
                    self.stdout.write(self.style.WARNING(f"Пропущена строка (неверный формат): {row}"))
                    continue

                name_ru, name_kk = row
                Language.objects.get_or_create(name=name_ru, name_kk=name_kk)

        self.stdout.write(self.style.SUCCESS("Языки обучения успешно загружены!"))

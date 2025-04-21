import csv
import os
from django.core.management.base import BaseCommand
from apps.education.models import Subject

# python manage.py load_subjects apps/education/csv/subjects.csv

class Command(BaseCommand):
    help = "Загружает предметы с названиями на русском и казахском из CSV-файла"

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help="Путь к CSV-файлу с предметами"
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
                if len(row) != 3:
                    self.stdout.write(self.style.WARNING(f"Пропущена строка (неверный формат): {row}"))
                    continue

                name_ru, name_kk, code = row
                subject, created = Subject.objects.get_or_create(
                    code=code,
                    defaults={'name': name_ru}
                )

                if not created:
                    self.stdout.write(self.style.WARNING(f"Предмет с кодом {code} уже существует."))

        self.stdout.write(self.style.SUCCESS("Предметы успешно загружены!"))

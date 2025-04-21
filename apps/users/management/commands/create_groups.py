from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.users.models import CustomUser


# python manage.py create_groups
class Command(BaseCommand):
    help = "Создает группы пользователей на основе ролей в CustomUser"

    def handle(self, *args, **kwargs):
        for role in CustomUser.Role:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Группа '{role}' создана"))
            else:
                self.stdout.write(self.style.WARNING(f"Группа '{role}' уже существует"))

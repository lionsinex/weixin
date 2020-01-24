import os
import sys
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Clear all migration files in project.'

    def handle(self, *args, **options):
        print(1111)
        def get_app():
            print(333)
            for app in settings.INSTALLED_APPS:
                path = os.path.join(settings.BASE_DIR, app.replace(".", "/"), "migrations")
                if os.path.exists(path):
                    yield app, path

        def clear(path):
            print(323)
            shutil.rmtree(path)
            os.makedirs(path)
            print(22)
            with open(os.path.join(path, "__init__.py"), "w+") as file:
                pass
            self.stdout.write(self.style.SUCCESS(f"Clear {path}"))

        for app, path in get_app():
            os.system(f"{sys.executable} manage.py migrate --fake {app} zero")

        for app, path in get_app():
            print(3)
            clear(path)

        self.stdout.write(self.style.SUCCESS('Successfully cleared!'))
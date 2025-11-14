from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Crea usuarios mock hardcoded para testing de la API"

    def handle(self, *args, **options):
        # Usuarios mock hardcoded
        mock_users = [
            {
                "username": "admin",
                "email": "admin@peliculas.com",
                "password": "admin123",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "usuario1",
                "email": "usuario1@test.com",
                "password": "pass123",
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "username": "usuario2",
                "email": "usuario2@test.com",
                "password": "pass123",
                "is_staff": False,
                "is_superuser": False,
            },
        ]

        for user_data in mock_users:
            username = user_data["username"]

            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Usuario "{username}" ya existe. Saltando...')
                )
                continue

            # Crear el usuario
            user = User.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
            )

            user.is_staff = user_data["is_staff"]
            user.is_superuser = user_data["is_superuser"]
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f'Usuario "{username}" creado exitosamente')
            )

        self.stdout.write(self.style.SUCCESS("\n✓ Usuarios mock creados correctamente"))
        self.stdout.write("\nCredenciales de acceso:")
        self.stdout.write("  - admin / admin123 (superusuario)")
        self.stdout.write("  - usuario1 / pass123")
        self.stdout.write("  - usuario2 / pass123")

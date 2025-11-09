from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reservas.models import PerfilUsuario

class Command(BaseCommand):
    help = 'Crea un superusuario admin si no existe'

    def handle(self, *args, **kwargs):
        username = 'admin'
        email = 'davidramirezdelaparra99@gmail.com'
        password = 'dramirez.1999'
        
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'El usuario {username} ya existe'))
            admin_user = User.objects.get(username=username)
            
            # Actualizar contraseña por si acaso
            admin_user.set_password(password)
            admin_user.email = email
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Contraseña actualizada para {username}'))
        else:
            # Crear el superusuario
            admin_user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='David Fernando',
                last_name='Ramírez de la Parra'
            )
            self.stdout.write(self.style.SUCCESS(f'Superusuario {username} creado exitosamente'))
        
        # Crear o actualizar perfil de administrador
        perfil, created = PerfilUsuario.objects.get_or_create(user=admin_user)
        perfil.rol = 'ADMINISTRADOR'
        perfil.telefono = '3153769551'
        perfil.departamento = 'Administración'
        perfil.notificaciones_email = True
        perfil.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Perfil de administrador creado'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Perfil de administrador actualizado'))
        
        self.stdout.write(self.style.SUCCESS('=============================================='))
        self.stdout.write(self.style.SUCCESS('✓ ADMIN CONFIGURADO CORRECTAMENTE'))
        self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        self.stdout.write(self.style.SUCCESS('=============================================='))
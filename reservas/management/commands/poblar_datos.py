from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reservas.models import TipoEspacio, Espacio, PerfilUsuario, Reserva
from django.utils import timezone
from datetime import timedelta, time

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando población de datos...')

        # Crear usuarios de prueba
        self.stdout.write('Creando usuarios...')
        
        # Usuario administrador (si no existe ya)
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@sistema.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema'
            )
            PerfilUsuario.objects.create(
                user=admin,
                rol='ADMINISTRADOR',
                telefono='3001234567',
                departamento='Sistemas'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Administrador creado: admin / admin123'))

        # Usuarios normales
        usuarios_data = [
            {'username': 'jperez', 'email': 'jperez@ejemplo.com', 'first_name': 'Juan', 'last_name': 'Pérez', 'departamento': 'Ingeniería'},
            {'username': 'mgarcia', 'email': 'mgarcia@ejemplo.com', 'first_name': 'María', 'last_name': 'García', 'departamento': 'Administración'},
            {'username': 'lrodriguez', 'email': 'lrodriguez@ejemplo.com', 'first_name': 'Luis', 'last_name': 'Rodríguez', 'departamento': 'Ciencias'},
        ]

        for data in usuarios_data:
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password='usuario123',
                    first_name=data['first_name'],
                    last_name=data['last_name']
                )
                PerfilUsuario.objects.create(
                    user=user,
                    rol='USUARIO',
                    telefono='300' + str(user.id).zfill(7),
                    departamento=data['departamento']
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Usuario creado: {data["username"]} / usuario123'))

        # Crear tipos de espacios
        self.stdout.write('Creando tipos de espacios...')
        tipos_data = [
            {'nombre': 'Aula', 'descripcion': 'Salones de clase tradicionales', 'capacidad_minima': 20, 'capacidad_maxima': 50},
            {'nombre': 'Laboratorio', 'descripcion': 'Espacios para prácticas experimentales', 'capacidad_minima': 15, 'capacidad_maxima': 30},
            {'nombre': 'Sala de Reuniones', 'descripcion': 'Espacios para reuniones y juntas', 'capacidad_minima': 5, 'capacidad_maxima': 20},
            {'nombre': 'Auditorio', 'descripcion': 'Espacios para eventos grandes', 'capacidad_minima': 50, 'capacidad_maxima': 200},
            {'nombre': 'Biblioteca', 'descripcion': 'Salas de estudio y lectura', 'capacidad_minima': 10, 'capacidad_maxima': 40},
        ]

        for data in tipos_data:
            tipo, created = TipoEspacio.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Tipo de espacio creado: {tipo.nombre}'))

        # Crear espacios
        self.stdout.write('Creando espacios...')
        tipo_aula = TipoEspacio.objects.get(nombre='Aula')
        tipo_lab = TipoEspacio.objects.get(nombre='Laboratorio')
        tipo_sala = TipoEspacio.objects.get(nombre='Sala de Reuniones')
        tipo_auditorio = TipoEspacio.objects.get(nombre='Auditorio')

        espacios_data = [
            {'nombre': 'Aula 101', 'tipo': tipo_aula, 'codigo': 'A-101', 'capacidad': 40, 'ubicacion': 'Edificio A, Piso 1', 'descripcion': 'Aula con proyector y pizarra', 'equipamiento': 'Proyector, Pizarra, 40 sillas'},
            {'nombre': 'Aula 102', 'tipo': tipo_aula, 'codigo': 'A-102', 'capacidad': 35, 'ubicacion': 'Edificio A, Piso 1', 'descripcion': 'Aula multimedia', 'equipamiento': 'Proyector, Computadora, Sonido'},
            {'nombre': 'Aula 201', 'tipo': tipo_aula, 'codigo': 'A-201', 'capacidad': 45, 'ubicacion': 'Edificio A, Piso 2', 'descripcion': 'Aula grande', 'equipamiento': 'Proyector, Pizarra'},
            {'nombre': 'Laboratorio de Física', 'tipo': tipo_lab, 'codigo': 'LAB-FIS-01', 'capacidad': 25, 'ubicacion': 'Edificio B, Piso 1', 'descripcion': 'Laboratorio equipado para experimentos de física', 'equipamiento': 'Mesas de trabajo, Instrumentos de medición, Computadoras'},
            {'nombre': 'Laboratorio de Química', 'tipo': tipo_lab, 'codigo': 'LAB-QUI-01', 'capacidad': 20, 'ubicacion': 'Edificio B, Piso 2', 'descripcion': 'Laboratorio con campanas extractoras', 'equipamiento': 'Campanas, Reactivos, Equipos de seguridad'},
            {'nombre': 'Laboratorio de Informática', 'tipo': tipo_lab, 'codigo': 'LAB-INF-01', 'capacidad': 30, 'ubicacion': 'Edificio C, Piso 1', 'descripcion': 'Sala con computadoras', 'equipamiento': '30 Computadoras, Proyector, Internet de alta velocidad'},
            {'nombre': 'Sala de Reuniones A', 'tipo': tipo_sala, 'codigo': 'SR-A', 'capacidad': 10, 'ubicacion': 'Edificio Administrativo, Piso 1', 'descripcion': 'Sala pequeña para reuniones', 'equipamiento': 'Mesa, 10 sillas, TV'},
            {'nombre': 'Sala de Reuniones B', 'tipo': tipo_sala, 'codigo': 'SR-B', 'capacidad': 15, 'ubicacion': 'Edificio Administrativo, Piso 2', 'descripcion': 'Sala mediana', 'equipamiento': 'Mesa grande, 15 sillas, Proyector, Videoconferencia'},
            {'nombre': 'Auditorio Principal', 'tipo': tipo_auditorio, 'codigo': 'AUD-01', 'capacidad': 150, 'ubicacion': 'Edificio Principal', 'descripcion': 'Auditorio con escenario', 'equipamiento': 'Sistema de sonido profesional, Proyector, Pantalla gigante, Iluminación'},
            {'nombre': 'Auditorio Secundario', 'tipo': tipo_auditorio, 'codigo': 'AUD-02', 'capacidad': 80, 'ubicacion': 'Edificio C, Piso 3', 'descripcion': 'Auditorio para eventos medianos', 'equipamiento': 'Proyector, Sistema de sonido, Micrófono'},
        ]

        for data in espacios_data:
            espacio, created = Espacio.objects.get_or_create(
                codigo=data['codigo'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Espacio creado: {espacio.nombre}'))

        # Crear algunas reservas de ejemplo
        self.stdout.write('Creando reservas de ejemplo...')
        
        usuarios = User.objects.filter(perfil__rol='USUARIO')
        espacios = Espacio.objects.all()[:5]
        
        hoy = timezone.now().date()
        
        reservas_data = [
            {'dias': 1, 'hora_inicio': time(8, 0), 'hora_fin': time(10, 0), 'motivo': 'Clase de Matemáticas', 'estado': 'CONFIRMADA'},
            {'dias': 1, 'hora_inicio': time(10, 30), 'hora_fin': time(12, 30), 'motivo': 'Práctica de Laboratorio', 'estado': 'CONFIRMADA'},
            {'dias': 2, 'hora_inicio': time(14, 0), 'hora_fin': time(16, 0), 'motivo': 'Reunión de Proyecto', 'estado': 'PENDIENTE'},
            {'dias': 3, 'hora_inicio': time(9, 0), 'hora_fin': time(11, 0), 'motivo': 'Seminario', 'estado': 'CONFIRMADA'},
            {'dias': 5, 'hora_inicio': time(15, 0), 'hora_fin': time(17, 0), 'motivo': 'Taller', 'estado': 'CONFIRMADA'},
        ]

        for i, data in enumerate(reservas_data):
            if usuarios.exists() and espacios.exists():
                try:
                    reserva = Reserva.objects.create(
                        usuario=usuarios[i % len(usuarios)],
                        espacio=espacios[i % len(espacios)],
                        fecha_reserva=hoy + timedelta(days=data['dias']),
                        hora_inicio=data['hora_inicio'],
                        hora_fin=data['hora_fin'],
                        motivo=data['motivo'],
                        estado=data['estado'],
                        descripcion=f'Reserva de ejemplo para {data["motivo"]}'
                    )
                    self.stdout.write(self.style.SUCCESS(f'✓ Reserva creada: {reserva.espacio.nombre} - {reserva.fecha_reserva}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'! No se pudo crear reserva: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('\n¡Datos poblados exitosamente!'))
        self.stdout.write(self.style.SUCCESS('\nCredenciales de acceso:'))
        self.stdout.write(self.style.SUCCESS('Administrador: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('Usuarios: jperez, mgarcia, lrodriguez / usuario123'))
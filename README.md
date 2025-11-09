# Sistema de Reservas de Espacios Institucionales

![Django](https://img.shields.io/badge/Django-5.2.8-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-Academic-orange)

## 📋 Descripción del Proyecto

Sistema web desarrollado con Django para la gestión y reserva de espacios institucionales (aulas, laboratorios, salas de reuniones). Permite a usuarios solicitar reservas con validación automática de conflictos de horarios, y a administradores gestionar espacios, confirmar reservas y visualizar estadísticas mediante gráficos interactivos.

**Proyecto desarrollado para la asignatura Electiva I del programa de Ingeniería de Software, Universidad Cooperativa de Colombia.**

### Características Principales

- ✅ Sistema de autenticación con roles diferenciados (Administrador y Usuario)
- ✅ CRUD completo de espacios y reservas
- ✅ Validación automática de conflictos de horarios
- ✅ Panel de administración con estadísticas y gráficos dinámicos
- ✅ Exportación de reportes en PDF y Excel
- ✅ Historial de reservas por usuario
- ✅ Interfaz responsive con Bootstrap 5
- ✅ Notificaciones por correo electrónico
- ✅ Filtros de búsqueda avanzados
- ✅ Despliegue en producción con PostgreSQL

---

## 👥 Equipo de Desarrollo

### Integrantes

- **David Fernando Ramírez de la Parra**
- **Daniers Alexander Solarte Limas**
- **Juan Felipe Mora Revelo**

### Docente

- **Cristian Camilo Ordoñez Quintero**

### Institución Académica

- **Universidad:** Universidad Cooperativa de Colombia
- **Programa:** Ingeniería de Software
- **Semestre:** Quinto (V)
- **Asignatura:** Electiva I
- **Año:** 2025

---

## 🏗️ Arquitectura del Sistema

### Patrón MVT (Model-View-Template)

El proyecto sigue el patrón arquitectónico MVT de Django:

- **Modelo (Model):** Gestión de datos mediante ORM de Django
- **Vista (View):** Lógica de negocio y procesamiento de datos
- **Template:** Presentación e interfaz de usuario

### Estructura del Proyecto
```
proyecto_final_Django/
├── reservas_espacios/          # Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py            # Configuración general
│   ├── urls.py                # URLs principales
│   ├── wsgi.py                # Configuración WSGI
│   └── asgi.py                # Configuración ASGI
├── reservas/                   # Aplicación principal
│   ├── migrations/            # Migraciones de base de datos
│   ├── management/            # Comandos personalizados
│   │   └── commands/
│   │       └── poblar_datos.py
│   ├── models.py              # Modelos de datos
│   ├── views.py               # Vistas y lógica de negocio
│   ├── forms.py               # Formularios
│   ├── urls.py                # URLs de la aplicación
│   └── admin.py               # Configuración del admin
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── reservas/              # Templates de la app
│   └── registration/          # Templates de autenticación
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── style.css          # Estilos personalizados
│   ├── js/
│   └── img/
├── media/                      # Archivos subidos por usuarios
│   └── espacios/              # Imágenes de espacios
├── requirements.txt           # Dependencias del proyecto
├── runtime.txt                # Versión de Python
├── build.sh                   # Script de construcción para Render
├── .gitignore                 # Archivos ignorados por Git
├── manage.py                  # Utilidad de gestión Django
└── README.md                  # Este archivo
```

---

## 🗄️ Modelos de Datos

### Diagrama de Relaciones
```
User (Django Auth)
    ↓ (OneToOne)
PerfilUsuario
    ↓ (ForeignKey)
Reserva ← (ForeignKey) → Espacio ← (ForeignKey) → TipoEspacio
```

### 1. TipoEspacio
Categorización de espacios (Aula, Laboratorio, Sala de Reuniones, Auditorio, Biblioteca)

**Campos:**
- `nombre` (CharField, max_length=50, unique=True): Nombre del tipo de espacio
- `descripcion` (TextField, blank=True): Descripción detallada
- `capacidad_minima` (IntegerField, default=1): Capacidad mínima de personas
- `capacidad_maxima` (IntegerField, default=100): Capacidad máxima de personas

**Métodos:**
- `__str__()`: Retorna el nombre del tipo de espacio

### 2. Espacio
Representación de espacios físicos disponibles para reserva.

**Campos:**
- `nombre` (CharField, max_length=100): Nombre descriptivo del espacio
- `tipo` (ForeignKey → TipoEspacio): Tipo de espacio al que pertenece
- `codigo` (CharField, max_length=20, unique=True): Código único identificador
- `capacidad` (IntegerField): Capacidad de personas
- `ubicacion` (CharField, max_length=200): Ubicación física detallada
- `descripcion` (TextField, blank=True): Descripción completa del espacio
- `equipamiento` (TextField, blank=True): Lista de equipos disponibles
- `activo` (BooleanField, default=True): Estado del espacio (activo/inactivo)
- `imagen` (ImageField, upload_to='espacios/', null=True, blank=True): Imagen del espacio
- `fecha_creacion` (DateTimeField, auto_now_add=True): Fecha de registro

**Métodos:**
- `__str__()`: Retorna código y nombre del espacio

**Meta:**
- `ordering`: ['nombre']
- `verbose_name`: 'Espacio'
- `verbose_name_plural`: 'Espacios'

### 3. Reserva
Registro de reservas de espacios con validaciones de horarios.

**Campos:**
- `usuario` (ForeignKey → User): Usuario que realiza la reserva
- `espacio` (ForeignKey → Espacio): Espacio reservado
- `fecha_reserva` (DateField): Fecha de la reserva
- `hora_inicio` (TimeField): Hora de inicio
- `hora_fin` (TimeField): Hora de finalización
- `motivo` (CharField, max_length=200): Motivo de la reserva
- `descripcion` (TextField, blank=True): Descripción detallada opcional
- `estado` (CharField, max_length=20, choices=ESTADO_CHOICES): Estado actual
  - PENDIENTE: Esperando confirmación
  - CONFIRMADA: Aprobada por administrador
  - CANCELADA: Cancelada por usuario o admin
  - COMPLETADA: Reserva finalizada
- `confirmacion_automatica` (BooleanField, default=True): Tipo de confirmación
- `fecha_creacion` (DateTimeField, auto_now_add=True): Fecha de creación
- `fecha_actualizacion` (DateTimeField, auto_now=True): Última actualización
- `confirmada_por` (ForeignKey → User, null=True, blank=True): Admin que confirma

**Validaciones en clean():**
- Fecha de reserva no puede ser en el pasado
- Hora de fin debe ser posterior a hora de inicio
- Detecta y previene conflictos de horarios con otras reservas

**Métodos:**
- `__str__()`: Retorna código de espacio, fecha y hora
- `save()`: Ejecuta validaciones y confirmación automática si aplica

**Meta:**
- `ordering`: ['-fecha_reserva', '-hora_inicio']
- `verbose_name`: 'Reserva'
- `verbose_name_plural`: 'Reservas'

### 4. PerfilUsuario
Extensión del modelo User de Django para roles y permisos adicionales.

**Campos:**
- `user` (OneToOneField → User): Usuario asociado de Django
- `rol` (CharField, max_length=20, choices=ROLES): Rol del usuario
  - USUARIO: Usuario normal con permisos básicos
  - ADMINISTRADOR: Usuario con permisos completos
- `telefono` (CharField, max_length=20, blank=True): Teléfono de contacto
- `departamento` (CharField, max_length=100, blank=True): Departamento o área
- `notificaciones_email` (BooleanField, default=True): Preferencia de notificaciones

**Métodos:**
- `__str__()`: Retorna username y rol

**Meta:**
- `verbose_name`: 'Perfil de Usuario'
- `verbose_name_plural`: 'Perfiles de Usuarios'

---

## 🔐 Sistema de Autenticación

### Roles y Permisos

#### Usuario Normal (USUARIO)
**Permisos:**
- ✅ Ver espacios disponibles
- ✅ Crear reservas para sí mismo
- ✅ Editar sus propias reservas (antes de la fecha)
- ✅ Cancelar sus propias reservas
- ✅ Ver su historial completo de reservas
- ✅ Actualizar su perfil personal
- ❌ No puede ver reservas de otros usuarios
- ❌ No puede crear o editar espacios
- ❌ No puede acceder a reportes

#### Administrador (ADMINISTRADOR)
**Permisos:**
- ✅ Todas las funciones de usuario normal
- ✅ Crear, editar y desactivar espacios
- ✅ Ver todas las reservas del sistema
- ✅ Confirmar reservas pendientes
- ✅ Cancelar cualquier reserva
- ✅ Acceder a dashboard de reportes
- ✅ Visualizar gráficos estadísticos
- ✅ Exportar datos en PDF y Excel
- ✅ Acceso completo al panel de administración de Django
- ✅ Gestionar usuarios y sus roles

---

## 🛣️ Rutas Principales del Sistema

### Públicas (sin autenticación)
- `GET /` - Página de inicio con información general
- `GET /espacios/` - Lista pública de espacios disponibles
- `GET /espacios/<id>/` - Detalle público de un espacio

### Autenticación
- `GET/POST /login/` - Inicio de sesión
- `GET/POST /registro/` - Registro de nuevos usuarios
- `POST /logout/` - Cierre de sesión
- `GET/POST /password_change/` - Cambio de contraseña
- `GET /password_change/done/` - Confirmación de cambio

### Perfil de Usuario
- `GET/POST /perfil/` - Ver y editar perfil personal

### Espacios (requiere autenticación)
- `GET /espacios/` - Lista de espacios con filtros
- `GET /espacios/<id>/` - Detalle completo de espacio
- `GET/POST /espacios/crear/` - Crear espacio (solo admin)
- `GET/POST /espacios/<id>/editar/` - Editar espacio (solo admin)
- `POST /espacios/<id>/eliminar/` - Desactivar espacio (solo admin)

### Reservas (requiere autenticación)
- `GET /reservas/` - Lista de reservas (propias o todas según rol)
- `GET /reservas/<id>/` - Detalle de reserva
- `GET/POST /reservas/crear/` - Crear nueva reserva
- `GET/POST /reservas/<id>/editar/` - Editar reserva (antes de fecha)
- `POST /reservas/<id>/cancelar/` - Cancelar reserva
- `POST /reservas/<id>/confirmar/` - Confirmar reserva (solo admin)
- `GET /historial/` - Historial completo de reservas del usuario

### Reportes y Estadísticas (solo admin)
- `GET /reportes/` - Dashboard de reportes con gráficos
- `GET /reportes/pdf/` - Exportar reporte completo en PDF
- `GET /reportes/excel/` - Exportar datos en formato Excel

### API Interna
- `GET /api/calendario/?espacio=<id>` - Datos JSON para calendario

### Panel de Administración Django
- `GET /admin/` - Panel completo de administración

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)
- Git

### Pasos de Instalación Local

#### 1. Clonar el repositorio
```bash
git clone https://github.com/[TU_USUARIO]/sistema-reservas-django.git
cd proyecto_final_Django
```

#### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno (opcional para desarrollo)

Crear archivo `.env` en la raíz:
```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

#### 5. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Crear superusuario
```bash
python manage.py createsuperuser
```

Ingresa:
- Username: admin
- Email: tu-email@ejemplo.com
- Password: (tu contraseña segura)

#### 7. Crear perfil de administrador para el superusuario
```bash
python manage.py shell
```

Ejecuta:
```python
from django.contrib.auth.models import User
from reservas.models import PerfilUsuario

admin = User.objects.get(username='admin')
perfil = PerfilUsuario.objects.create(
    user=admin,
    rol='ADMINISTRADOR',
    telefono='3001234567',
    departamento='Administración'
)
print(f"Perfil creado: {perfil.rol}")
exit()
```

#### 8. Poblar base de datos con datos de prueba
```bash
python manage.py poblar_datos
```

Este comando crea:
- 1 administrador adicional (admin/admin123)
- 3 usuarios normales (jperez, mgarcia, lrodriguez / usuario123)
- 5 tipos de espacios (Aula, Laboratorio, Sala de Reuniones, Auditorio, Biblioteca)
- 10 espacios de ejemplo completamente configurados
- 5 reservas de ejemplo con diferentes estados

#### 9. Recolectar archivos estáticos
```bash
python manage.py collectstatic --no-input
```

#### 10. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

El sistema estará disponible en: **http://127.0.0.1:8000/**

---

## 📦 Dependencias del Proyecto
```txt
Django==5.2.8
pillow==10.4.0
reportlab==4.2.5
openpyxl==3.1.5
django-crispy-forms==2.3
crispy-bootstrap4==2.0
python-decouple==3.8
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
dj-database-url==2.1.0
```

### Descripción de Dependencias Principales

- **Django 5.2.8:** Framework web principal
- **Pillow 10.4.0:** Procesamiento y manipulación de imágenes para espacios
- **reportlab 4.2.5:** Generación de reportes en formato PDF
- **openpyxl 3.1.5:** Exportación de datos a formato Excel (.xlsx)
- **django-crispy-forms 2.3:** Renderizado mejorado de formularios HTML
- **crispy-bootstrap4 2.0:** Integración de Bootstrap 4 con crispy-forms
- **python-decouple 3.8:** Gestión segura de variables de entorno
- **gunicorn 21.2.0:** Servidor WSGI para producción
- **psycopg2-binary 2.9.9:** Adaptador PostgreSQL para Python
- **whitenoise 6.6.0:** Servicio de archivos estáticos en producción
- **dj-database-url 2.1.0:** Configuración de base de datos mediante URL

---

## 🎨 Stack Tecnológico

### Backend
- **Framework:** Django 5.2.8
- **Lenguaje:** Python 3.12.3
- **ORM:** Django ORM
- **Autenticación:** Django Authentication System
- **Servidor Web:** Gunicorn 21.2.0

### Frontend
- **Framework CSS:** Bootstrap 5.3.0
- **Iconos:** Bootstrap Icons 1.11.0
- **Gráficos:** Chart.js 3.9.1
- **JavaScript:** Vanilla JS + jQuery 3.6.0
- **Plantillas:** Django Template Language

### Base de Datos
- **Desarrollo:** SQLite3
- **Producción:** PostgreSQL 16 (Render)

### Infraestructura
- **Hosting:** Render.com
- **Control de Versiones:** Git + GitHub
- **Gestión de Archivos Estáticos:** WhiteNoise 6.6.0

---

## 📊 Funcionalidades de Reportes

### Dashboard de Administrador

El sistema incluye un completo panel de reportes con visualizaciones interactivas que se alimentan dinámicamente desde la base de datos en tiempo real.

### Gráficos Implementados

#### 1. Reservas por Estado (Donut Chart)
- **Tipo:** Gráfico de dona interactivo
- **Datos:** Distribución de reservas según su estado
  - Confirmadas (verde)
  - Pendientes (amarillo)
  - Canceladas (rojo)
  - Completadas (gris)
- **Actualización:** Tiempo real desde la base de datos
- **Interactividad:** Hover muestra cantidad exacta y porcentaje

#### 2. Ocupación Semanal (Line Chart)
- **Tipo:** Gráfico de líneas con área sombreada
- **Datos:** Tendencia de reservas confirmadas en los últimos 7 días
- **Actualización:** Diaria
- **Utilidad:** Identificar días de mayor demanda

#### 3. Espacios Más Reservados (Horizontal Bar Chart)
- **Tipo:** Gráfico de barras horizontales
- **Datos:** Top 5 espacios con más reservas históricas
- **Actualización:** Tiempo real
- **Utilidad:** Identificar recursos más solicitados

#### 4. Reservas por Tipo de Espacio (Bar Chart)
- **Tipo:** Gráfico de barras verticales
- **Datos:** Distribución de reservas por tipo (Aula, Laboratorio, etc.)
- **Actualización:** Tiempo real
- **Utilidad:** Análisis de uso por categoría

### Tabla de Estadísticas Detalladas

Incluye:
- Resumen por estado de reservas
- Porcentajes calculados
- Barra de progreso visual
- Colores según estado

### Exportación de Datos

#### Reporte PDF
**Contenido:**
- Portada con título y fecha de generación
- Tabla de estadísticas generales:
  - Total espacios activos
  - Total reservas
  - Reservas confirmadas
  - Reservas pendientes
- Tabla detallada de últimas 20 reservas con:
  - Código de espacio
  - Usuario
  - Fecha
  - Estado
- Formato profesional con colores institucionales

#### Reporte Excel (.xlsx)
**Estructura de 3 hojas:**

**Hoja 1 - Estadísticas:**
- Título y fecha de generación
- Resumen general del sistema
- Formato con colores y estilos

**Hoja 2 - Reservas:**
- Todas las reservas del sistema
- Columnas: ID, Espacio, Código, Usuario, Fecha, Hora Inicio, Hora Fin, Motivo, Estado
- Filtros automáticos habilitados
- Anchos de columna ajustados

**Hoja 3 - Espacios:**
- Catálogo completo de espacios
- Columnas: Código, Nombre, Tipo, Capacidad, Ubicación, Estado
- Formato tabular con encabezados destacados

---

## 📧 Configuración de Correos

### Desarrollo Local

El sistema está configurado para mostrar correos en la consola durante el desarrollo:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Los correos aparecerán en la terminal donde se ejecuta `runserver`.

### Producción (Configuración SMTP)

Para enviar correos reales en producción, se debe configurar un servicio SMTP. Opciones recomendadas:

#### Opción 1: Gmail SMTP (Gratuito)

1. Crear una cuenta de Gmail específica para el proyecto
2. Habilitar "App Passwords" en la cuenta de Google
3. Configurar en `settings.py` (producción):
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-app-password'
DEFAULT_FROM_EMAIL = 'Sistema de Reservas <tu-email@gmail.com>'
```

4. Agregar variables de entorno en Render:
   - `EMAIL_HOST_USER`: tu-email@gmail.com
   - `EMAIL_HOST_PASSWORD`: tu-app-password

#### Opción 2: SendGrid (Recomendado para producción)

1. Crear cuenta gratuita en SendGrid (12,000 emails/mes gratis)
2. Generar API Key
3. Configurar en `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = 'noreply@tu-dominio.com'
```

4. Agregar variable en Render:
   - `SENDGRID_API_KEY`: tu-api-key

#### Opción 3: Mailgun (Alternativa)

Similar a SendGrid, ofrece plan gratuito con 5,000 emails/mes.

### Correos que envía el sistema

- **Confirmación de reserva:** Al crear una reserva
- **Recordatorio de reserva:** 24 horas antes (si se implementa tarea programada)
- **Cambio de estado:** Cuando un admin confirma/rechaza una reserva
- **Cancelación:** Cuando se cancela una reserva

---

## 🧪 Comandos de Gestión Personalizados

### poblar_datos

Comando personalizado para crear datos de prueba en la base de datos.

**Uso:**
```bash
python manage.py poblar_datos
```

**Funcionalidad:**
- Crea 1 superusuario admin (si no existe)
- Crea 3 usuarios normales de prueba
- Crea 5 tipos de espacios
- Crea 10 espacios completamente configurados
- Crea 5 reservas de ejemplo en diferentes estados
- Asigna perfiles con roles correspondientes

**Datos generados:**

**Usuarios:**
- admin / admin123 (ADMINISTRADOR)
- jperez / usuario123 (USUARIO - Ingeniería)
- mgarcia / usuario123 (USUARIO - Administración)
- lrodriguez / usuario123 (USUARIO - Ciencias)

**Tipos de Espacios:**
- Aula (20-50 personas)
- Laboratorio (15-30 personas)
- Sala de Reuniones (5-20 personas)
- Auditorio (50-200 personas)
- Biblioteca (10-40 personas)

**Espacios:**
1. Aula 101 - Edificio A, Piso 1 (40 personas)
2. Aula 102 - Edificio A, Piso 1 (35 personas)
3. Aula 201 - Edificio A, Piso 2 (45 personas)
4. Laboratorio de Física - Edificio B, Piso 1 (25 personas)
5. Laboratorio de Química - Edificio B, Piso 2 (20 personas)
6. Laboratorio de Informática - Edificio C, Piso 1 (30 personas)
7. Sala de Reuniones A - Edificio Administrativo, Piso 1 (10 personas)
8. Sala de Reuniones B - Edificio Administrativo, Piso 2 (15 personas)
9. Auditorio Principal - Edificio Principal (150 personas)
10. Auditorio Secundario - Edificio C, Piso 3 (80 personas)

---

## 🧪 Pruebas y Validaciones

### Validaciones Implementadas en el Sistema

#### 1. Validación de Fechas
- ❌ No permite crear reservas en fechas pasadas
- ✅ Solo acepta fechas actuales o futuras
- **Implementación:** Método `clean()` en modelo Reserva

#### 2. Validación de Horarios
- ❌ Hora de finalización debe ser posterior a hora de inicio
- ✅ Valida lógica temporal correcta
- **Implementación:** Validación en modelo y formulario

#### 3. Detección de Conflictos de Horarios
- ❌ No permite reservas solapadas en el mismo espacio
- ✅ Detecta conflictos con reservas CONFIRMADAS y PENDIENTES
- **Algoritmo:** Verifica si `(hora_inicio < reserva.hora_fin) AND (hora_fin > reserva.hora_inicio)`
- **Implementación:** Método `clean()` con query a base de datos

#### 4. Validación de Permisos por Rol
- ❌ Usuarios normales no pueden acceder a funciones de admin
- ❌ No se puede editar reserva de otro usuario
- ✅ Control de acceso en decoradores y vistas
- **Implementación:** Verificación de `user.perfil.rol` en vistas

#### 5. Validación de Formularios
- ✅ Campos requeridos marcados
- ✅ Formatos de datos validados (fecha, hora, email)
- ✅ Longitudes máximas controladas
- ✅ Mensajes de error descriptivos
- **Implementación:** Django Forms con validadores personalizados

#### 6. Validación de Código Único
- ❌ No permite duplicar códigos de espacios
- ✅ Constraint de unicidad en base de datos
- **Implementación:** `unique=True` en modelo

#### 7. Validación de Estado
- ✅ Solo estados válidos permitidos (PENDIENTE, CONFIRMADA, CANCELADA, COMPLETADA)
- ✅ Transiciones de estado controladas
- **Implementación:** Choices en modelo

### Casos de Uso Validados

#### Escenarios de Éxito ✅

1. **Usuario crea reserva sin conflictos**
   - Espacio disponible
   - Horario libre
   - Fecha futura
   - Resultado: Reserva creada (CONFIRMADA o PENDIENTE según configuración)

2. **Administrador confirma reserva pendiente**
   - Usuario con rol ADMINISTRADOR
   - Reserva en estado PENDIENTE
   - Resultado: Estado cambia a CONFIRMADA, se registra quién confirmó

3. **Usuario edita su propia reserva**
   - Reserva propia
   - Antes de la fecha
   - No cancelada
   - Resultado: Reserva actualizada exitosamente

4. **Filtros de búsqueda**
   - Por tipo de espacio
   - Por nombre/código
   - Por ubicación
   - Resultado: Lista filtrada correctamente

5. **Exportación de reportes**
   - Usuario ADMINISTRADOR
   - Datos en la base
   - Resultado: Archivos PDF/Excel generados correctamente

#### Escenarios de Error ❌

1. **Intento de reserva con conflicto de horario**
   - Espacio ya reservado en ese horario
   - Resultado: Error "El espacio ya está reservado de X a Y"

2. **Intento de reserva en fecha pasada**
   - Fecha anterior a hoy
   - Resultado: Error "No se puede reservar en fechas pasadas"

3. **Usuario normal intenta acceder a reportes**
   - Rol != ADMINISTRADOR
   - Resultado: Redirección con mensaje "No tienes permisos"

4. **Intento de editar reserva de otro usuario**
   - Reserva no pertenece al usuario actual
   - Usuario no es admin
   - Resultado: Error de permisos

5. **Hora fin menor que hora inicio**
   - Horario ilógico
   - Resultado: Error "La hora de fin debe ser posterior a la hora de inicio"

### Pruebas Realizadas

- ✅ Registro de nuevo usuario
- ✅ Login/Logout
- ✅ Creación de espacios (admin)
- ✅ Creación de reservas
- ✅ Detección de conflictos
- ✅ Edición de reservas
- ✅ Cancelación de reservas
- ✅ Confirmación de reservas (admin)
- ✅ Filtros de búsqueda
- ✅ Exportación PDF
- ✅ Exportación Excel
- ✅ Visualización de gráficos
- ✅ Responsive design en móviles
- ✅ Control de permisos por rol

---

## 🌐 Despliegue en Producción

### Plataforma: Render.com

**Características del despliegue:**
- ✅ Servicio Web con PostgreSQL 16
- ✅ Python 3.12.3
- ✅ Configuración automática con `build.sh`
- ✅ Variables de entorno seguras
- ✅ Archivos estáticos servidos con WhiteNoise
- ✅ HTTPS automático
- ✅
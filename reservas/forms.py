from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Reserva, Espacio, TipoEspacio, PerfilUsuario

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    telefono = forms.CharField(max_length=20, required=False, label='Teléfono')
    departamento = forms.CharField(max_length=100, required=False, label='Departamento')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        
        # Agregar clases CSS a todos los campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['espacio', 'fecha_reserva', 'hora_inicio', 'hora_fin', 'motivo', 'descripcion']
        widgets = {
            'fecha_reserva': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'espacio': forms.Select(attrs={'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Reunión de trabajo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción detallada (opcional)'}),
        }
        labels = {
            'espacio': 'Espacio a reservar',
            'fecha_reserva': 'Fecha de la reserva',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de finalización',
            'motivo': 'Motivo de la reserva',
            'descripcion': 'Descripción adicional',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar espacios activos
        self.fields['espacio'].queryset = Espacio.objects.filter(activo=True)

class EspacioForm(forms.ModelForm):
    class Meta:
        model = Espacio
        fields = ['nombre', 'tipo', 'codigo', 'capacidad', 'ubicacion', 'descripcion', 'equipamiento', 'activo', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: LAB-101'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Edificio A, Piso 2'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'equipamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ej: Proyector, Computadoras, Pizarra'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del espacio',
            'tipo': 'Tipo de espacio',
            'codigo': 'Código',
            'capacidad': 'Capacidad (personas)',
            'ubicacion': 'Ubicación',
            'descripcion': 'Descripción',
            'equipamiento': 'Equipamiento disponible',
            'activo': 'Activo',
            'imagen': 'Imagen',
        }

class TipoEspacioForm(forms.ModelForm):
    class Meta:
        model = TipoEspacio
        fields = ['nombre', 'descripcion', 'capacidad_minima', 'capacidad_maxima']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'capacidad_minima': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'capacidad_maxima': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['telefono', 'departamento', 'notificaciones_email']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'notificaciones_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'telefono': 'Teléfono',
            'departamento': 'Departamento',
            'notificaciones_email': 'Recibir notificaciones por email',
        }
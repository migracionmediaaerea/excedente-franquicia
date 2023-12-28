from ast import Pass
from subprocess import check_output
from django.forms import ModelForm, Form, IntegerField, DateInput, Select, CheckboxInput, NumberInput, ValidationError, CharField, ModelMultipleChoiceField, ChoiceField, FloatField, ModelChoiceField, TextInput
from django.http import Http404
from django.forms import utils
from lineas_modular.models import *
from catalogos_modular.models import *
from datetime import date
from dotenv import load_dotenv
from .utils.tipo_cambio import get_tipo_cambio
# import requests
load_dotenv()
import os


# import datetime

# #common error messages
# invalid = 'Introduce valores válidos'
# required = 'Este valor es requerido'
# null = 'Este valor es requerido'
# invalid_choice = 'Elige una opción válida'
# blank = 'Este valor es requerido'

# class ProductoForm(ModelForm):
#     class Meta:
#         model = Producto
#         fields = '__all__'

class DatosIdentificacionForm(Form):
    numero_pasajeros_mayores = IntegerField(label='Cantidad de pasajeros que viajan juntos (incluyendo al jefe de familia)', required=True, min_value=0, widget=NumberInput(attrs={'placeholder': 'Cantidad de pasajeros que viajan juntos'}), max_value=200)
    numero_pasajeros_menores = IntegerField(label='Cantidad de pasajeros menores de edad', required=True, min_value=0, widget=NumberInput(attrs={'placeholder': 'Cantidad de pasajeros menores de edad'}), initial=0, max_value=200)
    nombre_jefe_familia = CharField(
        label='Nombre(s)', 
        max_length=255, 
        required=True,
        widget=TextInput(attrs={'placeholder': 'Nombre(s)'})
    )
    apellido_jefe_familia = CharField(
        label='Primer apellido', 
        max_length=255, 
        required=True,
        widget=TextInput(attrs={'placeholder': 'Primer apellido'})
    )
    segundo_apellido_jefe_familia = CharField(
        label='Segundo apellido', 
        required=False,
        widget=TextInput(attrs={'placeholder': 'Segundo apellido'})
    )
    

    class Meta:
        fields =['numero_pasajeros', 'nombre_jefe_familia', 'apellido_jefe_familia', 'segundo_apellido_jefe_familia']


    def __init__(self, *args, **kwargs):
        folio = None
        if 'folio' in kwargs:
            folio = kwargs.pop('folio')
        super(DatosIdentificacionForm, self).__init__(*args, **kwargs)
        if folio:
            print("hay folio")
            declaracion = DeclaracionAduanera.objects.get(folio=folio)
            self.fields['nombre_jefe_familia'].initial = declaracion.nombre


            self.fields['apellido_jefe_familia'].initial = declaracion.apellido_paterno


            self.fields['segundo_apellido_jefe_familia'].initial = declaracion.apellido_materno


            self.fields['numero_pasajeros_menores'].initial = declaracion.num_familias - declaracion.mayores_edad


            self.fields['numero_pasajeros_mayores'].initial = declaracion.mayores_edad


    def clean(self):
        data = super(DatosIdentificacionForm, self).clean()
        print(f"{data=}")
        

class MercanciaForm(Form):

    categoria = ChoiceField(label='Selecciona la categoría del producto')
    subcategoria = ChoiceField(label='Selecciona la subcategoría del producto')
    producto = ChoiceField(label='Selecciona el producto')
    pais_origen = ChoiceField(label='Selecciona el pais de origen del producto')
    precio = FloatField(label='Precio del producto USD', widget=NumberInput(attrs={'placeholder': 'Precio del producto USD'}))
    # cantidad = IntegerField(label='Cantidad')
    graduacion = ChoiceField(label='Graduación')
    unidades_excedentes = IntegerField(label='Cantidad de unidades excedentes', widget=NumberInput(attrs={'placeholder': 'Cantidad de unidades excedentes'}))
    # tipo_cambio = FloatField(label='Tipo de cambio', required=True, initial=TipoCambio.objects.last().tipo_cambio)
    tipo_cambio = FloatField(label='Tipo de cambio', required=True)

    class Meta:
        fields = ['categoria', 'subcategoria', 'producto','pais_origen', 'precio']

    def __init__(self, *args, **kwargs):
        super(MercanciaForm, self).__init__(*args, **kwargs)
        self.fields['tipo_cambio'].widget.attrs['readonly'] = True
        tipo_cambio = get_tipo_cambio()
        #Si no hay tipo de cambio lanzo un 404
        if tipo_cambio:
            self.fields['tipo_cambio'].initial = get_tipo_cambio()
        else:
            raise Http404("Tipo de cambio no encontrado para la fecha actual")    
        



class ViajeForm(ModelForm):
    medio_transporte = ModelChoiceField(MedioTransporteLineas.objects.all().exclude(pk=1), label='Medio de arribo')
    class Meta:
        model = Viaje
        fields = ['medio_transporte', 'fecha_fin', 'equipo_computo', 'aduana_ingreso', 'punto_revision', 'numero_vuelo', 'nombre_embarcacion', 'numero_transporte', 'nacionalidad', 'procedencia']
        

        labels = {
            'equipo_computo': '¿Lleva consigo equipo de cómputo?',
            'nombre_embarcacion': 'Número de embarcación',
            'numero_transporte': 'Número de transporte',
        }

        widgets = {
            'fecha_fin': DateInput(attrs={'type': 'date'}, ),
            'nombre_embarcacion': TextInput(attrs={'placeholder': 'Número de embarcación'}),
            'numero_vuelo': TextInput(attrs={'placeholder': 'Número de vuelo'}),
            'numero_transporte': TextInput(attrs={'placeholder': 'Número de transporte'}),
        }

    def __init__(self, *args, **kwargs):
        folio = None
        if 'folio' in kwargs:
            folio = kwargs.pop('folio')
        super(ViajeForm, self).__init__(*args, **kwargs)
        if folio:
            declaracion = DeclaracionAduanera.objects.get(folio=folio)


            self.fields['fecha_fin'].initial = declaracion.fecha_arribo


            self.fields['medio_transporte'].initial = declaracion.medio_transporte

            
            self.fields['aduana_ingreso'].initial = declaracion.aduana_ingreso


            self.fields['punto_revision'].initial = declaracion.punto_revision

            print(declaracion.medio_transporte)
            if declaracion.medio_transporte_id == 4:
                print("4")
                self.fields['numero_vuelo'].initial = declaracion.num_transporte

            elif declaracion.medio_transporte_id == 3:
                print("3")
                self.fields['nombre_embarcacion'].initial = declaracion.num_transporte


    def save(self, commit=True):
        instance = super(ViajeForm, self).save(commit=False)
        if commit:
            instance.medio_transporte = self.medio_transporte
            instance.aduana_ingreso = self.aduana_ingreso
            instance.punto_revision = self.punto_revision
            instance.save()

        return super().save(commit)


class ProcedenciaForm(ModelForm):
    procedencia = ModelChoiceField(Procedencia.objects.all(), label='Procedencia')
    class Meta:
        model = Procedencia
        fields = ['procedencia']
        widgets = {
            'procedencia': Select(attrs={'class': 'form-control'}),
        }

        

class NacionalidadForm(ModelForm):
    nacionalidad = ModelChoiceField(Nacionalidad.objects.all(), label='Nacionalidad')
    class Meta:
        model = Nacionalidad
        fields = ['nacionalidad']
        widgets = {
            'nacionalidad': Select(attrs={'class': 'form-control'}),
        }
        




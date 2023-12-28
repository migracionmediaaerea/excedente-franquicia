import django_filters
from django import forms
from django_filters.widgets import RangeWidget

from lineas_modular.models import *
from catalogos_modular.models import *

from datetime import datetime

def get_aduana(request):
    queryset = AduanaLineas.objects.all().order_by('nombre').distinct('nombre')
    user=request.user

    is_director = user.groups.filter(name="Director central de excedente de franquicia").exists()
    is_capturista = user.groups.filter(name="Capturista de excedente de franquicia").exists()
    is_supervisor = user.groups.filter(name="Supervisor de excedente de franquicia").exists()

    if is_supervisor or is_capturista:
        aduana_user = UsuarioAduana.objects.get(user=user).aduana.numero_aduana
        queryset = AduanaLineas.objects.filter(numero_aduana = aduana_user).order_by('nombre').distinct('nombre')
    elif is_director:
        # aduana_user = UsuarioAduana.objects.get(user=user).aduana.numero_aduana
        queryset = AduanaLineas.objects.all().order_by('nombre').distinct('nombre')

    return queryset

class ExcedenteFilter(django_filters.FilterSet):
    tipo_filtro = django_filters.ChoiceFilter(
        choices=[
            ('DIA', 'Filtrar por día'), 
            ('MES', 'Filtrar por mes'), 
            ('SEMANA', 'Filtrar por semana')], 
        label='Filtrar por',
        method='filter_tipo_filtro'
    )

    fecha_fin__exact = django_filters.DateFilter(
        field_name='fecha_fin', 
        lookup_expr='exact', 
        label='Fecha de arribo',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    fecha_fin__year = django_filters.ChoiceFilter(
        field_name='fecha_fin',
        label='Año',
        method='filter_fecha_fin__year',
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        choices=[(year, year) for year in range(2022, datetime.now().year + 1)]
    )

    fecha_fin__month = django_filters.ChoiceFilter(
        field_name='fecha_fin',
        label='Mes',
        method='filter_fecha_fin__month',
        widget=forms.Select(attrs={'class': 'form-control form-select'}),
        choices=[
            (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'),
            (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
        ]
    )

    fecha_fin__range = django_filters.DateFromToRangeFilter(
        field_name='fecha_fin',
        label='Rango semanal de fecha de arribo',
        widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control'})
    )

    # created_at = django_filters.DateFromToRangeFilter(label='Filtrar por fecha de registro')
    folio = django_filters.CharFilter(label='Folio')
    # deleted__isnotnull = django_filters.BooleanFilter(field_name='deleted', lookup_expr="isnull")
    # fecha_notificacion = django_filters.DateFromToRangeFilter()
    aduana_ingreso = django_filters.ModelChoiceFilter(queryset=get_aduana, method='filter_aduana_ingreso')

    class Meta:
        model = Viaje
        fields = ['tipo_filtro', 'fecha_fin__exact', 'fecha_fin__year', 'fecha_fin__month', 'fecha_fin__range', 'folio', 'apellido_jefe_fa', 'seg_apellido_jefe', 'nombre_jefe_fa', 'aduana_ingreso']

    def filter_tipo_filtro(self, queryset, name, value):
        # es un input de seleccion, por lo que no importa el valor
        return queryset

    def filter_fecha_fin__year(self, queryset, name, value):
        if value:
            return queryset.filter(fecha_fin__year=value)
        return queryset
    
    def filter_fecha_fin__month(self, queryset, name, value):
        if value:
            return queryset.filter(fecha_fin__month=value)
        return queryset
    
    def filter_aduana_ingreso(self, queryset, name, value):
        if value:
            return queryset.filter(aduana_ingreso__numero_aduana=value.numero_aduana)
        return queryset

    def __init__(self, *args, **kwargs):
        super(ExcedenteFilter, self).__init__(*args, **kwargs)
        # self.filters['created_at'].field.widget.attrs.update({'class':'form-control', 'type' : 'date'})
        self.filters['folio'].field.widget.attrs.update({'class':'form-control', 'placeholder': 'Folio'})
        self.filters['apellido_jefe_fa'].field.widget.attrs.update({'class':'form-control', 'placeholder': 'Apellido paterno'})
        self.filters['seg_apellido_jefe'].field.widget.attrs.update({'class':'form-control', 'placeholder': 'Apellido materno'})
        self.filters['nombre_jefe_fa'].field.widget.attrs.update({'class':'form-control', 'placeholder': 'Nombre o razón social'})
        self.filters['aduana_ingreso'].field.widget.attrs.update({'class':'form-control', 'placeholder': 'Aduana de ingreso'})
        self.filters['tipo_filtro'].field.widget.attrs.update({'class':'form-control form-select'})

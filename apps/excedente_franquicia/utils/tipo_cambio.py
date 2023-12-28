from lineas_modular.models import TipoCambio
from datetime import date

def get_tipo_cambio():
    today = date.today()
    tipo_cambio = TipoCambio.objects.filter(fecha_inicio=today).first()
    if tipo_cambio:
        return tipo_cambio.tipo_cambio
    else:
        return TipoCambio.objects.latest('fecha_dof').tipo_cambio
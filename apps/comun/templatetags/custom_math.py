from django import template
import re
register = template.Library()

@register.filter(name='suma')
def suma(precio, cantidad):
    if not precio:
        return "N/A"
    total = precio * cantidad
    return f'${total:.2f}usd'

@register.filter(name='impuesto')
def impuesto(precio, tasa):
    if not precio or not tasa:
        return "N/A"
    tasa_decimal = tasa/100
    total = precio * tasa_decimal
    return total

@register.filter(name='multiplica')
def multiplica(precio, cantidad):
    if not precio or precio=="N/A":
        return "N/A"
    total = precio * cantidad
    return "$" + str(total) + "usd"

@register.filter(name='redondeo')
def redondeo(num):
    excedente_limpio = re.sub(r"[^\d.]+", "", num)
    if not excedente_limpio:
        return "Se necesita la intervención de un agente aduanal"
    excedente_float = float(excedente_limpio)
    excedente_redondeado = round(excedente_float)
    return "$" + str(excedente_redondeado) + " mxn"
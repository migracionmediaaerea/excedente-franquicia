from lineas_modular.models import Producto, Limite, Excedente, ExcedenteFranquicia, Procedencia
from django.forms.models import model_to_dict

import json


def get_limite(viaje, data):
    filtros = {
            "medio_transporte": viaje.medio_transporte,
            "procedencia_id": data['procedencia'],
            "nacionalidad_id": data['nacionalidad'],
            "residente": 'residente' in data if viaje.medio_transporte.medio_transporte == "Terrestre" else None
        }

    #Si es terrestre pero de procedencia es de franja fronteriza
    if filtros['procedencia_id'] is not "":
        if viaje.medio_transporte.medio_transporte == "Terrestre" and Procedencia.objects.get(pk=filtros['procedencia_id']).procedencia == "Franja o región fronteriza":
            filtros['residente'] = None

    print(f"Procedencia: {filtros['procedencia_id']}, Nacionalidad: {filtros['nacionalidad_id']}, Residente: {filtros['residente']}")

    filtros = {k: v for k, v in filtros.items() if v is not "" or None}
    print(f"{filtros=}")

    # Calcular la franquicia para obtener el limite
    excedente_franquicia = ExcedenteFranquicia.objects.filter(**filtros).first()
    print(f"{excedente_franquicia=}")

    limite = Limite.objects.filter(excedente=excedente_franquicia).first()
    limite_dict = model_to_dict(limite)
    print(f"{limite_dict=}")

    return limite_dict


#[{'id': 146, 'nombre_producto': 'Juego de herramienta de mano', 'precio': '600', 'valor_usd': '600', 'tasa_impuesto': 19, 'unidades_excedentes': 1, 'pais_origen': None}]
def calc_excedente(productos, datos_viaje, num_mayores, num_menores, data):
    """
    Calcula el excedente de franquicia para un conjunto de productos
    """
    # Se obtiene el limite en base al excedente de franquicia
    limite_dict = get_limite(datos_viaje, data)
    print(f"{limite_dict=}")
    limite = limite_dict['limite_excedente']
   
    equipo_computo = datos_viaje.equipo_computo

    if equipo_computo:
        limite = limite + limite_dict['limite_eq_computo']

    alcohol = False
    tabaco = False
    

    print(f"Limite para el viaje: {limite}")

    acumulado = 0
    acumulado_alcohol = 0
    acumulado_tabaco = 0
    mandar_agente = False
    cobro = 0
    dict_producto_acumulado = {}

    agente_tabaco = False
    agente_alcohol = False

    lleva_alcohol = False
    lleva_tabaco = False

    for datos_producto in productos:
        producto = Producto.objects.get(id=datos_producto['id'])
        producto_id = str(producto.id)
        unidades_excedentes =  float(datos_producto['unidades_excedentes'])
        impuesto = int(datos_producto['tasa_impuesto']) / 100
        precio = float(datos_producto['precio'])

        #Si lleva alcohol o cigarrillos se corba el limiite de tabaco o alcohol
        alcohol = producto.categoria.nombre_categoria == "Vino y bebidas alcohólicas" and 'residente' in data
        if alcohol:
            lleva_alcohol = True
        tabaco = producto.categoria.nombre_categoria == "Cigarrillos y otros productos que contienen tabaco" and 'residente' in data
        if tabaco:
            lleva_tabaco = True



        if not producto_id in dict_producto_acumulado:
            dict_producto_acumulado[producto_id] = unidades_excedentes
        else:
            dict_producto_acumulado[producto_id]= dict_producto_acumulado[producto_id]+unidades_excedentes

        #Acumulado por alcohol
        if lleva_alcohol:
            print("--------------------ALCOHOL---------------------")
            acumulado_alcohol = acumulado_alcohol + precio * unidades_excedentes
            print(f"{acumulado_alcohol=}")
            if acumulado_alcohol > limite_dict['limite_franq_alcohol']:
                agente_alcohol = True
            else:
                cobro = cobro +  (precio * unidades_excedentes) * impuesto
        #Acumulado por tabaco
        elif lleva_tabaco:
            print("--------------------TABACO---------------------")
            acumulado_tabaco = acumulado_tabaco + precio * unidades_excedentes
            print(f"{acumulado_tabaco=}")
            if acumulado_tabaco > limite_dict['limite_franq_tabaco']:
                agente_tabaco = True
            else:
                cobro = cobro +  (precio * unidades_excedentes) * impuesto
        #Acumulado normal
        else:
            acumulado = acumulado + precio * unidades_excedentes
            cobro = cobro +  (precio * unidades_excedentes) * impuesto

        if producto.cantidad_maxima and not alcohol and not tabaco:
            print(f"CANTIDAD MÁXIMA: {producto.cantidad_maxima}, {dict_producto_acumulado[producto_id]}")
            if dict_producto_acumulado[producto_id] > producto.cantidad_maxima - producto.cantidad_por_persona:
                mandar_agente = True
        if producto.clave == "AL" or producto.clave == "AN" or producto.clave == "ANC" or producto.clave == "ANCA":
            mandar_agente = True

        elif acumulado > limite:
            mandar_agente = True

    if agente_alcohol or agente_tabaco:
        mandar_agente = True
    if mandar_agente:
        cobro = 0

    #cobro con dos decimales
    cobro = round(cobro, 2)
    # print(f"DATOS DEL VIAJE: {datos_viaje}")
    print(f"{dict_producto_acumulado}")
    Excedente.objects.create(impuesto_a_pagar=cobro, viaje=datos_viaje, agente=mandar_agente)
    print(f"Excedente creado {Excedente.objects.get(viaje=datos_viaje)}")
    return {'mandar_agente': mandar_agente, 'cobro': cobro, 'pk': datos_viaje.pk}


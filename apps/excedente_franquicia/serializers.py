from rest_framework import serializers
# from comun.lineas_modular.models import ProductoPais
from lineas_modular.models import *
# from catalogos_modular.models import *
from django.db.models import F

class PaisTlcSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaisTlc
        fields = ['id', 'pais_tlc']


class ProductoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='nombre_producto')
    class Meta:
        model = Producto
        fields = ['id','nombre']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        ppais = ProductoPais.objects.filter(producto=instance)
        if ppais:
            any_ppais = ppais.first()

            has_graduacion = GraduacionPais.objects.filter(producto_pais=any_ppais).exists()
            if has_graduacion:
                ppais_list = AlcoholSerializer(ppais, many=True).data
            elif any_ppais.tasa_impuesto:
                ppais_list = ppais.values(nombre=F('pais__pais_tlc'), impuesto=F('tasa_impuesto'))
            else:
                ppais_list = list(ppais.values_list('pais__pais_tlc', flat=True))
            
            if len(ppais_list) > 0:
                response['pais'] = ppais_list
        
        if instance.clave:
            response['clave'] = instance.clave


        if instance.infinitos:
            response['cantidad'] = True
        else:
            if instance.cantidad_por_persona is not None:
                response['cantidad'] = instance.cantidad_por_persona 
        
        if instance.aplica_franquicia:
            response['franquicia'] = 1 if instance.aplica_franquicia else 0
        
        if instance.cantidad_maxima:
            response['limite'] = instance.cantidad_maxima

        if instance.tasa_impuesto:
            response['impuesto'] = instance.tasa_impuesto
        
        if instance.unidad_medida:
            response['unidad'] = instance.unidad_medida.unidad
            
        if instance.valuable:
            response['valuable'] = 1
        
        if instance.mensaje:
            response['mensaje'] = instance.mensaje

        if instance.leyenda:
            response['leyenda'] = instance.leyenda
        
        if instance.nota:
            response['nota'] = instance.nota

        if instance.agente is not None:
            response['agente'] = 1 if instance.agente else 0
        
        # viaje no se usa
        if instance.viaje:
            response['viaje'] = 1

        if instance.categoria_ci:
            response['categoria'] = instance.categoria_ci           
                
                
        return response


class SubcategoriaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='nombre_subcategoria')
    producto = ProductoSerializer(many=True, read_only=True)
    class Meta:
        model = Subcategoria
        fields = ['id', 'nombre', 'producto']    

    def to_representation(self, instance):
        response = super().to_representation(instance)
        productos = Producto.objects.filter(subcategoria=instance)
        productos_serializer = ProductoSerializer(productos, many=True)
        response['producto'] = productos_serializer.data
        return response   

class CategoriaSerializer(serializers.ModelSerializer):
    img = serializers.CharField(source='icono')
    nombre = serializers.CharField(source='nombre_categoria')
    subcategoria = SubcategoriaSerializer(many=True, read_only=True)
    class Meta:
        model = Categoria
        fields = ['id', 'img', 'nombre', 'subcategoria']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        subcategorias = Subcategoria.objects.filter(categoria=instance)
        subcategorias_serializer = SubcategoriaSerializer(subcategorias, many=True)
        subcategorias_data = subcategorias_serializer.data

        if instance.excedente:
            response['excedente'] = instance.excedente
        
        if instance.tipo_viajero and instance.tipo_viajero.tipo_viajero == 'Mayor de edad':
            response['edad'] = True

        if len(subcategorias_data) > 0:
            response['subcategoria'] = subcategorias_data
        else:
            productos = Producto.objects.filter(categoria=instance)
            productos_residentes = Producto.objects.filter(
                categoria=instance, 
                medio_transporte__medio_transporte='Terrestre residente de la frontera'
            )

            # TODO: fix categoria.only_internacional in seed
            # if instance.only_internacional:
            #     response['only'] = 'internacional' if instance.only_internacional else 'residente'
            
            if len(productos) == 0:
                response['producto'] = []
                return response
            
            producto = productos.first()
            if producto.only_internacional is not None:
                response['only'] = 'internacional' if producto.only_internacional else 'residente'
                productos_serializer = ProductoSerializer(productos, many=True)    
                response['producto'] = productos_serializer.data
                return response

            if len(productos_residentes) > 0:
                productos_serializer = ProductoSerializer(productos_residentes, many=True)    
                response['residente'] = {
                    'producto': productos_serializer.data
                }
                productos = productos.exclude(medio_transporte__medio_transporte='Terrestre residente de la frontera')

            productos_serializer = ProductoSerializer(productos, many=True)    
            response['producto'] = productos_serializer.data
            
        return response

class ProductoPaisSerializer(serializers.ModelSerializer):
    ppais = PaisTlcSerializer()
    class Meta:
        model = ProductoPais
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

class GraduacionPaisSerializer(serializers.ModelSerializer):
    pais_tlc = serializers.ReadOnlyField(source='pais.pais_tlc')
    class Meta:
        model = GraduacionPais
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

class ProductoPaisSerializerNotNull(serializers.ModelSerializer):
    pais = serializers.SerializerMethodField()
    class Meta:
        model = ProductoPais
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

    def get_pais(self, obj):
        query = PaisTlc.objects.filter(pk=obj.pais.id)
        return [PaisTlcSerializer(m).data for m in query]


class SubcategoriaConProductosSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()
    categoria = serializers.StringRelatedField()
    class Meta:
        model = Subcategoria
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

    def get_productos(self, obj):
        query = Producto.objects.filter(subcategoria=obj)
        return [ProductoSerializer(m).data for m in query]

class MercanciaSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()
    subcategorias = serializers.SerializerMethodField()
    class Meta:
        model = Categoria
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

    def get_productos(self, obj):
        query = Producto.objects.filter(categoria=obj)
        return [ProductoSerializer(m).data for m in query]

    def get_subcategorias(self, obj):
        query = Subcategoria.objects.filter(categoria=obj)
        return [SubcategoriaConProductosSerializer(m).data for m in query]


# Mi maleta apis

# class MedioTransporteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MedioTransporte
#         exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedidaProducto
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

class SubcategoriaSerializerTest(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()
    categoria = serializers.StringRelatedField()
    class Meta:
        model = Subcategoria
        # fields = sorted(['id', 'nombre', 'categoria', 'productos'])
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')


    def get_productos(self, obj):
        query = Producto.objects.filter(subcategoria=obj)
        return [ProductoSinPKsSerizalizer(m).data for m in query]

class GraduacionAlcoholSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduacion
        fields = ['graduacion']

graduaciones_qs = Graduacion.objects.all()
# GRADUACIONES = [
#     {
#         'nombre': graduaciones_qs[0].graduacion,
#     },
#     {
#         'nombre': graduaciones_qs[1].graduacion,
#     },
#     {
#         'nombre': graduaciones_qs[2].graduacion,
#     }
# ]

class ImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduacionPais
        fields = ['tasa_impuesto']

    
# graduaciones = Graduacion.objects.values('graduacion','id')
graduaciones_ = Graduacion.objects.values_list('graduacion', 'id')
GRADUACIONES = [{'nombre': graduacion, 'id': id} for graduacion, id in graduaciones_]


class AlcoholSerializer(serializers.ModelSerializer):
    # pais = serializers.SerializerMethodField()

    class Meta:
        model = ProductoPais
        fields = []


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['nombre'] = instance.pais.pais_tlc

        graduacion_pais = GraduacionPais.objects.filter(producto_pais=instance)
        graduaciones = []

        for graduacion in graduacion_pais:
            graduaciones.append({
                'nombre': graduacion.graduacion.graduacion,
                'impuesto': graduacion.tasa_impuesto
            })

        # print(graduaciones)
        representation['graduacion'] = graduaciones
        return representation

    

class ProductoSinPKsSerizalizer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField()
    pais_tlc = serializers.SerializerMethodField()

    nombre = serializers.SerializerMethodField()
    unidad_medida = serializers.ReadOnlyField(source='unidad_medida.unidad')
    franquicia = serializers.SerializerMethodField()

    medio_transporte = serializers.StringRelatedField()
    tipo_viajero = serializers.StringRelatedField()
    # graduacion = serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = sorted(['categoria', 'pais_tlc', 'nombre', 'unidad_medida', 'only_internacional', 'franquicia', 'cantidad_por_persona', 'valuable', 'cantidad_maxima', 'tasa_impuesto', 'infinitos', 'subcategoria', 'medio_transporte', 'tipo_viajero', 'nota', 'leyenda'])
        # exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if instance.pk == 22:
            representation['graduacion_pais'] = GraduacionSerializer(Graduacion.objects.all(), many=True).data

        # if instance.medio_transporte:
        #     representation['medio_transporte']: MedioTransporteSerializer(instance.medio_)
        #     print("medio transporte")
        

        return representation

    def get_pais_tlc(self, obj):
        query = ProductoPais.objects.filter(producto=obj)
        return [ProductoPaisSerializerNotNull(m).data for m in query]

    def get_unidad_medida(self, obj):
        query = obj.unidad_medida
        return UnidadMedidaSerializer(query).data

    def get_nombre(self, obj):
        return obj.nombre_producto

    def get_franquicia(self, obj):
        return obj.aplica_franquicia

        


class MercanciaTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print("INSTANCE PRODUCTOS:", instance.productos.all())
        representation['productos'] = ProductoSinPKsSerizalizer(instance.productos.all(), many=True).data

        return representation

    


#ADUANAS DE INGRESO
class AduanasSerializer(serializers.ModelSerializer):
    """Serializes a aduana field for testing our APIView."""

    class Meta:
        model = AduanaLineas
        fields = '__all__'

class PuntoRevisionSerializer(serializers.ModelSerializer):
    """Serializes a aduana field for testing our APIView."""

    class Meta:
        model = PuntoRevision
        fields = ['id', 'nombre','aduana_id']

#Limite

# class LimiteSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Limite
#         fields = ['limite_internacional', 'limite_residente', 'limite_eq_computo']

class FechaFranquiciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = FechaFranquicia
        fields = ['medio_transporte', 'fecha_inicio', 'fecha_fin', 'franquicia']


#Mi maleta serializers 
class BaseClass(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return dict(ret)
        
class ExcedenteFranquiciaSerializer(BaseClass):
    medio_transporte = serializers.CharField(source="medio_transporte.medio_transporte", allow_null=True)
    nacionalidad = serializers.CharField(source="nacionalidad.nacionalidad", allow_null=True)
    procedencia = serializers.CharField(source="procedencia.procedencia", allow_null=True)

    class Meta:
        model = ExcedenteFranquicia
        #fields = '__all__'
        fields = ["franquicia_normal", "franquicia_norm_fam", "franquicia_paisano", "equipaje", "medio_transporte", "nacionalidad", "procedencia"]

class LimiteFranquiciaSerializer(BaseClass):
    excedente = serializers.CharField(source="excedente.excedente", allow_null=True)

    class Meta:
        model = Limite
        fields = ["limite_excedente", "limite_eq_computo", "limite_franq_alcohol", "limite_franq_tabaco", "excedente"]


class PuntoRevisionSerializer(serializers.ModelSerializer):
    """Serializes a aduana field for testing our APIView."""

    class Meta:
        model = PuntoRevision
        fields = ['id', 'nombre_punto_revision','rel_medio_aduana_id']
from rest_framework import serializers
# from comun.lineas_modular.models import ProductoPais
from lineas_modular.models import *
# from catalogos_modular.models import *
class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        # fields = ['nombre_producto', 'categoria']
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

class CategoriaSerializer(serializers.ModelSerializer):
     class Meta:
        model = Categoria
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')


class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

class PaisTlcSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaisTlc
        exclude = (('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted'))

class ProductoPaisSerializer(serializers.ModelSerializer):
    pais = PaisTlcSerializer()
    class Meta:
        model = ProductoPais
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

class GraduacionPaisSerializer(serializers.ModelSerializer):
    pais_tlc = serializers.ReadOnlyField(source='producto_pais.pais.pais_tlc')
    pais_id = serializers.ReadOnlyField(source='producto_pais.pais.id')
    class Meta:
        model = GraduacionPais
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')


class GraduacionSerializer(serializers.ModelSerializer):
    pais = serializers.SerializerMethodField()

    class Meta:
        model = Graduacion
        exclude = ('created_at', 'created_by', 'updated_by', 'updated_at', 'deleted_by_cascade', 'deleted')

    def get_pais(self, obj):
        query = GraduacionPais.objects.filter(graduacion=obj)
        return [GraduacionPaisSerializer(m).data for m in query]



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
        model = PaisTlc
        fields = []


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['pais'] = instance.pais_tlc

        # graduaciones = GRADUACIONES.copy()
        graduaciones_ = Graduacion.objects.values_list('graduacion', 'id')
        graduaciones = [{'nombre': graduacion, 'id': id} for graduacion, id in graduaciones_]

        for graduacion in graduaciones:

            graduacion_pais = None
            try:
                graduacion_pais = GraduacionPais.objects.get(graduacion_id=graduacion['id'], pais=instance)
                impuesto = graduacion_pais.tasa_impuesto
                graduacion['impuesto'] = impuesto
                del graduacion['id']
            except:
                # del representation
                return None
                


        # print(graduaciones)
        representation['graduacion'] = graduaciones
        print(f"{representation=}")
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

    



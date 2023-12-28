from django.urls import path
from lineascomun import views
app_name = 'excedente_franquicia'




urlpatterns = [
    path('buscar',  views.SearchDeclaracion.as_view(), name='search_declaracion'),
    path('index', views.IndexView.as_view(), name='index'),
    path('registrar',  views.InternoCreateViajeView.as_view(), name='registrar'),
    path('registrar/<str:folio>',  views.InternoCreateViewFromFolio.as_view(), name='registrar_con_folio'),
    path('eliminar/<int:pk>',  views.DeleteView.as_view(), name='eliminar'),
    path('mostrar/<int:pk>',  views.ShowInternoView.as_view(), name='mostrar'),
    path('acuse/<int:pk>',  views.acuse_view, name='acuse'),
    path('csv', views.ViajeCsv.as_view(), name='csv'),


    #API VIEW
    path('api/viaje', views.ViajeAPIView.as_view()),

    path('api/productos', views.ProductoAllAPIView.as_view()),
    path('api/productos/<int:pk>', views.ProductoById.as_view()),
    path('api/productos/categoria/<int:pk>', views.ProductoByCategoriaAPIView.as_view()),
    path('api/productos/subcategoria/<int:pk>', views.ProductoBySubcategoriaAPIView.as_view()),
    
    path('api/categorias', views.CategoriasAPIView.as_view()),
    path('api/mm/categorias', views.CategoriasMiMaletaAPIView.as_view()),
    path('api/mm/categoria/<int:pk>', views.CategoriaMiMaletById.as_view()),
    path('api/categoria/<int:pk>', views.CategoriaById.as_view()),
    path('api/subcategorias/<int:pk>', views.SubcategoriasByCategoriaAPIView.as_view()),
    path('api/producto_pais/<int:pk>', views.ProductoPaisAPIView.as_view()),
    path('api/graduaciones', views.GraduacionAPIView.as_view()),

    path('api/productos/producto_pais', views.ProductosPaisAPIView.as_view()),

    # path('api/mercancias', views.MercanciaAPIView.as_view()),
    path('api/mercancias/<int:pk>', views.MercanciaAPIViewTEST.as_view()),
    path('api/alcohol/', views.AlcoholTest.as_view()),


    path('api/<int:medio>', views.AllPuntosRevision.as_view(), name='prs'),
    path('api/<int:medio>/<int:punto>', views.GetAduanaIngreso.as_view(), name='prs'),

    path('api/limite', views.LimiteAPIView.as_view()),
    path('api/fecha_franquicia', views.FechaFranquiciaAPIView.as_view()),

    #Necesario para que no truene
    path('api/mm/categorias', views.CategoriasMiMaletaAPIView.as_view(), name='categorias_mm'),
]

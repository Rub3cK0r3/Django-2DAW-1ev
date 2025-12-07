from django.urls import include,path
from . import views
from django.views import generic
from django.urls import reverse

"""
urlconf examen 1ºev - appprueba
"""

app_name = 'appprueba'

urlpatterns = [
    # como las reglas de un firewall
    path('',generic.RedirectView.as_view(url='index/',permanent=True)),

    # esta es realmente la que queremos ejecutar conseguimos el redireccionamiento con la url anterior
    path('index/',views.index,name='index_filtro_editores'),


]

# NUEVA URL para REDIRECCION usando REDIRECT hacia la aplicacion de catalog
urlpatterns += path('sacalibros/<int:pk>',views.redireccionar_editor,name='editor_detail'),

# La unica ListView que se nos es permitida en el examen
urlpatterns += path('editores/',views.EditorListView.as_view(),name='editor_list_view'),
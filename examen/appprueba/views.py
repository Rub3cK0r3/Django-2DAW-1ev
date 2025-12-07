from django.shortcuts import render,redirect
from .models import Editor
from django.views import generic

# Create your views here.

from .forms import FormularioFiltroEditores
def index(request):
    form = FormularioFiltroEditores(request.POST or None)
    if request.method == 'POST':
        # por defecto si no se aplica un filtro, se deben de
        # mostrar todos los editores
        editores = Editor.objects.all()
        if form.is_valid():
            if 'pais' in request.POST and form.cleaned_data['pais'] != '':
                pais_filtrar = form.cleaned_data['pais']
                editores = editores.filter(pais = pais_filtrar)
        return render(
            request,
            # Por convención, Django no tiene namespaces automáticos para templates.
            # Si varias apps tienen archivos con el mismo nombre (p. ej. index.html),
            # es obligatorio organizarlos como templates/<nombre_app>/archivo.html
            # para evitar conflictos. Por eso se usa 'appprueba/index.html'.
            'appprueba/index.html',
            {
                'form':form,
                'editores':editores
            }
        )
    return render(
        request,
        'appprueba/index.html',
        {
            'form':form
        }
        )

class EditorListView(generic.ListView):
    model = Editor
    context_object_name = 'editor_list'
    template_name = 'appprueba/editor_list.html'
    paginate_by = 2

def redireccionar_editor(request,pk):
    return redirect('catalog:sacalibros_editor' , pk)
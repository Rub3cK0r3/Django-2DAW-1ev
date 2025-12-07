from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models.functions import Lower
import datetime

from django.http import HttpResponse

from .models import Author, Book, Language, Genre, BookInstance, Editor
from .forms import RenewBookForm

def index(request):
    """
    Vista de la página de inicio del sitio.
    Muestra contadores de objetos principales.
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    num_instances_available = BookInstance.objects.filter(
        status__exact='a'  # __exact es lo mismo que '='
    ).count()
    
    num_authors = Author.objects.count()  # El 'all()' está implícito
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_visits':num_visits,
        },
    )


def book_detail_view(request, pk):
    book = Book.objects.get(pk=pk)
    return render(
        request,
        'catalog/book_detail.html',
        context={'book': book}
    )

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'  # 'object_list' es el nombre genérico
    queryset = Book.objects.all()
    template_name = 'catalog/book_list.html'

class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    queryset = Author.objects.all()
    template_name = 'author_list.html'
    context_object_name = 'author_list'


class AuthorDetailView(generic.DetailView):
    model = Author


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return redirect('all-borrowed')

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    return render(
        request,
        'catalog/book_renew_librarian.html',
        {
            'form': form, 
            'bookinst': book_inst
        }
    )

"""
EXAMEN DE DJANGO - 1ºEV
"""

# catalog/sacalibros/1
# podria ir realmente en las dos aplicaciones, yo por comodidad y por no ir moviendo
# los modelos la he hecho en catalog al ser la url de la aplicacion de catalog
def editor_detail_view(request,pk):
    editor_obtenido = get_object_or_404(Editor,pk = pk)

    # filtro por el nuevo campo
    editor_libros = BookInstance.objects.filter(editor = editor_obtenido)

    return render(
        request,
        'editor_detail.html', # uso el html del modulo de appprueba
        {
            'editor_libros':editor_libros, # segun el modelo que tenemos podemos acceder al 'editor' desde el BookInstance
        }
    )

from .forms import BookinstanceForm,GenreCheckForm,GenreAddForm
# books/1/edit
def bookinstance_detail_view(request,pk):
    form_libro = BookinstanceForm(None or request.POST)
    form_add_genre = GenreAddForm(None or request.POST)

    ejemplar = BookInstance.objects.get(pk = pk)

    form_generos_check = GenreCheckForm(None or request.POST,instance=ejemplar.book)

    if request.POST:
        if form_generos_check.is_valid():
            form_generos_check.save()

        if form_libro.is_valid():
            # guardamos manualemnte los datos en el libro del ejemplar y lo guardamos en la base de datos
            titulo = form_libro.cleaned_data['titulo']
            autor = form_libro.cleaned_data['autor']
            summary = form_libro.cleaned_data['summary']
            ejemplar.book.title = titulo
            ejemplar.book.author = autor
            ejemplar.book.summary = summary

            ejemplar.book.save()
        
        # si hemos añadido un genero lo añadimos en la base de datos y se lo introducimos
        # al libro base, no al ejemplar
        #print('ES VALIDO EL FORM DE ALADIR GENEROS?',form_add_genre.is_valid())
        if form_add_genre.is_valid():
            titulo_nuevo_genero = form_add_genre.cleaned_data['name']
            if titulo_nuevo_genero != '' and titulo_nuevo_genero not in Genre.objects.all().values_list('name',flat=True):
                nuevo_genero = Genre.objects.create(
                    name = titulo_nuevo_genero
                )
                ejemplar.book.genre.add(nuevo_genero)
        

    # paso a GET  
    form_libro = BookinstanceForm(initial={
        'titulo':ejemplar.book.title,
        'autor':ejemplar.book.author,
        'summary':ejemplar.book.summary,
    })

    form_generos_check = GenreCheckForm(instance=ejemplar.book)

    return render(
        request,
        'catalog/bookinstance_detail.html',
        {
            'form_libro':form_libro,
            'form_generos_check':form_generos_check,
            'form_add_genre':form_add_genre
        }
    )

#catalog/books/1
from .forms import GenreBookinstanceDetailForm
def administrar_libros(request,pk):
    bookinstance = BookInstance.objects.get( pk = pk )
    formulario_generos = GenreBookinstanceDetailForm(request.POST or None)
    if request.method == 'POST':
        if formulario_generos.is_valid():
            #print(formulario_generos.data)
            # si hemos creado un genero que no se encuentra ya en la base de datos
            if 'crear_genero' in request.POST and formulario_generos.cleaned_data['genero_creacion'] not in Genre.objects.all().values_list('name',flat=True) and formulario_generos.cleaned_data['genero_creacion'] != '':
                nuevo_genero = Genre.objects.create(
                    name = formulario_generos.cleaned_data['genero_creacion']
                )
                # lo añadimos al libro!
                bookinstance.book.genre.add(nuevo_genero)
            # si el genero que hemos seleccionado no esta ya en el libro
            elif formulario_generos.cleaned_data['genero_seleccion'] not in bookinstance.book.genre.all().values_list('name',flat=True):
                bookinstance.book.genre.add(formulario_generos.cleaned_data['genero_seleccion'])
    # tanto como si hemos entrado con GET como con POST tenemos que renderizar la template con el formulario
    return render(
        request,
        'bookinstance_form.html',
        {
            'formulario_generos':formulario_generos,
            'bookinstance':bookinstance
        }
    )

# para elimnar el genero de un libro especifico con el boton de la
# lista
def eliminar_genero_libro(request,genero_pk,bookinstance_pk):
    #print('estoy eliminando...')
    bookinstance = get_object_or_404(BookInstance, pk = bookinstance_pk)
    genero = get_object_or_404(Genre, pk = genero_pk)
    bookinstance.book.genre.remove(genero)
    bookinstance.book.save()

    return redirect('catalog:administrar_libros_editor' , bookinstance_pk)
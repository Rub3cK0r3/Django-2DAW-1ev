from django.contrib import admin

# Register your models here.
from .models import Author,Genre,Book,BookInstance,Language
from appprueba.models import Editor

admin.site.register(Genre)
admin.site.register(Language)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','birth_date','death_date')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # En el display_genre lo que me va a mostrar es el SHORT_DESCRIPTION
    # eso lo hace en todos los campos el admin
    list_display = ('title','author','display_genre')

    # Me conviene ver las instancias de un libro, pero de ese libro en concreto
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):  
    
    # ESTO ENTRA DENTRO DE LA VISTA DE LISTA
    list_display = ('book','status','due_back','id','editor')
    list_filter = ('status', 'due_back')

    # ESTO ENTRA DENTRO DE LA VISTA DE DETALLE
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
        ('Editor', {
            'fields': ('editor',)
        }),
    )

# Registro el editor
admin.site.register(Editor)
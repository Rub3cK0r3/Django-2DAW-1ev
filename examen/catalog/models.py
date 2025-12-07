from django.db import models
from django.urls import reverse
import uuid
from appprueba.models import Editor

class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Introduce el nombre del género",
        verbose_name="nombre"
    )

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Introduce el nombre del idioma")

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100, help_text="Introduce el nombre del autor")
    birth_date = models.DateField(
        blank=True, null=True,
        help_text="Introduce cuándo nació el autor si lo conoces"
    )
    death_date = models.DateField(
        blank=True, null=True,
        help_text="Introduce la fecha de fallecimiento si la conoces"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_detail', args=[str(self.id)])

class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Introduce el título del libro")
    
    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        help_text="Introduce el autor del libro",
        null=True, blank=True,
        related_name='librosaut'
    )
    
    isbn = models.CharField(max_length=13, help_text="Introduce el ISBN del libro")
    
    genre = models.ManyToManyField(
        Genre,
        help_text="Introduce el género del libro",
        related_name='librosgen'
    )
    
    summary = models.TextField(
        max_length=100,
        help_text="Introduce el resumen del libro",
        verbose_name="descripción"
    )
    
    original_language = models.ForeignKey(
        'Language',
        help_text="Introduce el idioma original del libro",
        on_delete=models.RESTRICT,
        related_name='librosidiom'
    )

    class Meta:
        ordering = ["author"]

    def __str__(self):
        return self.title

    def display_genre(self):
        """Muestra los primeros 3 géneros del libro"""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    
    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    
    book = models.ForeignKey(
        'Book',
        help_text="Introduce el libro al que pertenece el ejemplar",
        on_delete=models.RESTRICT,
        related_name='instancias'
    )
    
    LOAN_STATUS = (
        ('a', 'Available'),
        ('o', 'On loan'),
        ('r', 'Reserved'),
        ('m', 'Maintenance')
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default='m',
        help_text="Introduce el estado del ejemplar"
    )
    
    imprint = models.CharField(
        max_length=100,
        help_text="Introduce los detalles de esta edición"
    )
    
    due_back = models.DateField(
        null=True, blank=True,
        help_text="Introduce la fecha de devolución del préstamo"
    )

    # SI O SI tiene un editor un ejemplar ("Santillana","Planeta",...)
    editor = models.ForeignKey(Editor,on_delete=models.CASCADE,default=1)

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return f"{self.book} {self.id}"

    def get_absolute_url(self):
        return reverse('catalog:bookinstance_detail', args=[str(self.id)])
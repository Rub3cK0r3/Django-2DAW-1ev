from django.urls import path,include
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),

    path('books/',views.BookListView.as_view(),name='books'),
    path('authors/',views.AuthorListView.as_view(),name='authors'),
    path('book/<int:pk>',views.BookDetailView.as_view(),name='book_detail'),
    path('author/<int:pk>',views.AuthorDetailView.as_view(),name='author_detail'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

"""
urlconf examen 1ºev - catalog
"""

urlpatterns += path('sacalibros/<int:pk>',views.editor_detail_view,name='sacalibros_editor'),

urlpatterns += path('books/<uuid:pk>/edit/',views.bookinstance_detail_view,name='bookinstance_detail'),

urlpatterns += path('books/<uuid:pk>/',views.administrar_libros,name='administrar_libros_editor'),

urlpatterns += path('eliminar/genero/<int:genero_pk>/libro/<uuid:bookinstance_pk>/',
                    views.eliminar_genero_libro,
                    name='eliminar_genero_libro'
                ),
# Django Exam Project – 2º DAW, 1st Evaluation

This is my Django project for the **2º DAW 1st evaluation exam**.  
It has one main project (`examen`) and two apps:

- **catalog**: from the MDN LocalLibrary tutorial. Manages books, authors, genres, languages, and book copies.  
- **appprueba**: my own app to manage editors and filter books by editor.

> Note: all comments in the code are in Spanish.

---

## Requirements

- Python 3.x  
- Django 4.x  
- SQLite (default)

---

## How to run

1. Go to project folder:
2. Create virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r ../requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. (Optional) Create superuser:

```bash
python manage.py createsuperuser
```

5. Run server:

```bash
python manage.py runserver
```

6. Open in browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Apps

### Catalog

* Models: Author, Book, BookInstance, Genre, Language
* Features: list/view books and authors, edit authors, renew books, manage genres

### AppPrueba

* Model: Editor
* Features: list editors, filter by country, redirect to books of an editor

---

## Project Structure

```
examen/
├── appprueba/
├── catalog/
├── db.sqlite3
├── examen/
└── manage.py
```

---

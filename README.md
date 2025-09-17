# Django Projects

This repository contains two Django-based web applications developed for learning and demonstration purposes.

---

## 1. My Tennis Club

A simple Django project for managing tennis club members.

**Features:**
- List and view club members
- Member details page
- Home page with personalized greeting
- Uses Django templates and Bootstrap for styling

**Structure:**
- `my_tennis_club/` — Main Django project folder
- `members/` — Django app for member management
- `db.sqlite3` — SQLite database

**How to run:**
1. Activate the virtual environment:
   ```
   cd myworld
   .\Scripts\activate
   ```
2. Run migrations:
   ```
   python my_tennis_club/manage.py makemigrations
   python my_tennis_club/manage.py migrate
   ```
3. Start the server:
   ```
   python my_tennis_club/manage.py runserver
   ```
4. Access the app at `http://localhost:8000/`

---

## 2. Local Library

A Django project for managing a library catalog.

**Features:**
- Manage books, authors, genres, and languages
- Admin interface for adding and editing data
- Book instances with loan status
- Language model for supporting books in multiple languages

**Structure:**
- `local_lib/` — Main Django project folder
- `catalog/` — Django app for library catalog
- `db.sqlite3` — SQLite database

**How to run:**
1. Activate the virtual environment:
   ```
   cd lib_env
   .\Scripts\activate
   ```
2. Run migrations:
   ```
   python local_lib/manage.py makemigrations
   python local_lib/manage.py migrate
   ```
3. Create a superuser for admin access:
   ```
   python local_lib/manage.py createsuperuser
   ```
4. Start the server:
   ```
   python local_lib/manage.py runserver
   ```
5. Access the app at `http://localhost:8000/` and the admin at `http://localhost:8000/admin/`

---

## Note

The `book_list.html` template is not yet finished, but the main functionality is working.  
These projects are for demonstration and learning Django basics.
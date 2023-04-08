# Book-Spine
The backend framework written in django while using postgres as a DB

# Installation
1. Install required packages
```pip install -r requirements.txt```
2. Create .env file in root directory. Contact creator for details.
3. Install Postgres: https://www.postgresql.org/download/
4. Setup base db called 'journalai'
5. Run ```python3 -m spacy download en_core_web_lg```
6. Install redis (On Mac: ```brew install redis```)

# Presidio Installation
1. open a python terminal from the virtual environment
2. Run '''>>import spacy.cli'''
3. Run '''>>spacy.cli.download("en_core_web_lg")'''

# Run Server
```python manage.py runserver ```

# Run Celery 
```redis-server```
```python -m celery -A journal_ai worker -l info```

# Migrations
```python manage.py makemigrations```
```python manage.py migrate ```
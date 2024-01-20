# TOEFL practice

TOEFL practice website

![](https://shields.io/badge/dependencies-Python_3.11-blue)

## Usage

1. Visit https://djecrety.ir/ and generate a Django key.

2. Create a text file `django_key` and write the Django key to this file. Do not add a new line at the end.

3. Download a released database to the program root directory.

4. Run the following command.
   ```
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

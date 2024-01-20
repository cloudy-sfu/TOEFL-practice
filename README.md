# TOEFL practice

TOEFL practice website

![](https://shields.io/badge/dependencies-Python_3.11-blue)

## Usage

Create an empty file `security.json` at the program root directory. The example file is

```json
{
  "secret_key": "xq4%ni8h!)((25sh(yvys-8ec=ns71$&r91-w52vgg_r$j6u58",
  "allowed_hosts": [
    "example.com",
    "localhost"
  ],
  "csrf_trusted_origins": ["https://example.com"]
}
```

"secret_key": Visit https://djecrety.ir/ and generate a Django key.

"csrf_trusted_origins": It must contain the schema (usually "http" or "https").

Download a released database, unzip it, and move it to the program root directory.

Run the following command.
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

Start the service:

```
python manage.py runserver --insecure 0.0.0.0:8000
```


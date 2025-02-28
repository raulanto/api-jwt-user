# Api

```aiignore
Endpoint        Methods  Rule
--------------  -------  -----------------------
auth.login      POST     /auth/login            
auth.protected  GET      /auth/protected
auth.refresh    POST     /auth/refresh
auth.register   POST     /auth/register
static          GET      /static/<path:filename>

```
Preparar entorno de desarrollo
```bash
$ python3 -m venv venv
```

Activar entorno virtual
```bash
   Para mac
$ source venv/bin/activate
  Para windows
  venv\Scripts\activate
````
Instalar reuqermientos

```bash
   pip install -r requirements.txt
```
crear archivo .flaskenv
```
FLASK_APP=main
FLASK_ENV=development
```

crear archivo .env
```
SECRET_KEY=dfh24ru4h2rhg9482fh4of42ofy48o@r2f28f29f20
JWT_SECRET_KEY=nsifo0f8hwohnpw4hf04w9fw4fwfwfw4f8u4fh$fwf
```
Hacer mnigraciones
```
$ flask db init
```
```
    flask db migrate
```
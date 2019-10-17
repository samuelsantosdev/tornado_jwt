# Tornado + JWT + AsyncPG + Swagger

## Run
* pip install -r requirements.txt
* set the environment variables
```
    export MS_ALLOW_ORIGIN='*'
    export MS_ALLOW_METHODS="POST,GET,DELETE,PUT,PATCH,OPTIONS"
    export MS_PORT=8080
    export DB_HOST='127.0.0.1'
    export DB_PORT=5432
    export DB_USER=user
    export DB_PASS=pass
    export DB_NAME=database
```
* python main.py
* access in your browser 127.0.0.1:8080


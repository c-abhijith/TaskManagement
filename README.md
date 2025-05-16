Django Project with DRF & Template Rendering
This project integrates Django

This project integrates Django REST Framework (DRF) and traditional template rendering. You can access the login page via a browser, or interact with the API using Postman.


postman documention :https://documenter.getpostman.com/view/44984967/2sB2qWHPem

SETUP INSTRUCTIONS
    For Linux or macOS users:

    Run the following commands in your terminal:
            make env-setup
            make run-local

    For Windows users:

    Run the following commands in Command Prompt or PowerShell:

            python3 -m venv venv
            .\venv\Scripts\activate
            pip install -r requirements.txt
            python manage.py makemigrations
            python manage.py migrate
            python manage.py runserver

LoginUrl:http://127.0.0.1:8000/login/



You can create a superuser using the following command:         

            python manage.py createsuper
    
Alternatively, a superuser has already been created with the following credentials:


            username : Superuser
            password : Superuser@123


Docker commands :  docker-compose up --build
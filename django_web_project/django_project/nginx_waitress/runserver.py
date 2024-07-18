from waitress import serve

#AZURE
from django_project.wsgi import application
# documentation: https://docs.pylonsproject.org/projects/waitress/en/stable/api.html

if __name__ == '__main__':
    serve(application, host = 'localhost', port='8080')

from wfastcgi import WSGIServer
from fiscalia.wsgi import application  # Importa tu aplicación WSGI de Django

WSGIServer(application).run()

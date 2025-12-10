"""WSGI entry point for hosting the chatbot on production servers."""
from chatbot import app as application

# Optional alias for servers expecting `app`
app = application

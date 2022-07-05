import os
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PeersApp.settings.dev')


django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     # Just HTTP for now. (We can add other protocols later.)
# })


django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  # Just HTTP for now. (We can add other protocols later.)
})
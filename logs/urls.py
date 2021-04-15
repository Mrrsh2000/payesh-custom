from .views import *
from payesh.dynamic import *
from .models import *

urlpatterns = [
    generate_url(Log(), view=LogListView, add_model_to_url=False),
]

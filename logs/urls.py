from .views import *
from abresani.dynamic import *
from .models import *

urlpatterns = [
    generate_url(Log(), view=LogListView, add_model_to_url=False),
]

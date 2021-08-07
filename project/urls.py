from payesh.dynamic import *
from .views import *

urlpatterns = [
    generate_url(Project(), create=ProjectCreateView, add_model_to_url=False),
    generate_url(Project(), view=ProjectListView, add_model_to_url=False),
    generate_url(Project(), update=ProjectUpdateView, add_model_to_url=False),
    path('education_datatable', ProjectEducationListView.as_view(), name='education_project_datatable')
]

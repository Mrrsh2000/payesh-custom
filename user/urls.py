from abresani.dynamic import *
from .views import *

urlpatterns = [
    generate_url(User(), create=UserCreateView, add_model_to_url=False),
    generate_url(User(), view=UserListView, add_model_to_url=False),
    # generate_url(User(), datatable=UserDataTableView),
    generate_url(User(), update=UserUpdateView, add_model_to_url=False),
    path('self', SelfUpdateView.as_view(), name='self'),
]

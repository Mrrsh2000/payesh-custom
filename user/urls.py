from payesh.dynamic import *
from user.student import *
from .views import *

urlpatterns = [
    generate_url(User(), create=UserCreateView, add_model_to_url=False),
    generate_url(User(), view=UserListView, add_model_to_url=False),
    # generate_url(User(), datatable=UserDataTableView),
    generate_url(User(), update=UserUpdateView, add_model_to_url=False),
    path('self', SelfUpdateView.as_view(), name='self'),
    path('student/create', StudentCreateView.as_view(), name='student_create'),
    path('student/list', StudentListView.as_view(), name='student_list'),
    path('student/update', StudentUpdateView.as_view(), name='student_update'),
]

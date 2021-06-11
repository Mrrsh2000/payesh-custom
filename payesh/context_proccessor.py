from payesh.settings import ROLES_EXCEPT_STUDENT


def p(request):
    if not request.user.is_authenticated:
        return {}
    return {
        'can_user': request.user.role == 'admin',
        'can_student': request.user.role in ROLES_EXCEPT_STUDENT,
        'is_student': request.user.role == 'student',
    }

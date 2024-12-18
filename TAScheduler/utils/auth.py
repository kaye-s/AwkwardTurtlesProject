from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def group_required(group_name):
    """
    Decorator to check if a user belongs to a specific group.
    """
    def in_group(user):
        if user.is_authenticated and user.groups.filter(name=group_name).exists():
            return True
        raise PermissionDenied  # Raise 403 error for unauthorized users

    return user_passes_test(in_group)

def method_group_required(group_name):
    def wrap(func):
        def wrapper(self, request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return func(self, request, *args, **kwargs)
            else:
                raise PermissionDenied
            
        return wrapper
    return wrap
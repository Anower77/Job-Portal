from django.core.exceptions import PermissionDenied

def user_is_employer(function):
    def wrap(request, *args, **kwargs):   
        if request.user.role == 'employer':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap



def user_is_employee(function):
    def wrap(request, *args, **kwargs):    
        if request.user.role == 'employee':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap
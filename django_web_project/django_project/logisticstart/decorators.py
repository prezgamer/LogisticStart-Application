from django.shortcuts import redirect

def login_required(function):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session:
            return redirect('logisticstart-login')
        return function(request, *args, **kwargs)
    return wrap
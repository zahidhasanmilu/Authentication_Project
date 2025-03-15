from django.shortcuts import redirect, HttpResponse

def logout_required(view_func):
    """
    Custom decorator to restrict access to logged-in users.
    Redirects logged-in users to a specific page.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('You are already logged in.')
        return view_func(request, *args, **kwargs)
    return wrapper
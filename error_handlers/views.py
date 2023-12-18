from django.shortcuts import render

def error_handler(request, exception=None):
    status_code = getattr(exception, 'status_code', 500)
    if status_code == 400:
        message = "bad_request"
    elif status_code == 403:
        message = "permission_denied"
    elif status_code == 404:
        message = "page_not_found"
    else:
        message = "server_error"

    return render(request, "error.html", {"status_code":status_code, "message":message}, status=status_code)

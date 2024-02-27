from django.shortcuts import render


def error_400(request, exception):
    status_code = 400
    message = "bad_request"
    return render(
        request,
        "error.html",
        {"status_code": " ".join(str(status_code)), "message": message},
        status=status_code,
    )


def error_403(request, exception):
    status_code = 403
    message = "PERMISSION DENIED"
    return render(
        request,
        "error.html",
        {"status_code": " ".join(str(status_code)), "message": message},
        status=status_code,
    )


def error_404(request, exception):
    status_code = 404
    message = f"PAGE {request.path} NOT FOUND"
    return render(
        request,
        "error.html",
        {"status_code": " ".join(str(status_code)), "message": message},
        status=status_code,
    )


def error_500(request):
    status_code = 500
    message = "SERVER ERROR"
    return render(
        request,
        "error.html",
        {"status_code": " ".join(str(status_code)), "message": message},
        status=status_code,
    )

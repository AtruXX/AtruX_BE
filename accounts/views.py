from django.shortcuts import render

def activation_page(request, uid, token):
    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'pages/verify_email.html', context)

def reset_password_page(request, uid, token):
    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'pages/change_password.html', context)

def activation_page_ok(request):
    return render(request, "pages/verify_email_success.html");

def reset_pass_ok(request):
    return render(request, "pages/change_password_success.html")
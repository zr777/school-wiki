from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


# Create your views here.
def guest_login(request, page_id):

    user = authenticate(username='guest', password='xiaodengshen')
    # should add host auth...
    login(request, user)
    # host = 'http://127.0.0.1:8000'
    return redirect('/admin/pages/%s/edit/' % page_id)

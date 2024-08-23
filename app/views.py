from django.shortcuts import render


def menu_view(request, name=None):
    return render(request, 'page.html')

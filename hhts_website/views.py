from django.shortcuts import render


def home(request):
    return render(request, 'hh2/home.html')


def about(request):
    return render(request, 'hh2/about.html')


def guide_info(request):
    return render(request, 'hh2/guide.html')


def saijo_info(request):
    return render(request, 'hh2/saijo.html')

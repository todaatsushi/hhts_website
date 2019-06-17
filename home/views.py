from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html')


def about(request):
    return render(request, 'home/about.html')


def guide_info(request):
    return render(request, 'home/guide.html')


def saijo_info(request):
    return render(request, 'home/saijo.html')
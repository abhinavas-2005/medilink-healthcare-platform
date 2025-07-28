from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def page1_view(request):
    return render(request, 'page1.html')

def ab3(request):
    return render(request, 'ab3.html')

def ab1(request):
    return render(request, 'ab1.html')

def ab2(request):
    return render(request, 'ab2.html')


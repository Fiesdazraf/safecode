from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def portfolio(request):
    return render(request, 'main/portfolio.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/contact_success.html')
        else:
            print(form.errors)
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

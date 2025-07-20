from django.shortcuts import render
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
            return render(request, 'main/contact_success.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})
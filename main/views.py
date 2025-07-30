from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from .models import PortfolioItem, Service

# Create your views here.

# views.py

def home(request):
    all_items = PortfolioItem.objects.all().order_by('-created_at')
    todo_item = PortfolioItem.objects.filter(title__icontains='todo').first()
    return render(request, 'main/home.html', {
        'items': all_items,
        'todo_item': todo_item,
    })

def portfolio(request):
    items = PortfolioItem.objects.order_by('-created_at')  # جدیدترین‌ها اول
    return render(request, 'main/portfolio.html', {
        'items': items
    })

def contact(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            subject = f"New message from {contact.name}"
            message = f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, ['farzad.seif30@gmail.com'])

            success = True
            form = ContactForm()  # فرم خالی شود
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {
        'form': form, 
        'success': success
    })

def test_email(request):
    try:
        send_mail(
            'Test Email',
            'This is a test email.',
            'farzad.seif30@gmail.com',
            ['farzad.seif30@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully')
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    except Exception as e:
        return HttpResponse(f'Error occurred: {e}')


def todo_view(request):
    return render(request, 'todo-app/index.html')

def portfolio_detail(request, slug):
    item = get_object_or_404(PortfolioItem, slug=slug)
    return render(request, 'main/portfolio_detail.html', {
        'item': item
    })


def home_view(request):
    services = Service.objects.all()
    all_items = PortfolioItem.objects.all().order_by('-created_at')
    todo_item = PortfolioItem.objects.filter(title__icontains='todo').first()

    return render(request, 'main/home.html', {
        'services': services,
        'items': all_items,
        'todo_item': todo_item,
    })

from __future__ import annotations
import logging
from typing import Optional

from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods, require_GET

from .forms import ContactForm
from .models import PortfolioItem, Service

logger = logging.getLogger(__name__)

# --------------------------------
# Home
# --------------------------------
@cache_page(60 * 5) 
@require_GET
def home(request: HttpRequest) -> HttpResponse:
    services = Service.objects.only("title", "description", "icon", "order")

    # ۹ نمونه‌کار آخر
    items_qs = PortfolioItem.objects.only("id", "title", "slug", "created_at").order_by("-created_at")
    items = list(items_qs[:9])

    # نمونه‌کار todo (ویترین اختصاصی)
    todo_item = (
        items_qs.filter(Q(slug__icontains="todo") | Q(title__icontains="todo")).first()
    )
    if todo_item:
        items = [i for i in items if i.pk != todo_item.pk]

    context = {"services": services, "items": items, "todo_item": todo_item}
    return render(request, "main/home.html", context)


# برای سازگاری قدیمی
@require_GET
def home_view(request: HttpRequest) -> HttpResponse:
    return home(request)


# --------------------------------
# Portfolio
# --------------------------------
@require_GET
def portfolio_page(request: HttpRequest) -> HttpResponse:
    items = (
        PortfolioItem.objects
        .only("id", "title", "slug", "image", "description", "created_at", "icon_path", "project_url", "sort_order")  # include sort_order
        .order_by("-sort_order", "-created_at")  # respect custom order first
    )
    return render(request, "main/portfolio.html", {"items": items})

@require_GET
def portfolio_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """صفحه جزئیات نمونه‌کار"""
    item = get_object_or_404(
        PortfolioItem.objects.only("id", "title", "slug", "image", "description", "project_url"),
        slug=slug
    )
    related_items = (
        PortfolioItem.objects.only("title", "slug", "image", "description", "created_at")
        .exclude(pk=item.pk)
        .order_by("-created_at")[:3]
    )
    return render(request, "main/portfolio_detail.html", {
        "item": item,
        "related_items": related_items,
    })


# --------------------------------
# Contact
# --------------------------------
@require_http_methods(["GET", "POST"])
def contact(request: HttpRequest) -> HttpResponse:
    success = False
    email_sent = False
    email_error: Optional[str] = None

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_obj = form.save()
            success = True
            subject = f"new message from {contact_obj.name}"
            message = (
                f"name: {contact_obj.name}\n"
                f"email: {contact_obj.email}\n\n"
                f"message:\n{contact_obj.message}"
            )
            try:
                send_mail(
                    subject,
                    message,
                    getattr(settings, "EMAIL_HOST_USER", contact_obj.email),
                    ["farzad.seif30@gmail.com"],
                    fail_silently=False,
                )
                email_sent = True
                form = ContactForm()
            except BadHeaderError:
                email_error = "هدر ایمیل نامعتبر بود."
                logger.error("BadHeaderError while sending email for Contact(id=%s)", contact_obj.id)
            except Exception as e:
                email_error = "ارسال ایمیل با خطا مواجه شد."
                logger.error("Email sending failed for Contact(id=%s): %s", contact_obj.id, e, exc_info=True)
    else:
        form = ContactForm()

    context = {"form": form, "success": success, "email_sent": email_sent, "email_error": email_error}
    return render(request, "main/contact.html", context)


@require_GET
def test_email(request: HttpRequest) -> HttpResponse:
    try:
        send_mail(
            "Test Email",
            "This is a test email.",
            getattr(settings, "EMAIL_HOST_USER", "no-reply@example.com"),
            ["farzad.seif30@gmail.com"],
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully")
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    except Exception as e:
        logger.error("test_email failed: %s", e, exc_info=True)
        return HttpResponse(f"Error occurred: {e}")


# --------------------------------
# Todo App
# --------------------------------
@require_GET
def todo_view(request: HttpRequest) -> HttpResponse:
    return render(request, "todo-app/index.html")

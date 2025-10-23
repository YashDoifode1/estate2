from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Property, Amenity, PropertyView
from .forms import ScheduleVisitForm
import json

def property_list(request):
    """Property listing page with filters"""
    locations = Property.objects.filter(is_active=True).values_list('location', flat=True).distinct()
    
    context = {
        'locations': sorted([loc for loc in locations if loc]),
    }
    return render(request, 'properties/property_list.html', context)

def get_properties(request):
    """AJAX endpoint for property filtering and pagination"""
    # Get filter parameters
    status = request.GET.get('status', 'all')
    property_type = request.GET.get('type', 'all')
    location = request.GET.get('location', 'all')
    bedrooms = request.GET.get('bedrooms', 'all')
    price_range = request.GET.get('price', 'all')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'newest')
    page_number = int(request.GET.get('page', 1))
    
    # Start with active properties
    properties = Property.objects.filter(is_active=True)
    
    # Apply filters
    if status != 'all':
        properties = properties.filter(status=status)
    
    if property_type != 'all':
        properties = properties.filter(type=property_type)
    
    if location != 'all':
        properties = properties.filter(location__icontains=location)
    
    if bedrooms != 'all':
        if bedrooms == '4':
            properties = properties.filter(bedrooms__gte=4)
        else:
            properties = properties.filter(bedrooms=bedrooms)
    
    if price_range != 'all':
        price_ranges = {
            '0-20': (0, 2000000),
            '20-40': (2000000, 4000000),
            '40-60': (4000000, 6000000),
            '60-100': (6000000, 10000000),
            '100-999': (10000000, 999999999)
        }
        if price_range in price_ranges:
            min_price, max_price = price_ranges[price_range]
            properties = properties.filter(price__gte=min_price, price__lte=max_price)
    
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Apply sorting
    if sort_by == 'price-low':
        properties = properties.order_by('price')
    elif sort_by == 'price-high':
        properties = properties.order_by('-price')
    elif sort_by == 'name':
        properties = properties.order_by('title')
    else:  # newest
        properties = properties.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(properties, 9)  # 9 properties per page
    page_obj = paginator.get_page(page_number)
    
    # Prepare property data for JSON response
    property_data = []
    for prop in page_obj:
        primary_image = prop.images.filter(is_primary=True).first()
        image_url = primary_image.image.url if primary_image and primary_image.image else 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        
        # Format price based on status
        if prop.status == 'for_rent':
            price_display = f'₹{prop.price:,.0f}/month'
        else:
            price_display = f'₹{prop.price:,.0f}'
        
        property_data.append({
            'id': prop.id,
            'title': prop.title,
            'location': prop.location,
            'price': price_display,
            'type': prop.type,
            'status': prop.status,
            'bedrooms': prop.bedrooms,
            'bathrooms': prop.bathrooms,
            'image': image_url,
            'featured': prop.is_featured,
            'total_area': f'{prop.total_area} sq.ft.',
        })
    
    return JsonResponse({
        'properties': property_data,
        'current_page': page_number,
        'total_pages': paginator.num_pages,
        'total_properties': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    })

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Property, Amenity, PropertyView
from .forms import ScheduleVisitForm
import json

def property_detail(request, property_id):
    """Property detail page"""
    try:
        property_obj = get_object_or_404(Property, id=property_id, is_active=True)
    except Property.DoesNotExist:
        raise Http404("Property does not exist or is not active")
    
    # Track view
    if request.user.is_authenticated:
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        PropertyView.objects.create(
            property=property_obj,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    # Get similar properties
    similar_properties = Property.objects.filter(
        is_active=True,
        type=property_obj.type,
        status=property_obj.status
    ).exclude(id=property_obj.id)[:3]
    
    form = ScheduleVisitForm()
    
    context = {
        'property': property_obj,
        'similar_properties': similar_properties,
        'form': form,
    }
    return render(request, 'properties/property_detail.html', context)

from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from .models import Property, ScheduledVisit

def schedule_visit(request, property_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        message = request.POST.get('message', '')

        try:
            property_obj = Property.objects.get(id=property_id)

            # Save visit details in DB
            visit = ScheduledVisit.objects.create(
                property=property_obj,
                name=name,
                email=email,
                phone=phone,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                message=message,
            )

            # ---------- Email to Agent/Admin ----------
            agent_email = getattr(property_obj.agent, 'email', settings.DEFAULT_FROM_EMAIL)
            subject_agent = f"New Visit Scheduled for {property_obj.title}"
            message_agent = (
                f"Hello {property_obj.agent.name if hasattr(property_obj, 'agent') else 'Admin'},\n\n"
                f"A new property visit has been scheduled:\n\n"
                f"Property: {property_obj.title}\n"
                f"Location: {property_obj.location}\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Preferred Date: {preferred_date}\n"
                f"Preferred Time: {preferred_time}\n\n"
                f"Message: {message or 'N/A'}\n\n"
                f"— DreamHomes Realty"
            )

            send_mail(
                subject_agent,
                message_agent,
                settings.DEFAULT_FROM_EMAIL,
                [agent_email],
                fail_silently=False,
            )

            # ---------- Email Confirmation to User ----------
            subject_user = f"Visit Confirmation — {property_obj.title}"
            message_user = (
                f"Hi {name},\n\n"
                f"Thank you for scheduling a visit for the property '{property_obj.title}'.\n"
                f"Here are your visit details:\n\n"
                f"Date: {preferred_date}\n"
                f"Time: {preferred_time}\n"
                f"Address: {property_obj.location}\n\n"
                f"Our agent will contact you shortly to confirm the visit.\n\n"
                f"Best regards,\n"
                f"DreamHomes Realty"
            )

            send_mail(
                subject_user,
                message_user,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'Your visit has been scheduled successfully! A confirmation email has been sent.'})

        except Property.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Property not found.'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm  # Make sure you have a ContactForm in forms.py

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()  # Save in DB

            # ----- Email to Admin -----
            subject_admin = f"New Contact Message: {contact.subject}"
            message_admin = (
                f"You have received a new contact form message from DreamHomes Realty:\n\n"
                f"Name: {contact.name}\n"
                f"Email: {contact.email}\n"
                f"Phone: {contact.phone or 'N/A'}\n"
                f"Subject: {contact.subject}\n\n"
                f"Message:\n{contact.message}\n\n"
                f"---\nThis message was sent from DreamHomes Realty website."
            )

            send_mail(
                subject_admin,
                message_admin,
                settings.DEFAULT_FROM_EMAIL,
                ['info@dreamhomesrealty.com'],  # Admin/sales team email
                fail_silently=False,
            )

            # ----- Confirmation Email to User -----
            subject_user = "Thank you for contacting DreamHomes Realty"
            message_user = (
                f"Hi {contact.name},\n\n"
                f"Thank you for reaching out to DreamHomes Realty.\n"
                f"We’ve received your message and our team will get back to you shortly.\n\n"
                f"Your message details:\n"
                f"Subject: {contact.subject}\n"
                f"Message: {contact.message}\n\n"
                f"Best regards,\n"
                f"DreamHomes Realty Team\n"
                f"📞 +91 98765 43210\n"
                f"✉️ info@dreamhomesrealty.com"
            )

            send_mail(
                subject_user,
                message_user,
                settings.DEFAULT_FROM_EMAIL,
                [contact.email],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent successfully! Check your email for confirmation.")
            return redirect('properties:contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, 'properties/contact.html', {'form': form})


def contact(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data or send email
            contact_instance = form.save()  # if using a model form
            # Or send email logic here if not using model
            messages.success(request, "Thank you! Your message has been sent successfully.")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    # OpenStreetMap/OpenStreetView coordinates for Nagpur office
    office_location = {
        "lat": 21.1458,  # Latitude for Nagpur
        "lng": 79.0882,  # Longitude for Nagpur
        "zoom": 16
    }

    context = {
        'form': form,
        'office_location': office_location,
    }
    return render(request, 'properties/contact.html', context)

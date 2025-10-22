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

def schedule_visit(request, property_id):
    """Handle schedule visit form submission"""
    if request.method == 'POST':
        property_obj = get_object_or_404(Property, id=property_id)
        form = ScheduleVisitForm(request.POST)
        
        if form.is_valid():
            # Here you would typically:
            # 1. Save the inquiry to database
            # 2. Send email notifications
            # 3. Integrate with CRM
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you! Our agent will contact you shortly to schedule your visit.'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data()
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm  # Make sure you have a ContactForm in forms.py

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

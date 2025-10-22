from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Property, PropertyType, Amenity, FavoriteProperty, PropertyView
from .forms import PropertyFilterForm, ScheduleVisitForm, ContactForm  # We'll create ContactForm

# Add this contact view function
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email (in production, you'd use Celery for this)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Email to admin
            admin_subject = f"New Contact Form Submission: {subject}"
            admin_message = f"""
            Name: {name}
            Email: {email}
            Subject: {subject}
            Message: {message}
            
            This message was sent from the DreamHomes Realty contact form.
            """
            
            try:
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],  # Add this to settings
                    fail_silently=False,
                )
                
                # Confirmation email to user
                user_subject = "Thank you for contacting DreamHomes Realty"
                user_message = f"""
                Dear {name},
                
                Thank you for contacting DreamHomes Realty. We have received your message and will get back to you within 24 hours.
                
                Your Message:
                {message}
                
                Best regards,
                DreamHomes Realty Team
                """
                
                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                return redirect('contact')
                
            except Exception as e:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
    
    else:
        form = ContactForm()
    
    return render(request, 'properties/contact.html', {'form': form})
    
def property_list(request):
    form = PropertyFilterForm(request.GET or None)
    properties = Property.objects.filter(is_active=True)
    
    # Apply filters
    if form.is_valid():
        status = form.cleaned_data.get('status')
        property_type = form.cleaned_data.get('property_type')
        location = form.cleaned_data.get('location')
        bedrooms = form.cleaned_data.get('bedrooms')
        price_range = form.cleaned_data.get('price_range')
        search = form.cleaned_data.get('search')
        
        if status and status != 'all':
            properties = properties.filter(status=status)
        
        if property_type and property_type != 'all':
            properties = properties.filter(property_type__name=property_type)
        
        if location and location != 'all':
            properties = properties.filter(location__icontains=location)
        
        if bedrooms and bedrooms != 'all':
            if bedrooms == '4':
                properties = properties.filter(bedrooms__gte=4)
            else:
                properties = properties.filter(bedrooms=bedrooms)
        
        if price_range and price_range != 'all':
            min_price, max_price = map(int, price_range.split('-'))
            properties = properties.filter(price__gte=min_price*100000, price__lte=max_price*100000)
        
        if search:
            properties = properties.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
    
    # Get unique locations for filter dropdown
    locations = Property.objects.filter(is_active=True).values_list('location', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(properties, 9)  # 9 properties per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'properties': page_obj,
        'form': form,
        'locations': locations,
    }
    
    return render(request, 'properties/property_list.html', context)

def property_detail(request, pk, slug):
    property_obj = get_object_or_404(Property, pk=pk, slug=slug, is_active=True)
    
    # Track view
    ip_address = get_client_ip(request)
    PropertyView.objects.create(
        property=property_obj,
        user=request.user if request.user.is_authenticated else None,
        ip_address=ip_address
    )
    
    # Get similar properties
    similar_properties = Property.objects.filter(
        property_type=property_obj.property_type,
        location=property_obj.location,
        is_active=True
    ).exclude(pk=property_obj.pk)[:4]
    
    form = ScheduleVisitForm()
    
    context = {
        'property': property_obj,
        'similar_properties': similar_properties,
        'form': form,
    }
    
    return render(request, 'properties/property_detail.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_properties_api(request):
    """API endpoint for AJAX property filtering"""
    properties = Property.objects.filter(is_active=True)
    
    # Get filter parameters
    status = request.GET.get('status', 'all')
    property_type = request.GET.get('type', 'all')
    location = request.GET.get('location', 'all')
    bedrooms = request.GET.get('bedrooms', 'all')
    price_range = request.GET.get('price', 'all')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', 'newest')
    page = int(request.GET.get('page', 1))
    
    # Apply filters
    if status != 'all':
        properties = properties.filter(status=status)
    
    if property_type != 'all':
        properties = properties.filter(property_type__name=property_type)
    
    if location != 'all':
        properties = properties.filter(location__icontains=location)
    
    if bedrooms != 'all':
        if bedrooms == '4':
            properties = properties.filter(bedrooms__gte=4)
        else:
            properties = properties.filter(bedrooms=bedrooms)
    
    if price_range != 'all':
        min_price, max_price = map(int, price_range.split('-'))
        properties = properties.filter(price__gte=min_price*100000, price__lte=max_price*100000)
    
    if search:
        properties = properties.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    
    # Apply sorting
    if sort == 'price-low':
        properties = properties.order_by('price')
    elif sort == 'price-high':
        properties = properties.order_by('-price')
    elif sort == 'name':
        properties = properties.order_by('title')
    else:  # newest
        properties = properties.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(properties, 9)
    page_obj = paginator.get_page(page)
    
    # Prepare response data
    properties_data = []
    for prop in page_obj:
        primary_image = prop.images.filter(is_primary=True).first()
        properties_data.append({
            'id': prop.id,
            'title': prop.title,
            'location': prop.location,
            'price': prop.price_display,
            'bedrooms': prop.bedrooms,
            'type': prop.property_type.name,
            'status': prop.status,
            'featured': prop.featured,
            'image': primary_image.image.url if primary_image else '/static/images/default-property.jpg',
            'url': prop.get_absolute_url(),
        })
    
    return JsonResponse({
        'properties': properties_data,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_properties': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    })

@login_required
def schedule_visit(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id, is_active=True)
    
    if request.method == 'POST':
        form = ScheduleVisitForm(request.POST)
        if form.is_valid():
            # Here you would typically save to database and send email
            # For now, we'll just show a success message
            messages.success(
                request, 
                f"Thank you {form.cleaned_data['name']}! Your visit request for {property_obj.title} has been submitted. Our agent will contact you shortly."
            )
            return redirect('property_detail', pk=property_obj.pk, slug=property_obj.slug)
    
    return redirect('property_detail', pk=property_obj.pk, slug=property_obj.slug)

@login_required
def toggle_favorite(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id, is_active=True)
    favorite, created = FavoriteProperty.objects.get_or_create(
        user=request.user,
        property=property_obj
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    return JsonResponse({
        'is_favorite': is_favorite,
        'favorite_count': FavoriteProperty.objects.filter(property=property_obj).count()
    })

@login_required
def favorite_properties(request):
    favorites = FavoriteProperty.objects.filter(user=request.user).select_related('property')
    properties = [fav.property for fav in favorites]
    
    context = {
        'properties': properties,
        'title': 'Favorite Properties'
    }
    
    return render(request, 'properties/property_list.html', context)
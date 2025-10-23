from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Agent

def agents_list(request):
    agents = Agent.objects.filter(is_active=True)
    
    # Get filter from query parameters
    specialty_filter = request.GET.get('specialty', 'all')
    if specialty_filter != 'all':
        agents = [agent for agent in agents if specialty_filter in agent.specialties]
    
    context = {
        'agents': agents,
        'current_filter': specialty_filter,
    }
    return render(request, 'agents/agents_list.html', context)

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .models import Agent, ContactMessage

def contact_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id, is_active=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        property_type = request.POST.get('property_type')
        location = request.POST.get('location')
        budget = request.POST.get('budget')
        message_text = request.POST.get('message')
        newsletter = request.POST.get('newsletter') == 'on'

        # Save to database
        contact_message = ContactMessage.objects.create(
            agent=agent,
            name=name,
            email=email,
            phone=phone,
            property_type=property_type,
            location=location,
            budget=budget,
            message=message_text,
            newsletter=newsletter
        )

        # Send email notification
        subject = f"New Inquiry from {name} for {agent.name}"
        message_body = f"""
        You have received a new message from your contact form:

        Agent: {agent.name}
        Name: {name}
        Email: {email}
        Phone: {phone}
        Property Type: {property_type}
        Location: {location}
        Budget: {budget}

        Message:
        {message_text}
        """

        try:
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                [agent.email, settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
        except BadHeaderError:
            return JsonResponse({'success': False, 'message': 'Invalid email header found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return render(request, 'agents/contact_agent.html', {'agent': agent})

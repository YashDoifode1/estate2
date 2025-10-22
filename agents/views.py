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

def contact_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id, is_active=True)
    
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
    
    context = {
        'agent': agent,
    }
    return render(request, 'agents/contact_agent.html', context)
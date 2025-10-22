import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dreamhomes.settings')
django.setup()

from agents.models import Agent

def create_dummy_agents():
    agents_data = [
        {
            'name': 'Rajesh Sharma',
            'title': 'Senior Real Estate Consultant',
            'description': 'With over 12 years of experience in Nagpur real estate, Rajesh specializes in residential properties and has helped hundreds of families find their dream homes in areas like Civil Lines, Ramdaspeth, and Wardhaman Nagar.',
            'image_url': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop&crop=face',
            'phone': '+91 98765 43210',
            'email': 'rajesh.sharma@dreamhomes.com',
            'experience': 12,
            'properties_sold': 245,
            'specialties': ['residential', 'luxury'],
            'linkedin_url': 'https://linkedin.com/in/rajesh-sharma',
            'whatsapp_url': 'https://wa.me/919876543210'
        },
        {
            'name': 'Priya Patel',
            'title': 'Commercial Property Expert',
            'description': 'Priya has extensive knowledge of commercial real estate in Nagpur. She has successfully closed deals for office spaces in CBD, retail outlets in popular markets, and industrial properties in Hingna and Butibori.',
            'image_url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop&crop=face',
            'phone': '+91 98765 43211',
            'email': 'priya.patel@dreamhomes.com',
            'experience': 8,
            'properties_sold': 178,
            'specialties': ['commercial'],
            'linkedin_url': 'https://linkedin.com/in/priya-patel',
            'whatsapp_url': 'https://wa.me/919876543211'
        },
        {
            'name': 'Amit Verma',
            'title': 'Luxury Homes Specialist',
            'description': 'Amit focuses on luxury properties in premium locations of Nagpur like Civil Lines, Shankar Nagar, and Shraddhanand Peth. His clientele includes high-net-worth individuals seeking exclusive properties.',
            'image_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face',
            'phone': '+91 98765 43212',
            'email': 'amit.verma@dreamhomes.com',
            'experience': 15,
            'properties_sold': 89,
            'specialties': ['luxury', 'residential'],
            'linkedin_url': 'https://linkedin.com/in/amit-verma',
            'whatsapp_url': 'https://wa.me/919876543212'
        },
        {
            'name': 'Neha Singh',
            'title': 'Rental Properties Coordinator',
            'description': 'Neha specializes in rental properties across Nagpur and has helped numerous students and professionals find perfect accommodations in areas near institutions, IT parks, and commercial hubs.',
            'image_url': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face',
            'phone': '+91 98765 43213',
            'email': 'neha.singh@dreamhomes.com',
            'experience': 6,
            'properties_sold': 312,
            'specialties': ['rental'],
            'linkedin_url': 'https://linkedin.com/in/neha-singh',
            'whatsapp_url': 'https://wa.me/919876543213'
        },
        {
            'name': 'Vikram Joshi',
            'title': 'Real Estate Investment Advisor',
            'description': 'Vikram helps clients make smart real estate investment decisions in emerging areas of Nagpur. His expertise includes market analysis, property valuation, and investment strategies.',
            'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face',
            'phone': '+91 98765 43214',
            'email': 'vikram.joshi@dreamhomes.com',
            'experience': 10,
            'properties_sold': 156,
            'specialties': ['commercial', 'residential'],
            'linkedin_url': 'https://linkedin.com/in/vikram-joshi',
            'whatsapp_url': 'https://wa.me/919876543214'
        },
        {
            'name': 'Anjali Deshmukh',
            'title': 'Property Management Head',
            'description': 'Anjali oversees property management services for both residential and commercial properties across Nagpur. She ensures smooth operations and maintains excellent landlord-tenant relationships.',
            'image_url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop&crop=face',
            'phone': '+91 98765 43215',
            'email': 'anjali.deshmukh@dreamhomes.com',
            'experience': 9,
            'properties_sold': 201,
            'specialties': ['rental', 'residential'],
            'linkedin_url': 'https://linkedin.com/in/anjali-deshmukh',
            'whatsapp_url': 'https://wa.me/919876543215'
        }
    ]

    for agent_data in agents_data:
        agent, created = Agent.objects.get_or_create(
            email=agent_data['email'],
            defaults=agent_data
        )
        if created:
            print(f"✅ Created agent: {agent.name}")
        else:
            print(f"⚠️ Agent already exists: {agent.name}")

if __name__ == '__main__':
    create_dummy_agents()
    print("🎉 Dummy agents created successfully!")
from django.core.management.base import BaseCommand
from properties.models import PropertyType, Amenity, Property, PropertyImage
from accounts.models import CustomUser
from django.utils.text import slugify
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with sample property data'

    def handle(self, *args, **options):
        # Create property types
        property_types = [
            {'name': 'Apartment', 'icon_class': 'fas fa-building'},
            {'name': 'Villa', 'icon_class': 'fas fa-home'},
            {'name': 'House', 'icon_class': 'fas fa-house-user'},
            {'name': 'Commercial', 'icon_class': 'fas fa-store'},
            {'name': 'Land', 'icon_class': 'fas fa-map-marked-alt'},
        ]
        
        for pt_data in property_types:
            PropertyType.objects.get_or_create(**pt_data)
        
        # Create amenities
        amenities_data = [
            {'name': 'Swimming Pool', 'icon_class': 'fas fa-swimming-pool'},
            {'name': 'Gym', 'icon_class': 'fas fa-dumbbell'},
            {'name': 'Parking', 'icon_class': 'fas fa-parking'},
            {'name': 'Security', 'icon_class': 'fas fa-shield-alt'},
            {'name': 'Garden', 'icon_class': 'fas fa-tree'},
            {'name': 'Balcony', 'icon_class': 'fas fa-archway'},
            {'name': 'Air Conditioning', 'icon_class': 'fas fa-wind'},
            {'name': 'Heating', 'icon_class': 'fas fa-temperature-high'},
        ]
        
        amenities = []
        for amenity_data in amenities_data:
            amenity, _ = Amenity.objects.get_or_create(**amenity_data)
            amenities.append(amenity)
        
        # Get or create agent user
        agent, created = CustomUser.objects.get_or_create(
            email='agent@dreamhomes.com',
            defaults={
                'first_name': 'Raj',
                'last_name': 'Sharma',
                'phone': '+919876543210',
                'is_staff': True,
            }
        )
        if created:
            agent.set_password('password123')
            agent.save()
        
        # Sample property data
        sample_properties = [
            {
                'title': 'Luxury 3BHK Apartment in Civil Lines',
                'description': 'Beautiful luxury apartment with modern amenities in prime location.',
                'property_type': 'Apartment',
                'status': 'for_sale',
                'location': 'Civil Lines, Nagpur',
                'price': Decimal('7500000'),  # 75 Lakhs
                'bedrooms': 3,
                'bathrooms': 2,
                'total_area': Decimal('1200'),
                'year_built': 2020,
            },
            {
                'title': 'Spacious 2BHK Villa in Dharampeth',
                'description': 'Elegant villa with garden and private parking.',
                'property_type': 'Villa',
                'status': 'for_rent',
                'location': 'Dharampeth, Nagpur',
                'price': Decimal('25000'),  # Monthly rent
                'bedrooms': 2,
                'bathrooms': 2,
                'total_area': Decimal('1500'),
                'year_built': 2018,
            },
            # Add more sample properties...
        ]
        
        for prop_data in sample_properties:
            prop_type = PropertyType.objects.get(name=prop_data.pop('property_type'))
            property_obj, created = Property.objects.get_or_create(
                title=prop_data['title'],
                defaults={
                    **prop_data,
                    'property_type': prop_type,
                    'agent': agent,
                    'city': 'Nagpur',
                    'state': 'Maharashtra',
                    'pincode': '440001',
                    'furnishing': random.choice(['furnished', 'semi_furnished', 'unfurnished']),
                    'garage': random.randint(1, 2),
                }
            )
            
            if created:
                # Add random amenities
                property_obj.amenities.set(random.sample(amenities, random.randint(3, 6)))
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created property: {property_obj.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data!')
        )
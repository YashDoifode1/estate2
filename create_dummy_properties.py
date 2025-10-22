import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dreamhomes.settings')
django.setup()

from properties.models import Property, Amenity, PropertyAmenity, PropertyImage
from agents.models import Agent

def create_dummy_properties():
    # Get some agents
    agents = Agent.objects.all()[:3]
    
    if not agents:
        print("❌ No agents found. Please create agents first by running create_dummy_agents.py")
        return
    
    print(f"✅ Found {len(agents)} agents to assign properties to")
    
    properties_data = [
        {
            'title': 'Luxury 3 BHK Apartment in Civil Lines',
            'description': 'Beautiful luxury apartment in prime location with modern amenities and stunning views. Located in the heart of Civil Lines, this property offers premium living experience with 24/7 security, power backup, and modern fixtures.',
            'status': 'for_sale',
            'type': 'apartment',
            'price': 8500000,
            'location': 'Civil Lines, Nagpur',
            'city': 'Nagpur',
            'state': 'Maharashtra',
            'pincode': '440001',
            'total_area': 1850,
            'built_up_area': 1650,
            'bedrooms': 3,
            'bathrooms': 3,
            'balconies': 2,
            'garage': 2,
            'floors': 12,
            'floor_number': 8,
            'year_built': 2020,
            'furnishing': 'semi_furnished',
            'featured': True,
            'agent': agents[0],
        },
        {
            'title': 'Modern Villa in Ramdaspeth',
            'description': 'Spacious modern villa with garden and private swimming pool. Perfect for families looking for luxury living with privacy and all modern amenities.',
            'status': 'for_sale',
            'type': 'villa',
            'price': 12500000,
            'location': 'Ramdaspeth, Nagpur',
            'city': 'Nagpur',
            'state': 'Maharashtra',
            'pincode': '440010',
            'total_area': 3200,
            'built_up_area': 2800,
            'bedrooms': 4,
            'bathrooms': 4,
            'balconies': 3,
            'garage': 3,
            'floors': 2,
            'floor_number': 1,
            'year_built': 2018,
            'furnishing': 'furnished',
            'featured': True,
            'agent': agents[1],
        },
        {
            'title': '2 BHK Apartment for Rent in Dharampeth',
            'description': 'Well-maintained 2 BHK apartment available for rent in peaceful Dharampeth area. Close to schools, hospitals, and shopping centers.',
            'status': 'for_rent',
            'type': 'apartment',
            'price': 18000,
            'location': 'Dharampeth, Nagpur',
            'city': 'Nagpur',
            'state': 'Maharashtra',
            'pincode': '440012',
            'total_area': 1100,
            'built_up_area': 950,
            'bedrooms': 2,
            'bathrooms': 2,
            'balconies': 1,
            'garage': 1,
            'floors': 6,
            'floor_number': 3,
            'year_built': 2015,
            'furnishing': 'semi_furnished',
            'featured': False,
            'agent': agents[2],
        },
        {
            'title': 'Commercial Space in Sitabuldi',
            'description': 'Prime commercial space ideal for retail business or office. High footfall area with excellent visibility.',
            'status': 'for_sale',
            'type': 'commercial',
            'price': 5200000,
            'location': 'Sitabuldi, Nagpur',
            'city': 'Nagpur',
            'state': 'Maharashtra',
            'pincode': '440012',
            'total_area': 800,
            'built_up_area': 750,
            'bedrooms': 0,
            'bathrooms': 1,
            'balconies': 0,
            'garage': 0,
            'floors': 1,
            'floor_number': 0,
            'year_built': 2010,
            'furnishing': 'unfurnished',
            'featured': True,
            'agent': agents[0],
        },
        {
            'title': 'Independent House in Wardhaman Nagar',
            'description': 'Beautiful independent house with garden and car parking. Quiet neighborhood with all basic amenities nearby.',
            'status': 'for_sale',
            'type': 'house',
            'price': 6800000,
            'location': 'Wardhaman Nagar, Nagpur',
            'city': 'Nagpur',
            'state': 'Maharashtra',
            'pincode': '440008',
            'total_area': 1800,
            'built_up_area': 1600,
            'bedrooms': 3,
            'bathrooms': 2,
            'balconies': 2,
            'garage': 1,
            'floors': 2,
            'floor_number': 1,
            'year_built': 2012,
            'furnishing': 'unfurnished',
            'featured': False,
            'agent': agents[1],
        },
        {
            'title': '1 BHK Apartment in Manish Nagar',
            'description': 'Compact and cozy 1 BHK apartment perfect for singles or couples. Well-connected location with public transport.',
            'status': 'for_rent',
            'type': 'apartment',
            'price': 12000,
            'location': 'Manish Nagar, Nagpur',
            'city': 'Nagpur',
            'state': 'Maharashtra',
            'pincode': '440015',
            'total_area': 650,
            'built_up_area': 580,
            'bedrooms': 1,
            'bathrooms': 1,
            'balconies': 1,
            'garage': 0,
            'floors': 8,
            'floor_number': 5,
            'year_built': 2018,
            'furnishing': 'furnished',
            'featured': False,
            'agent': agents[2],
        },
        {
            'title': 'Luxury Penthouse in Civil Lines',
            'description': 'Exclusive penthouse with panoramic city views. Premium finishes and luxury amenities included.',
            'status': 'for_sale',
            'type': 'apartment',
            'price': 15000000,
            'location': 'Civil Lines, Nagpur',
            'city': 'Nagpur',
            'state': 'Maharashtra',
            'pincode': '440001',
            'total_area': 2800,
            'built_up_area': 2500,
            'bedrooms': 4,
            'bathrooms': 4,
            'balconies': 3,
            'garage': 2,
            'floors': 15,
            'floor_number': 15,
            'year_built': 2022,
            'furnishing': 'furnished',
            'featured': True,
            'agent': agents[0],
        },
        {
            'title': 'Plot/Land in Koradi Road',
            'description': 'Prime residential plot in developing area. Ideal for building your dream home with good appreciation potential.',
            'status': 'for_sale',
            'type': 'land',
            'price': 3500000,
            'location': 'Koradi Road, Nagpur',
            'city': 'Nagpur',
            'state': 'Maharashtra',
            'pincode': '440023',
            'total_area': 2400,
            'built_up_area': 0,
            'bedrooms': 0,
            'bathrooms': 0,
            'balconies': 0,
            'garage': 0,
            'floors': 0,
            'floor_number': 0,
            'year_built': 0,
            'furnishing': 'unfurnished',
            'featured': False,
            'agent': agents[1],
        }
    ]
    
    created_count = 0
    existing_count = 0
    
    for prop_data in properties_data:
        try:
            property_obj, created = Property.objects.get_or_create(
                title=prop_data['title'],
                defaults=prop_data
            )
            if created:
                print(f"✅ Created property: {property_obj.title} (₹{property_obj.price:,.0f})")
                created_count += 1
            else:
                print(f"⚠️ Property already exists: {property_obj.title}")
                existing_count += 1
        except Exception as e:
            print(f"❌ Error creating property '{prop_data['title']}': {str(e)}")
    
    print(f"\n🎉 Properties creation completed!")
    print(f"📊 Created: {created_count}, Already existed: {existing_count}")
    print(f"🏠 Total properties in database: {Property.objects.count()}")

def create_amenities():
    """Create common amenities"""
    amenities_data = [
        # General Amenities
        {'name': 'Swimming Pool', 'icon_class': 'fas fa-swimming-pool', 'category': 'general'},
        {'name': 'Gym', 'icon_class': 'fas fa-dumbbell', 'category': 'general'},
        {'name': 'Park', 'icon_class': 'fas fa-tree', 'category': 'general'},
        {'name': 'Security', 'icon_class': 'fas fa-shield-alt', 'category': 'general'},
        {'name': 'Power Backup', 'icon_class': 'fas fa-bolt', 'category': 'general'},
        {'name': 'Lift', 'icon_class': 'fas fa-elevator', 'category': 'general'},
        
        # Home Amenities
        {'name': 'Air Conditioning', 'icon_class': 'fas fa-wind', 'category': 'home'},
        {'name': 'Heating', 'icon_class': 'fas fa-temperature-high', 'category': 'home'},
        {'name': 'Balcony', 'icon_class': 'fas fa-door-open', 'category': 'home'},
        {'name': 'Fireplace', 'icon_class': 'fas fa-fire', 'category': 'home'},
        {'name': 'WiFi', 'icon_class': 'fas fa-wifi', 'category': 'home'},
        
        # Kitchen Amenities
        {'name': 'Modular Kitchen', 'icon_class': 'fas fa-utensils', 'category': 'kitchen'},
        {'name': 'Refrigerator', 'icon_class': 'fas fa-refrigerator', 'category': 'kitchen'},
        {'name': 'Microwave', 'icon_class': 'fas fa-microchip', 'category': 'kitchen'},
        {'name': 'Dishwasher', 'icon_class': 'fas fa-soap', 'category': 'kitchen'},
        
        # Outdoor Amenities
        {'name': 'Garden', 'icon_class': 'fas fa-seedling', 'category': 'outdoor'},
        {'name': 'Parking', 'icon_class': 'fas fa-car', 'category': 'outdoor'},
        {'name': 'Garage', 'icon_class': 'fas fa-warehouse', 'category': 'outdoor'},
    ]
    
    for amenity_data in amenities_data:
        amenity, created = Amenity.objects.get_or_create(
            name=amenity_data['name'],
            defaults=amenity_data
        )
        if created:
            print(f"✅ Created amenity: {amenity.name}")
        else:
            print(f"⚠️ Amenity already exists: {amenity.name}")

if __name__ == '__main__':
    print("🏗️ Starting properties and amenities creation...")
    create_dummy_properties()
    print("\n🔧 Creating amenities...")
    create_amenities()
    print("\n🎉 All dummy data created successfully!")
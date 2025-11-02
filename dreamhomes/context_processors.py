from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

def current_year(request):
    """Add current year to template context"""
    from datetime import datetime
    return {'current_year': datetime.now().year}

def site_info(request):
    """Add SEO-related site information to context"""
    return {
        'site_name': getattr(settings, 'SITE_NAME', 'DreamHomes Realty'),
        'site_description': getattr(settings, 'SITE_DESCRIPTION', 'Find your dream home with DreamHomes Realty'),
        'site_keywords': getattr(settings, 'SITE_KEYWORDS', 'real estate, properties, homes'),
        'domain': get_current_site(request).domain,
    }

def google_analytics(request):
    """Add Google Analytics ID to context"""
    return {
        'google_analytics_id': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
    }

def scheme_and_domain(request):
    """Add scheme and domain for absolute URLs"""
    return {
        'scheme': request.scheme,
        'domain': get_current_site(request).domain,
    }



def company_info(request):
    from django.conf import settings
    return {
        "company": settings.COMPANY_INFO,
        "office_location": settings.COMPANY_INFO.get("OFFICE_LOCATION", {}),
        "team_members": settings.COMPANY_INFO.get("TEAM_MEMBERS", []),
    }


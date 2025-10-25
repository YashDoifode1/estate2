# utils.py
import requests

def get_ip_info(ip_address):
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        if response.status_code == 200:
            data = response.json()
            return {
                'country': data.get('country_name'),
                'region': data.get('region'),
                'city': data.get('city'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'isp': data.get('org'),
            }
    except Exception:
        pass
    return {}

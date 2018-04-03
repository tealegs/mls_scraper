#googmaps api test
#3/12/2018
#testing geocoding to try and implement in listing scraper visualtization

import requests

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
def get_latlong(address):
    params = {
        'address': address,
        'sensor': 'false',
        'region': 'us'
        

        
    }

    #Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    #print res
    #Use the first result
    result = res['results'][0]

    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']
    #geodata['address'] = result['formatted_address']

    print('(lat, lng) = ({lat}, {lng})'.format(**geodata))
    return (geodata['lat'], geodata['lng'])
#latlong = get_latlong("466 Ontario Street, Albany, New York")
#print latlong
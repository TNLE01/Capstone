"""This file has the function for finding out the plant species."""

import requests
import json

API_KEY = '2b10wpZYSOcNBIAlvDEa6wt'
PROJECT = 'all'
api_endpoint = f'https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}'

def plantSearch(file):
    """
    This function takes a image file and find the plant species using that file.
    
    Parameters:
    file (str): The image file.

    Returns:
    str: The name of the plant.
    str: Error message if the request fails.
    """

    data = { 'organs': ['flower'] }
    files = [
        ('images', (file, open(file, 'rb'))),
    ]
    req = requests.Request('POST', url = api_endpoint, files = files, data = data)
    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)

    if (response.status_code == 200):
        return(json_result.get('results')[0].get('species').get('scientificNameWithoutAuthor'))
    else:
        print(response.status_code)
        return ('Unknown Plant')


"""This file has the function for looking up the plant ID and details."""

import requests
import json

API_KEY = '' # Add your API key here
baseUrl = f'https://perenual.com/api/v2/'

def plantLookUp(name):
    """
    This function takes a name and looks up the ID the plant has.
    
    Parameters:
    name (str): The plant name.

    Returns:
    function call: A call to another function that returns the plant details.
    str: Error message if the request fails.
    """

    url = baseUrl + f'species-list?key={API_KEY}&q=' + name
    response = requests.get(url = url)

    if response.status_code == 200:
        data = response.json()
        try:
            return(plantDetails(data.get('data')[0].get('id')))
        except:
            return(0)
    else:
        print(f"Error: {response.status_code}")
        return(response.text)

def plantDetails(id):
    """
    This function takes the plant ID and looks up the details of the plant.
    
    Parameters:
    id (int): The plant ID.

    Returns:
    dict: The dictionary with the plant details.
    str: Error message if the request fails.
    """

    url = baseUrl + f'species/details/{id}?key={API_KEY}'
    response = requests.get(url = url)

    if response.status_code == 200:
        data = response.json()
        return(data)
    else:
        print(f"Error: {response.status_code}")
        return(response.text)
import requests

def get_poke_info(pokemon):
    """ Gets all information about a specified Pokemonretrieved from the PokeAPI

    :param name: Pokemon name
    :returns: Dictionary of Pokemon info, if successful. None, if not. 
    """

    resp_msg = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon)

    if resp_msg.status_code == 200:
        return resp_msg.json()   
    else:
        return



def get_poke_list(limit=100, offset=0):
    url= 'https://pokeapi.co/api/v2/pokemon'

    params= {
        'limit': limit,
        'offset': offset
        }

    resp_msg = requests.get(url, params=params)

    if resp_msg.status_code == 200:
        dict = resp_msg.json()
        return [p['name'] for p in dict['results']]
    else:
        print('Failed to get Pokemon list.')
        print('Response code:', resp_msg.status_code)
        print(resp_msg.text)


def get_pokemon_image_url(name):
    poke_dict = get_poke_info(name)
    if poke_dict:
        return poke_dict['sprites']['other']['official-artwork']['front_default']
    
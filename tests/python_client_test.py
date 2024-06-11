# coding: utf-8

# Simple Python script that demonstrates how to use the API key stored in a file named umls.key
# in the application directory to execute an endpoint.

import requests
import os

# Read the API key.
fpath = os.path.dirname(os.getcwd())
fpath = os.path.join(fpath, 'tests', 'umls.key')
f = open(fpath, 'r')
apikey = f.read()
f.close()

# Add the API key to authorization for the URL.
headers = {'Authorization': f'UMLS-Key {apikey}'}

# Execute the endpoint.

# Compile demonstration scenarios into a list of tuples.

scenarios = []
scenario1='Misspelled base url (distilleryz instead of distillery), which will result in a ConnectionError.'
url1 = 'https://datadistilleryz.api.sennetconsortium.org/concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel=isa'
scenarios.append((scenario1,url1))

scenario2 = 'Nonexistent endpoint part of url (conceptsz instead of concepts), which will result in a 403 (Forbidden) from the gateway.'
url2 = 'https://datadistillery.api.sennetconsortium.org/conceptsz/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel=isa'
scenarios.append((scenario2,url2))

scenario3 = 'Error in query parameter name (sabz instead of sab), which will result in a 400 error.'
url3 = 'https://datadistillery.api.sennetconsortium.org/concepts/C2720507/paths/shortestpath/C1272753?sabz=SNOMEDCT_US&rel=isa'
scenarios.append((scenario3,url3))

scenario4 = 'Long query that should exceed the API timeout.'
url4='https://datadistillery.api.sennetconsortium.org/concepts/C2720507/paths/expand?sab=SNOMEDCT_US&rel=isa&mindepth=9&maxdepth=10&skip=1&limit=10'
scenarios.append((scenario4,url4))

scenario5 = 'Valid request'
url5 = 'https://datadistillery.api.sennetconsortium.org/concepts/C2720507/paths/shortestpath/C1272753?sab=SNOMEDCT_US&rel=isa'
scenarios.append((scenario5,url5))

for scenario in scenarios:
    print('')
    print('----------------')
    print(f'SCENARIO {scenarios.index(scenario)+1}: {scenario[0]}')
    url = scenario[1]
    try:
        response = requests.get(url,headers=headers)

        if response.status_code == 403:
            # The API gateway does not recognize the endpoint path--i.e., this is the gateway's translation of a 404.
            print(f'HTTP 403 error (forbidden). This endpoint does not exist: {response.request.path_url.split("?")[0]}')
            print('Check spelling of endpoint path string.')
            pass
        elif response.status_code == 404:
            # This could be the result of a timeboxed query that exceeded the DD-API's timeout.
            print(f'HTTP 404 error (not found) for URl: {url}')
            print('Note that the Data Distillery API returns 404 for queries that exceed the specified timeout.')
            pass
        elif response.status_code != 200:
            response.raise_for_status()
        else:
            print()
            print(f'RESPONSE for url: {url}')
            respjson = response.json()
            print(respjson)

    except requests.ConnectionError:
        # Unable to connect. This is likely because of an error in the base url.
        print(f'Unable to connect with url: {url}')
        print(f'Check spelling of base url {url[0:url.find(".org/")+4] }')
        pass
    except requests.HTTPError as err:
        print(err)
        pass
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        pass



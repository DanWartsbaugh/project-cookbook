# import requests
# from pprint import pprint
# query = 'cookies'
# api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(query)
# response = requests.get(api_url, headers={'X-Api-Key': 'Ix9mZtTU2HXk4JPwpqm+qg==wFif3nWrE0wvdwXg'})
# if response.status_code == requests.codes.ok:
#     pprint(response.json()[0]['ingredients'].split('|'))
# else:
#     print("Error:", response.status_code, response.text)
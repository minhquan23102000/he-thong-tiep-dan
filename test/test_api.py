import requests


make_request = requests.get('http://localhost:5000/get-reponse', data = {'message': 'Khai sinh'}).json()

print(make_request)
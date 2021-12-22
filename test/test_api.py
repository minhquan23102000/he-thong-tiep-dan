import requests

make_request = requests.get('https://hethongtiepdan.herokuapp.com/get-reponse',
                            data={
                                'message': 'Khai sinh'
                            }).json()

print(make_request)

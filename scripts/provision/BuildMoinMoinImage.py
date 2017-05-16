#!/usr/bin/python


import requests, json, docker
response = requests.post('https://hub.docker.com/v2/users/login/', data = {'username':'mazerunner', 'password':'UnJ3XwYt'})
#print (response)
#print (response.text)
responseObject = json.loads(response.text)
token = responseObject['token']

headers = {'Authorization': 'JWT '+token, 'Host' : 'hub.docker.com'}
response2 = requests.get('https://hub.docker.com/v2/repositories/mazerunner/?page_size=10000', headers=headers)
#print ( response2)
print (response2.text)

responseObject2 = json.loads(response2.text)
print (responseObject2)
print (responseObject2['results'])
moinmoinrepos = [ repo for repo in responseObject2['results'] if repo['name'] == 'moinmoin-wiki']
print (len(moinmoinrepos))

response3 = requests.get('https://hub.docker.com/v2/repositories/mazerunner/moinmoin-wiki/tags?page_size=10000', headers=headers)
print (response3)
print (response3.text)


response4 = requests.get('https://hub.docker.com/v2/_catalog?n=10000', headers=headers)
print (response4)

print (response4.text)

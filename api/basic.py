import requests

endpoint = "http://127.0.0.1:8000/api/meal/"
data ={'name':'nlokjf','description':'hfhhhd'}

response = requests.post(endpoint, json=data)

print(response.json())  # Vérifiez le code d'état de la réponse
if response.status_code == 200:
    print(response.json())  # Affichez la réponse JSON renvoyée par votre API







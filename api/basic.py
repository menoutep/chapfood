import requests

endpoint = "http://127.0.0.1:8000/api/registration/"
data ={'username':'mikou','email':'mikou@gmail.com','password1':'Leocadie0','password2':'Leocadie0','phone_number':'0908989090'}

response = requests.post(endpoint, json=data)

print(response.json())  # Vérifiez le code d'état de la réponse
if response.status_code == 200:
    print(response.json())  # Affichez la réponse JSON renvoyée par votre API
else:
    print("errerur")






import requests


ride = {
    'fico_score': 0,
    'lead_sold': 0,
    'dayofweek_created_at': 5,
    'successful_quote_count': 4,
    'age': 45,
    'prediction': 0.7
}
response = requests.post("http://192.168.49.2:30008/iterate/leads",  json=[ride])
print(response)

try:
    print(response.json())
except Exception as e: 
    print(e)

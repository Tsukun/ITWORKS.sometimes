import requests
url = "https://httpbin.org/"
response = requests.get("https://httpbin.org/get")
if(response.status_code == 200):
    print(response.text)
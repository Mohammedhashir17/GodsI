import requests

def getlocation():
    try:
        ip_request = requests.get("https://ipinfo.io/json")
        ip_request.raise_for_status()
        data = ip_request.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching location:", e)
        return None

print(getlocation())

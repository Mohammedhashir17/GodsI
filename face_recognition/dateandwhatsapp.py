import requests
from getlocationinfo2 import get_gps_location  # Import GPS function

def sendmessage(number, name, adhaar, location):
    try:
        # Fetch GPS location
        gps_location = get_gps_location()
        
        if "error" in gps_location:
            print("Error:", gps_location["error"])
            return
        
        latitude = gps_location["latitude"]
        longitude = gps_location["longitude"]

        # Generate Google Maps link
        maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

        # Format WhatsApp message
        message = (f"Your dear one, {name}, bearing Aadhaar number {adhaar}, has been found at:\n"
                   f"📌 Latitude: {latitude}\n"
                   f"📌 Longitude: {longitude}\n"
                   f"📍 Google Maps: {maps_link}\n"
                   "Regards, FindOne.")

        # WhatsApp API details (Ensure instance ID & token are correct)
        url = "https://api.ultramsg.com/instance110230/messages/chat"
        token = "oitwz9rsv4d0z292"  # Your UltraMSG API token

        payload = {
            "token": token,
            "to": f"+91{number}",  # Ensure correct phone number format
            "body": message,
            "priority": "1",
            "referenceId": ""
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # Send WhatsApp message
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Raise error if API call fails

        print("✅ WhatsApp Message Sent Successfully:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error Sending WhatsApp Message: {e}")

# Example usage:
if __name__ == "__main__":
    sendmessage("9876543210", "Shivam", "123456789012")

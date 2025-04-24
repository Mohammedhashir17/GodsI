import geocoder

def get_gps_location():
    try:
        g = geocoder.ip("me")  # Fetch real-time GPS location
        if g.latlng:
            return {"latitude": g.latlng[0], "longitude": g.latlng[1]}
        else:
            return {"error": "GPS location unavailable"}
    except Exception as e:
        return {"error": str(e)}

# Debugging/Test Run
if __name__ == "__main__":
    print(get_gps_location())  # Run this file to test GPS output

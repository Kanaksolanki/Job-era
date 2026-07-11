import requests

print("Sending request... (may take up to 2 minutes)")

try:
    response = requests.post(
        "https://jobera-0f9j.onrender.com/api/skill-gap",
        json={
            "role": "Data Scientist",
            "skills": ["machine_learning", "data_science", "python"]
        },
        timeout=120  
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)

except requests.exceptions.Timeout:
    print("TIMEOUT - Server took too long. Try again.")
except requests.exceptions.ConnectionError:
    print("CONNECTION ERROR - Server is down.")

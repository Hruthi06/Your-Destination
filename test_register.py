import requests

def test_register():
    url = "http://127.0.0.1:8000/api/auth/register"
    data = {
        "name": "Test User",
        "email": "test_new@example.com",
        "password": "password123"
    }
    res = requests.post(url, json=data)
    print(f"Status: {res.status_code}")
    print(f"Body: {res.text}")

if __name__ == "__main__":
    test_register()

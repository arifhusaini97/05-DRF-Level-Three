import requests


def client():
    token_h ="Token 8da9d190a31b77674426c7967836327ac1b91005"
    credentials = {"username": "admin", "password": "adminpassword"}

    # response = requests.post(
    #     "http://127.0.0.1:8000/api/rest-auth/login/",
    #     data=credentials
    # )
    headers = {"Authorization": token_h}
    response = requests.get("http://127.0.0.1:8000/api/profiles/", headers=headers)

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)

if __name__ == "__main__":
    client()

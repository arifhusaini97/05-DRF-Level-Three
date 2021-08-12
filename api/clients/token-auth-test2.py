import requests


def client():
    
    data = {
        "username": "admin2",
        "email": "admin2@gmail.com",
        "password1": "admin2password",
        "password2": "admin2password"
    }

    response = requests.post(
        "http://127.0.0.1:8000/api/rest-auth/registration/",
        data=data
    )


    # credentials = {
    #     "username": "admin",
    #     "password": "adminpassword"
    # }
    # response = requests.post(
    #     "http://127.0.0.1:8000/api/rest-auth/login/",
    #     data=credentials
    # )
    
    # token_h = "Token 8da9d190a31b77674426c7967836327ac1b91005"
    # headers = {"Authorization": token_h}
    # response = requests.get("http://127.0.0.1:8000/api/profiles/", headers=headers)

    print("Status Code: ", response.status_code)
    response_data = response.json()
    print(response_data)


if __name__ == "__main__":
    client()

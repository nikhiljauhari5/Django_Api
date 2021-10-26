import requests
import os
import json

#token url testing
# AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/"
# REFRESH_ENDPOINT = AUTH_ENDPOINT + "refresh/"
# ENDPOIN = "http://127.0.0.1:8000/api/status/mixinsAPIView/"

# header = {
#     "Content-Type": "application/json"
#     }
#
# data = {
#     "username":"admin",
#     "password":"admin"
# }
#
# r = requests.post(AUTH_ENDPOINT,data=data,headers=header)
# token = r.json()['token']
# print(token)

# refresh_data = {
#     "token": token
# }
# new_response =requests.post(REFRESH_ENDPOINT,data=json.dumps(refresh_data),headers=header)
# new_token = new_response.json()['token']
# print(new_token)


# # this is use for token refreshing
# header1 = {
#     "Content-Type": "application/json",
#     "Authorization" : "JWT " + token
# }
#
# #post data with using token
# post_Data = json.dumps({"content":"some random data or stuff"})
# posted_response = requests.post(ENDPOIN,data=post_Data,headers=header1)
# print(posted_response.text)

# get_endpoint = ENDPOIN + str(10)

# to check RegisterView

#token url testing
# AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/register/"
AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/register2/"
REFRESH_ENDPOINT = AUTH_ENDPOINT + "refresh/"
ENDPOIN = "http://127.0.0.1:8000/api/status/mixinsAPIView/"



header = {
    "Content-Type": "application/json",
    # "Authorization":"JWT " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNiwidXNlcm5hbWUiOiJrYW1sZXNoMSIsImV4cCI6MTU5NDc1MTM4MywiZW1haWwiOiJrYW1sZXNoMUBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTU5NDc1MTA4M30.GyUBJ6s1TlRYzFCWK9kceskbIN4RBw2rw_PvR6E4arE"
}

data = {
    "username":"kamlesh10",
    "email":"kamlesh10@gmail.com",
    "password":"admin",
    "password2":"admin"
}

r = requests.post(AUTH_ENDPOINT,data=data)
token = r.json()#['token']
print(token)

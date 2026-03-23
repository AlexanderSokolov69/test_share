import datetime

from requests import post, get, delete

srv = "http://localhost:8080/api/v2/"

print(get(f"{srv}users").json())
print(get(f"{srv}users/1").json())
print(get(f"{srv}users/300").json())

user = {
    'name': "User3",
    'surname': "fam3",
    'age': 25,
    'position': "manager",
    'speciality': "manager",
    'address': "address",
    'email': "email3@email.com",
    'password': "password",
    'modified_date': datetime.date.today().isoformat()
}

uset_id = post(f"{srv}users", json=user).json()
print(uset_id)

print(delete(f"{srv}users/{uset_id['id']}").json())


from requests import get

print(get('http://localhost:8080/api/jobs').json())

print(get('http://localhost:8080/api/jobs/2').json())

print(get('http://localhost:8080/api/jobs/55').json())

print(get('http://localhost:8080/api/jobs/55q').json())
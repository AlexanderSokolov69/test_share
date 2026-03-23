import datetime

from requests import post, get

job = {
"team_leader": 1,
    "job": "test job",
    "work_size": 1,
    "collaborators": "1, 2, 3",
    "start_date": datetime.date.today().isoformat(),
    "end_date": "",
    "is_finished": False
}

print(post("http://localhost:8080/api/jobs", json=job).json())

job = {
    "job": "test job",
    "work_size": 1,
    "collaborators": "1, 2, 3",
    "start_date": datetime.date.today().isoformat(),
    "end_date": "",
    "is_finished": False
}

print(post("http://localhost:8080/api/jobs", json=job).json())

job = {
    "team_leader": 1,
    "job": "test job",
    "work_size": 1,
    "collaborators": "1, 2, 3",
    "start_date": "123",
    "end_date": "",
    "is_finished": False
}

print(post("http://localhost:8080/api/jobs", json=job).json())




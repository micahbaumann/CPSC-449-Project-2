enroll: uvicorn --port $PORT enroll.api:app --reload
users: uvicorn --port $PORT users.auth:app --reload
krakend: echo krakend.json | entr -nrz krakend run --port $PORT --config krakend.json

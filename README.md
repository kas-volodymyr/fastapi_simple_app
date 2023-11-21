# Project General Info
Greetings!
This is a simple test project that includes CRUD operations for users and a journal.
Users belong to one of three roles: admin, developer, or a simple mortal.
The journal is a text file where users can write messages.
The authentication process is implemented using JWT.

# Cloning the project
```
git clone git@github.com:volodymyr-kasaraba/fastapi_user_app.git
```

# Preparation
Paste `.env` file that you got from a dev to project root.

# Running
## In Docker
For buidling and running all conteiners use:
```
make up
```

## Local
### Create and activate virtual environment and install all requirements
```
python -m venv .venv/
source .venv/bin/activate
pip install -r requirements.txt
```
### Start the project
```
uvicorn src.main:app --reload
```

### Ports:
- mongodb: `27017`
- user_app: `8000`

# SEEDERS
## Default users with different roles:
**Running seeders**:
### In Docker container (in another terminal)
```
docker exec -it user_app python seeders/users_seeders.py
```

### Locally
```
python seeders/users_seeders.py
```
**Default users login info**:
- admin@corporation.com: My_pass1
- developer@corporation.com: My_pass1
- simple@corporation.com: My_pass1

# Base URLs
### Docker: ```http://0.0.0.0:8000```
### Local: ```http://127.0.0.1:8000```

# Docs
### Swagger: `<base_url>/docs`
### Redoc: `<base_url>/redoc`

# API Overview using Swagger
## Health Check
- GET `<base_url>/health_check`: check that the API is running
![alt text](https://drive.google.com/uc?export=view&id=1gBQyNxRJ84ufhGjYlax9sMzuXnwv3kKN)

## Auth
### Auth is implemented using JSON Web Token
- POST `<base_url>/token/pair`: Create access and refresh tokens for a user
- POST `<base_url>/token/refresh`: Refresh an access token using refresh token

### Auth in Swagger
You can pass auth process in Swagger by clicking on 'lock' icon and pasting
JWT_ACCESS_SECRET_KEY and user's email and password.
![alt text](https://drive.google.com/uc?export=view&id=1fmygPtzMROAzIQr7SHyVqnKrTB7gMDWS)
![alt text](https://drive.google.com/uc?export=view&id=1KnZDVCKODRE8I8XcHg0lLTSJkXf5Lieg)

### All other endpoints require Authorization header: "Bearer <access token>"
#### Users App
- GET `<base_url>/users`: List all users
![alt text](https://drive.google.com/uc?export=view&id=19SpOTqS9N3zrEz41yBEY5KmqjVT2NOrH)
- GET `<base_url>/users/<id>`: Get a user by id
![alt text](https://drive.google.com/uc?export=view&id=10bPxhBnUQRHdc61AbMirKLe8ox1qN_rS)
- POST `<base_url>/users`: Create a user (Only available for a user with admin role)
![alt text](https://drive.google.com/uc?export=view&id=11kkSDWxGu8M-yKZwzw9gDR8ttjtXMivz)
![alt text](https://drive.google.com/uc?export=view&id=1AdkzZPT4RWKGYKiQxShkT2r8WiT6tvd5)
- PATCH `<base_url>/users/<id>`: Partially update a user by id (Only available for a user with admin role. Cannot update hashed_password)
![alt text](https://drive.google.com/uc?export=view&id=1qINOFj4GqqSzC3QQkD_6ow9-J3BsixoW)
![alt text](https://drive.google.com/uc?export=view&id=1_PA-QTiSYmZ0A-_Dw0POtYwNleENODU4)
- PUT `<base_url>/users/<id>`: Update a user by id (Only available for a user with admin role. Cannot update hashed_password)
![alt text](https://drive.google.com/uc?export=view&id=19ggOqW8q-zbrch1hPIv0u_p8c5yHxLOR)
![alt text](https://drive.google.com/uc?export=view&id=1b88vBv9p1Yk8JkAI8nhwyMKkL_mwsYV3)
- DELETE `<base_url>/users/<id>`: Delete a user by id (Only available for a user with admin role)
![alt text](https://drive.google.com/uc?export=view&id=1C0A3cpsx64y-hvQTMWmELUFckec6DlLx)

#### Journal Management App
- POST `<base_url>/journal/write`: Write a message to the journal
![alt text](https://drive.google.com/uc?export=view&id=1JAHycTGsUG9oFa5_hgd5h0TYPlzdFpap)
- GET `<base_url>/journal/read`: Read all messages from the journal
![alt text](https://drive.google.com/uc?export=view&id=15kdQXtZETZ1MWysxukbUsP0c1SnwELC_)

# Project structure
```
├── Dockerfile
├── Makefile
├── README.md
├── docker-compose.yml
├── requirements.txt
├── seeders
│   └── users_seeders.py
└── src
    ├── __init__.py
    ├── auth
    │   ├── __init__.py
    │   ├── background_tasks.py
    │   ├── dependencies.py
    │   ├── middlewares.py
    │   ├── routers
    │   │   ├── __init__.py
    │   │   ├── jwt_router.py
    │   │   └── users_router.py
    │   ├── schemas.py
    │   └── utils.py
    ├── config.py
    ├── core
    │   ├── databases
    │   │   └── mongo_db.py
    │   └── exceptions.py
    ├── journal_management
    │   ├── journal.txt
    │   ├── journal_router.py
    │   └── schemas.py
    └── main.py
```
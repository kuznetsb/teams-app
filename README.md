# Teams API

**DRF** project where implemented basic api logic for creating users, teams 
and possibility to add or remove users to/from teams 
<br/>
`PosgtreSQL` used as DB and `Docker` with docker-compose for DB and API

## Prerequisites
> 👉 You should have Docker installed on your local machine [link](https://www.docker.com)

## Installing instructions
> 👉 Clone this repository  

```bash
$ git clone git@github.com:kuznetsb/teams-app.git
```
<br />

> 👉 Configure environmental variables
```bash
$ create .env file in project directory
$ Use default.env as template and copy all those DB variables to .env
$ fill DB variables with your values in .env file (exmaple: POSTGRES_DB=teams_app)
```
Now your Postgres database will be configured properly

<br />

> 👉 Run docker-compose in detached mode

```bash
$ docker-compose up -d
```
That will run application with all installed dependencies, database and so on.
Now you can use API!
<br />
<br />

## Usage instructions

> 👉 At this point, the app runs at http://127.0.0.1:8000/
<br />
👉 Go to /api/docs/ to see documentation with endpoints
> If you want to try all functionality follow next steps:
```bash
$ run docker exec -it <container_id> sh in terminal
$ run python manage.py createsuperuser and follow next steps
$ /api/user/token/login/ to authorize after creating superuser and get token
```
<br />


## Features
* Admin panel /admin/
* Documentation is located at /api/docs/
* Admin can create new users
* All users can create teams
* User can add only himself to team, admin can add or remove all users
* Filtering for users

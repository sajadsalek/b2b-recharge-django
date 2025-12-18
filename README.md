# b2b-recharge-django
## Installation

Use the package manager [uv](https://docs.astral.sh/uv/) to packages:

```bash
uv sync
```
after that run this command and edit the .env file:
```bash
cp .env.example .env
```

## Database
in root of project run this command:

```bash
docker compose up -d
```

## Run Project
in root of project run this command:
```bash
./manage.py runserver
```
## Tests
for running test run this command:
```bash
pytest -v
```

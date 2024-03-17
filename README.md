## Getting Started

1) Create and start Virtual Enviaronment
2) Install requirements.txt

```bash
pip install -r requirements.txt
```

3) Make Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
4) Load fixtures data
```bash
python manage.py loaddata server/fixtures/initData.json
```
5) Start redis server in another terminal
```bash
redis-server
```
6) Run django server
```bash
python manage.py runserver
```

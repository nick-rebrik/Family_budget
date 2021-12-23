# Family budget
***REST API Application to maintain a family budget.***
### Description
Application for budgeting, with the possibility of:
- Create budget lists and share them with other users
- Create budgets
- Sort expenses and receipts in budgets on categories.
To use, you need to log in and receive your token. The program is covered with tests and has test fixtures

### Technologies

- Python 3.9
- Django 2.2.6
- Django REST Framework 3.10
- Djoser 2.1.0
- Swagger documentation 1.17.1
- Docker

### Quick start

Docker:
1. In the main directory of the project run in command line:
```docker-compose up -d```
2. Run in command line:
```docker-compose exec app python manage.py migrate```
3. To load test data:
```docker-compose exec app python manage.py loaddata test_data.json```
4. To view all API commands, go to the [Docs](http://127.0.0.1:8000/api/docs/) page:
```http://127.0.0.1:8000/api/docs/```

Local:
1. Install and activate the virtual environment
2. Install all packages from [requirements.txt](https://github.com/nick-rebrik/Family_budget/blob/main/requirements.txt):
  ```pip install -r requirements.txt```
3. Run in command line:
  ```python manage.py migrate```
4. To load test data:
```docker-compose exec app python manage.py loaddata test_data.json```
5. Run server:
```python manage.py runserver```
6. Go to the [Docs](http://127.0.0.1:8000/api/docs/):
```http://127.0.0.1:8000/api/docs/```

> #### _* The project was tested using Django tests._

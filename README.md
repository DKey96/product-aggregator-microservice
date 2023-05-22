# Product Aggregator Microservice
Service developed as a homework assignment from Applifting. Purpose of this app is to register new products (whatever they are)
and gather the offers with prices for each.

## Dependendencies
- `python3.11`
- `django` + `django rest framework` -> Used for developments of the BE Application and REST API. 
- `appscheduler` -> Used for background tasks of gathering offers
- all other dependencies can be found in `requirements.txt`

## How to use
### Docker Environment
- As a part of the projects, there is a Dockerfile and docker-compose.yaml, so that the app can be run without 
need to setup the local environment. 
- Only necessary things to be install is [Docker](https://docs.docker.com/engine/install/).
- Then just navigate to the top folder and run:
```bash
docker-compose build && docker-compose up
```

### Local Environment
#### PostgreSQL Setup
- Creating the PostgreSQL Database and User
```bash
sudo -u postgres psql
```
```bash
CREATE DATABASE applifting;
CREATE USER applifting WITH PASSWORD 'applifting';

ALTER ROLE applifting SET client_encoding TO 'utf8';
ALTER ROLE applifting SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE applifting TO applifting;
```
#### Django Setup
- Create a virtual environment and activate it
```bash
python3 -m venv venv
source /venv/bin/activate
```
- Install all necessary libraries
```bash
python3 -m pip install -r requirements.txt 
```
- Migrate the database (make sure you are in the `product_aggregator_microservice` folder)
```bash
python3 manage.py migrate 
```
- Before the start of the application, make sure you have Environment Variable `APPLIFTING_SERVICE_BASE_URL` 
set to the Offer Microservice base URL (https://python.exercise.applifting.cz/api/v1)

- Start the application
```bash
python3 manage.py runserver 
```
### After your environment is ready and app running
- First things first, as the application has the TokenAuthentication enabled, user has to register:
```bash
curl --location --request POST 'http://127.0.0.1:8000/auth/registration/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "daniel.klic",
    "password": "klic"
}'
```
Response:
```json
{
    "message": "User successfully created!",
    "username": "daniel.klicx"
}
```
- After the registration, user must obtain an authentication token as follows:
```bash
curl --location --request POST 'http://127.0.0.1:8000/auth/api-token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "daniel.klic@rossum.ai",
    "password": "klic"
}'
```
Response
```json
{
    "token": "dca5e4e620a5772f14eee427e59c7cd8d42062dc"
}
```
- With this token inserted into the header as `"Authentication": "Token dca5e4e620a5772f14eee427e59c7cd8d42062dc"`
can user discover the beauty of the other calls of the API.
- For that purpose there is a SwaggerUI and Redoc documentation available on `/api/docs/swagger` or `/api/docs/redoc/`

## Assignment overview
Create a REST API JSON Python microservice which allows users to browse a product catalog and which automatically updates prices from the offer service, provided by appligting.

### Requirements
- Provide an API to create, update and delete products
- Periodically query the provided microservice for offers
- Provide an API to get product offers

### Data model
#### Products
Each product corresponds to a real world product you can buy.

- id - UUID
- name - string
- description - string

A product has many offers.

#### Offers
Each offer represents a product offer being sold for a price.

- id - UUID
- price - integer
- items_in_stock - integer

Each offer belongs to one product.

### Specification
#### Must haves:
- Use an SQL database as an internal data store; the library for the API layer is up to you
- Use an access token from sign-up to access the offers microservice - this should be done only once, all your registered products are tied to this token
- To authenticate your requests, use a Bearer: <access-token> header
- Create CRUD for products
- Once a new product is created, call the offers microservice to register it
- Your API does not need authentication
- Create a background service which periodically calls the offers microservice to request offers for your products
- Price in the offers microservice updates every minute, and offers sell out
- Once an offer sells out, it is replaced by another one
- Create a read-only API for product offers
- Base URL for the offers microservice should be configurable via an environment variable
- Write basic tests with pytest
- Add a README with information on how to start & use your service
- Push your code into git repository and send us access (our preference is gitlab.com)

#### You can earn extra points for:
- JSON REST API simple authentication (e.g. access-token)
- Consider adding some reasonable error handling to the API layer
- Provide a working Dockerfile and docker-compose.yml for your application for easy testing
- Use reasonable dependency management (requirements.txt, Pipenv, Poetry, ...)
- Deploy your application to Heroku
- Track the history of offer prices and create an endpoint which returns the trend in offer prices and compute the percentual rise / fall in price for a chosen period of time

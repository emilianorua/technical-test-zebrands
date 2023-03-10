#  Zebrands backend technical test
Technical test for zebrands interview

# Technology

* Web framework:
  - **Flask**
* Authentication:
  - **flask_jwt_extended**
* Database:
  - **flask_sqlalchemy (sqlite)**

# Running the app
Preferably, first create a virtualenv and activate it, perhaps with the following command:

```
virtualenv -p python3 venv
source venv/bin/activate
```

Next, run

```
pip install -r requirements.txt
```
to get the dependencies.

# Run the app

```
flask run
```

# Create an admin user

You can create an admin user using the following endpoint (only works in DEBUG mode):

## POST /api/v1/users/createadminuser
**Description:** Create a new admin user.

**Params:**

| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| username (body)| string, required | 10 | 100 | - |
| password (body)| string, required | 10 | 100 | - |
| email (body)| string, required | - | 80 | Valid email |

**Return:**

The new admin user. Example:

``` json
{
    "email": "admin@admin.com",
    "public_id": "c76be712-7158-4c97-b861-13d4e8170860",
    "role": "ADMIN",
    "username": "AdminUser"
}
```

# TEST 

You can test the API with this postman collection: https://easyupload.io/8jd77u

# API Documentation

## POST /api/v1/auth/register
**Description:** Register a new user

**Params:**
| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| username (body) | string, required | 10 | 100 | - |
| password (body) | string, required | 10 | 100 | - |
| email (body) | string, required | - | 80 | Valid email |

**Return:**

The registered user. Example:

``` json
{
    "email": "emilianorua@gmail.com",
    "public_id": "9a5d2689-3e77-4f5a-b1a2-58118ea9d9f1",
    "role": "ADMIN",
    "username": "emilianorua"
}
```
## POST /api/v1/auth/login
**Description:** Login a user

**Params**:  
| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| username (body) | string, required | 10 | 100 | - |
| password (body) | string, required | 10 | 100 | - |

**Return:**

The access token. Example:

``` json
{
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODM0MjEyOCwianRpIjoiMjY0MmVhZTAtNjg0Zi00NTMwLWE4YzQtNjFhYTM1YmVlYjMxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImE1OWYwMTBjLWY0NmQtNDI0Ny1hZGQ5LWY3ODg5MjAxMWE3NCIsIm5iZiI6MTY3ODM0MjEyOCwiZXhwIjoxNjc4MzQ1NzI4fQ.SvFxEfjYXm3gz0fnnFiwoF9IVgNQQt7bB1J7uHdX_e4"
}
```
## GET /api/v1/users/
**Description:** Gets a single user or a list of users

**Security**: Valid Bearer token and ADMIN role

**Params:** 
| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| id (path)| string, optional | - | - | A valid id |

**Return:**

A single user, list of users.  
Example for list of users:

``` json
[
    {
        "email": "emilianorua@gmail.com",
        "public_id": "a59f010c-f46d-4247-add9-f78892011a74",
        "role": "ADMIN",
        "username": "emilianorua"
    },
    {
         "email": "user@hotmail.com",
        "public_id": "c76be712-7158-4c97-b861-13d4e8170860",
        "role": "USER",
        "username": "NuevoUsuario"
    }
]
```
## POST /api/v1/users/
**Description:** Create a new user.

**Security**: Valid Bearer token and ADMIN role

**Params:**

| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| username (body)| string, required | 10 | 100 | - |
| password (body)| string, required | 10 | 100 | - |
| email (body)| string, required | - | 80 | Valid email |
| role (body)| string, required | - | - | USER, ADMIN |

**Return:**

The new user. Example:

``` json
{
    "email": "user@hotmail.com",
    "public_id": "c76be712-7158-4c97-b861-13d4e8170860",
    "role": "USER",
    "username": "NuevoUsuario"
}
```
## PUT /api/v1/users/{id}
**Description:** Updates a user.

**Security**: Valid Bearer token and ADMIN role

**Params:**

| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| id (path)| string, required | - | - | A valid id |
| username (body)| string, required | 10 | 100 | - |
| password (body)| string, required | 10 | 100 | - |
| email (body)| string, required | - | 80 | Valid email |
| role (body)| string, required | - | - | USER, ADMIN |

**Return:**

The user updated. Example:

``` json
{
    "email": "user@hotmail.com",
    "public_id": "c76be712-7158-4c97-b861-13d4e8170860",
    "role": "USER",
    "username": "NuevoUsuario"
}
```
## DELETE /api/v1/users/{id}
**Description:** Delete a user.

**Security**: Valid Bearer token and ADMIN role

**Params:**
| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| id (path)| string, required | - | - | A valid id |

**Return:**

status 200 OK

## GET /api/v1/products/{id}
**Description:** Gets a single product or a list of products

**Security**: None

**Params:**

| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| id (path)| string, optional | - | - | A valid id |

**Return:**

A single product or a list of products.  
Example for list of products:

``` json
[
    {
        "brand": "Pirelli",
        "name": "Rueda de auto",
        "price": 45000.0,
        "public_id": "cb603ea2-d5e2-4ff6-ae5b-6cd195034463",
        "queries": 0,
        "sku": "12345678"
    },
    {
        "brand": "Firestone",
        "name": "Rueda",
        "price": 42000.0,
        "public_id": "f04cde58-dd54-4d6e-8860-9ef137698368",
        "queries": 0,
        "sku": "123456789"
    }
]
```
## POST /api/v1/products/
**Description:** Create a new product.

**Security**: Valid Bearer token and ADMIN role

**Params:**
| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| name (body) | string, required | - | 100 | - |
| sku (body) | string, required | - | 50 | - |
| price (body) | float, required | - | - | Valid email |
| brand (body) | string, required | - | -50 | USER, ADMIN |

**Return:**

The new product. Example:

``` json
{
    "brand": "Pirelli",
    "name": "Rueda",
    "price": 42000.0,
    "public_id": "26c2603d-93c1-48dd-8e21-8467b780ad9c",
    "queries": 0,
    "sku": "123456789"
}
```
## PUT /api/v1/products/{id}
**Description:** Updates a product.

**Security**: Valid Bearer token and ADMIN role

**Params:** 

| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| id (path)| string, required | - | - | A valid id |
| name (body)| string, required | - | 100 | - |
| sku (body)| string, required | - | 50 | - |
| price (body)| float, required | - | - | Valid email |
| brand (body)| string, required | - | -50 | USER, ADMIN |

**Return:**

The updated product. Example:

``` json
{
    "brand": "Pirelli",
    "name": "Rueda",
    "price": 42000.0,
    "public_id": "26c2603d-93c1-48dd-8e21-8467b780ad9c",
    "queries": 0,
    "sku": "123456789"
}
```
## DELETE /api/v1/products/{id}
**Description:** Delete a product.

**Security**: Valid Bearer token and ADMIN role

**Params:**

| **Name** | **Type** | **Min** | **Max** | **Validation** |
| --- | --- | --- | --- | --- |
| id (path)| string, required | - | - | A valid id |

**Return:**

status 200 OK
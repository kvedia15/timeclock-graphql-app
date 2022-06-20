# Time Clock GraphQL Application

A graphQL backend project that allows users to register, authenticate and make authenticated queries and mutations. This service allows employees to clock in and clock out of the work place. It also allows the employees to see how many hours they worked today, in the current week and in the current month.

## Requirements

The project requires [Python 3.7](https://www.python.org/downloads/release/python-370/) or higher and
the [PIP](https://pip.pypa.io/en/stable/) package manager.

## Useful Python commands

### Installation

Install the project dependencies

```console
$ python3.7 -m pip install --requirement requirements.txt
```

### Run the tests

Run all tests

```console
$ python3.7 manage.py test
```

### Run the application

Run the application locally

```console
$ python3.7 manage.py runserver
```

Then go to [http://127.0.0.1:8000/graphql to start writing queries and mutations](http://127.0.0.1:8000/graphql)

### API

Below is a list of all mutations and queries with their respective input and output. Please note that the application needs to be running for the following queries and mutations to work. For more information about how to run the application, please refer
to [run the application](#run-the-application) section above.

### Add User

```console

mutation{
  addUser (email:"user@gmail.com",username: "user", password: "password") {
      user{
          username
          email
      }
  }
}

```

Return Data

```json
{
  "data": {
    "addUser": {
      "user": {
        "username": "user",
        "email": "user@gmail.com"
      }
    }
  }
}
```

### Authenticate User

```console

mutation{
  tokenAuth(username: "user", password: "password") {
    token
    payload
    refreshExpiresIn
  }
}

```

Return Data if credentials are valid

```json
{
  "data": {
    "tokenAuth": {
      "token": "token",
      "payload": {
        "username": "user",
        "exp": 1655694250,
        "origIat": 1655693950
      },
      "refreshExpiresIn": 1656298750
    }
  }
}
```

To use authenticated queries we must use the token provided above.

### [AUTHENTICATED] Clock In User

```console

mutation {
  clockIn(token: "token"){
    clockItem{
      user{
        username
      }
      clockIn
    }
  }
}

```

Return Data

```json
{
    "clockIn": {
        "clockItem": {"user": {"username": "user"}, "clockIn": "2022-06-20T04:10:16.932004"}
    }
}

```

### [AUTHENTICATED] Clock Out User

```console

mutation {
  clockOut(token: "token"){
    clockItem{
      user{
        username
      }
      clockIn
      clockOut
    }
  }
}

```

Return Data

```json
{
    "clockIn": {
        "clockItem": {"user": {"username": "user"}, "clockIn": "2022-06-20T04:10:16.932004", "clockIn": "2022-06-20T16:10:16.932004"}
    }
}

```

### [AUTHENTICATED] Get Current Clock for User

```console

            query  {
            currentClock(token"token") {
                user{
                    username
                }
                clockOut
            }
}

```

Return Data

```json
{
    "clockIn": {
        "clockItem": {"user": {"username": "user"}, "clockIn": "2022-06-20T04:10:16.932004", "clockIn": "2022-06-20T16:10:16.932004"}
    }
}

```

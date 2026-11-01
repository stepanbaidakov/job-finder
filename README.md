# Vacancy Management Application

An application for retrieving job vacancies from the hh.ru platform. It allows users to search for vacancies, save them to a JSON file, and manage the stored data by adding, filtering, and deleting vacancies.

## Features

The application provides the following features:

- retrieve job vacancies from hh.ru through its API;
- search for vacancies based on a user-defined query;
- convert API responses into structured vacancy objects;
- save vacancies to a JSON file;
- load saved vacancies from a file;
- compare vacancies based on their salaries;
- add new vacancies to the stored data;
- delete stored vacancy data.

## Architecture and Key Features

- **API Integration** is used to connect to hh.ru and retrieve job vacancy information.
- **Object-Oriented Programming (OOP)** is used to represent vacancies as objects with selected attributes.
- **Data Serialization** converts vacancy objects into JSON-compatible data for storage and further processing.
- **JSON Storage** is used to save and retrieve vacancy data from a file.
- **Salary Comparison** allows vacancy objects to be compared based on their salary values.

## Tech Stack

- Python
- Requests
- JSON
- Python-dotenv
- Object-Oriented Programming (OOP)
- hh.ru API

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/stepanbaidakov/job-finder.git
cd job-finder
```

### 2. Install dependencies

If the project uses Poetry:

```bash
poetry install
```

To install the dependencies without installing the project itself:

```bash
poetry install --no-root
```

Alternatively, if a `requirements.txt` file is available, install the dependencies using pip:

```bash
pip install -r requirements.txt
```

If the project uses a `.env` file to load environment variables, make sure `python-dotenv` is included in the project dependencies.

### 3. Register an application on hh.ru

To access the hh.ru API, you need to register an application and obtain an access token.

1. Open the [hh.ru developer portal](https://dev.hh.ru/).
2. Sign in to your hh.ru account.
3. Open the [application management page](https://dev.hh.ru/admin).
4. Register a new application and complete the required information.
5. Open the registered application and obtain its `client_id` and `client_secret`.

Keep your application credentials private.

### 4. Obtain an Access Token

After registering your application, use your `client_id` and `client_secret` to send an HTTP `POST` request to the hh.ru token endpoint:

`https://hh.ru/oauth/token`

Include the following form data in the request:

- `grant_type=client_credentials`
- `client_id=YOUR_CLIENT_ID`
- `client_secret=YOUR_CLIENT_SECRET`

Example using `curl`:

```bash
curl -X POST https://hh.ru/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

The response contains an `access_token`. Copy its value for the next step.

### 5. Configure Environment Variables

Use the `.env.sample` file provided in the repository as a template for your local environment configuration.

1. Create a copy of `.env.sample` named `.env`.
2. Open `.env` and replace the placeholder with your access token:

```dotenv
ACCESS_TOKEN=YOUR_ACCESS_TOKEN
```

3. Save the file.

Make sure `.env` is listed in `.gitignore` to prevent your access token from being uploaded to GitHub.

The application will use this token to authorize requests to the hh.ru API.
## Running the Application

Run the application using Poetry:

```bash
poetry run python main.py
```

If the Poetry virtual environment is activated:

```bash
python main.py
```

The application can also be launched directly from PyCharm by running `main.py`.

## Output

The application stores retrieved job vacancies in a JSON file. Users can search for vacancies in the saved file by providing their URLs, and the matching vacancies will be displayed.

Vacancy data can also be loaded, filtered, compared, and managed for further processing.

## Testing

The project can be tested using `pytest`.

To run all tests:

```bash
pytest
```

To run tests with more detailed output:

```bash
pytest -v
```

The project also uses `unittest.mock` to mock external API requests, allowing the tests to run without making real HTTP requests.

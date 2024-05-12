# SnipSaver

This Django project implements a RESTful API for saving and retrieving short text snippets. Each snippet is associated with a title, timestamp, and the user who created it. Additionally, each snippet is related to one or more tags, represented by a simple model with a title field. Tags are unique, and if a tag with the same title already exists, the snippet is linked to that tag.

## Features

- Save short text snippets with title, timestamp, and user information.
- Associate snippets with tags and ensure tag uniqueness.
- Implement JWT authentication for user authorization.
- Integrated Swagger UI for easy API documentation access.

### Prerequisites

Make sure you have the following installed on your local machine:

- Python 3.11+
- pip (Python package manager)

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:

    ```bash
   cd snip_saver
   ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

- On macOS and Linux:

  ```bash
  source venv/bin/activate
  ```
5. Install dependencies:

    ```bash
   pip install -r requirements.txt
   ```

6. Apply migrations:
    ```bash
   python manage.py migrate

   ```

## Usage

1. Create a superuser to access the API:
    ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create a superuser account.

2. Start the development server:

    ```bash
   python manage.py runserver
   ```

3. To access Swagger UI for API documentation, navigate to:
    ```bash
   http://localhost:8000/api/docs/
   ```

## Logging in and Obtaining JWT Token

1. Go to `/auth/api/token/` in the Swagger UI.
2. Provide the admin username and password.
3. Copy the JWT token provided.
4. Press the "Authorize" button on the top right corner of the Swagger UI.
5. Paste the copied token into the input field and press "Authorize".



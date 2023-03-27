# Simple Blog REST APIs with Flask

This project provides a RESTful API for a simple blog application. The API is built using the Flask web framework and uses SQLAlchemy as the ORM to interact with the database.

## Features

The following features are implemented in this project:

   *  User authentication (registration, login, logout)
   *  Create, read, update, and delete blog posts
   *  Display a list of all blog posts on the homepage
   *  Display a single blog post on a separate page
   *  Pagination API for displaying multiple blog posts

## Dependencies

The following dependencies are required to run the project:

    Flask
    SQLAlchemy
    Flask-RESTful

## Installation

To install the required dependencies, run the following command:

```bash
python -m venv env

source env/bin/activate

pip install -r requirements.txt
```

## Usage

To start the application, run the following command:

```bash
python app.py
```
This will start the application on http://localhost:5000.

## API Documentation
The api can be found on the route. Post-id is optional.
```
http://localhost:5000:/api/post/<post-id>/
```
## License

This project is licensed under the MIT License. See the LICENSE file for details.
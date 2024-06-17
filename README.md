# Authentication Service

This is a simple authentication service built with Flask.
It provides endpoints for user registration, login, password reset, and token refresh using JWT.

## Features

- User registration
- User login
- Password reset
- Token refresh
- Rate limiting
- Swagger API documentation

## Requirements

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- Flask-CORS
- Flask-Limiter
- Flasgger

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/samuelogboye/auth-service-flask.git
cd auth-service-flask
```

### 2. Install the Requirements

It's recommended to use a virtual environment to manage dependencies.

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory of your project and add the following environment variables:

```bash
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
DATABASE_URL=sqlite:///site.db
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
SWAGGER_HOST=localhost:5000
```

### 4. Initialize the Database

Run the following command to create the database and apply migrations:

```bash
flask db upgrade
```

### 5. Run the Application

You can run the application locally using Gunicorn.

```bash
gunicorn -w 4 -b 0.0.0.0:5000 manage:app
```

This will start the application on port 5000, accessible at `http://localhost:5000`.

## API Documentation

The API documentation is generated using Swagger and can be accessed at `http://localhost:5000/apidocs`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

For any inquiries, please contact [Samuel Ogboye](mailto:ogboyesam@gmail.com).

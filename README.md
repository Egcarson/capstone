
---

# Movie Listing API - ALTSCHOOL CAPSTONE PROJECT

## Project Overview

This capstone project is a Movie Listing API developed using FastAPI. The API enables users to list movies, view movies, rate them, and add comments. The application is secured using JSON Web Tokens (JWT), ensuring that only the user who listed a movie can edit or delete it. The API is designed with both public and authenticated access and is deployed on a cloud platform for scalability and availability.

## Features

### User Authentication
- **User Registration**: Allows new users to create an account.
- **User Login**: Enables users to log in and receive a JWT for authenticated access.
- **JWT Token Generation**: Secures the application, ensuring only authenticated users can perform certain actions.

### Movie Management
- **View a Movie**: Public access to view the details of any listed movie.
- **Add a Movie**: Authenticated users can list a new movie.
- **View All Movies**: Public access to view all listed movies.
- **Edit a Movie**: Only the user who listed the movie can edit its details.
- **Delete a Movie**: Only the user who listed the movie can delete it.

### Movie Rating
- **Rate a Movie**: Authenticated users can rate a movie.
- **Get Movie Ratings**: Public access to view ratings for a movie.

### Comments
- **Add a Comment to a Movie**: Authenticated users can add comments to a movie.
- **View Comments for a Movie**: Public access to view all comments on a movie.
- **Nested Comments**: Authenticated users can add comments to existing comments (i.e., replies).

## Requirements

### Language & Framework
- **Python**: Version 3.12.1
- **FastAPI**: A modern, fast web framework for building APIs with Python

### Authentication
- **JWT**: JSON Web Tokens are used to secure API endpoints.

### Database
- **SQL**: Compatible with PostgreSQL database or any other SQL database.

### Testing
- **Unit Tests**: Comprehensive tests are included for all API endpoints to ensure reliability.

### Documentation
- **OpenAPI/Swagger**: API documentation is automatically generated and available via the `/docs` endpoint.

### Logging
- **Logging**: Important application events and errors are logged for monitoring and debugging purposes.

### Deployment
- **Cloud Platform**: The application is deployed on a Render cloud server for accessibility and scalability.
- **Docker**: The application is containerized using Docker for consistency across environments.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Egcarson/capstone.git
   cd capstone
   ```

2. **Create a Virtual Environment** (if not using Docker):
   ```bash
   python3 -m venv env
   `env\Scripts\activate`  # On MAC PC use "source env/bin/activate"
   ```

3. **Install Dependencies** (if not using Docker):
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root with the following variables:
     ```env
     DATABASE_URL=your-database-url
     SECRET_KEY=your-secret-key
     ```

5. **Run Database Migrations**:
   ```bash
   alembic upgrade head  # If using Alembic for migrations
   ```

6. **Run the Application**:

   **Using Docker:**
   - Build and run the Docker container:
     ```bash
     docker-compose up --build
     ```
   - This will start the application and make it available at `http://localhost:8000`.

   **Without Docker:**
   - Run the application using Uvicorn:
     ```bash
     uvicorn app.main:app --reload
     ```

7. **Access the API**:
   - API documentation will be available at `http://localhost:8000/docs`.

## Usage

### API Endpoints

- **Authentication**
  - `POST /register`: Register a new user
  - `POST /login`: Log in and obtain a JWT
- **Movies**
  - `GET /movies`: Retrieve all movies
  - `POST /movies`: Add a new movie (Authenticated)
  - `GET /movies/{movie_title}`: Retrieve a single movie by its ID
  - `PUT /movies/{movie_title}`: Edit a movie (Authenticated, Owner only)
  - `DELETE /movies/{movie_title}`: Delete a movie (Authenticated, Owner only)
- **Ratings**
  - `POST /ratings`: Rate a movie (Authenticated)
  - `GET /ratings`: Get ratings for a movie
- **Comments**
  - `POST /comments`: Add a comment to a movie (Authenticated)
  - `GET /comments/{movie_title}`: View comments for a movie
  - `POST /comments/{comment_id}/reply`: Add a reply to a comment (Authenticated)

### Testing

Run the test suite to ensure all features work as expected:
```bash
pytest
```

## Deployment

The application can be deployed to any cloud platform of your choice. Ensure that the following environment variables are set:

- `DATABASE_URL`: Connection string for your database
- `SECRET_KEY`: A secret key for JWT token generation

**Docker Deployment**:
- The application is containerized using Docker. To deploy the Docker container, use the following command:
  ```bash
  docker-compose up --build
  ```
- Ensure that your cloud provider supports Docker, and configure your environment variables accordingly.

## Logging

The application logs important events, such as user authentication attempts, movie additions, and errors, to provide insights into the application's performance and security.

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are welcome.

## Contact

For any inquiries or support, please contact me at [esehgodprevail@gmail.com](mailto:esehgodprevail@gmail.com).

---
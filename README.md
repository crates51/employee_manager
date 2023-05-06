# Employee Manager

A simple application for managing employees and calculating some statistics about them.

## Dependencies

This project requires the following dependencies to be installed:

- Docker
- Docker Compose

## Installation

To run the project, follow these steps:

1. Clone the repository:

   ```
   git clone git@github.com:crates51/employee_manager.git
   ```

2. Navigate to the project directory:

   ```
   cd employee-manager
   ```

3. Build the Docker containers:

   ```
   make build
   ```

4. Start the project:

   ```
   make up
   ```

5. Use the project:

   You can access the API at `http://localhost:8000/employee/`.

   You can also connect to the PostgreSQL database using the following command:

   ```
   make connect_db
   ```

   This will open the PostgreSQL command-line interface, where you can execute SQL queries.

## Usage

The project provides an API for managing employee data. You can perform the following operations:

- Create a new employee: `POST /employee/`
- Retrieve a list of all employees: `GET /employee/`
- Retrieve a specific employee by ID: `GET /employee/{id}/`
- Update an employee: `PUT /employee/{id}/`
- Delete an employee: `DELETE /employee/{id}/`

### Quick Commands

The following commands are available to use in the terminal:

- `make build`: Builds the Docker images for the application
- `make up`: Starts the application
- `make down`: Stops the application and removes the containers and volumes
- `make connect_main`: Connects to the main Docker container
- `make connect_db`: Connects to the PostgreSQL database container

## Statistics

The following statistics are calculated based on the employee data:

- Average age per industry
- Average salary per industry
- Average salary per years of experience
- Proportion of female employees per industry

build:
	docker-compose build

up:
	echo "Bringing up the project..."
	make down
	docker-compose up --abort-on-container-exit

down:
	docker-compose down -v

connect_main:
	docker exec -it employee_manager_employee_manager_1 bash

connect_db:
	docker exec -it employee_manager_postgres_1 psql --username=postgres --dbname=postgres

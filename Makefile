.PHONY: prod start build run down clean drop_db prune auto_backup stop_backup backup restore frontend_build frontend_export

BACKUP_COMMAND := 0 0 * * * cd "$(PWD)" && python3 scripts/backup.py

prod:
	@if [ $$(docker ps -q -f name=backend_app) ]; then \
			docker compose stop backend_app; \
			docker compose rm -f backend_app; \
	fi
	docker compose up -d --build

down:
	docker compose down

run: down 
	docker compose up postgres redis -d
	sleep 2
	alembic upgrade head
	uvicorn src.main:app --reload

start:
	uvicorn src.main:app --reload

build: down
	docker compose up -d --build

open-redis:
	docker exec -it redis_cats redis-cli

clean:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf

auto_backup:
	@if crontab -l ; then \
		crontab -l > mycron ; \
	else \
		touch mycron ; \
	fi
	@echo '$(BACKUP_COMMAND)' >> mycron
	@crontab mycron
	@rm mycron
	@echo "Backup script added to cron"
	
stop_backup:
	crontab -l | grep -v '$(BACKUP_COMMAND)' | crontab -

backup:
	python3 scripts/backup.py
	@echo "Backup complete"

restore:
	python3 scripts/restore.py

frontend_build:
	if [ -d dist.tar.xz ]; then \
		sudo rm -rf dist.tar.xz; \
	fi
	tar -cJvf dist.tar.xz dist

frontend_export:
	if [ -d /var/www/school/dist ]; then \
		sudo rm -rf /var/www/cat-for-future/dist; \
	fi
	sudo mkdir -p /var/www/cat-for-future/
	sudo tar -xJvf dist.tar.xz -C /var/www/cat-for-future/

drop_db: down
	if docker volume ls -q | grep -q $$(basename "$$(pwd)")_postgres_data; then \
		docker volume rm $$(basename "$$(pwd)")_postgres_data; \
		echo "successfully drop_db command";\
	fi
	if docker volume ls -q | grep -q $$(basename "$$(pwd)")_backend_data; then \
		docker volume rm $$(basename "$$(pwd)")_backend_data; \
		echo "successfully drop_db command";\
	fi

prune: down
	docker system prune -a
	docker volume prune -a

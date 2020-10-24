# Variable Names
LOCAL_DB ?= ~/Documents/Classes/Computer-Science/info253b/final/database/
SERVER_NAME ?= server253bproj
NETWORK_NAME ?= net253bProj
DB_NAME ?= db253bProj
MYSQL_PASSWORD ?= asg253dbProj
MYSQL_DB_NAME ?= db253BProj

# Network Targets

initNet:
	docker network create $(NETWORK_NAME)

rmNet:
	docker network rm $(NETWORK_NAME)

# Database Targets

db-it:
	docker exec -it $(DB_NAME) /bin/bash

db-rm:
	docker rm $(DB_NAME)

db-stop:
	docker stop $(DB_NAME)

db-start:
	docker start $(DB_NAME)

db-run:
	docker run --name $(DB_NAME) --network $(NETWORK_NAME) \
		-e MYSQL_ROOT_PASSWORD=$(MYSQL_PASSWORD) \
		-e MYSQL_DATABASE=$(MYSQL_DB_NAME) \
		-v $(LOCAL_DB):/var/lib/mysql \
		-dit mysql:latest \
		--default-authentication-plugin=mysql_native_password

# Server Targets

svr-it:
	docker exec  -it $(SERVER_NAME) /bin/bash

svr-build:
	docker build -t $(SERVER_NAME) .

svr-run:
	docker run -d -p 5000:5000 --network $(NETWORK_NAME) --name $(SERVER_NAME) $(SERVER_NAME)

svr-stop:
	docker stop $(SERVER_NAME)

svr-rm:
	docker rm $(SERVER_NAME)

svr-start:
	docker start $(SERVER_NAME)

svr-restart: svr-stop svr-rm svr-build svr-run

# Comprehensive Targets

terminate: svr-stop svr-rm db-stop db-rm rmNet

setup: initNet db-run svr-build svr-run

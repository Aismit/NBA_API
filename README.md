## Basketball API

Info 253B Spring 2020 Final Project

Aismit Das, Rishabh Meswani, Bryant Le, Sahil Mehta, John Yang

### Local Setup
To run the repository code and Docker container code successfully, do the following:
1. Within the `Makefile`, set the `LOCAL_DB` path variable to point at the `database` repository in this file
2. Run the following Makefile commands to set up the Network, Database, and Server containers. Optionally, you can also run `make setup` which calls all 4 targets below.
  * `make initNet`: Creates network for server, database communication
  * `make db-run`: Create and start MySQL database
  * `make svr-build`: Builds server container from `Dockerfile`
  * `make svr-run`: Runs server container

### Useful Targets
* If you have made changes to `server.py` and would like to test them, run `make svr-restart`. This target 1. stops + removes the existing server container 2. rebuilds the server image 3. runs a new server container from the rebuilt image

### Repository Description
* `data`: CSV files containing data imported into database
* `database`: Folder containing information for MySQL database
* `misc`: Web-scraping, dependency requirements, table schemas, project proposal

### MySQL Table Configurations
Table configurations stored within `db_schema.sql` file.

### Endpoints List

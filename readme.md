# Apriori analysis

Analyzing csv file with pandas and apriori algorithm.

## Team members

- Jason Carneiro
- Marcos Paulo
- Nicolas Fernando

## Setup (docker)

Clone the `.env.sample` file to `.env`.

```bash
cp .env.sample .env
```

### Database setup

Turn on database container using docker-compose file

```bash
docker-compose up
```

Run `setup-db` make command and put database password (`dba` as user and password)

```bash
make setup-db
```

Run Python script to populate the database

```bash
make run # takes you to the container
python populate_db.py # executes python script
```

### Analysis scripts

Run make command to take you to the container and execute python scripts

```bash
make run
# container bash
python analysis.py
python apriori.py
```

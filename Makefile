include .env
export

define CREATE_DB_SCRIPT
USE recommendations; \
CREATE TABLE IF NOT EXISTS products ( \
  product_id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, \
  product_name varchar(255) NOT NULL \
); \
CREATE TABLE IF NOT EXISTS transactions ( \
  transaction_id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, \
  date_time datetime NOT NULL, \
  period_name varchar(255) NOT NULL, \
  weekday_end varchar(255) NOT NULL \
); \
CREATE TABLE IF NOT EXISTS transaction_items ( \
  transaction_item_id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, \
  product_id int(11) NOT NULL, \
  transaction_id int(11) NOT NULL \
);
endef

setup-db:
	@echo "Setting up database..."
	docker-compose exec maria-db bash -c 'mysql -u $(DB_USER) -e "$(CREATE_DB_SCRIPT)" -p'

run:
	docker run --rm -ti -v ${PWD}:/app -w /app --network=ml-apriori-recommendation_default python:3.9-slim \
    bash -c "/usr/local/bin/pip install -r /app/requirements.txt; bash"

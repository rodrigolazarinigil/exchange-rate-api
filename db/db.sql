grant all privileges on database "exchange_rate_api" to exchange_user;

CREATE SCHEMA exchange
    AUTHORIZATION exchange_user;

CREATE TABLE exchange.euro_to_dollar_rate
(
	date DATE NOT NULL,
	timestamp timestamp NOT NULL,
	usd_value NUMERIC(10, 8) NOT NULL
);
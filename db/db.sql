grant all privileges on database "exchange_rate" to exchange_rate_user;

CREATE SCHEMA exchange
    AUTHORIZATION exchange_rate_user;

CREATE TABLE exchange.euro_to_dollar_rate
(
	date DATE NOT NULL,
	timestamp timestamp NOT NULL,
	usd_value NUMERIC(10, 8) NOT NULL,
	CONSTRAINT un_euro_to_dollar_rate UNIQUE (date, timestamp)
);
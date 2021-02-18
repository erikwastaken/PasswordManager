# Very basic command line password manager

## local PostgreSQL database
### create table statements
 CREATE TABLE users(
   user_id SERIAL PRIMARY KEY,
   username VARCHAR ( 50 ) UNIQUE NOT NULL,
   password VARCHAR ( 64 ) NOT NULL,
   created_on TIMESTAMP NOT NULL
 );

 CREATE TABLE accounts(
   account_id SERIAL PRIMARY KEY,
   user_id VARCHAR ( 50 ) NOT NULL,
   service VARCHAR ( 50 ) NOT NULL,
   login_name VARCHAR ( 50 ) NOT NULL,
   login_password VARCHAR ( 50 ) NOT NULL,
   created_on TIMESTAMP NOT NULL,
   last_changed_on TIMESTAMP,
   FOREIGN KEY (user_id)
   REFERENCES users (user_id)
 );

# Very basic command line password manager

## local PostgreSQL database
### create table statements
```
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
   login_password VARCHAR NOT NULL,
   created_on TIMESTAMP NOT NULL,
   last_changed_on TIMESTAMP,
   FOREIGN KEY (user_id)
   REFERENCES users (user_id)
 );
 ```
## how to use
on the "server side" have a postgresql database running and create the aforementioned tables;\
create a database.ini file in the server directory with the access data for the database, e.g.:
```
[postgresql]
host=localhost
database=password_manager
user=basic
password=HelloWorld
```
create a communication.ini file in the client directory with the address on which the server will be running, e.g.:
```
[connection]
address=http://localhost:5000
```
can be run locally by running the following code:
```
python3 server/api.py
```
once the server is up and running you can execute the following to access the password manager:
```
python3 client/manager.py
```  
the server can be run on e.g. a raspberryPi; in this case change the address in the communication.ini file to the Pi's address;

## dependencies
```
psycopg2
hashlib
requests
json
flask
configparser
getpass
pyperclip
random
cryptography
```

# banking backend app

## This application includes bank transaction apis.

### To run this application please follow the following steps

### Minimum requirements
1. Python 3.6+
2. PostgreSQL

### Clone Rapository

1. `git clone https://github.com/sattyapatil/banking_backend_app.git`
2. Then go to the main application folder `cd ./banking_backend_app`

### Installation

1. First create virtual env and activate it.
2. `sudo apt install python3-virtualenv`
3. `virtualenv -p python3 venv`
4. `source ./venv/bin/activate`
5. Install all required packages `pip3 install -r requirements.txt`
6. export APP_SETTINGS="config.DevelopmentConfig"
7. export DATABASE_URL="postgresql db url"

## Run application
1. Then run this command `python app.py`

## User Guide

1. After starting application go to the [http://127.0.0.1:5000](http://127.0.0.1:5000)
2. Application includes four endpoints
   1. "/" - GET - return all the transaction data
   2. "/transactions/`date`" - GET - returns all transaction for specific date
   3. "/balance/`date`" - GET - return the balance amount at the end of the day
   4. "/details/`id`" - GET - return transaction detail for transaction id
   5. "/add" - POST - save transaction data
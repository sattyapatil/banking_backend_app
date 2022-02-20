from datetime import datetime
from functools import wraps

from flask import jsonify
from cerberus import Validator


"""This file includes all supported function for the application"""


'''data validator'''
txn_schema = {
    'account_no': {'type': 'integer', 'required': True},
    'date': {'type': 'string', 'required': True, 'regex': '(?:[0-9]{2}-){2}[0-9]{2}'},
    'transaction_details': {'type': 'string', 'required': True},
    'value_date': {'type': 'string', 'required': True, 'regex': '(?:[0-9]{2}-){2}[0-9]{2}'},
    'withdrawal_amt': {'type': 'string', 'required': True},
    'deposit_amt': {'type': 'string', 'required': True},
    'balance_amt': {'type': 'string', 'required': True},
}

txn_schema_validator = Validator(txn_schema)


def date_parser(date):
    try:
        datetime_format = datetime.strptime(date, '%d-%m-%y')
        datetime_to_str = datetime_format.strftime('%d %b %y')
        date_in_proper_format = datetime_to_str.lstrip('0')
    except Exception as er:
        raise Exception('please enter proper date | {}'.format(er))
    return date_in_proper_format


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            return jsonify(code=400, massage=str(err))
    return wrapper


import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.inspection import inspect
from sqlalchemy import Column, String, UniqueConstraint

from config import *
from supported_functions import date_parser, error_handler, txn_schema_validator


'''create app instance'''
app = Flask(__name__)

'''SqlAlchemy Setup'''
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)


'''Database modals'''


class BankDetails(db.Model):

    __tablename__ = 'bank_details'

    txn_id = Column(db.Integer, primary_key=True, index=True)
    account_no = Column(db.BigInteger, nullable=False)
    date = Column(String(50), nullable=False)
    transaction_details = Column(String(250), nullable=False)
    value_date = Column(String(50))
    withdrawal_amt = Column(String(50))
    deposit_amt = Column(String(50))
    balance_amt = Column(String(50))
    __table_args__ = (UniqueConstraint('txn_id'),)

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}


'''Create all tables initially'''
db.create_all()


'''if data not present in db create initial data'''


def get_initial_txn_data_from_file():
    data_to_store = []
    with open('./data/details.json', 'r') as f:
        txn_details = json.load(f)
        f.close()
    for txn in txn_details:
        data = BankDetails(
            account_no=txn['Account No'],
            date=txn['Date'],
            transaction_details=txn['Transaction Details'],
            value_date=txn['Value Date'],
            withdrawal_amt=txn['Withdrawal AMT'],
            deposit_amt=txn['Deposit AMT'],
            balance_amt=txn['Balance AMT']
        )
        data_to_store.append(data)
    return data_to_store


if not BankDetails.query.get(1):
    txn_details = get_initial_txn_data_from_file()
    db.session.add_all(txn_details)
    db.session.commit()


'''routes'''


@app.route('/add', methods=['POST'])
def add():
    data = request.json
    is_data_valid = txn_schema_validator.validate(data)
    if not is_data_valid:
        return jsonify(message='Bad request | {}'.format(txn_schema_validator.errors), code=400)

    data_obj = BankDetails(
            account_no=data['account_no'],
            date=date_parser(data['date']),
            transaction_details=data['transaction_details'],
            value_date=date_parser(data['value_date']),
            withdrawal_amt=data['withdrawal_amt'],
            deposit_amt=data['deposit_amt'],
            balance_amt=data['balance_amt']
        )

    '''save transaction data'''
    db.session.add(data_obj)
    db.session.commit()

    return jsonify(message='success', code=200)


@app.route('/', methods=['GET'])
def home():
    bank_details = BankDetails.query.all()
    return jsonify([bank_detail.serialize() for bank_detail in bank_details])


@app.route('/transactions/<date>', methods=['GET'])
def transactions_by_date(date):
    date = date_parser(date)
    transaction_details = BankDetails.query.filter(BankDetails.date == date)
    if not transaction_details.first():
        return jsonify(message="No Data Found!", code=404)
    return jsonify(data=[transaction_detail.serialize() for transaction_detail in transaction_details], code=200,
                   message='success')


@app.route('/balance/<date>', methods=['GET'])
@error_handler
def remaining_balance_by_date(date):
    date = date_parser(date)
    balance_detail = BankDetails.query.filter(BankDetails.date == date).order_by(BankDetails.txn_id.desc()).first()
    if not balance_detail:
        return jsonify(message="No Data Found!", code=404)

    response_obj = {
        'account_no': balance_detail.account_no,
        'date': balance_detail.date,
        'balance_amt': balance_detail.balance_amt
    }
    return jsonify(data=response_obj, code=200, message="success")


@app.route('/details/<id>', methods=['GET'])
def get_txn_details(id):
    transaction_detail = BankDetails.query.get(id)
    if not transaction_detail:
        return jsonify(message="No Data Found!", code=404)
    return jsonify(data=transaction_detail.serialize(), code=200,
                   message='success')


'''error handling'''


@app.errorhandler(404)
def not_found(e):
    return jsonify(code=404, massage='URL not found | Please check entered url')


'''run application'''


if __name__ == "__main__":
    app.run(host='localhost', port=5000)


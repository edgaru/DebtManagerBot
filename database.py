from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["debt_manager"]


def add_debtor(debtor_name, owner):
    debtor = {"name": debtor_name, "owner": owner, "debts": []}
    db.debtors.insert_one(debtor)


def add_debt(owner, debtor_name, concept, amount, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    debt = {"concept": concept, "amount": amount, "date": date, "payments": []}
    db.debtors.update_one({"name": debtor_name, "owner": owner}, {"$push": {"debts": debt}})


def add_payment(owner, debtor_name, concept, payment_date, amount, note=None):
    payment = {"date": payment_date, "amount": amount}
    if note:
        payment["note"] = note

    db.debtors.update_one(
        {"name": debtor_name, "owner": owner, "debts.concept": concept},
        {"$push": {"debts.$.payments": payment}}
    )


def get_debtor_details(owner, debtor_name):
    return db.debtors.find_one({"name": debtor_name, "owner": owner})


def get_all_debtors(owner: str):
    debtors = db.debtors.find({"owner": owner})
    return list(debtors)


def get_debtor(owner: str, debtor_id: ObjectId) -> dict:
    debtor = db.debtors.find_one({"owner": owner, "_id": debtor_id})
    return debtor

import os
import csv
from tink_http_python.tink import Tink
from tink_http_python.transactions import Transactions
from storage.storage import TokenStorage
from cat.categories import get_category
from ui.ui import get_memo, should_add_to_existing, ask_category


def render_transaction(transaction):
    print("==========================")
    print(transaction.dates.value)
    print(transaction.descriptions.original)
    print(Transactions.calculate_real_amount(transaction.amount.value))
    print("==========================")

transactions = Tink(
    client_id=os.environ.get("TINK_CLIENT_ID"),
    client_secret=os.environ.get("TINK_CLIENT_SECRET"),
    storage=TokenStorage()
).transactions().get()


with open('output.csv', 'w') as f:
    writer = csv.writer(f,  delimiter=';')
    for transaction in transactions.transactions:
        category = get_category(transaction.descriptions.original)
        memo = ""
        if category is None:
            render_transaction(transaction)
            if should_add_to_existing():
                category = ask_category()
            else:
                memo = get_memo()
        writer.writerow((
            transaction.dates.value,
            0,
            transaction.descriptions.original,
            None,
            memo,
            Transactions.calculate_real_amount(transaction.amount.value),
            category,
            None
        ))

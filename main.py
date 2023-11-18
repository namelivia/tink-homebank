import os
import csv
from tink_http_python.tink import Tink
from tink_http_python.transactions import Transactions
from tink_http_python.exceptions import NoAuthorizationCodeException
from storage.storage import TokenStorage
from cat.categories import get_category, insert_item
from ui.ui import get_memo, should_add_to_existing, ask_category
from dotenv import load_dotenv
from notifications.notifications import Notifications

load_dotenv()

def render_transaction(transaction):
    print("==========================")
    print(transaction.dates.booked)
    print(transaction.descriptions.original)
    print(Transactions.calculate_real_amount(transaction.amount.value))
    print("==========================")

try:
    tink = Tink(
        client_id=os.environ.get("TINK_CLIENT_ID"),
        client_secret=os.environ.get("TINK_CLIENT_SECRET"),
        redirect_uri=os.environ.get("TINK_CALLBACK_URI"),
        storage=TokenStorage()
    )
    transactions = tink.transactions().get()
except NoAuthorizationCodeException:
    link = tink.get_authorization_code_link()
    Notifications.send(link)
    exit()


with open('output.csv', 'w') as f:
    writer = csv.writer(f,  delimiter=';')
    for transaction in transactions.transactions:
        category = get_category(transaction.descriptions.original)
        memo = ""
        if category is None:
            render_transaction(transaction)
            if should_add_to_existing():
                category = ask_category()
                insert_item(category, transaction.descriptions.original)
            else:
                memo = get_memo()
        writer.writerow((
            transaction.dates.booked,
            0,
            transaction.descriptions.original,
            None,
            memo,
            Transactions.calculate_real_amount(transaction.amount.value),
            category,
            None
        ))

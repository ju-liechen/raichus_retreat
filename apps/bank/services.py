from . import plaid

from .models import Account, Institution, Item, Transaction, TransactionCategory


def import_plaid_account(user, public_token):
    data = plaid.exchange_public_token(public_token)
    item = create_item(user, data['access_token'])
    create_accounts(item)
    import_transactions(item, initial=True)


def _get_or_create_category(tx):
    category_name = tx['personal_finance_category']['primary']

    # Format category
    bits = category_name.lower().split('_')
    formatted_name = ' '.join(bit.capitalize()
                              for bit in bits).replace('And', '&')

    category, _ = TransactionCategory.objects.get_or_create(
        name=formatted_name)
    return category


def create_institution(plaid_id):
    """
    Get or create an Institution object based on the given Plaid ID.

    """
    try:
        return Institution.objects.get(plaid_id=plaid_id)
    except Institution.DoesNotExist:
        data = plaid.get_institution(plaid_id)
        return Institution.objects.create(
            name=data['institution']['name'],
            plaid_id=plaid_id
        )


def create_item(user, access_token):
    """
    Create a new Item associated with the given access token and associate with user.

    Also creates an Institution object if necessary and links to Item. This needs to be done after
    item creation so we have the relevant institution id.

    """
    data = plaid.get_item(access_token)
    inst = create_institution(data['item']['institution_id'])
    item = Item.objects.create(
        user=user,
        institution=inst,
        plaid_id=data['item']['item_id'],
        access_token=access_token,
    )
    return item


def create_accounts(item):
    """
    Create accounts associated with a given Item.

    """
    data = plaid.get_accounts(item.access_token)
    accounts = []
    for acct in data['accounts']:
        acct = Account.objects.create(
            item=item,
            name=acct['name'],
            plaid_id=acct['account_id'],
        )
        accounts.append(acct)
    return accounts


def import_transactions(item, initial=False):
    """
    Import new transactions from Plaid using cursor and create them in the database.

    """
    added, modified, removed, cursor = plaid.sync_transactions(
        item.access_token,
        item.cursor,
        initial=initial
    )

    for a in added:
        create_transaction(a)

    for m in modified:
        update_transaction(m)

    for r in removed:
        remove_transaction(r)

    item.cursor = cursor
    item.save()
    return len(added), len(modified), len(removed)


def create_transaction(data):
    """
    Create an individual transaction associated with an account.

    """
    account = Account.objects.get(plaid_id=data['account_id'])
    return Transaction.objects.get_or_create(
        plaid_id=data['transaction_id'],
        defaults=dict(
            account=account,
            category=_get_or_create_category(data),
            name=data.get('merchant_name') or data['name'],
            # Plaid returns positive numbers for debits
            amount=data['amount'] * -1,
            date=data.get('authorized_date') or data['date'],
            pending=data['pending'],
        )
    )


def update_transaction(data):
    """
    Update an individual transaction by its plaid id.

    """
    t = Transaction.objects.get(plaid_id=data['transaction_id'])
    t.name = data['name']
    t.amount = data['amount']
    t.date = data['date']
    t.pending = data['pending']
    t.save()
    return t


def remove_transaction(data):
    """
    Remove an individual transaction by its plaid id.

    """
    return Transaction.objects.get(plaid_id=data['transaction_id']).delete()

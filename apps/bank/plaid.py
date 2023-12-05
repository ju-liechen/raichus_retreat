import logging
import time

import plaid
from plaid.api import plaid_api
from plaid.exceptions import ApiException
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.country_code import CountryCode
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_sync_request_options import TransactionsSyncRequestOptions

from django.conf import settings


log = logging.getLogger(__name__)
host = plaid.Environment.Sandbox

if settings.ENV == settings.STAGING:
    host = plaid.Environment.Development

elif settings.ENV == settings.PRODUCTION:
    host = plaid.Environment.PRODUCTION

configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': settings.PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


def get_link_token(user_id):
    request = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(
            client_user_id=str(user_id),
        ),
        client_name=settings.PLAID_CLIENT_NAME,
        products=[Products(i) for i in settings.PLAID_PRODUCTS],
        country_codes=[CountryCode(i) for i in settings.PLAID_COUNTRY_CODES],
        language=settings.PLAID_LANG,
    )

    response = client.link_token_create(request)
    return response['link_token']


def exchange_public_token(public_token):
    """
    Returns:
        {
            "access_token": "...",
            "item_id": "...",
            "request_id": "...",
        }
    """
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    return client.item_public_token_exchange(request)


def get_institution(inst_id):
    request = InstitutionsGetByIdRequest(
        institution_id=inst_id,
        country_codes=[CountryCode(i) for i in settings.PLAID_COUNTRY_CODES],
    )
    return client.institutions_get_by_id(request)


def get_item(access_token):
    request = ItemGetRequest(access_token=access_token)
    return client.item_get(request)


def get_accounts(access_token):
    request = AccountsGetRequest(access_token=access_token)
    return client.accounts_get(request)


def sync_transactions(access_token, cursor, initial=False):
    count = 0
    retry = 0
    added = []
    modified = []
    removed = []
    has_more = True
    options = TransactionsSyncRequestOptions(
        include_personal_finance_category=True
    )

    try:
        while has_more:
            count += 1

            # Passing in an empty cursor sometimes causes issues
            if count == 1:
                request = TransactionsSyncRequest(
                    access_token=access_token, options=options)
            else:
                request = TransactionsSyncRequest(
                    access_token=access_token,
                    cursor=cursor or None,
                    options=options,
                )

            response = client.transactions_sync(request)

            added.extend(response['added'])
            modified.extend(response['modified'])
            removed.extend(response['removed'])
            has_more = response['has_more']
            cursor = response['next_cursor']
    except ApiException as e:
        log.error(e)
        retry += 1
        if retry <= 3:
            return sync_transactions(access_token, cursor='', initial=initial)
        log.debug('Plaid sync failed, too many retries.')

    # If this is our initial import and we don't have any transactions yet
    # Wait and try again, sometimes Plaid has a delay
    if initial and len(added) == 0 and retry <= 3:
        log.debug('Retrying initial sync in 10 seconds...')
        time.sleep(10)
        return sync_transactions(access_token, cursor='', initial=initial)

    log.debug(
        f'Plaid sync: {len(added)} added, {len(modified)} modified, {len(removed)} removed ')
    return (added, modified, removed, cursor)

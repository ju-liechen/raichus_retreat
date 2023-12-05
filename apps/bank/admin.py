from django.contrib import admin
from .models import (
    Account,
    Institution,
    Item,
    TransactionCategory,
    Transaction,
)

admin.site.register(Account)
admin.site.register(Institution)
admin.site.register(Item)
admin.site.register(TransactionCategory)
admin.site.register(Transaction)

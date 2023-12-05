from django.db import models
from django.contrib.auth import get_user_model


class Institution(models.Model):
    name = models.CharField(max_length=255)
    plaid_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    cursor = models.CharField(max_length=255, blank=True)
    plaid_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.plaid_id


class Account(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False, db_index=True)
    plaid_id = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TransactionCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(
        TransactionCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    pending = models.BooleanField(default=False)
    plaid_id = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return self.name

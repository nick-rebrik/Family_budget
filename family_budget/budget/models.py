from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BudgetsList(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='budgets_lists'
    )

    class Meta:
        verbose_name = 'List of budgets'
        verbose_name_plural = 'Lists of budgets'

    def __str__(self):
        return f"{str(self.user).title()}'s list of budgets"


class Category(models.Model):
    title = models.CharField(
        max_length=50
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Budget(models.Model):
    class Currency:
        USD = 'USD'
        EURO = 'Euro'
        PLN = 'zl'

        choises = [
            (USD, 'USD'),
            (EURO, 'Euro'),
            (PLN, 'PLN')
        ]

    title = models.CharField(max_length=100)
    currency = models.CharField(
        max_length=25,
        choices=Currency.choises
    )
    initial_balance = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    balance = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        editable=False,
        blank=True
    )
    create_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    budget_list = models.ForeignKey(
        BudgetsList,
        on_delete=models.CASCADE,
        related_name='budgets'
    )

    class Meta:
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def save(self, *args, **kwargs):
        if not self.balance:
            self.balance = self.initial_balance
        super(Budget, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class BudgetOperation(models.Model):
    class OperationType:
        INCOME = 'Income'
        EXPENSE = 'Expense'

        choises = [
            (INCOME, 'Income'),
            (EXPENSE, 'Expense')
        ]

    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name='budget_operations'
    )
    operation_type = models.CharField(
        max_length=25,
        choices=OperationType.choises
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2
    )
    note = models.TextField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Budget operation'
        verbose_name_plural = 'Budget operations'

    def update_balance(self):
        operation = BudgetOperation.objects.get(pk=self.pk)
        if operation.operation_type == 'Expense':
            self.budget.balance += operation.amount
        else:
            self.budget.balance -= operation.amount
        self.budget.save()

    def save(self, *args, **kwargs):
        if BudgetOperation.objects.filter(pk=self.pk).exists():
            self.update_balance()
        if self.operation_type == 'Expense':
            self.budget.balance -= self.amount
        else:
            self.budget.balance += self.amount
        self.budget.save()
        super(BudgetOperation, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.operation_type == 'Expense':
            self.budget.balance += self.amount
        else:
            self.budget.balance -= self.amount
        self.budget.save()
        super(BudgetOperation, self).delete()

    def __str__(self):
        return (f'{self.operation_type}. {self.category} '
                f'- {self.amount} {self.budget.currency}')

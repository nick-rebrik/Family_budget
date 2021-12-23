from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BudgetsList(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='budgets_lists'
    )

    class Meta:
        verbose_name = 'List of budgets'
        verbose_name_plural = 'Lists of budgets'
        ordering = ('id',)

    def __str__(self):
        return f"{str(self.owner).title()}'s {self.title} list of budgets"


class Category(models.Model):
    title = models.CharField(
        max_length=50
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('id',)

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
    owner = models.ForeignKey(
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
        ordering = ('create_date',)

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
        related_name='budget_operations',
        null=True
    )
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2
    )
    note = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='budget_operations'
    )
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Budget operation'
        verbose_name_plural = 'Budget operations'
        ordering = ('date',)

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


class SharePermission(models.Model):
    budgets_list = models.ForeignKey(
        BudgetsList,
        on_delete=models.CASCADE,
        related_name='shared_permissions'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='permits_granted'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='permits_obtained'
    )

    class Meta:
        verbose_name = 'Shared permission'
        verbose_name_plural = 'Shared permissions'
        ordering = ('id',)

    def __str__(self):
        return f'{self.budgets_list} shared to {self.user}'

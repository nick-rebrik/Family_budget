from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from budget.models import (Budget, BudgetOperation, BudgetsList,
                           Category, SharePermission)

User = get_user_model()


class BudgetsListModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username='TestUser')
        cls.budgets_list = BudgetsList.objects.create(
            title='Testing',
            owner=user,
        )

    def test_str_method(self):
        budgets_list = self.budgets_list
        model_str = (f"{str(self.budgets_list.owner).title()}'s "
                     f"{self.budgets_list.title} list of budgets")
        self.assertEqual(model_str, str(budgets_list))


class CategoryModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(title='Testing')

    def test_str_method(self):
        category = self.category
        self.assertEqual(category.title, str(category))


class BudgetModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username='TestUser')
        cls.budgets_list = BudgetsList.objects.create(
            title='Testing',
            owner=user,
        )
        cls.budget = Budget.objects.create(
            title='Main',
            currency=Budget.Currency.USD,
            owner=user,
            budget_list=cls.budgets_list
        )

    def test_str_method(self):
        budget = self.budget
        self.assertEqual(budget.title, str(budget))


class BudgetOperationModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.budgets_list = BudgetsList.objects.create(
            title='Testing',
            owner=cls.user,
        )
        cls.category = Category.objects.create(title='Test category')
        cls.budget = Budget.objects.create(
            title='Main',
            currency=Budget.Currency.USD,
            initial_balance=Decimal('5000.00'),
            owner=cls.user,
            budget_list=cls.budgets_list
        )

    def create_operation(self, operation_type, amount):
        operation_types = {
            'income': BudgetOperation.OperationType.INCOME,
            'expense': BudgetOperation.OperationType.EXPENSE
        }
        operation = BudgetOperation.objects.create(
            budget=self.budget,
            operation_type=operation_types[operation_type],
            category=self.category,
            amount=Decimal(amount),
            note=f'{operation_type} operation for test',
            user=self.user
        )
        return operation

    def test_str_method(self):
        operation = self.create_operation(
            operation_type='income', amount='1000.00'
        )
        model_str = (f'{operation.operation_type}. {operation.category} '
                     f'- {operation.amount} {operation.budget.currency}')
        self.assertEqual(model_str, str(operation))

    def test_income_operation(self):
        balance_before = self.budget.balance
        income_operation = self.create_operation(
            operation_type='income', amount='1000.00'
        )
        balance_after = balance_before + income_operation.amount
        self.assertEqual(balance_after, self.budget.balance)

    def test_expense_operation(self):
        balance_before = self.budget.balance
        expense_operation = self.create_operation(
            operation_type='expense', amount='1000.00'
        )
        balance_after = balance_before - expense_operation.amount
        self.assertEqual(balance_after, self.budget.balance)

    def test_delete_income_operation(self):
        balance_before = self.budget.balance
        income_operation = self.create_operation(
            operation_type='income', amount='1000.00'
        )
        income_operation.delete()
        self.assertEqual(balance_before, self.budget.balance)

    def test_delete_expense_operation(self):
        balance_before = self.budget.balance
        expense_operation = self.create_operation(
            operation_type='expense', amount='1000.00'
        )
        expense_operation.delete()
        self.assertEqual(balance_before, self.budget.balance)

    def test_update_income_operation(self):
        balance_before = self.budget.balance
        income_operation = self.create_operation(
            operation_type='income', amount='1000.00'
        )
        income_operation.amount = Decimal('5000.00')
        income_operation.save()
        balance_after = balance_before + income_operation.amount
        self.assertEqual(balance_after, self.budget.balance)

    def test_update_expense_operation(self):
        balance_before = self.budget.balance
        expense_operation = self.create_operation(
            operation_type='expense', amount='1000.00'
        )
        expense_operation.amount = Decimal('2000.00')
        expense_operation.save()
        balance_after = balance_before - expense_operation.amount
        self.assertEqual(balance_after, self.budget.balance)


class SharePermissionModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        owner = User.objects.create_user(username='TestOwner')
        user = User.objects.create_user(username='TestUser')
        cls.budgets_list = BudgetsList.objects.create(
            title='Testing',
            owner=owner,
        )
        cls.budget = Budget.objects.create(
            title='Main',
            currency=Budget.Currency.USD,
            owner=owner,
            budget_list=cls.budgets_list
        )
        cls.shared_permission = SharePermission.objects.create(
            budgets_list=cls.budgets_list,
            owner=owner,
            user=user
        )

    def test_str_method(self):
        shared_permission = self.shared_permission
        model_str = (f'{shared_permission.budgets_list} shared to '
                     f'{shared_permission.user}')
        self.assertEqual(model_str, str(shared_permission))

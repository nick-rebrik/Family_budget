from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from budget.models import (Budget, BudgetOperation, BudgetsList,
                           Category, SharePermission)

User = get_user_model()


class BudgetsListViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user_token = Token.objects.create(user=self.user)
        self.token = f'Token {self.user_token.key}'

    def test_budgets_list_create(self):
        objects_count = BudgetsList.objects.count()
        data = {
            'title': 'Test list',
            'owner': self.user.username
        }
        self.authorized_client.post(
            reverse('budget:budgets_lists-list'),
            data=data,
            follow=True,
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(BudgetsList.objects.count(), objects_count + 1)
        last_object = BudgetsList.objects.last()
        self.assertEqual(last_object.title, data['title'])


class CategoryViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user_token = Token.objects.create(user=self.user)
        self.token = f'Token {self.user_token.key}'

    def test_category_create(self):
        objects_count = Category.objects.count()
        data = {
            'title': 'Test category',
        }
        self.authorized_client.post(
            reverse('budget:categories-list'),
            data=data,
            follow=True,
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(Category.objects.count(), objects_count + 1)
        last_object = Category.objects.last()
        self.assertEqual(last_object.title, data['title'])


class BudgetViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.budgets_list = BudgetsList.objects.create(
            title='Testing',
            owner=cls.user,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user_token = Token.objects.create(user=self.user)
        self.token = f'Token {self.user_token.key}'

    def test_budget_create(self):
        objects_count = Budget.objects.count()
        data = {
            'title': 'Test budget',
            'currency': 'USD'
        }
        self.authorized_client.post(
            reverse(
                'budget:budgets-list',
                kwargs={
                    'list_id': self.budgets_list.id,
                }
            ),
            data=data,
            follow=True,
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(Budget.objects.count(), objects_count + 1)
        last_object = Budget.objects.last()
        self.assertEqual(last_object.title, data['title'])
        self.assertEqual(last_object.currency, data['currency'])


class BudgetOperationViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.budgets_list = BudgetsList.objects.create(
            title='Testing',
            owner=cls.user,
        )
        cls.category = Category.objects.create(title='Testing')
        cls.budget = Budget.objects.create(
            title='Main',
            currency=Budget.Currency.USD,
            owner=cls.user,
            budget_list=cls.budgets_list
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user_token = Token.objects.create(user=self.user)
        self.token = f'Token {self.user_token.key}'

    def test_budget_operation_create(self):
        objects_count = BudgetOperation.objects.count()
        data = {
            'operation_type': 'Income',
            'category': self.category.title,
            'amount': '1000.00'
        }
        self.authorized_client.post(
            reverse(
                'budget:budget_operation-list',
                kwargs={
                    'list_id': self.budgets_list.id,
                    'budget_id': self.budget.id
                }
            ),
            data=data,
            follow=True,
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(BudgetOperation.objects.count(), objects_count + 1)
        last_object = BudgetOperation.objects.last()
        self.assertEqual(last_object.operation_type, data['operation_type'])
        self.assertEqual(last_object.category.title, data['category'])
        self.assertEqual(last_object.amount, Decimal(data['amount']))


class SharePermissionViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = User.objects.create_user(username='TestOwner')
        cls.user = User.objects.create_user(username='TestUser')
        cls.budgets_list = BudgetsList.objects.create(
            title='Testing',
            owner=cls.owner,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.owner)
        self.user_token = Token.objects.create(user=self.owner)
        self.token = f'Token {self.user_token.key}'
        self.second_authorized_client = Client()
        self.second_authorized_client.force_login(self.user)
        self.second_user_token = Token.objects.create(user=self.user)
        self.second_token = f'Token {self.second_user_token.key}'

    def test_share_permission_create(self):
        objects_count = SharePermission.objects.count()
        data = {
            'user': self.user.username
        }
        self.authorized_client.post(
            reverse(
                'budget:share_list-list',
                kwargs={'list_id': self.budgets_list.id}
            ),
            data=data,
            follow=True,
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(SharePermission.objects.count(), objects_count + 1)
        last_object = SharePermission.objects.last()
        self.assertEqual(last_object.user.username, data['user'])

    def test_budgets_list_access_received(self):
        budgets_lists_before = self.second_authorized_client.get(
            reverse('budget:budgets_lists-list'),
            HTTP_AUTHORIZATION=self.second_token
        ).json()

        data = {
            'user': self.user.username
        }
        self.authorized_client.post(
            reverse(
                'budget:share_list-list',
                kwargs={'list_id': self.budgets_list.id}
            ),
            data=data,
            follow=True,
            HTTP_AUTHORIZATION=self.token
        )

        budgets_lists_after = self.second_authorized_client.get(
            reverse('budget:budgets_lists-list'),
            HTTP_AUTHORIZATION=self.second_token
        ).json()
        self.assertNotEqual(budgets_lists_before, budgets_lists_after)
        self.assertEqual(
            self.budgets_list.id, budgets_lists_after['results'][0]['id']
        )




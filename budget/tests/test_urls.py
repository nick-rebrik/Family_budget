from decimal import Decimal
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from budget.models import (Budget, BudgetOperation, BudgetsList,
                           Category, SharePermission)

User = get_user_model()


class AllURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.second_user = User.objects.create_user(username='TestUser2')
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
        cls.budget_operation = BudgetOperation.objects.create(
            budget=cls.budget,
            operation_type=BudgetOperation.OperationType.INCOME,
            category=cls.category,
            amount=Decimal('1000.00'),
            note='Income operation for test',
            user=cls.user
        )
        cls.shared_permission = SharePermission.objects.create(
            budgets_list=cls.budgets_list,
            owner=cls.user,
            user=cls.second_user
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user_token = Token.objects.create(user=self.user)
        self.token = f'Token {self.user_token.key}'

        self.urls = {
            'budget_lists-list': reverse(
                'budget:budgets-list',
                kwargs={
                    'list_id': self.budgets_list.id,
                }
            ),
            'budget_lists-detail': reverse(
                'budget:budgets-detail',
                kwargs={
                    'list_id': self.budgets_list.id,
                    'pk': self.budget.pk
                }
            ),
            'categories-list': reverse('budget:categories-list'),
            'categories-detail': reverse(
                'budget:categories-detail',
                kwargs={'pk': self.category.pk}
            ),
            'budgets-list': reverse(
                'budget:budgets-list',
                kwargs={
                    'list_id': self.budgets_list.id,
                }
            ),
            'budgets-detail': reverse(
                'budget:budgets-detail',
                kwargs={
                    'list_id': self.budgets_list.id,
                    'pk': self.budget.pk
                }
            ),
            'budget_operation-list': reverse(
                'budget:budget_operation-list',
                kwargs={
                    'list_id': self.budgets_list.id,
                    'budget_id': self.budget.id
                }
            ),
            'budget_operation-detail': reverse(
                'budget:budget_operation-detail',
                kwargs={
                    'list_id': self.budgets_list.id,
                    'budget_id': self.budget.id,
                    'pk': self.budget_operation.pk
                }
            ),
            'share_list-list': reverse(
                'budget:share_list-list',
                kwargs={'list_id': self.budgets_list.id}
            ),
            'share_list-detail': reverse(
                'budget:share_list-detail',
                kwargs={
                    'list_id': self.budgets_list.id,
                    'pk': self.shared_permission.pk
                }
            ),
        }

    def test_urls_status_authorized(self):
        for url in self.urls.values():
            with self.subTest(url=url):
                response = self.authorized_client.get(
                    url, HTTP_AUTHORIZATION=self.token
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_status_unauthorized(self):
        for url in self.urls.values():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .filters import OperationFilter
from .models import (Budget, BudgetOperation, BudgetsList, Category,
                     SharePermission)
from .permissions import AdmittedOrOwner, OnlyOwnerDelete
from .serializers import (BudgetCreateSerializer, BudgetOperationSerializer,
                          BudgetSerializer, BudgetsListSerializer,
                          CategorySerializer, ShareSerializer,
                          ShortBudgetSerializer)


class BudgetsListViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetsListSerializer
    permission_classes = (OnlyOwnerDelete,)

    def get_queryset(self):
        user = self.request.user
        all_lists = BudgetsList.objects.filter(
            Q(owner=user.id) | Q(shared_permissions__user=user.id)
        ).distinct()
        return all_lists

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)


class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerDelete, AdmittedOrOwner)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BudgetsList.objects.none()

        budgets_list = get_object_or_404(
            BudgetsList, id=self.kwargs['list_id']
        )
        return budgets_list.budgets.all()

    def perform_create(self, serializer):
        user = self.request.user
        budget_list = get_object_or_404(
            BudgetsList, id=self.kwargs['list_id']
        )
        serializer.save(owner=user, budget_list=budget_list)

    def get_serializer_class(self):
        if self.action == 'create':
            return BudgetCreateSerializer
        elif self.action == 'list':
            return ShortBudgetSerializer
        return BudgetSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class BudgetOperationViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetOperationSerializer
    permission_classes = (AdmittedOrOwner,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OperationFilter

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BudgetOperation.objects.none()

        budget = get_object_or_404(Budget, id=self.kwargs['budget_id'])
        return budget.budget_operations.all()

    def perform_create(self, serializer):
        budget = get_object_or_404(Budget, id=self.kwargs['budget_id'])
        serializer.save(user=self.request.user, budget=budget)


class ShareViewSet(viewsets.ModelViewSet):
    serializer_class = ShareSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return SharePermission.objects.none()

        budgets_list = get_object_or_404(
            BudgetsList, id=self.kwargs['list_id']
        )
        return budgets_list.shared_permissions.all()

    def perform_create(self, serializer):
        budgets_list = get_object_or_404(
            BudgetsList, id=self.kwargs['list_id']
        )
        serializer.save(owner=self.request.user, budgets_list=budgets_list)

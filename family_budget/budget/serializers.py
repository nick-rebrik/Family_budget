from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (Budget, BudgetOperation, BudgetsList, Category,
                     SharePermission)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title')


class BudgetOperationSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Category.objects.all()
    )

    class Meta:
        model = BudgetOperation
        fields = (
            'id',
            'operation_type',
            'category',
            'amount',
            'note',
            'user',
            'date'
        )


class BudgetCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ('id', 'title', 'currency', 'initial_balance')


class ShortBudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = (
            'id',
            'title',
            'balance',
            'currency',
            'create_date'
        )


class BudgetSerializer(serializers.ModelSerializer):
    budget_operations = BudgetOperationSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = (
            'id',
            'title',
            'balance',
            'currency',
            'budget_operations',
        )


class BudgetsListSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    budgets = ShortBudgetSerializer(many=True, read_only=True)

    class Meta:
        model = BudgetsList
        fields = ('id', 'title', 'owner', 'budgets')


class ShareSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = SharePermission
        fields = ('id', 'user',)

    def validate(self, attrs):
        if self.context['request'].method != 'POST':
            return attrs
        if self.context['request'].user == attrs['user']:
            raise ValidationError('You cannot share access to yourself')
        return attrs

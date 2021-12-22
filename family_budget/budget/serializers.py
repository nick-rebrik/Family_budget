from rest_framework import serializers

from .models import BudgetsList, Budget, Category, BudgetOperation


class BudgetOperationSerializer(serializers.ModelSerializer):
    budget = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BudgetOperation
        fields = '__all__'


class BudgetCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ('title', 'currency', 'initial_balance')


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
            'create_date',
        )


class BudgetsListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    budgets = BudgetSerializer(many=True, read_only=True)

    class Meta:
        model = BudgetsList
        fields = ('id', 'title', 'user', 'budgets')

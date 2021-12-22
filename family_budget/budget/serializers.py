from rest_framework import serializers

from .models import Budget, BudgetOperation, BudgetsList, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title',)


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
            'date'
        )


class BudgetCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ('title', 'currency', 'initial_balance')


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
    user = serializers.CharField(source='user.username', read_only=True)
    budgets = ShortBudgetSerializer(many=True, read_only=True)

    class Meta:
        model = BudgetsList
        fields = ('id', 'title', 'user', 'budgets')

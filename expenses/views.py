from expenses import utils

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
import json
from .models import Budget, Expense
from .forms import BudgetForm, ExpenseForm


@login_required
def charts(request):
    template = "charts.html"
    
    expenses = Expense.objects.filter(owner=request.user)
    budget = Expense.objects.getBudget(request.user)
    statistics = Expense.objects.getStatistics(request.user)

    context = {"expenses": expenses, "budget": budget, "statistics": statistics}
    return render(request, template, context)


@login_required
def homepage(request):
    Expense.objects.addTestuserExpenses(request)

    template = "homepage.html"
    userExpenses = Expense.objects.filter(owner=request.user).order_by("-date")

    totalExpenseAmount = Expense.objects.getTotalExpenses(owner=request.user)
    budget = Expense.objects.getBudget(owner=request.user)

    page = request.GET.get("page", 1)
    paginator = Paginator(userExpenses, 15)

    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        expenses = paginator.page(1)
    except EmptyPage:
        expenses = paginator.page(paginator.num_pages)

    pagination_range_down = expenses.number - 5
    pagination_range_up = expenses.number + 5

    context = {
        "expenses": expenses,
        "totalExpenseAmount": totalExpenseAmount,
        "budget": budget,
        "num_expenses": len(userExpenses),
        "num_pages": paginator.num_pages,
        "pagination_range_down": pagination_range_down,
        "pagination_range_up": pagination_range_up,
    }

    if budget:
        currentMonthExpenses = Expense.objects.getMonthlyExpenseSum(
            owner=request.user
        )
        expenses_vs_budget_percentage_diff = (
            (currentMonthExpenses / budget * 100) if budget else 0
        )
        amount_over_budget = currentMonthExpenses - budget

        context["currentMonthExpenses"] = currentMonthExpenses
        context[
            "expenses_vs_budget_percentage_diff"
        ] = expenses_vs_budget_percentage_diff
        context["amount_over_budget"] = amount_over_budget

    return render(request, template, context)


@login_required
def updateExpense(request, pk):
    template = "updateExpense.html"
    expense = get_object_or_404(Expense, pk=pk)

    if request.method != "POST":
        form = ExpenseForm(instance=expense)

    else:
        form = ExpenseForm(instance=expense, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("expenses:home")

    context = locals()
    return render(request, template, context)


@login_required
def createExpense(request):
    template = "createExpense.html"

    if request.method != "POST":
        # No data submitted; create a blank form.
        form = ExpenseForm()
    else:
        # POST data submitted; process data.
        form = ExpenseForm(request.POST)
        if form.is_valid():
            newExpense = form.save(commit=False)
            newExpense.owner = request.user
            newExpense.save()
            return redirect("expenses:home")

    context = locals()
    return render(request, template, context)


@login_required
def viewExpense(request, pk):
    template = "viewExpense.html"
    expense = get_object_or_404(Expense, pk=pk)
    context = locals()

    return render(request, template, context)


@login_required
def deleteExpense(request, pk):
    template = "deleteExpense.html"
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":
        expense.delete()
        return redirect("expenses:home")

    return render(request, template, {})


@login_required
def updateBudget(request):
    template = "updateBudget.html"
    budget = get_object_or_404(Budget, owner=request.user)

    if request.method != "POST":
        form = BudgetForm(instance=budget)

    else:
        form = BudgetForm(instance=budget, data=request.POST)
        if form.is_valid():
            updated_budget = form.save(commit=False)
            updated_budget.owner = request.user
            updated_budget.save()
            return redirect("expenses:home")

    context = locals()
    return render(request, template, context)


@login_required
def createBudget(request):
    template = "createBudget.html"

    if request.method != "POST":
        # No data submitted; create a blank form.
        form = BudgetForm()
    else:
        # POST data submitted; process data.
        form = BudgetForm(request.POST)
        if form.is_valid():
            new_budget = form.save(commit=False)
            new_budget.owner = request.user
            new_budget.save()
            return redirect("expenses:home")

    context = locals()
    return render(request, template, context)




@login_required
def deleteBudget(request):
    template = "deleteBudget.html"
    budget = get_object_or_404(Budget, owner=request.user)

    if request.method == "POST":
        budget.delete()
        return redirect("expenses:home")

    return render(request, template, {})


@login_required
def line_chart_data(request):
    userExpenses = Expense.objects.filter(owner=request.user)

    page = request.GET.get("page", 1)
    paginator = Paginator(userExpenses, 15)

    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        expenses = paginator.page(1)
    except EmptyPage:
        expenses = paginator.page(paginator.num_pages)

    dates = [exp.date for exp in expenses]
    dates = [utils.reformat_date(date, "%d' %b") for date in dates]
    dates.reverse()

    amounts = [round(float(exp.amount), 2) for exp in expenses]
    amounts.reverse()

    chart_data = {}

    for i in range(len(dates)):
        if dates[i] not in chart_data:
            chart_data[dates[i]] = amounts[i]
        else:
            chart_data[dates[i]] += amounts[i]
    return JsonResponse(chart_data)



@login_required
def view_404(request, exception):
    template = "errors/404.html"
    return render(request, template, {})


@login_required
def view_500(request):
    template = "errors/500.html"
    return render(request, template, {})




@login_required
def total_expenses_pie_chart_data(request):
    userExpenses = Expense.objects.filter(owner=request.user)

    chart_data = {}
    for exp in userExpenses:
        if exp.category not in chart_data:
            chart_data[exp.category] = float(exp.amount)
        else:
            chart_data[exp.category] += float(exp.amount)

    for category, amount in chart_data.items():
        chart_data[category] = round(amount, 2)
    return JsonResponse(chart_data)


@login_required
def expenses_by_week_bar_chart_data(request):
    weeks = ["current week", "last week", "2 weeks ago", "3 weeks ago"]
    weeks.reverse()

    expenses = [
        Expense.objects.getWeeklyExpenseSum(request.user),
        Expense.objects.getWeeklyExpenseSum(request.user, -1),
        Expense.objects.getWeeklyExpenseSum(request.user, -2),
        Expense.objects.getWeeklyExpenseSum(request.user, -3),
    ]
    expenses.reverse()

    chart_data = {}
    for i, week in enumerate(weeks):
        chart_data[week] = expenses[i]
    return JsonResponse(chart_data)


@login_required
def monthly_expenses_pie_chart_data(request):
    userExpenses = Expense.objects.filter(owner=request.user)

    month_num = utils.get_month_num()
    monthly_expenses = userExpenses.filter(date__month=month_num)

    chart_data = {}
    for exp in monthly_expenses:
        if exp.category not in chart_data:
            chart_data[exp.category] = float(exp.amount)
        else:
            chart_data[exp.category] += float(exp.amount)

    for category, amount in chart_data.items():
        chart_data[category] = round(amount, 2)
    return JsonResponse(chart_data)


@login_required
def expenses_by_month_bar_chart_data(request):
    userExpenses = Expense.objects.filter(owner=request.user)
    current_year = utils.get_year_num()
    last_year = current_year - 1

    last_year_month_expenses = utils.get_yearly_month_expense_data(
        last_year, userExpenses
    )
    current_year_month_expenses = utils.get_yearly_month_expense_data(
        current_year, userExpenses
    )
    chart_data = {**last_year_month_expenses, **current_year_month_expenses}
    return JsonResponse(chart_data)


@login_required
def delete_testuser_data(request):
    """Function to remove all data from testusers that can be access via url by tests."""
    user = str(request.user)

    if user == "testuser1" or user == "testuser3":
        Expense.objects.deleteTestuserExpenses(request)
        Expense.objects.deleteTestuserBudget(request)

        testusers_to_delete = User.objects.exclude(username="testuser1").exclude(
            username="testuser3"
        )
        testusers_to_delete.delete()

        return redirect("expenses:home")
    else:
        print(
            "Not allowed to delete the expenses or budget of any user other than testuser1 and testuser3"
        )
        return redirect("expenses:home")


@login_required
def addTestuserData(request):
    user = str(request.user)
    if user == "testuser1" or user == "testuser3":
        req_post_dict = dict(request.POST)
        expenses_str_dict = req_post_dict["expenses"][0]
        expenses = json.loads(expenses_str_dict)

        Expense.objects.createTestExpenses(request.user, expenses)
        return redirect("expenses:home")



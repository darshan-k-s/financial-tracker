from expenses import views
from django.urls import path

app_name = "expenses"

urlpatterns = [
    path("", views.homepage, name="home"),
    path("create/", views.createExpense, name="create"),
    path("charts/", views.charts, name="charts"),
    path("delete/<int:pk>/", views.deleteExpense, name="delete"),
    path("update/<int:pk>/", views.updateExpense, name="update"),
    path("line-chart-data/", views.line_chart_data, name="line_chart_data"),
    path("update-budget/", views.updateBudget, name="updateBudget"),
    path("create-budget/", views.createBudget, name="createBudget"),
    path("delete-budget/", views.deleteBudget, name="deleteBudget"),
    path(
        "expenses-by-month-bar-chart-data/",
        views.expenses_by_month_bar_chart_data,
        name="expenses_by_month_bar_chart_data",
    ),
    path(
        "total-expenses-pie-chart-data/",
        views.total_expenses_pie_chart_data,
        name="total_expenses_pie_chart_data",
    ),
    path(
        "monthly-expenses-pie-chart-data/",
        views.monthly_expenses_pie_chart_data,
        name="monthly_expenses_pie_chart_data",
    ),
    path("add-testuser-data/", views.addTestuserData, name="addTestuserData"),
    path(
        "delete-testuser-data/", views.delete_testuser_data, name="delete_testuser_data"
    ),
    path(
        "expenses-by-week-bar-chart-data/",
        views.expenses_by_week_bar_chart_data,
        name="expenses_by_week_bar_chart_data",
    ),
    
]

from django.db.models import Sum
from datetime import date, datetime, timedelta
import json
from dateutil.relativedelta import relativedelta

def get_data_from_json(file):
    with open(file) as f:
        data = json.load(f)
    return data

def get_percentage_diff(a, b):
    if a == 0 or b == 0:
        return 0
    return safely_round(((a / b) * 100), 2)

def safely_round(val, decimals=2):
    try:
        return round(val, decimals)
    except Exception:
        return 0

def get_month_num(month_timedelta_num=0):
    """
    Passing month_timedelta_num will add or substract to current month,
    so month_timedelta_num=0(current month), month_timedelta_num=1(next month),
    month_timedelta_num=-1(last month), and so on.
    """
    return (date.today() + relativedelta(months=int(month_timedelta_num))).month

def get_week_iso_num(week_timedelta_num=0):
    """
    Passing week_timedelta_num will add or substract to current week,
    so week_timedelta_num=0(current week), week_timedelta_num=1(next week),
    week_timedelta_num=-1(last week), and so on.
    """
    return (date.today() + timedelta(days=(7 * int(week_timedelta_num)))).isocalendar()[
        1
    ]


def reformat_date(date, format):
    return date.strftime(format)

def get_year_num():
    return date.today().year


def get_first_and_last_day_of_current_month():
    today = datetime.now()
    first_day_of_current_month = today.replace(day=1)

    next_month_date = today + relativedelta(months=+1)
    next_month_first_day_date = next_month_date.replace(day=1)

    last_day_of_the_current_month = next_month_first_day_date - timedelta(days=1)

    return {
        "first_day": first_day_of_current_month,
        "last_day": last_day_of_the_current_month,
    }

def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

def get_months_list():
    return [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]



def get_yearly_month_expense_data(year, userExpenses):
    yearly_month_expense_data = {}
    months = get_months_list()
    year = int(year)
    year_expenses = userExpenses.filter(date__year=year)

    if year_expenses:
        year_suffix = f" '{str(year)[2:]}"
        for month in months:
            month_num = months.index(month) + 1
            monthly_expenses = year_expenses.filter(date__month=month_num)

            if monthly_expenses:
                monthly_expenses_sum = round(
                    monthly_expenses.aggregate(amount=Sum("amount"))["amount"], 2
                )
                yearly_month_expense_data[month + year_suffix] = monthly_expenses_sum
    return yearly_month_expense_data


class DateGenerator:

    @staticmethod
    def get_date_one_month_ago():
        todays_date = DateGenerator.get_date()
        changed_date = todays_date + relativedelta(months=-1)
        return DateGenerator.get_formated_date(changed_date)
    
    @staticmethod
    def get_date_three_week_ago():
        todays_date = DateGenerator.get_date()
        changed_date = todays_date + timedelta(days=-21)
        return DateGenerator.get_formated_date(changed_date)

    @staticmethod
    def get_date_two_months_ago():
        todays_date = DateGenerator.get_date()
        changed_date = todays_date + relativedelta(months=-2)
        return DateGenerator.get_formated_date(changed_date)

    @staticmethod
    def get_date_three_months_ago():
        todays_date = DateGenerator.get_date()
        changed_date = todays_date + relativedelta(months=-3)
        return DateGenerator.get_formated_date(changed_date)

    @staticmethod
    def modify_date_with_timedelta(date, num_days):
        todays_date = DateGenerator.get_date(date) if date else DateGenerator.get_date()
        changed_date = todays_date + timedelta(days=num_days)
        return DateGenerator.get_formated_date(changed_date)
    
    @staticmethod
    def get_date(date=None):
        if date is not None:
            return datetime.strptime(str(date), "%Y-%m-%d")
        else:
            return datetime.now()

    @staticmethod
    def get_date_two_week_ago():
        todays_date = DateGenerator.get_date()
        changed_date = todays_date + timedelta(days=-14)
        return DateGenerator.get_formated_date(changed_date)

    @staticmethod
    def get_date_one_week_ago():
        todays_date = DateGenerator.get_date()
        changed_date = todays_date + timedelta(days=-7)
        return DateGenerator.get_formated_date(changed_date)

    @staticmethod
    def get_formated_date(date=None):
        """Returns a date string in the format : yyyy-mm-dd!"""
        if date:
            return datetime.strftime(date, "%Y-%m-%d")
        else:
            return datetime.strftime(DateGenerator.get_date(), "%Y-%m-%d")


class ExpenseGenerator:
    """
    Class that generates an expense instances array.
    Will fail if not given expensesByData object as parameter.
    Handles assigning dates to expenses that require them such as
    one week ago, one month ago or three months ago dates.
    Handles modifying expense dates in order not to have them
    all grouped on the same day.
    """

    def __init__(self, expenses_by_date):
        self.expenses_by_date = expenses_by_date

    def assign_date_to_expense(self, date, expense):
        if date == "today":
            expense["date"] = DateGenerator.get_formated_date()
        elif date == "one_week_ago":
            expense["date"] = DateGenerator.get_date_one_week_ago()
        elif date == "two_weeks_ago":
            expense["date"] = DateGenerator.get_date_two_week_ago()
        elif date == "three_weeks_ago":
            expense["date"] = DateGenerator.get_date_three_week_ago()
        elif date == "one_month_ago":
            expense["date"] = DateGenerator.get_date_one_month_ago()
        elif date == "two_month_ago":
            expense["date"] = DateGenerator.get_date_two_months_ago()
        elif date == "three_month_ago":
            expense["date"] = DateGenerator.get_date_three_months_ago()
        else:
            print(f"Unrecognized date given: ", {date})


    def modify_expense_date(
        self, expense_index, date_section, expense_data, days_to_add
    ):
        if expense_index == 0 or date_section == "today":
            return

        days_to_add += 1
        current_date = expense_data["date"]
        expense_data["date"] = DateGenerator.modify_date_with_timedelta(
            current_date, days_to_add
        )

    def generate_expenses(self):
        expenses = []

        for date_section in self.expenses_by_date:
            days_to_add = 0
            date_section_expenses = self.expenses_by_date[date_section]

            for expense_data in date_section_expenses:
                current_expense_index = date_section_expenses.index(expense_data)
                self.assign_date_to_expense(date_section, expense_data)
                self.modify_expense_date(
                    current_expense_index, date_section, expense_data, days_to_add
                )

                days_to_add += 1
                expenses.append(expense_data)
        return expenses

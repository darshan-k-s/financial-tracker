# Generated by Django 3.0.1 on 2021-04-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0014_auto_20210330_2002"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="category",
            field=models.CharField(
                choices=[
                    ("ATM WITHDRAWL", "Atm withdrawl"),
                    ("BAR TABS", "Bar tabs"),
                    ("MONTHLY BILL", "Monthly bill"),
                    ("ONLINE SHOPPING", "Online shopping"),
                    ("ELECTRONICS", "Electronic"),
                    ("GROCERIES", "Groceries"),
                    ("TAXI FARE", "taxi fare"),
                    ("MISCELLANEOUS", "Miscellaneous"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
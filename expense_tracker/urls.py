from django.urls import include, path
from django.contrib import admin

handler500 = "expenses.views.view_500"
handler404 = "expenses.views.view_404"

urlpatterns = [
    path("", include("expenses.urls")),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
]

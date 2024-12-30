from django.urls import path
from .views import ItemListView,fetch_twilio_numbers,fetch_provider_data,fetch_provider_numbers

urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),
    path('fetch_provider_numbers/', fetch_provider_numbers, name='fetch_provider_numbers'),

    path('fetch_twilio_numbers/', fetch_twilio_numbers, name='fetch_twilio_numbers'),

]

# urlpatterns = +[
    # path('admin/fetch_twilio_numbers/', fetch_twilio_numbers, name='fetch_twilio_numbers'),
# ]

# urlpatterns = +[
# ]
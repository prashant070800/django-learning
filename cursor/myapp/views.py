from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Item
from .serializer import ItemSerializer
from django.shortcuts import render
import datetime


class ItemCursorPagination(CursorPagination):
    page_size = 5
    ordering = 'id'  

class ItemListView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='pagination',
                type=str,
                enum=['cursor', 'none'],
                description='Specify pagination type: cursor or none',
            ),
        ],
        responses={200: ItemSerializer(many=True)},
    )
    def get(self, request):
        pagination_type = request.query_params.get('pagination', 'cursor')

        # Fetch all items
        queryset = Item.objects.all()

        # Apply cursor pagination if requested
        if pagination_type == 'cursor':
            paginator = ItemCursorPagination()
            page = paginator.paginate_queryset(queryset, request)
            return paginator.get_paginated_response(ItemSerializer(page, many=True).data)

        # No pagination, return all items
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)


def fetch_twilio_numbers(request):
    # Twilio credentials
    # account_sid = 'your_account_sid'
    # auth_token = 'your_auth_token'

    # client = Client(account_sid, auth_token)
    # twilio_numbers = client.incoming_phone_numbers.list()
    
    twilio_data = []
    # for number in twilio_numbers:
    twilio_data.append({
        "sid": "dsdsdsdds",
        "phone_number": "+9186545852",
        "date_created": datetime.datetime.now(),
        "date_updated": datetime.datetime.now(),
        "capabilities": "call/sms",
        "only_in_twilio": True
    })

    # Compare with database
    # for data in twilio_data:
    #     if PhoneNumber.objects.filter(phone_number=data['phone_number']).exists():
    #         data["only_in_twilio"] = False

    return render(request, 'admin/twilio_numbers.html', {'twilio_data': twilio_data})



from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def fetch_provider_data(request):
    # Hardcoded providers for the dropdown
    providers = ["twilio", "plivo", "exotel"]

    # Handle the POST request when a provider is selected
    if request.method == "POST":
        provider = request.POST.get("provider")

        # Fake data based on the selected provider
        fake_data = {
            "twilio": [
                {"sid": "TW123", "phone_number": "+1234567890", "capabilities": "SMS, Voice"},
                {"sid": "TW124", "phone_number": "+1234567891", "capabilities": "SMS"},
            ],
            "plivo": [
                {"sid": "PL123", "phone_number": "+1928374655", "capabilities": "SMS, Voice"},
            ],
            "exotel": [
                {"sid": "EX123", "phone_number": "+9876543210", "capabilities": "Voice"},
            ],
        }

        # Fetch data for the selected provider
        provider_data = fake_data.get(provider, [])
        return render(
            request, "admin/twilio_numbers.html", {"provider": provider, "twilio_data": provider_data}
        )

    # Render the dropdown form if the request is GET
    return render(request, "admin/provider_dropdown.html", {"providers": providers})


import datetime
from django.http import JsonResponse
from django.shortcuts import render


def fetch_provider_numbers(request):
    provider = request.GET.get('provider')
    data = []

    if provider == 'twilio':
        data = [
            {
                "sid": "twilio-sid-1",
                "phone_number": "+1234567890",
                "date_created": datetime.datetime.now(),
                "date_updated": datetime.datetime.now(),
                "capabilities": "call/sms",
                "only_in_provider": True,
            }
        ]
    elif provider == 'exotel':
        data = [
            {
                "sid": "exotel-sid-1",
                "phone_number": "+1987654321",
                "date_created": datetime.datetime.now(),
                "date_updated": datetime.datetime.now(),
                "capabilities": "call",
                "only_in_provider": False,
            }
        ]
    elif provider == 'plivo':
        data = [
            {
                "sid": "plivo-sid-1",
                "phone_number": "+1123456789",
                "date_created": datetime.datetime.now(),
                "date_updated": datetime.datetime.now(),
                "capabilities": "sms",
                "only_in_provider": True,
            }
        ]

    return JsonResponse(data, safe=False)

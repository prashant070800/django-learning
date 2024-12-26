from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Item
from .serializer import ItemSerializer

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

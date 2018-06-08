"""
Views Module for Ona App
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from kaznet.apps.ona.api import process_instance


@api_view(['GET', 'POST'])
def create_instance(request):
    """
    Creates an Instance
    """
    if request.method == 'POST':
        data = request.data.dict()
        if process_instance(data):
            return Response({"success": True}, status=status.HTTP_201_CREATED)
    return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

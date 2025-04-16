from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def root_route(request):
    """
    Root route for the API.
    """
    return Response({"message": "Welcome to the Memer API!"})
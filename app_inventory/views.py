from django.shortcuts import render

from common.utils import json_response, get_general_context

# Create your views here.
def inventory(request):
    return render(request, 'inventory/inventory.html', get_general_context(request))
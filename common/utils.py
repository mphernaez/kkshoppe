from django.http import JsonResponse

def json_response(message, status):
    if status == 200:
        return JsonResponse({'message': message}, status=status)
    else:
        return JsonResponse({'error': message}, status=status)

def get_general_context(request):
    print(request.user.first_name)
    return {
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
    }
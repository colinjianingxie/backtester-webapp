def api_response(type, view, status, message, data=None):
    return {
        'status': status,
        'view': view,
        'type': type,
        'message': message,
        'data': data,
    }

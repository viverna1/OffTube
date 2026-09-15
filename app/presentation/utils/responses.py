# responses.py
from flask import jsonify

# ? Это функции слоя presentation, если быть ещё точнее то api интерфейса.

def response_err(message: str, status_code: int):
    response = jsonify({'ok': False, 'error': message})
    response.status_code = status_code
    return response

def response_ok(data=None):
    response = jsonify({'ok': True, 'data': data})
    response.status_code = 200
    return response

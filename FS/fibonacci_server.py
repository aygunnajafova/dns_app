from flask import Flask, request, jsonify
import requests

server = Flask(__name__)

def calculate_fib(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        previous, current = 0, 1
        for _ in range(2, n + 1):
            previous, current = current, previous + current
        return current

@server.route('/register', methods=['PUT'])
def add_service():
    data = request.get_json()
    if not data or not all(key in data for key in ('hostname', 'ip', 'as_ip', 'as_port')):
        return "Bad Request", 400
    
    service_name = data['hostname']
    service_ip = data['ip']
    auth_server_ip = data['as_ip']
    auth_server_port = data['as_port']

    reg_message = f'TYPE=A\nNAME={service_name}\nVALUE={service_ip}\nTTL=10\n'
    try:
        resp = requests.post(f'http://{auth_server_ip}:{auth_server_port}/register', data=reg_message)
        if resp.status_code == 201:
            return "Successfully registered", 201
        else:
            return "Registration failed with DNS server", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

@server.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    try:
        number = int(request.args.get('number'))
    except (ValueError, TypeError):
        return "Bad Request: 'number' must be an integer", 400
    
    fib_result = calculate_fib(number)
    return jsonify({'Fibonacci': fib_result}), 200

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=9090)

from flask import Flask, request, jsonify
import requests

server = Flask(__name__)

@server.route('/compute-fibonacci', methods=['GET'])
def get_fibonacci_result():
    hostname = request.args.get('service_name')
    port_number = request.args.get('service_port')
    fib_number = request.args.get('sequence_index')
    nameserver_ip = request.args.get('dns_ip')
    nameserver_port = request.args.get('dns_port')

    if not (hostname and port_number and fib_number and nameserver_ip and nameserver_port):
        return "Bad Request: Missing required parameters", 400

    try:
        lookup_data = f'TYPE=A\nNAME={hostname}\n'
        lookup_result = requests.get(f'http://{nameserver_ip}:{nameserver_port}/resolve', params={'query': lookup_data})
        if lookup_result.status_code == 200:
            target_ip = lookup_result.json().get('VALUE')
        else:
            return "Error: Unable to resolve service IP via DNS", 500
    except Exception as error:
        return f"Error: {str(error)}", 500

    try:
        calculation_result = requests.get(f'http://{target_ip}:{port_number}/compute', params={'index': fib_number})
        if calculation_result.status_code == 200:
            return jsonify(calculation_result.json())
        else:
            return "Error: Failed to retrieve Fibonacci number", 500
    except Exception as error:
        return f"Error: {str(error)}", 500

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)

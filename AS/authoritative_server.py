from flask import Flask, request, jsonify
import json
import os

application = Flask(__name__)

record_storage_path = 'dns_records.json'

if not os.path.exists(record_storage_path):
    with open(record_storage_path, 'w') as file:
        json.dump({}, file)

def retrieve_dns_records():
    with open(record_storage_path, 'r') as file:
        return json.load(file)

def persist_dns_records(dns_records):
    with open(record_storage_path, 'w') as file:
        json.dump(dns_records, file)

@application.route('/register', methods=['POST'])
def process_registration_request():
    request_data = request.data.decode('utf-8').split('\n')
    if len(request_data) < 4:
        return "Bad DNS registration request", 400
    
    record_type = request_data[0].split('=')[1]
    record_name = request_data[1].split('=')[1]
    record_value = request_data[2].split('=')[1]
    record_ttl = request_data[3].split('=')[1]

    if record_type != 'A':
        return "Invalid record type", 400

    # Save DNS record
    dns_records = retrieve_dns_records()
    dns_records[record_name] = {'VALUE': record_value, 'TTL': record_ttl}
    persist_dns_records(dns_records)

    return "Registered", 201

@application.route('/dns-query', methods=['GET'])
def process_lookup_request():
    query_content = request.args.get('query')
    if not query_content:
        return "Bad Request", 400

    query_parts = query_content.split('\n')
    if len(query_parts) < 2 or query_parts[0] != 'TYPE=A':
        return "Invalid query", 400
    
    record_name = query_parts[1].split('=')[1]

    dns_records = retrieve_dns_records()
    found_record = dns_records.get(record_name)
    if found_record:
        response = {
            'TYPE': 'A',
            'NAME': record_name,
            'VALUE': found_record['VALUE'],
            'TTL': found_record['TTL']
        }
        return jsonify(response), 200
    else:
        return "Not Found", 404

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=53533)

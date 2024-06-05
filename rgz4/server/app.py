from flask import Flask, request, jsonify
import hashlib
import os
from scan_services import scan_file
from db import get_report, save_report, get_statistics

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/'
MAX_FILE_SIZE = 100 * 1024 * 1024

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file.content_length > MAX_FILE_SIZE:
        return jsonify({'error': 'File size exceeds 100MB'}), 400

    if file:
        file_content = file.read()
        print(file_content)
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Проверка наличия отчета
        report = get_report(file_hash)
        if report:
            return jsonify(report)

        # Сканирование файла
        clamav_result = scan_file(file_content)["clamav"]
        print("ClamAV result:", clamav_result) 
        
        clamav_parsed_result = parse_clamav_result(clamav_result)
        
        save_report(file_hash, clamav_parsed_result)
        
        file_path = os.path.join(UPLOAD_FOLDER, file_hash)
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return jsonify(clamav_parsed_result)

    return jsonify({'error': 'Invalid file type or no file provided'}), 400

def parse_clamav_result(result):
    lines = result.split('\n') 

    clamav_result = {
        "known_viruses": None,
        "engine_version": None,
        "scanned_directories": None,
        "scanned_files": None,
        "infected_files": None,
        "data_scanned": None,
        "data_read": None,
        "time": None,
        "start_date": None,
        "end_date": None
    }

    for line in lines:
        if line.startswith("Known viruses:"):
            clamav_result["known_viruses"] = int(line.split(': ')[1])
        elif line.startswith("Engine version:"):
            clamav_result["engine_version"] = line.split(': ')[1]
        elif line.startswith("Scanned directories:"):
            clamav_result["scanned_directories"] = int(line.split(': ')[1])
        elif line.startswith("Scanned files:"):
            clamav_result["scanned_files"] = int(line.split(': ')[1])
        elif line.startswith("Infected files:"):
            clamav_result["infected_files"] = int(line.split(': ')[1])
        elif line.startswith("Data scanned:"):
            clamav_result["data_scanned"] = float(line.split(': ')[1].split()[0])
        elif line.startswith("Data read:"):
            clamav_result["data_read"] = float(line.split(': ')[1].split()[0])
        elif line.startswith("Time:"):
            clamav_result["time"] = float(line.split(': ')[1].split()[0])
        elif line.startswith("Start Date:"):
            clamav_result["start_date"] = line.split(': ')[1]
        elif line.startswith("End Date:"):
            clamav_result["end_date"] = line.split(': ')[1]

    return clamav_result

@app.route('/report', methods=['GET'])
def report():
    file_hash = request.args.get('hash')
    report = get_report(file_hash)
    if report:
        return jsonify(report)
    return jsonify({'error': 'Report not found'}), 404

@app.route('/statistics', methods=['GET'])
def statistics():
    stats = get_statistics()
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

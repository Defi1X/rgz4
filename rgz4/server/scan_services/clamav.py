import subprocess
import os
import tempfile

def scan_with_clamav(file_content):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name
    
    try:
        result = subprocess.run(['clamscan', temp_file_path], capture_output=True, text=True, check=True)
        return result.stdout
    finally:
        os.remove(temp_file_path)
        pass
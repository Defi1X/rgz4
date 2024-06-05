from .clamav import scan_with_clamav

def scan_file(file_content):
    clamav_result = scan_with_clamav(file_content)

    return {
        'clamav': clamav_result,
    }

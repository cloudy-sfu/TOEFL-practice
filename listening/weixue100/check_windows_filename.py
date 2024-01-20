import re


def sanitize_filename(filename):
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)
    # Remove trailing spaces or dots
    sanitized = sanitized.rstrip('. ')
    # Check for reserved names
    reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5",
                      "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4",
                      "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
    if sanitized in reserved_names or any(
            sanitized.upper().startswith(f'{name}.') for name in reserved_names):
        sanitized = '_' + sanitized
    return sanitized

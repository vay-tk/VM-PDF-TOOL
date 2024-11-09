import os
import time
from contextlib import contextmanager
import tempfile

@contextmanager
def safe_file_ops():
    temp_files = []
    try:
        yield temp_files
    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    time.sleep(0.1)  # Small delay to ensure file is released
            except Exception:
                pass

def create_temp_file(content=None, suffix=None):
    """Create a temporary file and return its path"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.close()
    if content:
        with open(temp_file.name, 'wb') as f:
            f.write(content)
        time.sleep(0.1)  # Small delay after writing
    return temp_file.name
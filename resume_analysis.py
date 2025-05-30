import os
import bencodepy

# Correct path to the folder containing .resume files
RESUME_DIR = '/home/efi/transmission/config-backup/resume'

def deserialize_resume_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.resume'):
            path = os.path.join(directory, filename)
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                    decoded = bencodepy.decode(data)
                    print(f"\n=== {filename} ===")
                    for key, value in decoded.items():
                        k = key.decode(errors='ignore') if isinstance(key, bytes) else key
                        if isinstance(value, bytes):
                            try:
                                v = value.decode(errors='ignore')
                            except:
                                v = str(value)
                        else:
                            v = str(value)
                        print(f"{k}: {v[:80]}")
            except Exception as e:
                print(f"Failed to decode {filename}: {e}")

if __name__ == '__main__':
    deserialize_resume_files(RESUME_DIR)


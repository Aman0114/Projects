import os
import time
import datetime
from google.cloud import storage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === CONFIGURATION ===
WATCH_FOLDER = "D:/Aman_Repository/Projects/global_health_data/incoming_files"
BUCKET_NAME = "healthcare_data_0114"
gcs_folder = 'healthcare_data'

# Initialize GCS client
storage_client = storage.Client()

# Get today's date string
def today_date_str():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Check if file is readable (not locked)
def is_file_ready(filepath):
    try:
        with open(filepath, "rb"):
            return True
    except (PermissionError, OSError):
        return False

# Upload file to GCS with retry if file is locked
def upload_to_gcs(local_file_path):
    filename = os.path.basename(local_file_path)
    blob_path = f"{gcs_folder}/{filename}"
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_path)

    for i in range(10):
        if is_file_ready(local_file_path):
            blob.upload_from_filename(local_file_path,timeout=300)
            print(f"✅ Uploaded: {local_file_path} → gs://{BUCKET_NAME}/{blob_path}")
            return
        else:
            print(f"⏳ File not ready (attempt {i+1}/10): {filename}")
            time.sleep(10)

    print(f"❌ Failed to upload after multiple attempts: {filename}")

# Upload existing files that match today's date
def upload_existing_files():
    print("🔎 Scanning existing files...")
    for file in os.listdir(WATCH_FOLDER):
        if file.endswith(".csv") and today_date_str() in file:
            full_path = os.path.join(WATCH_FOLDER, file)
            print(f"📄 Found existing file: {file}")
            upload_to_gcs(full_path)

# File event handler for new files
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            filename = os.path.basename(event.src_path)
            if today_date_str() in filename:
                print(f"📥 Detected new file: {filename}")
                upload_to_gcs(event.src_path)

# Main execution
if __name__ == "__main__":
    print(f"👀 Watching folder: {WATCH_FOLDER} for new CSVs with today's date: {today_date_str()}")

    upload_existing_files()  # <-- This handles already existing files

    observer = Observer()
    observer.schedule(FileHandler(), path=WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

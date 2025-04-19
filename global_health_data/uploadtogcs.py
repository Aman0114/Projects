import os
from google.cloud import storage
from datetime import datetime

# Configuration
local_watch_folder = 'C:/Users/Aman/global_health_data/incoming_files'
gcs_bucket_name = 'healthcare_data_0114'
gcs_folder = 'healthcare_data/'  # Folder inside the bucket

# Initialize GCS client
client = storage.Client()
bucket = client.bucket(gcs_bucket_name)

# Process files
print('Checking File in local')
for filename in os.listdir(local_watch_folder):
    if filename.endswith(".csv"):
        print('File found - Uploading data')
        local_path = os.path.join(local_watch_folder, filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destination_blob_name = f"{gcs_folder}{timestamp}_{filename}"

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_path)

        print(f"Uploaded: {local_path} to gs://{gcs_bucket_name}/{destination_blob_name}")

        # Optional: move or delete local file after upload
        # os.remove(local_path)
        # print(f"Deleted local file: {local_path}")

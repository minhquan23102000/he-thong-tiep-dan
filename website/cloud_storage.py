
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate('website/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

bucket = storage.bucket('hethongtiepdan.appspot.com')


def upload_file(buffer, cloud_path, file_name):
    path = f"{cloud_path}/{file_name}"
    blob = bucket.blob(path)
    blob.upload_from_file(buffer)
    blob.make_public()
    return blob.public_url

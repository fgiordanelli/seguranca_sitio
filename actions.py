import cv2
from google.cloud import storage
from twilio.rest import Client
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()

twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
google_cloud_credentials = json.loads(os.getenv('GOOGLE_CLOUD_CREDENTIALS'))

def handle_detection(frame):
    # Salvar imagem com timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"motion_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Image saved: {filename}")

    # Inicializar o cliente do Google Cloud Storage
    client = storage.Client.from_service_account_info(google_cloud_credentials)
    bucket_name = 'people_detected'
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    url = f"https://storage.googleapis.com/{bucket_name}/{filename}"
    print(f"Uploaded image URL: {url}") 

    # Enviar notificação via WhatsApp
    twilio_client = Client(twilio_account_sid, twilio_auth_token)
    message = twilio_client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'Motion Detected! Image saved at: {url}',
        media_url=[url],
        to='whatsapp:+5511956028279'
    )
    print(f"Message sent with ID: {message.sid}")
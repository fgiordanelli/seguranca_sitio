"""
import cv2
from google.cloud import storage
import time

if person_detected and not photo_taken:
    # Inicializa o cliente do Google Cloud Storage
    filename = f"detected_{int(time.time())}.jpg"  # Salva com um timestamp para evitar sobreposições
    cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))         


    client = storage.Client.from_service_account_json('sitio-421517-cbcc42238a47.json')

    # Nome do seu bucket no Google Cloud Storage
    bucket_name = 'people_detected'
    bucket = client.get_bucket(bucket_name)

    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)  # Faz o upload para o GCS
    url = f"https://storage.googleapis.com/{bucket_name}/{filename}"  # Retorna a URL pública
    print(url)

    account_sid = ''  # Use o SID da sua conta real para produção
    auth_token = ''  # Use o token real da sua conta para produção
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Número do WhatsApp Sandbox do Twilio
        body='Alerta',
        media_url=[url],  # URL do arquivo local
        to='whatsapp:+5511956028279'  # Seu número de WhatsApp com código do país
    )
    photo_taken = True
"""
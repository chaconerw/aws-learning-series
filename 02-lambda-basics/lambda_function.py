import boto3
import json
import urllib.parse

# Clientes de AWS
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    """
    Lambda que analiza imágenes con Amazon Rekognition
    cuando se suben a S3.
    
    Detecta: objetos, escenas, texto, caras
    """
    
    # Obtener información del evento S3
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(record['s3']['object']['key'])
    
    # Solo procesar archivos en uploads/
    if not key.startswith('uploads/'):
        print(f"Ignorado - no está en uploads/: {key}")
        return {
            'statusCode': 200,
            'body': 'Archivo ignorado - no está en carpeta uploads/'
        }
    
    print(f"Analizando imagen: {bucket}/{key}")
    
    # ============================================
    # 1. DETECTAR OBJETOS Y ESCENAS (Labels)
    # ============================================
    labels_response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        MaxLabels=10,           # Máximo 10 etiquetas
        MinConfidence=70        # Solo si tiene 70%+ de confianza
    )
    
    labels = []
    for label in labels_response['Labels']:
        labels.append({
            'nombre': label['Name'],
            'confianza': round(label['Confidence'], 2)
        })
    
    print(f"Objetos detectados: {labels}")
    
    # ============================================
    # 2. DETECTAR TEXTO EN LA IMAGEN (Opcional)
    # ============================================
    text_response = rekognition.detect_text(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        }
    )
    
    textos = []
    for text in text_response['TextDetections']:
        if text['Type'] == 'LINE':  # Solo líneas completas
            textos.append({
                'texto': text['DetectedText'],
                'confianza': round(text['Confidence'], 2)
            })
    
    print(f"Texto detectado: {textos}")
    
    # ============================================
    # 3. DETECTAR CARAS (Opcional)
    # ============================================
    faces_response = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        Attributes=['ALL']  # Detectar emociones, edad, etc.
    )
    
    caras = []
    for face in faces_response['FaceDetails']:
        # Obtener la emoción principal
        emociones = face.get('Emotions', [])
        emocion_principal = None
        if emociones:
            emocion_principal = max(emociones, key=lambda x: x['Confidence'])
        
        cara_info = {
            'edad_estimada': f"{face['AgeRange']['Low']}-{face['AgeRange']['High']} años",
            'genero': face['Gender']['Value'],
            'sonriendo': face['Smile']['Value'],
            'lentes': face['Eyeglasses']['Value'],
            'emocion': emocion_principal['Type'] if emocion_principal else 'N/A'
        }
        caras.append(cara_info)
    
    print(f"Caras detectadas: {len(caras)}")
    
    # ============================================
    # 4. GUARDAR RESULTADOS EN S3
    # ============================================
    # Crear nombre del archivo de resultados
    filename = key.split('/')[-1]
    filename_sin_extension = filename.rsplit('.', 1)[0]
    resultado_key = f"resultados/{filename_sin_extension}_analisis.json"
    
    # Preparar el JSON con todos los resultados
    resultado = {
        'archivo_analizado': key,
        'bucket': bucket,
        'analisis': {
            'objetos_detectados': labels,
            'texto_detectado': textos,
            'caras_detectadas': caras,
            'total_caras': len(caras)
        }
    }
    
    # Guardar en S3
    s3.put_object(
        Bucket=bucket,
        Key=resultado_key,
        Body=json.dumps(resultado, indent=2, ensure_ascii=False),
        ContentType='application/json'
    )
    
    print(f"Resultados guardados en: {resultado_key}")
    
    # ============================================
    # 5. RESPUESTA FINAL
    # ============================================
    return {
        'statusCode': 200,
        'body': json.dumps({
            'mensaje': 'Imagen analizada exitosamente',
            'archivo': key,
            'resultados': resultado_key,
            'resumen': {
                'objetos': len(labels),
                'textos': len(textos),
                'caras': len(caras)
            }
        }, ensure_ascii=False)
    }

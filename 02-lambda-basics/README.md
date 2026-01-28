# 02 - AWS Lambda + Rekognition (Serverless Image Analyzer)

En este módulo conectamos **Amazon S3** con **AWS Lambda** para analizar imágenes automáticamente usando **Amazon Rekognition**.

Cuando subes una imagen a `uploads/`, S3 dispara un evento, Lambda procesa la imagen con Rekognition y guarda un archivo JSON con los resultados en `resultados/`.

---

## Arquitectura

Usuario sube imagen → S3 (`uploads/`) → Evento `ObjectCreated` → Lambda → Rekognition → S3 (`resultados/`)

---

## Objetivo

- Entender qué es AWS Lambda (serverless)
- Entender qué es un trigger por eventos (S3 ObjectCreated)
- Conectar Lambda con Rekognition
- Guardar resultados automáticamente en S3 (JSON)

---

## Requisitos

- Un bucket S3 (en el video usamos: **bucket-mrrobot**)
- Permisos IAM para que Lambda pueda:
  - Leer/Escribir en S3
  - Llamar a Rekognition

---

## Archivos de este módulo

- `lambda_function.py` – Código de la función Lambda (S3 → Rekognition → S3)
- `event_sample.json` – Evento de prueba para simular S3 en la consola de Lambda

---

## Pasos generales

### 1) Crear carpetas en el bucket

Dentro del bucket:

- `uploads/` (entrada)
- `resultados/` (salida)

### 2) Crear función Lambda

- Runtime: Python
- Pegar el contenido de `lambda_function.py`
- Ajustar timeout (ej: 30 segundos)

### 3) Permisos IAM (rol de la Lambda)

La Lambda necesita permisos para:

- `s3:GetObject` (leer imagen)
- `s3:PutObject` (guardar JSON en resultados)
- `rekognition:DetectLabels`, `rekognition:DetectText`, `rekognition:DetectFaces`

### 4) Crear trigger S3

- Evento: `All object create events`
- Prefix: `uploads/`

### 5) Probar

- Sube una imagen a `uploads/`
- Verifica:
  - Logs en CloudWatch
  - JSON generado en `resultados/`

---

## Notas

- El evento de prueba (`event_sample.json`) solo simula el evento; para prueba real, sube una imagen al bucket.
- Asegúrate de que Lambda y el bucket estén en la misma región.

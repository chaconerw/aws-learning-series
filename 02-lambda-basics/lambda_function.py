import boto3
from PIL import Image
import io
import urllib.parse

s3 = boto3.client("s3")

THUMB_SIZE = (300, 300)
INPUT_PREFIX = "uploads/"
OUTPUT_PREFIX = "thumbnails/"

def lambda_handler(event, context):
    # Tomamos el primer registro del evento S3
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

    # Evitar loops: solo procesar archivos en uploads/
    if not key.startswith(INPUT_PREFIX):
        print(f"Ignorado porque no está en {INPUT_PREFIX}: {key}")
        return {"statusCode": 200, "body": "Ignored"}

    # Descargar imagen original
    obj = s3.get_object(Bucket=bucket, Key=key)
    original_bytes = obj["Body"].read()

    # Abrir imagen con Pillow
    image = Image.open(io.BytesIO(original_bytes))
    image.thumbnail(THUMB_SIZE)

    # Guardar thumbnail en memoria
    out = io.BytesIO()
    fmt = (image.format or "JPEG").upper()
    if fmt == "JPG":
        fmt = "JPEG"
    image.save(out, format=fmt)
    out.seek(0)

    # Nuevo nombre en carpeta thumbnails/
    filename = key.split("/")[-1]
    out_key = f"{OUTPUT_PREFIX}{filename}"

    # Subir thumbnail al bucket
    s3.put_object(
        Bucket=bucket,
        Key=out_key,
        Body=out.getvalue(),
        ContentType=obj.get("ContentType", "image/jpeg"),
    )

    print(f"OK: {key} -> {out_key}")

    return {
        "statusCode": 200,
        "body": f"Thumbnail creado: {out_key}"
    }

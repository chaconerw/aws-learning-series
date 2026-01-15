# 02 - AWS Lambda Basics

En este módulo conectamos S3 con Lambda para crear thumbnails automáticamente cuando se sube una imagen.

## Arquitectura

Usuario sube imagen → S3 (uploads/) → Evento ObjectCreated → Lambda (+ Layer Pillow) → S3 (thumbnails/)

## Objetivo

- Entender qué es Lambda
- Entender qué es un trigger
- Entender qué es un Layer
- Crear thumbnails automáticamente

## Archivos de este módulo

- lambda_function.py – Código de la función
- event_sample.json – Ejemplo de evento
- scripts/build_layer_cloudshell.sh – Script para crear el Layer con Pillow

## Pasos generales

1) Crear bucket con carpetas:
   - uploads/
   - thumbnails/

2) Crear Layer:
   - Usar CloudShell
   - Ejecutar scripts/build_layer_cloudshell.sh
   - Subir el zip como Lambda Layer

3) Crear función Lambda:
   - Runtime Python
   - Pegar lambda_function.py
   - Conectar el Layer

4) Crear trigger S3:
   - Evento ObjectCreated
   - Prefix: uploads/

5) Probar:
   - Subir una imagen a uploads/
   - Ver thumbnail en thumbnails/

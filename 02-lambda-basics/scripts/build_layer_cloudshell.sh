#!/bin/bash

# Crear carpeta para el layer
mkdir python

# Instalar Pillow dentro de esa carpeta
pip install pillow -t python/

# Crear el zip
zip -r pillow-layer.zip python

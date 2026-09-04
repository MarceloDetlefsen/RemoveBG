#!/usr/bin/env python3
"""
quitar_fondo.py
----------------
Recorre una carpeta, le quita el fondo a todas las imágenes que encuentre
(jpg, jpeg, png, webp, bmp, tiff...) y guarda el resultado como .webp con
fondo transparente en una subcarpeta de salida.

USO:
    python quitar_fondo.py
        -> procesa la carpeta actual, guarda en ./sin_fondo

    python quitar_fondo.py "C:/ruta/a/mis/fotos"
        -> procesa esa carpeta, guarda en "C:/ruta/a/mis/fotos/sin_fondo"

    python quitar_fondo.py "C:/ruta/a/mis/fotos" -o "C:/salida"
        -> guarda el resultado en otra carpeta específica

INSTALACIÓN (una sola vez):
    pip install rembg pillow onnxruntime

La primera vez que se ejecuta, descarga el modelo de IA (~180 MB) y lo
guarda en tu computadora; las siguientes veces ya no vuelve a descargarlo.
"""

import sys
import argparse
from pathlib import Path

EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def main():
    parser = argparse.ArgumentParser(description="Quita el fondo de imágenes y las convierte a WebP.")
    parser.add_argument("carpeta", nargs="?", default=".", help="Carpeta con las imágenes (por defecto: la carpeta actual)")
    parser.add_argument("-o", "--salida", default=None, help="Carpeta de salida (por defecto: <carpeta>/sin_fondo)")
    parser.add_argument("--modelo", default="isnet-general-use",
                         help="Modelo de rembg a usar (por defecto: isnet-general-use, buena calidad para productos)")
    args = parser.parse_args()

    try:
        from rembg import remove, new_session
        from PIL import Image
    except ImportError:
        print("Faltan librerías. Instálalas con:\n\n    pip install rembg pillow onnxruntime\n")
        sys.exit(1)

    carpeta = Path(args.carpeta).expanduser().resolve()
    if not carpeta.is_dir():
        print(f"La carpeta no existe: {carpeta}")
        sys.exit(1)

    salida = Path(args.salida).expanduser().resolve() if args.salida else carpeta / "sin_fondo"
    salida.mkdir(parents=True, exist_ok=True)

    imagenes = sorted(
        p for p in carpeta.iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONES_VALIDAS and p.parent != salida
    )

    if not imagenes:
        print(f"No se encontraron imágenes en: {carpeta}")
        sys.exit(0)

    print(f"Cargando modelo '{args.modelo}' (la primera vez tarda un poco, descarga ~180MB)...")
    session = new_session(args.modelo)

    print(f"Se encontraron {len(imagenes)} imágenes. Procesando...\n")

    ok, fallidas = 0, []
    for i, ruta in enumerate(imagenes, 1):
        destino = salida / (ruta.stem + ".webp")
        try:
            with open(ruta, "rb") as f:
                datos_originales = f.read()

            resultado = remove(datos_originales, session=session)

            img = Image.open(__import__("io").BytesIO(resultado)).convert("RGBA")
            img.save(destino, "WEBP", quality=95, method=6)

            print(f"[{i}/{len(imagenes)}] OK  -> {ruta.name}  =>  {destino.name}")
            ok += 1
        except Exception as e:
            print(f"[{i}/{len(imagenes)}] ERROR con {ruta.name}: {e}")
            fallidas.append(ruta.name)

    print(f"\nListo. {ok} imágenes procesadas correctamente.")
    print(f"Resultado guardado en: {salida}")
    if fallidas:
        print(f"\n{len(fallidas)} fallaron: {', '.join(fallidas)}")


if __name__ == "__main__":
    main()

# Quitar fondo y convertir a WebP

Script para eliminar el fondo de las fotos de productos (botellas, licores, etc.)
y guardarlas convertidas a `.webp` con fondo transparente.

## Requisitos

- Tener Python 3 instalado ([python.org](https://www.python.org/downloads/))
- Conexión a internet (solo la primera vez, para descargar el modelo de IA)

## Instalación

### Opción recomendada en Linux: usar `venv`

Si estás en Linux, lo más seguro es crear un entorno virtual dentro del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install rembg pillow onnxruntime
```

### Instalación global

Abrí una terminal (CMD, PowerShell o Terminal) y corré:

```bash
pip install rembg pillow onnxruntime
```

Esto instala todo lo necesario. Solo hay que hacerlo una vez.

## Uso

### 1. Ubicá el script

Poné el archivo `quitar_fondo.py` en cualquier carpeta (no necesita estar
junto a las imágenes).

### 2. Corré el script

**Opción A — procesar la carpeta actual:**

Abrí la terminal *dentro* de la carpeta donde están las fotos y ejecutá:

```bash
python quitar_fondo.py
```

En Linux con `venv`:

```bash
source .venv/bin/activate
python quitar_fondo.py
```

**Opción B — indicar la carpeta con las fotos:**

```bash
python quitar_fondo.py "C:\ruta\a\mis\fotos"
```

En Linux con `venv`:

```bash
source .venv/bin/activate
python quitar_fondo.py "/ruta/a/mis/fotos"
```

(en Mac/Linux también puede ser `python3 quitar_fondo.py "/ruta/a/mis/fotos"`)

**Opción C — elegir también dónde guardar el resultado:**

```bash
python quitar_fondo.py "C:\ruta\a\mis\fotos" -o "C:\ruta\a\salida"
```

En Linux con `venv`:

```bash
source .venv/bin/activate
python quitar_fondo.py "/ruta/a/mis/fotos" -o "/ruta/a/salida"
```

### 3. Esperá a que termine

La primera vez que lo corrés, va a descargar el modelo de IA (~180 MB), así
que tarda un poco más. Vas a ver algo así en pantalla:

```
Cargando modelo 'isnet-general-use'...
Se encontraron 12 imágenes. Procesando...

[1/12] OK  -> botella1.jpg   =>  botella1.webp
[2/12] OK  -> botella2.png   =>  botella2.webp
...
Listo. 12 imágenes procesadas correctamente.
Resultado guardado en: .../sin_fondo
```

### 4. Buscá el resultado

Por defecto, las imágenes procesadas quedan en una subcarpeta llamada
**`sin_fondo`**, dentro de la carpeta original. Tus fotos originales
**no se tocan ni se borran**.

## Qué hace exactamente

- Recorre la carpeta indicada (no entra a subcarpetas).
- Toma todas las imágenes con extensión `.jpg`, `.jpeg`, `.png`, `.webp`,
  `.bmp`, `.tiff` o `.tif`.
- Le quita el fondo a cada una usando un modelo de IA (rembg).
- Guarda el resultado en formato `.webp` con fondo transparente, con el
  mismo nombre que el archivo original.
- **Aunque una imagen ya esté en `.webp`, igual se vuelve a procesar**
  (le quita el fondo otra vez y la regraba).
- Si una imagen falla por algún motivo, el script sigue con las demás y
  al final te dice cuáles fallaron.

## Problemas comunes

**"Faltan librerías" / `ModuleNotFoundError`**
No corriste (o falló) el `pip install`. Volvé a correr:
```bash
pip install rembg pillow onnxruntime
```

Si usás `venv` en Linux:
```bash
source .venv/bin/activate
pip install rembg pillow onnxruntime
```

**El recorte queda con bordes raros en botellas de vidrio transparente**
Es normal, el vidrio transparente es difícil para cualquier IA de recorte.
Podés probar otro modelo agregando `--modelo`:
```bash
python quitar_fondo.py --modelo u2net
```
Modelos disponibles para probar: `u2net`, `isnet-general-use` (el que usa
por defecto), `silueta`.

**Tarda mucho**
Solo la primera corrida tarda más (descarga del modelo). Además, cuantas
más imágenes y más grandes sean, más tiempo toma procesarlas.

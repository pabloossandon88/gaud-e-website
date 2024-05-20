# api.py

import requests
from django.conf import settings


def send_generation_request(host, params):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {settings.STABILITY_KEY}"
    }

    # Encode parameters
    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = image  # No necesitas abrir el archivo aquí
    if mask is not None and mask != '':
        files["mask"] = mask  # No necesitas abrir el archivo aquí
    if len(files) == 0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response


def llamar_api_replace(image, select, replace):

    seed = 0 #@param {type:"integer"}
    output_format = "jpeg" #@param ["webp", "jpeg", "png"]

    host = f"https://api.stability.ai/v2beta/stable-image/edit/search-and-replace"


    params = {
        "image" : image,
        "prompt": replace,
        "search_prompt": select,
        "seed" : seed,
        "output_format": output_format,
    }

    response = send_generation_request(
        host,
        params
    )

    # Decode response
    output_image = response.content
    print(output_image)
    
    # Verificamos que la respuesta sea exitosa
    if response.status_code == 200:
        # Convertimos la respuesta a JSON y la retornamos
        #return response.json()
        return response.content
    else:
        # Manejo de errores o respuesta no exitosa
        return {"error": "Hubo un problema con la solicitud a la API"}
    
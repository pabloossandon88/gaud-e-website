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


def llamar_api_outpaint(image, prompt, left, right, up, down, seed):
    
    output_format = "jpeg" #@param ["webp", "jpeg", "png"]

    host = f"https://api.stability.ai/v2beta/stable-image/edit/outpaint"

    final_prompt = "I want you to make an extension to this dwelling, consider " + prompt

    params = {
        "image" : image,
        "prompt": final_prompt,
        "left": left,
        "right": right,
        "up": up,
        "down": down,
        "seed" : seed,
        "output_format": output_format,
    }

    response = send_generation_request(
        host,
        params
    )
    
    if response.status_code == 200:
        # Si la respuesta es exitosa (código 200), devolver el contenido de la respuesta
        return response.content
    else:
        # Si hay un error, determinar el tipo de error y devolver un mensaje apropiado
        if response.status_code == 400:
            error_message = "Invalid parameter(s), see the errors field for details."
        elif response.status_code == 403:
            error_message = "Your request was flagged by our content moderation system."
        elif response.status_code == 413:
            error_message = "Your request was larger than 10MiB."
        elif response.status_code == 422:
            error_message = "You made a request with an unsupported language."
        elif response.status_code == 429:
            error_message = "You have made more than 150 requests in 10 seconds."
        elif response.status_code == 500:
            error_message = "An internal error occurred. If the problem persists contact support."
        else:
            error_message = "Hubo un problema con la solicitud a la API"

        # Devolver un diccionario con el mensaje de error
        return {"error": error_message}
    
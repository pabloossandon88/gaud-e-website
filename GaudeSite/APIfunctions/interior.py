import requests
from django.conf import settings


def send_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {settings.STABILITY_KEY}"
    }

    # Encode parameters
    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
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

def llamar_api_interior(prompt, aspect_ratio, negative_prompt, model):
    seed = 0 
    output_format = "jpeg" 
    
    host = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"

    params = {
        "prompt" : prompt,
        "negative_prompt" : negative_prompt,
        "aspect_ratio" : aspect_ratio,
        "seed" : seed,
        "output_format" : output_format,
        "model" : model,
        "mode" : "text-to-image"
    }
    response = send_generation_request(host, params)
    
    output_image = response.content
    print(output_image)
    
    # Verificamos que la respuesta sea exitosa
    if response.status_code == 200:
        # Convertimos la respuesta a JSON y la retornamos
        #return response.json()
        return output_image
    else:
        # Manejo de errores o respuesta no exitosa
        return {"error": "Hubo un problema con la solicitud a la API"}
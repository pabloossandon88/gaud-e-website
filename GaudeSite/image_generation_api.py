# api.py

import requests
STABILITY_KEY = "sk-tQepiNbR3T3X8VQGLuk7E9yB6joOaoi3xOdNXdgky0yto6E6"


def send_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_KEY}"
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

def llamar_api(prompt, num_imgs):
    negative_prompt = "" 
    aspect_ratio = "21:9" 
    seed = 0 
    output_format = "jpeg" 
    
    host = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"

    params = {
        "prompt" : prompt,
        "negative_prompt" : negative_prompt,
        "aspect_ratio" : aspect_ratio,
        "seed" : seed,
        "output_format" : output_format,
        "model" : "sd3",
        "mode" : "text-to-image"
    }
    response = send_generation_request(host, params)
    
    # Decode response
    output_image = response.content
    print(output_image)
    
    #finish_reason = response.headers.get("finish-reason")
    #seed = response.headers.get("seed")

    # Check for NSFW classification
    #if finish_reason == 'CONTENT_FILTERED':
    #    raise Warning("Generation failed NSFW classifier")

    # Save and display result
    #generated = f"generated_{seed}.{output_format}"
    
    # Hacemos el POST request a la API
    #response = requests.post(host, json=params)

    # Verificamos que la respuesta sea exitosa
    if response.status_code == 200:
        # Convertimos la respuesta a JSON y la retornamos
        #return response.json()
        return output_image
    else:
        # Manejo de errores o respuesta no exitosa
        return {"error": "Hubo un problema con la solicitud a la API"}
    

"""
def llamar_api(prompt, num_imgs):
    # URL de tu API
    url = "https://tryudv28tj.execute-api.us-east-1.amazonaws.com/default/SDXL-Turbo"

    # Estructura del body de la solicitud, ajusta esto según lo que espera tu API
    data = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 1,
            "num_images_per_prompt": num_imgs,
            "guidance_scale":0.0
        }
    }

    # Hacemos el POST request a la API
    response = requests.post(url, json=data)

    # Verificamos que la respuesta sea exitosa
    if response.status_code == 200:
        # Convertimos la respuesta a JSON y la retornamos
        return response.json()
    else:
        # Manejo de errores o respuesta no exitosa
        return {"error": "Hubo un problema con la solicitud a la API"}
"""
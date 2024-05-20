# api.py
import os
import time
import json
import requests
STABILITY_KEY = "sk-tQepiNbR3T3X8VQGLuk7E9yB6joOaoi3xOdNXdgky0yto6E6"


# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA
# PROBLEMA


def send_async_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    # Encode parameters
    files = {}
    if "init_image" in params:
        init_image = params.pop("init_image")
        files = {"image": open(init_image, 'rb')}

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

    # Process async response
    response_dict = json.loads(response.text)
    generation_id = response_dict.get("id", None)
    assert generation_id is not None, "Expected id in response"

    # Loop until result or timeout
    timeout = int(os.getenv("WORKER_TIMEOUT", 500))
    start = time.time()
    status_code = 202
    while status_code == 202:
        response = requests.get(
            f"{host}/result/{generation_id}",
            headers={
                **headers,
                "Accept": "image/*"
            },
        )

        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        status_code = response.status_code
        time.sleep(10)
        if time.time() - start > timeout:
            raise Exception(f"Timeout after {timeout} seconds")

    return response


def llamar_api_upscale(image, prompt, negative_prompt, seed):
    output_format = "png" #@param ["webp", "jpeg", "png"]

    host = f"https://api.stability.ai/v2beta/stable-image/upscale/creative"

    params = {
        "prompt" : prompt,
        "negative_prompt" : negative_prompt,
        "seed" : seed,
        #"creativity" : creativity,
        "init_image" : image,
        "output_format": output_format
    }

    response = send_async_generation_request(
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
    
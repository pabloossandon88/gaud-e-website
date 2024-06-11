import requests
from django.conf import settings
from django.contrib.auth import get_user_model
import pdb


from GaudeSite.models import UserProfile

User = get_user_model()
usuario = User.objects.first()
user_profile, created = UserProfile.objects.get_or_create(user=usuario)

def send_generation_request( host, params ):
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

def call_api(parameters):
    seed = 0 
    output_format = "jpeg" 
    
    host = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"

    params = {
        "prompt" : parameters['final_prompt'],
        "negative_prompt" : parameters['negative'],
        "aspect_ratio" : parameters['aspect_ratio'],
        "seed" : seed,
        "output_format" : output_format,
        "model" : parameters['model'],
        "mode" : "text-to-image"
    }
    
    if validate_credits(10):

        response = send_generation_request(host, params)
        
        output_image = response.content
        
        if response.status_code == 200:
            
            deduct_credits(10)

            return output_image
        else:
            return {"error": "Hubo un problema con la solicitud a la API"}
    else:
            return {"error": "Usuario sin creditos Gaud-e"}

def validateRequestPost(name, validate):
    if prompt :
            promptt['value'] = prompt
    return

def call_api_image(image, parameters ):

    control_strength = 0.2  #@param {type:"slider", min:0, max:1, step:0.05}
    seed = 0 #@param {type:"integer"}
    output_format = "jpeg" #@param ["webp", "jpeg", "png"]

    host = f"https://api.stability.ai/v2beta/stable-image/control/sketch"
    
    params = {
        "prompt" : "Improve this image considerably as if you were an expert architect. " + parameters['final_prompt'],
        "negative_prompt" : parameters['negative'],
        "seed" : seed,
        "output_format" : output_format,
        "control_strength" : control_strength,
        "image" : image,
        }
    
    if validate_credits(10):

        response = send_generation_request( host, params )

        output_image = response.content
        print(output_image)
        
        if response.status_code == 200:
            
            #deduct_credits(10)

            return response.content
        else:
            return {"error": "Hubo un problema con la solicitud a la API"}

    else:
        return {"error": "Usuario sin creditos Gaud-e"}
   

def deduct_credits(amount):
    user_profile.credits -= amount
    user_profile.save()

def validate_credits(amount):
    if user_profile.credits >= amount : 
        return True
    
    return False
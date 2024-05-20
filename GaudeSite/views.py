from django.shortcuts import render, redirect
from django.http import HttpResponse
import base64

# Import API functions
from .image_generation_api import llamar_api
from .remove_back import llamar_api_remove_back
from .sketch_image import llamar_api_boceto
from .master_plan import llamar_api_masterplan
from .interior import llamar_api_interior
from .exterior import llamar_api_exterior
from .searchReplace import llamar_api_replace
from .replaceStructure import llamar_api_replace_structure
from .outpaint import llamar_api_outpaint
from .interiorRedecoration import llamar_api_interiorRedecoration
from .upscale import llamar_api_upscale

# Function to convert bytes to base64
def bytes_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode()

def home(request):
    return render(request, 'GaudeSite/home.html')

def imgGenerator(request):
    if request.method == 'POST':
        tipo_construccion = request.POST.get('select1')
        estilo_construccion = request.POST.get('select2')
        tipo_vista = request.POST.get('select3')
        num_imgs = int(request.POST.get('select4'))
        detalles = request.POST.get('textoEjemplo')

        prompt = f'{tipo_construccion} {estilo_construccion} {tipo_vista} {detalles}'

        resultado = llamar_api(prompt, num_imgs)
        imagenes_base64 = bytes_to_base64(resultado)
        
        context = {
            'imagenes_base64': imagenes_base64,
            'tipo_construccion': tipo_construccion,
            'estilo_construccion': estilo_construccion,
            'tipo_vista': tipo_vista,
            'num_imgs': num_imgs,
            'detalles': detalles
        }
        
        return render(request, 'GaudeSite/imgen.html', context)
    return render(request, 'GaudeSite/imgen.html')

def projEval(request):
    return render(request, 'GaudeSite/projeval.html')

def sketchImg(request):
    if request.method == 'POST':

        detalles = request.POST.get('textoEjemplo')      
        imagen = request.FILES.get('imagen')

        if imagen:
            resultado = llamar_api_boceto(imagen, detalles)
            imagenes_base64 = bytes_to_base64(resultado)
            context = {'imagenes_base64': imagenes_base64,
                       'detalles': detalles
            }
        
            return render(request, 'GaudeSite/sketchimg.html', context)
        
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
    return render(request, 'GaudeSite/sketchimg.html')

def removeBackground(request):
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')

        if imagen:
            resultado = llamar_api_remove_back(imagen)
            imagenes_base64 = bytes_to_base64(resultado)
            context = {
                'imagenes_base64': imagenes_base64,
            }
        
            return render(request, 'GaudeSite/removeback.html', context)
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
        
    return render(request, 'GaudeSite/removeback.html')


def masterPlan(request):
    if request.method == 'POST':
        tipo_construccion = request.POST.get('select1')
        negative_prompt = request.POST.get('textoEjemplo2')
        detalles = request.POST.get('textoEjemplo')
        imagen = request.FILES.get('imagen')

        prompt = f'{tipo_construccion} {detalles}'

        if imagen:
            resultado = llamar_api_masterplan(imagen, prompt, negative_prompt)
            imagenes_base64 = bytes_to_base64(resultado)

            context = {'imagenes_base64': imagenes_base64,
                       'tipo_construccion': tipo_construccion,
                       "negative_prompt": negative_prompt,
                       'detalles': detalles
            }
        
            return render(request, 'GaudeSite/masterplan.html', context)
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)       
    return render(request, 'GaudeSite/masterplan.html')


def searchReplace(request):
    if request.method == 'POST':
        
        select = request.POST.get('seleccionar')
        replace = request.POST.get('reemplazar')
        imagen = request.FILES.get('imagen')

        if imagen:
            resultado = llamar_api_replace(imagen, select, replace)
            imagenes_base64 = bytes_to_base64(resultado)

            context = {
                'imagenes_base64': imagenes_base64,
                'seleccionar': select,
                'reemplazar': replace
            }
        
            return render(request, 'GaudeSite/searchreplace.html', context)
        
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)        
    return render(request, 'GaudeSite/searchreplace.html')

def replaceStructure(request):
    if request.method == 'POST':
        
        replace = request.POST.get('prompt')
        imagen = request.FILES.get('imagen')

        if imagen:
            resultado = llamar_api_replace_structure(imagen, replace)
            imagenes_base64 = bytes_to_base64(resultado)

            context = {
                'imagenes_base64': imagenes_base64,
                'prompt': replace,
            }
        
            return render(request, 'GaudeSite/replacestructure.html', context)
        
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)        
    return render(request, 'GaudeSite/replacestructure.html')



def interiorImage(request):
    if request.method == 'POST':
        
        prompt = request.POST.get('prompt')
        room = request.POST.get('select1')
        style = request.POST.get('select2')
        aspect_ratio = request.POST.get('select3')
        negative_prompt = request.POST.get('negative_prompt')
        model = request.POST.get('select6')
        final_prompt= "Create a stunning architectural image featuring a " + room + " in" + style + " style, capturing its essence and ambiance in vivid detail. The image must have " + prompt
       
        resultado = llamar_api_interior(final_prompt, aspect_ratio, negative_prompt, model)
        imagenes_base64 = bytes_to_base64(resultado)

        context = {
            'imagenes_base64': imagenes_base64,
            'prompt': prompt,
        }
        
        return render(request, 'GaudeSite/interior.html', context)                
    return render(request, 'GaudeSite/interior.html')


def exteriorImage(request):
    if request.method == 'POST':
        
        prompt = request.POST.get('prompt')
        construction = request.POST.get('select1')
        style = request.POST.get('select2')
        aspect_ratio = request.POST.get('select3')
        negative_prompt = request.POST.get('negative_prompt')
        model = request.POST.get('select6')
        
        final_prompt= "Create a stunning architectural an image from the exterior featuring a " + construction + " in" + style + " style, capturing its essence and ambiance in vivid detail. The construction must have " + prompt       
        resultado = llamar_api_exterior(final_prompt, aspect_ratio, negative_prompt, model)        
        imagenes_base64 = bytes_to_base64(resultado)

        context = {
            'imagenes_base64': imagenes_base64,
            'prompt': prompt,
        }

        return render(request, 'GaudeSite/exterior.html', context)                
    return render(request, 'GaudeSite/exterior.html')


def outPaint(request):
    if request.method == 'POST':
        
        imagen = request.FILES.get('imagen')
        left = request.POST.get('left')
        right = request.POST.get('right')
        up = request.POST.get('up')
        down = request.POST.get('down')
        prompt = request.POST.get('textoEjemplo')
        seed = request.POST.get('seed')
        
        if imagen:       
            resultado = llamar_api_outpaint(imagen, prompt, left, right, up, down, seed)

            if isinstance(resultado, dict) and 'error' in resultado:
                return redirect('/') 
            
            else:
                imagenes_base64 = bytes_to_base64(resultado)
                context = {
                    'imagenes_base64': imagenes_base64,
                    'prompt': prompt,
                }
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)            
        return render(request, 'GaudeSite/outpaint.html', context)        
    
    return render(request, 'GaudeSite/outpaint.html')


def interiorRedecoration(request):
    if request.method == 'POST':
               
        imagen = request.FILES.get('imagen')
        prompt = request.POST.get('textoEjemplo')
        style = request.POST.get('select2')
        negative_prompt = request.POST.get('textoEjemplo2')
        seed = request.POST.get('seed')
        
        full_prompt = f"""
            Redesing the image in the {style} style, 
            taking into account the following details: "{prompt}". 
            As an expert interioir designer, ensure the design reflects your expertise
            and creativity.
        """

        if imagen:
            resultado = llamar_api_interiorRedecoration(imagen, full_prompt, negative_prompt, seed)
            imagenes_base64 = bytes_to_base64(resultado)

            context = {
                'imagenes_base64': imagenes_base64,
                "negative_prompt": negative_prompt,
                'detalles': prompt
            }
        
            return render(request, 'GaudeSite/interiorredecoration.html', context)
        
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
        
    return render(request, 'GaudeSite/interiorredecoration.html')    
    
    
    
def landScape(request):
    if request.method == 'POST':
        estilo_espacio = request.POST.get('select3')
        imagen = request.FILES.get('imagen')
        prompt = request.POST.get('textoEjemplo')
        tipo_espacio = request.POST.get('select1')
        negative_prompt = request.POST.get('textoEjemplo2')

        full_prompt = f"""
            Create a {tipo_espacio} Landscape in the {estilo_espacio} style, 
            taking into account the following details: "{prompt}". 
            As an expert architect, ensure the design reflects your expertise
            and creativity.
        """

        if imagen:
            resultado = llamar_api_masterplan(imagen, full_prompt, negative_prompt)
            imagenes_base64 = bytes_to_base64(resultado)

            context = {
                'imagenes_base64': imagenes_base64,
                'tipo_construccion': estilo_espacio,
                "negative_prompt": negative_prompt,
                "tipo_espacio": tipo_espacio,
                'detalles': prompt
            }
        
            return render(request, 'GaudeSite/landscape.html', context)
        
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
        
    return render(request, 'GaudeSite/landscape.html')


def upScale(request):
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        negative_prompt = request.POST.get('textoEjemplo2')
        prompt = request.POST.get('textoEjemplo')
        seed = request.POST.get('seed')
        
        if imagen:
            resultado = llamar_api_upscale(imagen, prompt, negative_prompt, seed)
            imagenes_base64 = bytes_to_base64(resultado)
            context = {
                'imagenes_base64': imagenes_base64,
            }
        
            return render(request, 'GaudeSite/upscale.html', context)
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
        
    return render(request, 'GaudeSite/upscale.html')
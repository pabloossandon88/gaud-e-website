from django.shortcuts import render, redirect
from django.http import HttpResponse
import base64
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Import API functions
from .APIfunctions.image_generation_api import llamar_api
from .APIfunctions.remove_back          import llamar_api_remove_back
from .APIfunctions.sketch_image         import llamar_api_boceto
from .APIfunctions.master_plan          import llamar_api_masterplan
from .APIfunctions.interior             import llamar_api_interior
from .APIfunctions.exterior             import llamar_api_exterior
from .APIfunctions.searchReplace        import llamar_api_replace
from .APIfunctions.replaceStructure     import llamar_api_replace_structure
from .APIfunctions.outpaint             import llamar_api_outpaint
from .APIfunctions.interiorRedecoration import llamar_api_interiorRedecoration
from .APIfunctions.upscale              import llamar_api_upscale

promptt = {
            'name' : 'Añade detalles (Prompt)',
            'slug' : 'prompt',
            'type' : 'textarea'
    }

negative = {
            'name' : 'Negative Prompt',
            'slug' : 'negative',
            'type' : 'textarea'
    }

models = {
        'name' : 'Modelo',
        'slug' : 'model',
        'type' : 'ratio',
        'items' : [
            ['SD3', 'sd3'],
            ['SD3-TURBO', 'sd3-turbo']
        ]
    }
    
aspectratio = { 
        'name' : 'Aspect Ratio',
        'slug' : 'aspectratio',
        'type' : 'ratio',
        'items' : [
                ['1:1', '1:1'],
                ['2:3', '2:3'],
                ['3:2', '3:2'],
                ['4:5', '4:5'],
                ['5:4','5:4'],
                ['9:16', '9:16'],
                ['9:21', '9:21'],
                ['16:9', '16:9'],
                ['21:9', '21:9']
        ]
    }
seed = {
        'name' : 'Seed',
        'slug' : 'seed',
        'type' : 'range'
        }
    

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
    styles = {
                'name' : 'Estilo',
                'slug' : 'estilo',
                'type' : 'ratio',
                'items' : [
                    ['MaterPlan', 'masterplan']
                ]
        }
    imagen = {
                'name' : 'Imagen',
                'slug' : 'imagen',
                'type' : 'file'
        }
    
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
    
    context = {
        'name': 'Master Plan',
        'description': 'Genera un loteo o un condominio en 3D, a partir solamente de un esquema o fotografía. Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
        'controls' : [ imagen, promptt, styles, negative ],
        'action' : '/interior/'
    }

    return render(request, 'GaudeSite/tool.html', context)

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

@login_required
def interiorImage(request):

    living_room = {
            'name' : 'Tipo de habitación',
            'slug' : 'living_room',
            'type' : 'ratio',
            'items' : [
                ['Living Room', 'living_room'],
                ['Dormitorio', 'bedroom'],
                ['Baño', 'bathroom'],
                ['Cocina', 'kitchen'],
                ['dining_room', 'Comedor'],
                ['reception', 'Recepción'],
                ['dressing_room', 'Vestidor'],
                ['loft', 'Desván'],
                ['office', 'Oficina'],
                ['meeting_room', 'Sala de Reuniones'],
                ['coworking_space', 'Espacio de Coworking'],
                ['study_room', 'Sala de estudio'],
                ['gaming_room', 'Sala de juegos'],
                ['coffee_shop', 'Cafetería'],
                ['restaurant', 'Restaurant'],
                ['hotel_lobby', 'Lobby de hotel'],
                ['hotel_room', 'Cuarto de hotel'],
                ['hotel_bathroom', 'Baño de hotel'],
                ['auditorium', 'Auditorio'],
                ['classroom', 'Sala de clases'],
                ['fitness_gym_room', 'Sala de gimnasio'],
                ['clothing_store_room', 'Tienda de ropa']
                ]   
            #['Edificio de Oficinas', 'office_building'],
        }
    styles = {
                'name' : 'Estilo',
                'slug' : 'estilo',
                'type' : 'ratio',
                'items' : [
                    ['Cálida y acogedora', 'warm_and_cosy'],
                    ['Lujoso', 'luxurious'],
                    ['Minimalista', 'minimalist'],
                    ['Boho-chic', 'boho_chic'],
                    ['Neoclásico', 'neoclassic'],
                    ['Art Decó', 'art_deco'],
                    ['Art Nouveau', 'art_nouveau'],
                    ['IKEA', 'ikea'],
                    ['Biophilic', 'biophilic'],
                    ['Industrial', 'industrial'],
                    ['Japandi', 'japandi'],
                    ['Moderno', 'modern'],
                    ['Contemporáneo', 'contemporary'],
                    ['Ecléctico', 'eclectic'],
                    ['Wabi-sabi', 'wabi_sabi'],
                    ['Zen', 'zen'],
                    ['Costero', 'coastral'],
                    ['Mediterráneo', 'mediterranean'],
                    ['Shabby Chic', 'shabby_chic'],
                    ['Bauhaus', 'bauhaus'],
                    ['Futurista', 'futuristic'],
                    ['Faraónico', 'pharaonic'],
                    ['Tropical', 'tropical'],
                    ['Tribal', 'tribal'],
                    ['Rústico', 'rustic'],
                    ['Moderno de mediados de siglo', 'midcentury_modern'],
                    ['Maximalista', 'maximalist'],
                    ['Vintage', 'vintage'],
                    ['Medieval', 'medieval'],
                    ['Barroco', 'barroque'],
                    ['Halloween', 'halloween'],
                    ['Cyberpunk', 'cyberpunk'],
                    ['Navideño', 'chrismas']
                ]
        }
    
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
    
    context = {
        'name': 'Interior',
        'description': 'Sube un boceto o modelo para rediseñar tu espacio interior con más de 20 estilos únicos.',
        'controls' : [ living_room, styles, promptt, negative, models, aspectratio  ],
        'action' : '/interior/'
    }
    return render(request, 'GaudeSite/tool.html', context)  

@login_required
def exteriorImage(request):
    types_construction = {
            'name' : 'Tipo de construcción',
            'slug' : 'construction',
            'type' : 'ratio',
            'items' : [
                        ['Casa', 'house'],
                        ['Edificio', 'building'],
                        ['Cafeteria', 'coffe_shop'],
                        ['Fabrica', 'factory'],
                        ['Restaurant', 'restaurant'],
                        ['Hospital', 'hospital'],
                        ['Hotel', 'hotel'],
                        ['Libreria', 'library'],
                        ['Teatro', 'theater'],
                        ['Cine', 'cinema'],
                        ['Museo', 'museum'],
                        ['Centro Comercial', 'mall']
                    ]   
            #['Edificio de Oficinas', 'office_building'],
        }
    styles = {
                'name' : 'Estilo',
                'slug' : 'estilo',
                'type' : 'ratio',
                'items' : [
                    ['Realista', 'realistic'],
                    ['CGI', 'CGI'],
                    ['Night', 'night'],
                    ['Snow', 'snow'],
                    ['Rain', 'rain'],
                    ['sketch', 'sketch'],
                    ['watercolor', 'watercolor'],
                    ['illustration', 'illustration']
                ]
        }
    
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
        d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        context = {
            'imagenes_base64': imagenes_base64,
            'prompt': prompt
        }

        return render(request, 'GaudeSite/exterior.html', context) 

    context = {
        'name': 'Exterior',
        'description': 'Sube un boceto o modelo para rediseñar tu espacio exterior con más de 20 estilos únicos.',
        'controls' : [ types_construction, styles, promptt, negative, models, aspectratio  ],
        'action' : '/exterior/'
    }        
    return render(request, 'GaudeSite/tool.html', context)

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
        
            return render(request, 'GaudeSite/tools/interiorredecoration.html', context)
        
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
        
    return render(request, 'GaudeSite/tools/interiorredecoration.html')    
       
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

def login(request):
    return render(request, 'GaudeSite/login.html')

def register(request):
    return render(request, 'GaudeSite/register.html')

def imgbox():
    return render(request, 'GaudeSite/img-box.html')

def exit():
    logout()
    return redirect('/')

def exploreTools(request):
    return render(request, 'GaudeSite/explore-tools.html')

def prices(request):
    return render(request, 'GaudeSite/prices.html')
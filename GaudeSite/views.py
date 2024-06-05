from django.shortcuts import render, redirect
from django.http import HttpResponse
import base64
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings

import paypalrestsdk
from django.urls import reverse

from .payments import paypal_config

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

from .APIfunctions.dynamic_request      import call_api

promptt = {
            'name' : 'Añade detalles (Prompt)',
            'slug' : 'prompt',
            'type' : 'textarea',
            'value' : ''
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
image = {
                'name' : 'Imagen',
                'slug' : 'imagen',
                'type' : 'file'
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

@login_required
def sketchImg(request):
    if request.method == 'POST':

        detalles = request.POST.get('textoEjemplo')      
        imagen = request.FILES.get('imagen')

        if imagen:
            resultado = llamar_api_boceto(imagen, detalles)
            imagenes_base64 = bytes_to_base64(resultado)
            context = {
                'name': 'Renderización de dibujo o imagen',
                'description': 'Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
                'controls' : [ image ],
                'action' : '/sketchimg/',
                
                'imagenes_base64': imagenes_base64,
                       'detalles': detalles
            }
        
            return render(request, 'GaudeSite/tool.html', context)
        
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
    
    context = {
        'name': 'Renderización de dibujo o imagen',
        'description': 'Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
        'controls' : [ image ],
        'action' : '/sketchimg/'
    }        
    return render(request, 'GaudeSite/tool.html', context)

@login_required
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
        
    context = {
        'name': 'Remove Background',
        'description': 'Elimina el fondo de tu diseño',
        'controls' : [ image ],
        'action' : '/removebackground/'
    }        
    return render(request, 'GaudeSite/tool.html', context)

def masterPlan(request):
    styles = {
                'name' : 'Estilo',
                'slug' : 'estilo',
                'type' : 'ratio',
                'items' : [
                    ['MaterPlan', 'masterplan']
                ]
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
        'controls' : [ image, promptt, styles, negative ],
        'action' : '/masterplan/'
    }

    return render(request, 'GaudeSite/tool.html', context)

@login_required
def searchReplace(request):

    search = {
            'name' : 'Menciona lo que quieres cambiar en tu imagen',
            'slug' : 'seleccionar',
            'type' : 'textarea'
        }

    replace = {
            'name' : 'Menciona lo que quieres reemplazar en tu imagen',
            'slug' : 'replace',
            'type' : 'textarea'
        }

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
    
    context = {
        'name': 'Search Replace',
        'description': 'Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
        'controls' : [ image, search, replace ],
        'action' : '/searchreplace/'
    }
    return render(request, 'GaudeSite/tool.html', context)  

@login_required
def replaceStructure(request):
    replace = {
            'name' : 'Menciona lo que quieres reemplazar en tu imagen',
            'slug' : 'replace',
            'type' : 'textarea'
        }

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
    
    context = {
        'name': 'Replace Structure',
        'description': 'Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
        'controls' : [ image, replace ],
        'action' : '/replacestructure/'
    }
    return render(request, 'GaudeSite/tool.html', context)  

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
        room = request.POST.get('living_room')
        style = request.POST.get('estilo')
        aspect_ratio = request.POST.get('aspectratio')
        negative_prompt = request.POST.get('negative')
        model = request.POST.get('model')

        if prompt :
            promptt['value'] = prompt

        if room :
            living_room['value'] = room

        if style :
            styles['value'] = style
        
        if negative_prompt : 
            negative['value'] = negative_prompt
        
        if aspect_ratio :
            aspectratio['value'] = aspect_ratio
        
        if model :
            models['value'] = model
        

        final_prompt= "Create a stunning architectural image featuring a " + room + " in" + style + " style, capturing its essence and ambiance in vivid detail. The image must have " + prompt

        # 'aspect_ratio' : request.POST.get('aspectratio'),
        # 'model' : request.POST.get('model')

        resultado = llamar_api_interior(final_prompt, aspect_ratio, negative, model)
        imagenes_base64 = bytes_to_base64(resultado)

        context = {
            'name': 'Interior',
            'description': 'Sube un boceto o modelo para rediseñar tu espacio interior con más de 20 estilos únicos.',
            'controls' : [ living_room, styles, promptt, negative, models, aspectratio  ],
            'action' : '/interior/',
            'imagenes_base64': imagenes_base64,
            'prompt': prompt,
        }

        return render(request, 'GaudeSite/tool.html', context)   


    context = {
        'name': 'Interior',
        'description': 'Sube un boceto o modelo para rediseñar tu espacio interior con más de 20 estilos únicos.',
        'controls' : [ living_room, styles, promptt, negative, models, aspectratio  ] ,
        'action' : '/interior/'
    }
    return render(request, 'GaudeSite/tool.html', context)  

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
    controls = [ types_construction, styles, promptt, negative, models, aspectratio  ]
    if request.method == 'POST':
        
        prompt = request.POST.get('prompt')
        construction = request.POST.get('select1')
        style = request.POST.get('select2')
        aspect_ratio = request.POST.get('select3')
        negative_prompt = request.POST.get('negative_prompt')
        model = request.POST.get('select6')
        
        #final_prompt= "Create a stunning architectural an image from the exterior featuring a " + construction + " in" + style + " style, capturing its essence and ambiance in vivid detail. The construction must have " + prompt       
        final_prompt= "Create a stunning architectural an image from the exterior featuring a"
        resultado = llamar_api_exterior(final_prompt, aspect_ratio, negative_prompt, model)        
        imagenes_base64 = bytes_to_base64(resultado)
        d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        context = {
            'name': 'Exterior',
            'description': 'Sube un boceto o modelo para rediseñar tu espacio exterior con más de 20 estilos únicos.',
            'controls' : [ types_construction, styles, promptt, negative, models, aspectratio  ],
            'action' : '/exterior/',
            'imagenes_base64': imagenes_base64,
            'prompt': prompt
        }

        return render(request, 'GaudeSite/tool.html', context) 

    context = {
        'name': 'Exterior',
        'description': 'Sube un boceto o modelo para rediseñar tu espacio exterior con más de 20 estilos únicos.',
        'controls' : controls,
        'action' : '/exterior/'
    }        
    return render(request, 'GaudeSite/tool.html', context)

@login_required
def outPaint(request):

    left = {
        'name' : 'left',
        'slug' : 'left',
        'type' : 'range'
        }

    right = {
        'name' : 'right',
        'slug' : 'right',
        'type' : 'range'
        }

    up = {
        'name' : 'up',
        'slug' : 'up',
        'type' : 'range'
        }

    down = {
        'name' : 'down',
        'slug' : 'down',
        'type' : 'range'
        }
  
  
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
    
    context = {
        'name': 'Ampliaciones',
        'description': 'Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
        'controls' : [ image, left, right, up, down ],
        'action' : '/outpaint/'
    }        
    return render(request, 'GaudeSite/tool.html', context)

@login_required 
def interiorRedecoration(request):
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
               
        imagen = request.FILES.get('imagen')
        prompt = request.POST.get('textoEjemplo')
        style = request.POST.get('select2')
        negative_prompt = request.POST.get('textoEjemplo2')
        seedd = request.POST.get('seed')
        
        full_prompt = f"""
            Redesing the image in the {style} style, 
            taking into account the following details: "{prompt}". 
            As an expert interioir designer, ensure the design reflects your expertise
            and creativity.
        """

        if imagen:
            resultado = llamar_api_interiorRedecoration(imagen, full_prompt, negative_prompt, seedd)
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
        
    context = {
        'name': 'Interior',
        'description': 'Sube un boceto o modelo para rediseñar tu espacio interior con más de 20 estilos únicos.',
        'controls' : [ image, promptt, styles, negative, seed ],
        'action' : '/interiorredecoration/'
    }
    return render(request, 'GaudeSite/tool.html', context) 

@login_required    
def landScape(request):
    types = {
                'name' : 'Tipo de espacio',
                'slug' : 'type-spot',
                'type' : 'ratio',
                'items': [
                    ['Patio interior', 'backyard'],
                    ['Entrada del edificio', 'building_entrance'],
                    ['Patio', 'courtyard'],
                    ['Piscina', 'swimming_pool'],
                    ['Jardín exterior', 'outdoor_garden'],
                    ['Paisaje de club', 'club_landscape'],
                    ['Parque', 'park'],
                    ['Paseo peatonal', 'pedestrian_promenade']
                ]
        }
    styles = {
                'name' : 'Estilo de espacio',
                'slug' : 'style-spot',
                'type' : 'ratio',
                'items': [
                    ['Moderno', 'modern'],
                    ['Tropical', 'tropical'],
                    ['Contemporáneo', 'contemporary'],
                    ['Toscano', 'tuscan'],
                    ['Jardín japonés', 'japanese_garden'],
                    ['Jardín inglés', 'english_garden'],
                    ['Jardín francés', 'french_garden'],
                    ['Rústico', 'rustic'],
                    ['Pradera', 'prairie'],
                    ['Boscoso', 'woodland'],
                    ['Español', 'spanish'],
                    ['Costero', 'coastal'],
                    ['Minimalista', 'minimalist'],
                    ['Cálido y acogedor', 'warm_and_cosy']
                ]
        }    

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
        
    context = {
        'name': 'Paisajismo',
        'description': 'Genera un proyecto de paisajismo, a partir solamente de un esquema o fotografía',
        'controls' : [ image, promptt, types, styles, negative ],
        'action' : '/landscape/'
    }
    return render(request, 'GaudeSite/tool.html', context)

@login_required 
def upScale(request):
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        negative_prompt = request.POST.get('textoEjemplo2')
        prompt = request.POST.get('textoEjemplo')
        seedd = request.POST.get('seed')
        
        if imagen:
            resultado = llamar_api_upscale(imagen, prompt, negative_prompt, seedd)
            imagenes_base64 = bytes_to_base64(resultado)
            context = {
                'imagenes_base64': imagenes_base64,
            }
        
            return render(request, 'GaudeSite/upscale.html', context)
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
        
    context = {
        'name': 'Upscale',
        'description': 'Cree una versión de mayor resolución de una imagen de entrada.',
        'controls' : [ image, promptt, negative, seed ],
        'action' : '/upscale/'
    }
    return render(request, 'GaudeSite/tool.html', context)

def login(request):
    return render(request, 'registration/login.html')

def register(request):
    return render(request, 'registration/register.html')

def imgbox():
    return render(request, 'GaudeSite/img-box.html')

def exit():
    logout()
    return redirect('/')

def exploreTools(request):
    context = {
        'URL_BASE' : settings.URL_BASE
    }
    return render(request, 'GaudeSite/explore-tools.html')

def prices(request):
    return render(request, 'GaudeSite/prices.html')

def create_payment(request):
    if request.method == "POST":
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('execute_payment')),
                "cancel_url": request.build_absolute_uri(reverse('payment_cancelled')),
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Suscripción Starter",
                        "sku": "12345",
                        "price": "20.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "20.00",
                    "currency": "USD"
                },
                "description": "Compra de Suscripción Starter."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            return render(request, 'GaudeSite/payments/payment_error.html', {'error': payment.error})

    return render(request, 'GaudeSite/payments/payment.html')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'GaudeSite/payments/payment_success.html')
    else:
        return render(request, 'GaudeSite/payments/payment_error.html', {'error': payment.error})

def payment_cancelled(request):
    return render(request, 'GaudeSite/payments/payment_cancelled.html')

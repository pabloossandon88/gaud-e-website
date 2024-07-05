from django.shortcuts import render, redirect
from django.http import HttpResponse
import base64
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings

from django.core.cache import cache

import paypalrestsdk
from django.urls import reverse

from .payments import paypal_config

# Import API functions
from .APIfunctions.image_generation_api import llamar_api
from .APIfunctions.remove_back          import llamar_api_remove_back
from .APIfunctions.sketch_image         import llamar_api_boceto
from .APIfunctions.master_plan          import llamar_api_masterplan
#from .APIfunctions.interior             import llamar_api_interior
from .APIfunctions.exterior             import llamar_api_exterior
from .APIfunctions.searchReplace        import llamar_api_replace
from .APIfunctions.replaceStructure     import llamar_api_replace_structure
from .APIfunctions.outpaint             import llamar_api_outpaint
from .APIfunctions.interiorRedecoration import llamar_api_interiorRedecoration
from .APIfunctions.upscale              import llamar_api_upscale

from .APIfunctions.dynamic_request      import call_api, call_api_image, validateRequestPost

from .models import UserProfile

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
styles_interior = {
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
styles_exterior = {
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
styles_masterPlan = {
                'name' : 'Estilo',
                'slug' : 'estilo',
                'type' : 'ratio',
                'items' : [
                    ['MaterPlan', 'masterplan']
                ]
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


#TOOLS

def set_controls_value(request, controls):
    #reescribo los valores que se veran en los input
    for index, control in enumerate(controls):
        if request.POST.get(control['slug']):
            controls[index]['value'] = request.POST.get(control['slug'])
    return controls

def interiorImage(request):

    context = {
        'name': 'Interior',
        'description': 'Sube un boceto o modelo para rediseñar tu espacio interior con más de 20 estilos únicos.',
        'controls' : [ living_room, styles_interior, promptt, negative, models, aspectratio  ] ,
        'action' : '/interior/'
        }

    if request.method == 'POST':
        context['controls'] = set_controls_value(request, context['controls'])
        
        #AQUI SI CAMBIARA SEGUN LA HERRAMIENTA
        final_prompt = f"""
            Create a stunning architectural image featuring a 
            "{context['controls'][0].get('value', 'Unspecified')}" in  
            "{context['controls'][1].get('value', 'Unspecified')}" style, capturing its essence and ambiance in vivid detail. The image must have  
            "{context['controls'][2].get('value', 'Unspecified')}" 
        """

        params = {
            'final_prompt' : final_prompt, 
            'aspect_ratio' : context['controls'][5].get('value', ''),
            'negative' : context['controls'][3].get('value', ''), 
            'model' : context['controls'][4].get('value', '')
        }

        #Generacion imagen -> llamado a API
        context['imagenes_base64'] = bytes_to_base64( call_api(params) )

    return render(request, 'GaudeSite/tool.html', context)  

def exteriorImage(request):
    context = {
        'name': 'Exterior',
        'description': 'Sube un boceto o modelo para rediseñar tu espacio exterior con más de 20 estilos únicos.',
        'controls' : [ types_construction, styles_exterior, promptt, negative, models, aspectratio  ],
        'action' : '/exterior/'
    }  

    if request.method == 'POST':
        context['controls'] = set_controls_value(request, context['controls'])

        #AQUI SI CAMBIARA SEGUN LA HERRAMIENTA
        final_prompt = f"""
            Create a stunning architectural an image from the exterior featuring a
            "{context['controls'][0].get('value', 'Unspecified')}" in  
            "{context['controls'][1].get('value', 'Unspecified')}" style, capturing its essence and ambiance in vivid detail. The construction must have  
            "{context['controls'][2].get('value', 'Unspecified')}" 
        """

        params = {
            'final_prompt' : final_prompt, 
            'aspect_ratio' : context['controls'][5].get('value', ''),
            'negative' : context['controls'][3].get('value', ''), 
            'model' : context['controls'][4].get('value', '')
        }

        context['imagenes_base64'] = bytes_to_base64( call_api(params) )
    
    return render(request, 'GaudeSite/tool.html', context)

def masterPlan(request):
    context = {
        'name': 'Master Plan',
        'description': 'Genera un loteo o un condominio en 3D, a partir solamente de un esquema o fotografía. Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
        'controls' : [ image, promptt, styles_masterPlan, negative ],
        'action' : '/masterplan/'
    }

    if request.method == 'POST':
        context['controls'] = set_controls_value(request, context['controls'])

        imagen = request.FILES.get('imagen')

        if imagen:
            final_prompt = f"""
                "{context['controls'][2].get('value', 'Unspecified')}"   
                "{context['controls'][1].get('value', 'Unspecified')}" 
             """

            params = {
                'final_prompt' : final_prompt, 
                #'aspect_ratio' : context['controls'][5].get('value', ''),
                'negative' : context['controls'][3].get('value', ''), 
                #'model' : context['controls'][4].get('value', '')
             }

            context['imagenes_base64'] = bytes_to_base64( call_api_image(imagen, params ) )
    
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)       
    
    

    return render(request, 'GaudeSite/tool.html', context)
    
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

    context = {
        'name': 'Paisajismo',
        'description': 'Genera un proyecto de paisajismo, a partir solamente de un esquema o fotografía',
        'controls' : [ image, promptt, types, styles, negative ],
        'action' : '/landscape/'
    }

    if request.method == 'POST':
        context['controls'] = set_controls_value(request, context['controls'])

        imagen = request.FILES.get('imagen')

        if imagen:
            final_prompt = f"""
                Create a "{context['controls'][2].get('value', 'Unspecified')}" _espacio Landscape in the "{context['controls'][2].get('value', 'Unspecified')}" style, 
                taking into account the following details: "{context['controls'][1].get('value', 'Unspecified')}". 
                As an expert architect, ensure the design reflects your expertise
                and creativity.
             """

            params = {
                'final_prompt' : final_prompt, 
                #'aspect_ratio' : context['controls'][5].get('value', ''),
                'negative' : context['controls'][3].get('value', ''), 
                #'model' : context['controls'][4].get('value', '')
             }

            context['imagenes_base64'] = bytes_to_base64( call_api_image(imagen, params ) )
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)

    return render(request, 'GaudeSite/tool.html', context)

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
  
    context = {
        'name': 'Ampliaciones',
        'description': 'Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
        'controls' : [ image, left, right, up, down ],
        'action' : '/outpaint/'
    }

    if request.method == 'POST':
        context['controls'] = set_controls_value(request, context['controls'])

        imagen = request.FILES.get('imagen')

        if imagen:
            final_prompt = f"""
                Visualize an expansion for the provided image. The expansion should adjust the structure based on the following dimensions:
                - Left: {context['controls'][1].get('value', 0)} units
                - Right: {context['controls'][2].get('value', 0)} units
                - Up: {context['controls'][3].get('value', 0)} units
                - Down: {context['controls'][4].get('value', 0)} units
                Ensure the expansion integrates seamlessly with the existing architectural style and enhances the overall design.
             """

            params = {
                'final_prompt' : final_prompt, 
                #'aspect_ratio' : context['controls'][5].get('value', ''),
                'negative' : '', 
                #'model' : context['controls'][4].get('value', '')
             }

            context['imagenes_base64'] = bytes_to_base64( call_api_image(imagen, params ) )
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
  
            
    return render(request, 'GaudeSite/tool.html', context)

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
    
    context = {
        'name': 'Interior',
        'description': 'Sube un boceto o modelo para rediseñar tu espacio interior con más de 20 estilos únicos.',
        'controls' : [ image, promptt, styles, negative, seed ],
        'action' : '/interiorredecoration/'
    }

    if request.method == 'POST':
        context['controls'] = set_controls_value(request, context['controls'])

        imagen = request.FILES.get('imagen')

        if imagen:
            final_prompt = f"""
                Redesing the image in the {context['controls'][2].get('value', 'Unspecified')} style, 
                taking into account the following details: {context['controls'][1].get('value', 'Unspecified')} . 
                As an expert interioir designer, ensure the design reflects your expertise
                and creativity.
             """

            params = {
                'final_prompt' : final_prompt, 
                #'aspect_ratio' : context['controls'][5].get('value', ''),
                'negative' : '', 
                #'model' : context['controls'][4].get('value', '')
             }

            context['imagenes_base64'] = bytes_to_base64( call_api_image(imagen, params ) )
        else:
            error_message = "No se ha subido ninguna imagen."
            return HttpResponse(error_message)
  
    
    return render(request, 'GaudeSite/tool.html', context) 

def sketchImg(request):
    context = {
        'name': 'Renderización de dibujo o imagen',
        'description': 'Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
        'controls' : [ image ],
        'action' : '/sketchimg/'
    }  

    if request.method == 'POST':
        context['controls'] = set_controls_value(request, context['controls'])

        imagen = request.FILES.get('imagen')

        if imagen:
            

            params = {
                'final_prompt' : '', 
                #'aspect_ratio' : context['controls'][5].get('value', ''),
                'negative' : '', 
                #'model' : context['controls'][4].get('value', '')
             }

            context['imagenes_base64'] = bytes_to_base64( call_api_image(imagen, params ) )

    return render(request, 'GaudeSite/tool.html', context)

@login_required
def replaceStructure(request):
    
    replace = {
        'name' : 'Menciona lo que quieres reemplazar en tu imagen',
        'slug' : 'replace',
        'type' : 'textarea'
    }

    context = {
        'name': 'Replace Structure',
        'description': 'Sube tu boceto o dibujo y conviértelo en un diseño arquitectónico de alta calidad.',
        'controls' : [ image, replace ],
        'action' : '/replacestructure/'
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

#def login(request):
    #return render(request, 'registration/login.html')

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

    pasareladepago = request.POST.get('xx')
    
    #PAY PAL 
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

                    amount = 20
                    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                    user_profile.credits += amount
                    user_profile.save()
                    
                    return redirect(link.href)
        else:
            return render(request, 'GaudeSite/payments/payment_error.html', {'error': payment.error})

    #MERCADO PAGO 
    
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        preference_data = {
            "items": [
                {
                    "title": "Producto de ejemplo",
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": 100.0
                }
            ],
            "back_urls": {
                "success": "http://localhost:8000/success",
                "failure": "http://localhost:8000/failure",
                "pending": "http://localhost:8000/pending"
            },
            "auto_return": "approved",
        }
        
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        #return redirect(preference['init_point'])

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


#Estos no sirven estan deshabilitados
@login_required
def add_credits_view(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        user_profile = request.user.userprofile
        user_profile.credits += amount
        user_profile.save()
        return redirect('some_view')

@login_required
def deduct_credits_view(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        user_profile = request.user.userprofile
        user_profile.credits -= amount
        user_profile.save()
        return redirect('some_view')


def clear_cache(request):
    cache.clear()
    return HttpResponse("Cache cleared")
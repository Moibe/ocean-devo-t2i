import bridges
import globales
import sulkuPypi
import sulkuFront
import gradio as gr
import gradio_client
import time
import tools
from huggingface_hub import InferenceClient
import random
from PIL import Image
import fireWhale

mensajes, sulkuMessages = tools.get_mensajes(globales.mensajes_lang)

btn_buy = gr.Button("Get Credits", visible=False, size='lg')

#PERFORM es la app INTERNA que llamará a la app externa.
def perform(input1, request: gr.Request):

    if globales.acceso == "login": 
        usuario = request.username
    else:        
        usuario = globales.usuario     

    tokens = fireWhale.obtenDato('usuarios', usuario, 'tokens')
    
    #1: Reglas sobre autorización si se tiene el crédito suficiente.
    autorizacion = sulkuPypi.authorize(tokens, globales.work)
    if autorizacion is True:
        try: 
            resultado = mass(input1)
        except Exception as e:
            print("Éste es el except de perform...")            
            info_window, resultado, html_credits = sulkuFront.aError(usuario, tokens, excepcion = tools.titulizaExcepDeAPI(e))
            return resultado, info_window, html_credits, btn_buy
    else:
        info_window, resultado, html_credits = sulkuFront.noCredit(usuario)
        return resultado, info_window, html_credits, btn_buy 

    #Primero revisa si es imagen!: 
    if isinstance(resultado, Image.Image) or "image.webp" in str(resultado):
        #Si es imagen, debitarás.
        html_credits, info_window = sulkuFront.presentacionFinal(usuario, "debita")
    else: 
        #Si no es imagen es un texto que nos dice algo.
        info_window, resultado, html_credits = sulkuFront.aError(usuario, tokens, excepcion = tools.titulizaExcepDeAPI(resultado))
        return resultado, info_window, html_credits, btn_buy      
            
    #Lo que se le regresa oficialmente al entorno.
    return resultado, info_window, html_credits, btn_buy

#MASS es la que ejecuta la aplicación EXTERNA
def mass(input1): #IMPORTANTE: Cuando estás entre Inferencia o API, en MASS es donde se decide.

    api, tipo_api = tools.eligeAPI(globales.seleccion_api)
    
    #Si tipo API es inferencia ve directo a las nuevas formas de Inferencia.

    if tipo_api == "inferencia": 

        client = InferenceClient(
        provider= globales.inference_provider,
        api_key=bridges.hug
    ) 
        
        try: 
            image = client.text_to_image(
            input1,
            model="black-forest-labs/FLUX.1-dev",
            #seed=42, #default varía pero el default es que siempre sea la misma.
            #guidance_scale=7.5,
            #num_inference_steps=50,
            #width=1024, #El default es 1024 x 1024 y quizá 1024*768, el max es 1536. 
            #height=1024 #El límite de replicate es 1024.
        )              
            
            return image

        except Exception as e:
                #La no detección de un rostro es mandado aquí?! Siempre?
                mensaje = tools.titulizaExcepDeAPI(e)        
                return mensaje
        
    else: #Si no es inferencia entonces usa API tradicional:

        client = gradio_client.Client(api, hf_token=bridges.hug)

        try:  

            result = client.predict(
            prompt=input1,
            seed=42,
            randomize_seed=True,
            width=1024,
            height=1024,
            guidance_scale=3.5,
            num_inference_steps=28,
            api_name="/infer"
            )
            print(f"Esto es el result via API: {result} y su tipo es: {type(result)}...")

            #(Si llega aquí, debes debitar de la quota, incluso si detecto no-face o algo.)
            if tipo_api == "quota": #IMPORTANTE: En inferencia llamaremos quota a la quota de inferencia que tenemos.
                #print("Como el tipo api fue gratis, si debitaremos la quota.")
                quota_actual = fireWhale.obtenDato("quota", "quota", "segundos")
                print("La quota actual que hay es: ", quota_actual)
                quota_nueva = quota_actual - globales.process_cost
                print("La quota nueva es: ", quota_nueva)
                fireWhale.editaDato("quota", "quota", "segundos", quota_nueva)
                
            result = tools.desTuplaResultado(result)
            return result 

        except Exception as e:
                #La no detección de un rostro es mandado aquí?! Siempre?
                mensaje = tools.titulizaExcepDeAPI(e)        
                return mensaje
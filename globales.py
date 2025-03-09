import gradio as gr

#MAIN
version = "2.2.1"
env = "dev"
aplicacion = "t2i-dev"

seleccion_api = "eligeQuotaOCosto" #eligeGratisOCosto , eligeAOB o eligeGratisOCosto
max_size = 20

#Quota o Costo
api_zero = ("black-forest-labs/FLUX.1-dev", "quota")
api_cost = ("models/black-forest-labs/FLUX.1-dev", "inferencia") #Cuando es inferencia es realidad es un don't care el nombre de la instancia.

inference_provider = "fal-ai" #"hf-inference", "fal-ai", "together", "replicate"  --> Los otros proveedores si son más veloces.

interface_api_name = "/predict" #El endpoint al que llamará client.

process_cost = 90 #Expresado en segundos para que los deduzca de la quota.
seto = "txt2image"
work = "picswap"
costo_work = 1 #Se integró costo_work para definir aquí directamente lo que cueta picswap, y dejar de usar la var work.
app_path = "/t2i"
server_port=1111
#tema = tools.theme_selector()
tema = gr.themes.Default()
flag = "never"

neural_wait = 3
mensajes_lang = "es"

#Access related
acceso = "libre"  #login, metrado o libre, login para medición y acceso normal, metrado para no usar login pero si medir los créditos, para eso se utilizará el parámetro global de usuario, y libre no tiene login ni metrado.
#Recuerda que si el acceso es login, entonces en app debe estar seleccionada la opción de usar auth.
usuario = "ella"
credits_visibility = False
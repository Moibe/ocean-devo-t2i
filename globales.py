import gradio as gr

#MAIN
version = "1.0.0"
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
app_path = "/t2i"
server_port=7860
#tema = tools.theme_selector()
tema = gr.themes.Default()
flag = "never"

#Future: Put age to cookies.

neural_wait = 3
mensajes_lang = "es"
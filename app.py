import inputs
import globales
import funciones
import sulkuFront
import autorizador
import gradio as gr

def iniciar():    
    app_path = globales.app_path
    main.queue(max_size=globales.max_size)
    #Con autorizador
    #main.launch(auth=autorizador.authenticate, root_path=app_path, server_port=globales.server_port)
    #Paso directo 
    main.launch(root_path=app_path, server_port=globales.server_port)
    
#INTERFAZ
#Credit Related Elements
html_credits = gr.HTML(visible=globales.credits_visibility)
lbl_console = gr.Label(label="AI Terminal " + globales.version +  " messages", container=True)
btn_buy = gr.Button("Get Credits", visible=False, size='lg')

#Customizable Inputs and Outputs
#Los valores que recibe si debes de agregarlos manualmente para cada app que hagas.
input1, result = inputs.inputs_selector(globales.seto)

with gr.Blocks(theme=globales.tema, css="footer {visibility: hidden}") as main:   
    #Cargado en Load: Función, input, output
    main.load(sulkuFront.precarga, None, html_credits) if globales.acceso != "libre" else None
   
    with gr.Row():
        try:
            demo = gr.Interface(
                fn=funciones.perform,
                inputs=[input1], #Agregar inputs manualmente.
                outputs=[result, lbl_console, html_credits, btn_buy], 
                flagging_mode=globales.flag            
                )
        except Exception as e:
            print("Interface error...") #Checar si alguna vez entra.
        
iniciar()
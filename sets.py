import gradio as gr
import globales
import tools

mensajes, sulkuMessages = tools.get_mensajes(globales.mensajes_lang)

# Diccionario para mapear los sets a sus respectivas configuraciones
configuraciones = {    
    "txt2image": {
        "input1": gr.Textbox(label=mensajes.label_input1),
        "result": gr.Image(label=mensajes.label_resultado, type="filepath"),
    }
}
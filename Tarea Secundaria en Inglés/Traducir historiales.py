import json
from openai import OpenAI
import os

def get_completion(messages, model="gpt-3.5-turbo",temperature=0):
    cliente=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = cliente.chat.completions.create(
    model=model,
    messages=messages,
    temperature=temperature
    )
    return(response.choices[0].message.content)

with open("train_v2.json") as archivo:
        datos=json.load(archivo)

'''for i in range(0,len(datos["lista"])):
    historiales_traducidos=[]
    prompt='Eres un traductor y debes traducir este historial al inglés:'
    messages =  [  
                        {'role':'system', 'content':prompt},    
                        {'role':'user', 'content':str(datos["lista"][i])}]
                    
                    
    response=get_completion(messages)
    historiales_traducidos.append(response)
json_final={'lista':historiales_traducidos,'num':(datos["num"])}
with open("Historiales médicos ingles.json", "w") as outfile: 
    json.dump(json_final, outfile)'''
prompt='Eres un traductor y debes traducir este texto al inglés:'
lista_conversaciones=[]
for i in range(50,98):
    preguntas=[]
    respuestas=[]
    for qa in datos["data"][i]["paragraphs"][0]["qas"]:
        pregunta = qa['question']
        preguntas.append(pregunta)
        respuesta = qa['answers'][0]['text'] if qa['answers'] else 'No se menciona en el historial medico.'  # Tomamos la primera respuesta o un string vacío si no hay respuesta
        respuestas.append(respuesta)

    preguntas_y_respuestas = zip(preguntas, respuestas)
    preguntas_y_respuestas_ordenadas = sorted(preguntas_y_respuestas, key=lambda x: int(x[0].split('#')[0].split(' ')[0]))

    # Obtener las preguntas y respuestas ordenadas y limpias
    preguntas_ordenadas = [pregunta.split('#', 1)[1].strip() for pregunta, _ in preguntas_y_respuestas_ordenadas]
    respuestas_ordenadas = [respuesta for _, respuesta in preguntas_y_respuestas_ordenadas]

    historial_medico=datos["data"][i]["paragraphs"][0]["context"]
    messages =  [  
            {'role':'system', 'content':prompt},    
            {'role':'user', 'content':historial_medico}]
        
        
    historial_traducido=get_completion(messages)
    #text_file.write('El número de la entrevista es: '+str(entrevista)+'\n')
    #text_file.write(historial_medico+'\n')
    
    j=0
    lista_preguntas=[]
    for pregunta in preguntas_ordenadas:
        
        messages =  [  
            {'role':'system', 'content':prompt},    
            {'role':'user', 'content':pregunta}]
        
        
        pregunta_Trad=get_completion(messages)
        print(pregunta_Trad)
        
        messages =  [  
            {'role':'system', 'content':prompt},    
            {'role':'user', 'content':respuestas_ordenadas[j]}]
        

        #Respuesta que nos da Chatgpt    
        
        #Respuesta real del paciente en la entrevista original
        respuesta_Trad=get_completion(messages)
        print(respuesta_Trad)

        caso_pregunta_respuesta={'pregunta':pregunta_Trad,'respuesta':respuesta_Trad}
        lista_preguntas.append(caso_pregunta_respuesta)
        j+=1

    conversacion={'Historial':historial_traducido,'lista_preguntas':lista_preguntas}
    lista_conversaciones.append(conversacion)
    print("CONVERSACION AÑADIDA")
json_final={'lista_conversaciones':lista_conversaciones,'numero Conversaciones':49}
with open("Datos_entrada_Ingles_50-98.json", "w") as outfile: 
        json.dump(json_final, outfile)

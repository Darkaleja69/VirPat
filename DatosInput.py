import json
import os

with open("train_v2.json" ) as archivo:
    datos1=json.load(archivo)
with open("dev_v2.json" ) as archivo:
    datos2=json.load(archivo)
with open("test_v2.json" ) as archivo:
    datos3=json.load(archivo)   

media_historial=0
total_historiales=0
media_preguntas=0
total_preguntas=0
SumaTotal_PreguntasRespuestas=0
i=0
lista_json=[datos1,datos2,datos3]
for datos in lista_json:
    for entrevista in datos["data"]:
        preguntas = []
        respuestas = []
        for qa in entrevista["paragraphs"][0]["qas"]:
            pregunta = qa['question']
            preguntas.append(pregunta)
            respuesta = qa['answers'][0]['text'] if qa['answers'] else ''  # Tomamos la primera respuesta o un string vacío si no hay respuesta
            respuestas.append(respuesta)
        
        historial_medico=entrevista["paragraphs"][0]["context"]
        total_historiales+=len(historial_medico)
        total_preguntas+=len(preguntas)
        SumaTotal_PreguntasRespuestas=SumaTotal_PreguntasRespuestas+len(preguntas)+len(respuestas)
        i+=1
        print("Total preguntas "+str(i)+" "+str(total_preguntas))
        print("Total historiales "+str(i)+" "+str(total_historiales))

media_historial=total_historiales/i
media_preguntas=total_preguntas/i

print("Media historiales "+str(media_historial))
print("Media preguntas "+str(media_preguntas))
print("Suma de Preguntas y respuestas "+str(SumaTotal_PreguntasRespuestas))


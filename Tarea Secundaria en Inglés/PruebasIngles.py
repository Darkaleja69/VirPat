import os
from sys import exit, argv
from getopt import getopt,GetoptError
from openai import OpenAI
import datetime
import json
import evaluate
from tabulate import tabulate
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

INPUT_FILE    = "Datos_entrada_Ingles_50-98.json" # Path del archivo con la información necesaria de input(historial medico, entrevistas)
OUTPUT_RESULTS    = "resultadosIngles50-98.txt" 

def get_completion(messages, model="gpt-3.5-turbo",temperature=0):
    cliente=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = cliente.chat.completions.create(
    model=model,
    messages=messages,
    temperature=temperature
    )
    return(response.choices[0].message.content)

def prompt_utilizado():
    with open('prompt.json') as archivo:
        json_string=json.load(archivo)
    prompt=json_string["2"]
    print(prompt)
    return prompt
bleu = evaluate.load('bleu')

text_file = open(OUTPUT_RESULTS, "a")

with open(INPUT_FILE) as archivo:
    datos=json.load(archivo)
prompt=prompt_utilizado()
fscore_total=0
text_file = open(OUTPUT_RESULTS, "a")
text_file.write("PRUEBAS: "+str(datetime.datetime.now()))
z=0
while(z<len(datos["lista_conversaciones"])):
    print("Inicio bucle ")
    j=0
    while (j<10):
        text_file.write("----------------------------------------------------------------------------------------------------\n")
        j+=1
    # Obtener las preguntas del JSON y eliminar el número y el hashtag
    
    preguntas = []
    respuestas = []
    print("Prueba "+str(z))
    for qa in datos["lista_conversaciones"][z]["lista_preguntas"]:
        pregunta = qa['pregunta']
        preguntas.append(pregunta)
        respuesta = qa['respuesta']
        respuestas.append(respuesta)

    historial_medico=datos["lista_conversaciones"][z]["Historial"]
    print(historial_medico)
    contexto=historial_medico+'\n'+prompt
    #text_file.write('El número de la entrevista es: '+str(entrevista)+'\n')
    #text_file.write(historial_medico+'\n')
    
    i=0
    suma=0
    media_total=0
    score_questions_cant_find_answers=0
    total_questions_cant_find_answers=0
    score_questions_no_need_answers=0
    total_questions_no_need_answers=0
    total_questions_with_answers=0
    score_questions_with_answers=0
    
    for pregunta in preguntas:
        print(pregunta)
        messages =  [  
            {'role':'system', 'content':contexto},    
            {'role':'user', 'content':pregunta}]
        
        
        response=get_completion(messages)
        

        

        #Respuesta que nos da Chatgpt    
        predictions = [response]
        #Respuesta real del paciente en la entrevista original
        references = [
                [respuestas[i]]
        ]
        
        #Prueba minBleu
        #print("Predictions solo primer campo: \n"+predictions[0])
        #En los casos en los que en la entrevista no hay respuesta cambiamos "" por No se menciona para que se pueda evaluar correctamente.
        
        
        # Para evaluar tiene que haber un mínimo de carácteres por eso modificamos ambos
        if references[0]==['I']:
            references[0]="I I I I"
        if predictions[0]=="I":
            predictions[0]="I I I I"

        #Eliminar el punto final para equiparar las dos respuestas y hacer la evaluación lo más justa posible.    
        if predictions[0][-1]=="." and references[0][0][-1]==".":
            predictions[0]=predictions[0][:-1]
            references[0][0]=references[0][0][:-1]
        elif predictions[0][-1]==".":
            
            predictions[0]=predictions[0][:-1]
        elif references[0][0][-1]=='.':
            references[0][0]=references[0][0][:-1]
            
        results = bleu.compute(predictions=predictions, references=references, max_order = 2)
        print(predictions[0])
        print(results["bleu"])
        print(references[0][0])
        #text_file = open(OUTPUT_RESULTS, "a")
        #text_file.write("\n-----------------------------------------\n")
        #text_file.write("(Q)-"+str(pregunta)+ "\n(A)-"+str(predictions[0])+"\n(Real answer)"+str(references[0][0])+"\n"+str(results)+"\n")
        #Solo guardamos las preguntas y respuestas dentro del contexto si superan el límite de 0.3
        '''if results["bleu"]>=MIN_BLEU:
            contexto=contexto+'\n(Q)-'+pregunta+'\n(A)-'+predictions[0]+'\n' '''
            #print(contexto)

        if(references[0][0]=='It is not mentioned in the medical record'):
            
            if(predictions[0]=="It is not mentioned in the medical record"):
                score_questions_cant_find_answers+=1
                
            total_questions_cant_find_answers+=1
        
        elif(references[0]=="I I I I"):
            if(predictions[0]=="I I I I"):
                score_questions_no_need_answers+=1
            total_questions_no_need_answers+=1
        else:
            total_questions_with_answers+=1
            score_questions_with_answers+=results["bleu"]
        
        
        suma=suma+results["bleu"]

        i=i+1
    
    if(total_questions_cant_find_answers>0):
        score_questions_cant_find_answers=score_questions_cant_find_answers/total_questions_cant_find_answers
    if (total_questions_no_need_answers>0):
        score_questions_no_need_answers=score_questions_no_need_answers/total_questions_no_need_answers
    
    score_questions_with_answers=score_questions_with_answers/total_questions_with_answers
    media_total=suma/len(preguntas)

    dataforTableResults=[
        ["Questions that don't appear in the text: ",str(total_questions_cant_find_answers),str(score_questions_cant_find_answers)],
        ["Questions that don't require an answer: ",str(total_questions_no_need_answers),str(score_questions_no_need_answers)],
        ["Questions that have answer",str(total_questions_with_answers),str(score_questions_with_answers)],
        ["Total",str(i),str(media_total)]
    ]
    dataforVariables=[
        ["Num of interview: ",str(z)],
        ["Temperature for the chatGpt ","0"],
    ]
    
    headResults=["     ","Num of questions","F-Score"]
    headVariables=["Type of variable",""]
    
    print("Tabla va")
    text_file.write("----------------------------------------------------------------------------------------------------\n")
    text_file.write("----------------------------------------------------------------------------------------------------\n")
    text_file.write(tabulate(dataforTableResults,headers=headResults,tablefmt="grid"))
    text_file.write(tabulate(dataforVariables,headers=headVariables,tablefmt="grid"))
    text_file.write("----------------------------------------------------------------------------------------------------\n")
    text_file.write("----------------------------------------------------------------------------------------------------\n")
    #text_file.write("Contexto final: \n"+contexto)

    fscore_total=media_total+fscore_total
    z+=1
    print("Fin bucle")

fscore_total=fscore_total/z
dataFscore=[
            ["F-score prueba: "+str(fscore_total)]
        ]
headFscore=["   ","     "]
text_file.write(tabulate(dataFscore,headers=headFscore,tablefmt="grid"))


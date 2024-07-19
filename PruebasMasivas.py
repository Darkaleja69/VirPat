import os
from sys import exit, argv
from getopt import getopt,GetoptError
from openai import OpenAI
import datetime
import json
import evaluate
from tabulate import tabulate
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type


  # for exponential backoff
# Variables globales
OUTPUT_RESULTS    = "/pruebas/resultadosDemo.txt"             # Fichero donde se imprimen los resultados de las pruebas
INPUT_FILE    = "train_v2.json" # Path del archivo con la información necesaria de input(historial medico, entrevistas)
MIN_TEMPERATURE= 0                                  #Parámetro de aleatoriedad de chatGPT
MAX_TEMPERATURE= 1                                  #Parámetro de aleatoriedad de chatGPT
PROMPT=False                                         # Prompt a utilizar: True si es en 1ªpersona, False si es extractivo
MIN_BLEU= 1                                         #Bleu necesario para que la pregunta y respuesta se introduzca en el contexto


temperatura=0
#Código para modelo 3.5 turbo

def get_completion(messages, model="gpt-3.5-turbo",temperature=temperatura):
    cliente=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = cliente.chat.completions.create(
    model=model,
    messages=messages,
    temperature=temperature
    )
    
    return(response.choices[0].message.content)

#Código para modelo 3.5 turbo instruct
'''def get_completion_instruct(messages,model="gpt-3.5-turbo-instruct",temperature=temperatura):
    openai.api_key=os.environ["OPENAI_API_KEY"]
    response=openai.Completion.create(
        model=model,
        prompt=messages,
        temperature=temperature,
    )
    return response.choices[0].text
'''
def crear_archivos_con_entrevistas(data):
    i=0
    lista_historiales=[]
    num_conv=len(data["data"])
    while i in range(0,num_conv):
        historial=data["data"][i]["paragraphs"][0]["context"]
        lista_historiales.append({str(i):historial})
        i=i+1
    json_final={'lista':lista_historiales,'num':num_conv}
    with open("Historiales médicos test.json", "w") as outfile: 
        json.dump(json_final, outfile)

def prompt_utilizado():
    with open('prompt.json') as archivo:
        json_string=json.load(archivo)
    if PROMPT:
        prompt=json_string["1"]
    else:
        prompt=json_string["0"]
    print(prompt)
    return prompt


def usage():
    # PRE: ---
    # POST: se imprime por pantalla la ayuda del script y salimos del programa
    print("Usage: PruebasMasivas.py <optional-args>")
    print("The options supported by pruebas Masivas are:")
    print(f"-h, --help          show the usage")
    print(f"-i, --input         input file path of the data                    DEFAULT: ./{INPUT_FILE}")
    print(f"-o, --output        output file path for the results               DEFAULT: ./{OUTPUT_RESULTS}")
    print("Variables:")
    print(f"-n, --minT                 min temperature(ChatGpT's randomness)   DEFAULT: {MIN_TEMPERATURE}")
    print(f"-x, --maxT                 max temperature(ChatGpT's randomness)   DEFAULT: {MAX_TEMPERATURE}")
    print(f"-p, --prompt                 prompt to Use True 1. person and False extractive   DEFAULT: {PROMPT}")
    print(f"-b                  bleu's minimum score to put the answer in the context                DEFAULT: {MIN_BLEU}")
    print("")
    
    print(f"Example: pruebasMasivas.py")
    print(f"Example: pruebasMasivas.py -i /home/Downloads/Documentos_Practicas.json -o results.txt -n 0.1 -x 0.3")

    # Salimos del programa
    exit(1)
def load_options(options):
    # PRE: argumentos especificados por el usuario
    # POST: registramos la configuración del usuario en las variables globales
    global INPUT_FILE, OUTPUT_RESULTS, MIN_TEMPERATURE,MAX_TEMPERATURE,MIN_BLEU,PROMPT 

    for opt,arg in options:
        if opt in ('-h', '--help'):
            usage()
        elif opt in ('-i', '--input'):
            INPUT_FILE = str(arg)
        elif opt in ('-o', '--output'):
            OUTPUT_RESULTS = str(arg)    
        elif opt in ('-n', '--minT'):
            MIN_TEMPERATURE = float(arg)
        elif opt in ('-x', '--maxT'):
            MAX_TEMPERATURE = float(arg)
        elif opt in ('-p', '--prompt'):
            PROMPT = bool(arg)
        elif opt in ('-b'):
            print(arg)
            MIN_BLEU = float(arg)




def show_script_options():
    print("pruebasMasivas.py configuration:")
    print(f"-i                  input file path of the data             -> {INPUT_FILE}")
    print(f"-o                  output file path for the results        -> {OUTPUT_RESULTS}")
    print("Variables:")
    print(f"-n                 min temperature(ChatGpT's randomness) -> {MIN_TEMPERATURE}")
    print(f"-x                 max temperature(ChatGpT's randomness) -> {MAX_TEMPERATURE}")
    print(f"-b   bleu's minimum score to put the answer in the context  -> {MIN_BLEU}")
    print(f"-p                 Prompt to Use: True 1. person and False extractive   DEFAULT: {PROMPT}")
    print("")
    print()


def main():
    print(os.environ["OPENAI_API_KEY"])
    temperatura=MIN_TEMPERATURE
    bleu = evaluate.load('bleu')

    text_file = open(OUTPUT_RESULTS, "a")

    with open(INPUT_FILE) as archivo:
        datos=json.load(archivo)
    crear_archivos_con_entrevistas(datos)
    prompt=prompt_utilizado()

    num_entrevistas=(len(datos["data"]))
    fscore_total=0
    text_file = open(OUTPUT_RESULTS, "a")
    text_file.write("PRUEBAS: "+str(datetime.datetime.now()))
    buenaSuma=False
    while not buenaSuma:
        print("¿Qué entrevista quieres probar del 0 al "+str(num_entrevistas-1)+" ?")
        entrevista=int(input())
        print("¿Cuantas entrevistas quieres probar? ")
        num_total=int(input())

        if(entrevista+num_total<=num_entrevistas):
            buenaSuma=True
        else:
            print("No puede probar tantas entrevistas, ya que supera el número total.")
    
    z=0
    fuera=False
    while not fuera:
        print("Inicio bucle "+str(fuera))
        j=0
        
        temperatura=MIN_TEMPERATURE
        while (j<10):
            text_file.write("----------------------------------------------------------------------------------------------------\n")
            j+=1
        
        print(str(entrevista) +"     "+str(num_entrevistas))
        print("z: ",z,"Numero de vueltas: ",num_total)
        if z>=num_total:
            fuera=True
        # Obtener las preguntas del JSON y eliminar el número y el hashtag
        else:
            while temperatura<=MAX_TEMPERATURE:
                preguntas = []
                respuestas = []
                print("Prueba"+str(entrevista))
                for qa in datos["data"][entrevista]["paragraphs"][0]["qas"]:
                    pregunta = qa['question']
                    preguntas.append(pregunta)
                    respuesta = qa['answers'][0]['text'] if qa['answers'] else ''  # Tomamos la primera respuesta o un string vacío si no hay respuesta
                    respuestas.append(respuesta)

                preguntas_y_respuestas = zip(preguntas, respuestas)
                preguntas_y_respuestas_ordenadas = sorted(preguntas_y_respuestas, key=lambda x: int(x[0].split('#')[0].split(' ')[0]))

                # Obtener las preguntas y respuestas ordenadas y limpias
                preguntas_ordenadas = [pregunta.split('#', 1)[1].strip() for pregunta, _ in preguntas_y_respuestas_ordenadas]
                respuestas_ordenadas = [respuesta for _, respuesta in preguntas_y_respuestas_ordenadas]

                historial_medico=datos["data"][entrevista]["paragraphs"][0]["context"]
                print(historial_medico)
                contexto='\n'+historial_medico+prompt
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
                
                for pregunta in preguntas_ordenadas:
                    print(pregunta)
                    messages =  [  
                        {'role':'system', 'content':contexto},    
                        {'role':'user', 'content':pregunta}]
                    
                    
                    response=get_completion(messages,temperature=float(temperatura))
                    

                    

                    #Respuesta que nos da Chatgpt    
                    predictions = [response]
                    #Respuesta real del paciente en la entrevista original
                    references = [
                            [respuestas_ordenadas[i]]
                    ]
                    
                    #Prueba minBleu
                    #print("Predictions solo primer campo: \n"+predictions[0])
                    #En los casos en los que en la entrevista no hay respuesta cambiamos "" por No se menciona para que se pueda evaluar correctamente.
                    if references[0]==['']:
                        references[0]=['No se menciona en el historial médico.']
                    
                    # Para evaluar tiene que haber un mínimo de carácteres por eso modificamos ambos
                    if references[0]==['I']:
                        references[0]=['I I I I']
                    if predictions[0]=='I':
                        predictions[0]='I I I I'

                    #Eliminar el punto final para equiparar las dos respuestas y hacer la evaluación lo más justa posible.    
                    if predictions[0][-1]=="." and references[0][0][-1]==".":
                        predictions[0]=predictions[0][:-1]
                        references[0][0]=references[0][0][:-1]
                    elif predictions[0][-1]==".":
                        predictions[0]=predictions[0][:-1]
                    elif references[0][0][-1]=='.':
                        references[0][0]=references[0][0][:-1]
                        
                    results = bleu.compute(predictions=predictions, references=references, max_order = 2)
                    text_file
                    print(predictions[0])
                    print(results["bleu"])
                    print(references[0])
                    #text_file = open(OUTPUT_RESULTS, "a")
                    #text_file.write("\n-----------------------------------------\n")
                    text_file.write("(Q)-"+str(pregunta)+ "\n(A)-"+str(predictions[0])+"\n(Real answer)"+str(references[0])+"\n"+str(results)+"\n")
                    #Solo guardamos las preguntas y respuestas dentro del contexto si superan el límite de 0.3
                    '''if results["bleu"]>=MIN_BLEU:
                        contexto=contexto+'\n(Q)-'+pregunta+'\n(A)-'+predictions[0]+'\n' '''
                        #print(contexto)

                    if(references[0]==['No se menciona en el historial médico']):
                        
                        if(predictions[0]=="No se menciona en el historial médico"):
                            score_questions_cant_find_answers+=1
                            
                        total_questions_cant_find_answers+=1
                    
                    elif(references[0][0]=="I I I I"):
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
                media_total=suma/len(preguntas_ordenadas)

                dataforTableResults=[
                    ["Questions that don't appear in the text: ",str(total_questions_cant_find_answers),str(score_questions_cant_find_answers)],
                    ["Questions that don't require an answer: ",str(total_questions_no_need_answers),str(score_questions_no_need_answers)],
                    ["Questions that have answer",str(total_questions_with_answers),str(score_questions_with_answers)],
                    ["Total",str(i),str(media_total)]
                ]
                dataforVariables=[
                    ["Num of interview: ",str(entrevista)],
                    ["Minimum bleu for adding the answer in the context: ",str(MIN_BLEU)],
                    ["Temperature for the chatGpt ",str(temperatura)],
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
                '''
                i=0
                
                while (i<10):
                    text_file = open(OUTPUT_RESULTS, "a")
                    text_file.write("----------------------------------------------------------------------------------------------------\n")
                    i+=1
                '''
                temperatura+=0.05
                entrevista+=1
                fscore_total=media_total+fscore_total
                z+=1
                print("Fin bucle")

    print(fuera)
    fscore_total=fscore_total/num_total
    dataFscore=[
                ["F-score prueba: "+str(fscore_total)]
            ]
    headFscore=["   ","     "]
    text_file.write(tabulate(dataFscore,headers=headFscore,tablefmt="grid"))


if __name__ == "__main__":
    try:
        # options: registra los argumentos del usuario
        # remainder: registra los campos adicionales introducidos -> entrenar_knn.py esto_es_remainder
        options, remainder = getopt(argv[1:], 'hi:o:n:x:b:', ['help', 'input=', 'output=','minT=','maxT='])
            
    except GetoptError as err:
        # Error al parsear las opciones del comando
        print("ERROR: ", err)
        exit(1)

    print(options)
    # Registramos la configuración del script
    load_options(options)
    # Imprimimos la configuración del script
    show_script_options()
    # Ejecutamos el programa principal
    main()
    

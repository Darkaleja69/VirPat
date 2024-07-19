#DISEÑO DE PACIENTE VIRTUAL CON CHATGPT Y FURHAT
Este es un Proyecto Final de Grado realizado por Alejandro Gómez, cuyo objetivo principal es diseñar e implementar un sistema que simule un paciente virtual utilizando ChatGPT y Furhat.
La memoria que explica la realización del proyecto es 'Documentos/VirPat_TFG.pdf'
Se va a explicar la función de los archivos creados y cómo se podría continuar con el proyecto, al igual que lo que se ha conseguido.

##Explicación objetivos
Para lograr el objetivo principal, primero se han alcanzado dos objetivos: analizar la capacidad de ChatGPT para extraer de un historial médico las respuestas para las preguntas que se le hagan y analizar si ChatGPT es capaz de generar una conversación realista, tal y como lo haría un paciente común.
###Capacidad extractiva
Para lograr el primer objetivo se ha desarrollado un archivo en Python 'PruebasMasivas.py' el cual está pensado para que obtenga la valoración BLEU del prompt que se le pase al programa. Actualmente, hay un prompt desarrollado para esta tarea que correspondería al 0 en el archivo _'Prompt.json'_
Este busca que ChatGPT al dar las respuestas a las preguntas utilice únicamente las palabras que aparecen en el historial. Está pensado para que recree varias conversaciones, tantas como desees del archivo de entrada que tengas con las conversaciones (train_v2.json, dev_v2.json y test_v2.json).
En el archivo de texto que se especifique al lanzar el programa se escribirán las puntuaciones obtenidas por cada conversación, y una media de la valoración BLEU al final de la ejecución del programa. Esto se hará en un archivo dentro de la carpeta 'Pruebas'. Se escribirá la conversación completa y la precisión BLEU para cada respuesta (la mayoría de documentos .txt no tienen las conversaciones completas).
En el archivo 'Documentos/PruebasPrompt.ods' están los resultados de las pruebas realizadas para mejorar el prompt, 0,5 es la puntuación media obtenida.

###Capacidad conversacional
Para lograr este objetivo se ha creado un prompt, el cual indica a ChatGPT cómo debe responder a las preguntas siguiendo el historial médico, pero generando una conversación más realista (habla en 1ª persona, utiliza expresiones corrientes... ). Para valorar cómo de bueno es Furhat respondiendo, se valoraron 3 características de las respuestas: fluidez (respuesta en 1ª persona y gramaticalmente correcta), exactitud (lo que dice la respuesta corresponde con la información del historial médico) y coherencia (la respuesta podría ser perfectamente de un paciente real). Las pruebas que realizaron 4 evaluadores están en la carpeta: 'Pruebas Prompt Conversacional'

### Probar en inglés
Se decidió hacer unas pruebas traduciendo los historiales y las preguntas y respuestas al inglés, para ver si ChatGPT al haber sido entrenado mayoritariamenrte en inglés acertaba más. Todos los archivos de la tarea se encuentran en la carpeta 'Tarea Secundaria en Inglés'. Se han traducido con el programa 'Traducir historiales.py', las pruebas con el prompt extractivo se realizan mediante el programa 'PruebasIngles.py' y los datos de entrada se han traducido del 10-29 y del 50-98. Se pueden traducir los del dev y test mediante 'Traducir historiales.py'

##Funcionamiento PruebasMasivas
Para conocer los parámetros de entrada que tiene el archivo se puede saber utilizando este comando:
<python3 PruebasMasivas.py --help>
El programa está pensado para que la apiKey de ChatGPT no esté escrito en texto plano, sino que cada vez que inicies el programa en un nuevo terminal, la apiKey está establecida como variable de entorno.
Estos son los comandos necesarios para establecerla:
<echo "export OPENAI_API_KEY='sk-...'" >> ~/.zshrc >
<source ~/.zshrc>

Está pensado que todas las pruebas y resultados se creen en la 

##Funcionamiento Skill en Furhat
Dentro de la carpeta 'ProgramaFurhat/Prueba' se encuentra otro README, que explica su funcionamiento.

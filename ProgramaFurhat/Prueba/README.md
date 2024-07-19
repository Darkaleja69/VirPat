# Skill
Skill desarrollada para que el robot Furhat actúe como paciente virtual. Utiliza ChatGPT para dar las respuestas al médico

## Description
Tiene varios archivos kotlin en los que hay varios estados. El proceso que va siguiendo la variable estado es el siguiente: Main para inicializarlo, Init(configuración de parámetros iniciales, revisión necesaria en este estado para mejorar la conexión con el robot Furhat físico)->Context (se pregunta al médico qué historial médico quiere usar de los que están en la base de datos. La respuesta debe ser un número, para eso se creó el Intent 'Numero')->Greeting (Comienza la conversación con un saludo y gestiona cómo se responde a las preguntas. En caso de que haya una despedida se despide el robot, y si no se pasa la pregunta del médico a la función dentro del archivo OpenAI (en este archivo se hace la conexión con ChatGPT y se añade el prompt diseñado disponible en la carpeta resources. Es necesario utilizar una apiKey válida que habría que actualizarla en el archivo de texto apiKey.txt)

## Usage
IntellIJ es el IDE más adecuado para modificar el software mediante Kotlin. Simplemente pulsando en Run en el archivo Main, la SKILL se ejecutará. Se pueden crear archivos ejecutables para poder utilizar la Skill sin tener que entrar en IntellIj, de modo que sean archivos .skill (muy útil para pruebas con robot físico). Dentro de la carpeta general hay uno con la última versión de la skill. Para poder usar ese archivo debe usar este comando:
<java -jar Prueba-all.skill>

##Conversación
La conversación comenzará con una pregunta del médico para elegir el historial. Debes responder un número válido, ya que te dice el número de historiales que tiene cargados actualmente. Tras decir el número, Furhat tendrá cargado en la memoria el historial médico y comenzará con un saludo 'Buenos días, doctor' tras este saludo se debe comenzar con el interrogatorio del médico al paciente para conocer su historial.
Para terminar la conversación, di una despedida, como puede ser 'Adiós', 'Hasta Luego'. De esta forma el robot se quedará en el estado 'Idle' o inactivo. Luego para cerrar la interacción para la Skill, bien por el IDE IntellIJ o por FurhatSDK (Pestaña en el navegador en la que se puede ir viendo cómo va la conversación, ya que va transcribiendo lo que escucha y dice Furhat).

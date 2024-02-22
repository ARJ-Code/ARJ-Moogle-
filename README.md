# ARJ-News-Bot

## Sistema de Extracción de Información de Noticias

### Autores

- [Raudel Gomez](https://github.com/raudel25) C411.
- [Juan Carlos Espinosa](https://github.com/Jky45) C411.
- [Alex Sierra](https://github.com/alexsierra45) C411.

### Descripción del Problema

El proyecto se centra en la creación de un sistema capaz de extraer información relevante y estructurada de artículos de noticias disponibles en línea. Este sistema debe ser capaz de identificar y presentar datos clave como titulares, autores, fecha de publicación, resumen del contenido, entidades mencionadas (personas, organizaciones, países) y también sugerir otras noticias similares.

### Consideraciones al Desarrollar la Solución

- Se ha optado por utilizar el lenguaje de programación Python debido a su amplia disponibilidad de bibliotecas especializadas en procesamiento de lenguaje natural y análisis de datos.
- La solución se divide en varios módulos para facilitar la modularidad y la mantenibilidad del código.
- Se ha empleado la biblioteca `newsplease` para la extracción de datos de los artículos de noticias, `spacy` para el procesamiento de lenguaje natural, `gensim` para la representación de texto y `networkx` para el cálculo de similitudes entre textos.
- Se recomienda revisar detenidamente la documentación de cada módulo y biblioteca utilizada para comprender mejor su funcionamiento y aplicaciones específicas.

### Uso de Bot de Telegram como Interfaz Gráfica

El proyecto implementa un bot de Telegram como interfaz gráfica para interactuar con el sistema de extracción de información de noticias. Este enfoque proporciona una forma conveniente y accesible para los usuarios de enviar URLs de artículos de noticias y recibir información relevante de manera interactiva a través de Telegram. Puede acceder a este mediante este nick **@arj_sri_bot**.

#### Funcionalidades del Bot

1. **Inicio y Ayuda**: Al iniciar una conversación con el bot o al enviar el comando `/start` o `/help`, el bot responde proporcionando instrucciones sobre cómo usar el sistema y qué tipo de URL de artículo de noticias se puede enviar.

2. **Solicitudes de Información Específica**: Cuando se envía una URL de un artículo de noticias al bot, el sistema procesa la URL y extrae información relevante. Luego el usuario puede solicitar información específica sobre el artículo, como el resumen, los autores, la fecha de publicación, etc., enviando los comandos correspondientes al bot.

3. **Recomendación de Noticias Similares**: Además de la información del artículo enviado, el bot también puede sugerir otras noticias similares utilizando técnicas de análisis de similitud de texto.

#### Ventajas de Usar un Bot de Telegram

- **Accesibilidad**: Telegram es una plataforma popular y ampliamente utilizada, lo que hace que el bot sea fácilmente accesible para una amplia audiencia de usuarios.
- **Interactividad**: La interfaz de chat proporcionada por Telegram permite una interacción fluida y natural entre el usuario y el sistema, facilitando la comunicación y la comprensión de la información presentada.
- **Facilidad de Uso**: No se requiere instalar ninguna aplicación adicional, ya que Telegram está disponible en múltiples plataformas, incluyendo dispositivos móviles y de escritorio.

- **Seguridad**: Telegram ofrece un cifrado de extremo a extremo para garantizar la privacidad y seguridad de las conversaciones entre los usuarios y el bot.

#### Implementación Técnica

La implementación técnica del bot de Telegram se realiza utilizando la biblioteca `telebot` en Python, que proporciona una interfaz sencilla para interactuar con la API de Telegram y gestionar las conversaciones y comandos del bot. El bot se ejecuta en un bucle infinito de escucha para detectar y responder a los mensajes de los usuarios en tiempo real.

En resumen, el uso de un bot de Telegram como interfaz gráfica en el proyecto ofrece una manera conveniente y eficaz de interactuar con el sistema de extracción de información de noticias, permitiendo a los usuarios acceder y obtener información relevante de manera rápida y sencilla a través de la popular plataforma de mensajería.

### Ejecución del Proyecto

Para ejecutar el proyecto en tu entorno local, sigue estos pasos:

1. Instala las dependencias necesarias utilizando `pip` y el archivo `requirements.txt`:

   ```
   pip install -r requirements.txt
   ```

2. Crea una carpeta `data` en el directorio raíz del proyecto para almacenar los datos de los artículos de noticias y descarga la base de datos de [Kaggle](https://www.kaggle.com/rmisra/news-category-dataset):

3. Descomprime el archivo `archive.zip` descargado y coloca el archivo `News_Category_Dataset_v2.json` con nombre `data.json` en la carpeta `data`.

4. Descarga los modelos de spacy para español e inglés:

   ```
   make models
   ```

5. Ejecuta el archivo `build.py` para construir el sistema con los datos descargados y procesados:

   ```
   make build
   ```

6. Ejecuta el archivo `main.py` para iniciar el sistema:

   ```
   make dev
   ```

7. Abre el siguiente acceso al [bot](https://t.me/arj_sri_bot)

### Parámetros de Entrada

El programa espera recibir como entrada la URL de un artículo de noticias en línea. Esta URL puede ser proporcionada por el usuario a través del bot de Telegram.

### Explicación de la Solución Desarrollada

El sistema implementado utiliza técnicas de procesamiento de lenguaje natural (NLP) y modelos de representación de texto para extraer información relevante de los artículos de noticias. A continuación, se describe brevemente el flujo de trabajo del sistema:

1. **Extracción de Datos**: Se utiliza la biblioteca `newsplease` para obtener datos estructurados de los artículos de noticias a partir de sus URL.

2. **Procesamiento de Texto**: Se emplea la biblioteca `spacy` para realizar el análisis sintáctico y semántico del texto de los artículos, identificando entidades nombradas, realizando tokenización y lematización.

3. **Análisis de Similitud**: Se calcula la similitud entre los textos de los artículos utilizando modelos de representación de texto como TF-IDF. Esto permite identificar otras noticias similares dentro de un conjunto de datos predefinido.

4. **Presentación de Resultados**: Finalmente, el sistema presenta al usuario la información extraída de los artículos, incluyendo titulares, autores, fecha de publicación, resumen del contenido, entidades mencionadas y recomendaciones de otras noticias similares.

### Algoritmo de TextRank

El algoritmo TextRank es una técnica utilizada para el procesamiento de lenguaje natural que sigue uma idea similar al algoritmo PageRank de Google, adaptado para el análisis de texto en lugar de páginas web. Se utiliza para calcular la importancia relativa de las palabras y oraciones en un texto. Se basa en el concepto de grafos y la idea de que las palabras o frases importantes en un texto estarán conectadas con otras palabras o frases importantes. El algoritmo de TextRank se utiliza en el proyecto para detectar y resaltar las oraciones más relevantes en los artículos de noticias, y así poder confeccionar el resumen deseado.

Después de tener el grafo con las aristas y los pesos relativos a la similitud entre oraciones, el algoritmo de TextRank sigue los siguientes pasos:

1. Construcción del grafo: Dada una colección de oraciones (o palabras), se construye un grafo donde los nodos representan las unidades de texto (oraciones o palabras) y las aristas representan la relación entre ellos.

2. Asignación de pesos a las aristas: Se asignan pesos a las aristas del grafo en función de la similitud entre las unidades de texto que conectan. Cuanto mayor sea la similitud, mayor será el peso de la arista.

3. Inicialización de los valores de importancia de las oraciones.

4. Cálculo de la importancia de las oraciones: Se calcula la importancia de cada oración (o palabra) en función de la importancia de las oraciones (o palabras) que la conectan. Este cálculo se realiza mediante un proceso iterativo que converge hacia un conjunto de valores de importancia estables.

5. Selección de las oraciones más importantes: Finalmente, se seleccionan las oraciones (o palabras) más importantes en función de sus valores de importancia calculados.

La formulación matemática del algoritmo de TextRank es:

- Sea G = (V, E) un grafo no dirigido que representa el texto, donde V es el conjunto de nodos que representan las oraciones (o palabras) y E es el conjunto de aristas que representan la relación entre las oraciones (o palabras).
- Sea W una matriz de adyacencia que representa la similitud entre las oraciones (o palabras) en el grafo G.
- Sea d un factor de amortiguación que controla la probabilidad de saltar a un nodo aleatorio en el grafo.
- Sea r una matriz de valores de importancia que se inicializa con valores iguales para todas las oraciones (o palabras).
- Sea r' una matriz de valores de importancia que se actualiza en cada iteración del algoritmo.

El algoritmo de TextRank se puede resumir en el siguiente pseudocódigo:

```
function TextRank(G, W, d, max_iter):
    r = initialize_importance_values(G)
    for i in range(max_iter):
        r' = (1 - d) + d * W * r
        if converge(r, r'):
            break
        r = r'
    return r
```

### Insuficiencias de la Solución y Mejoras Propuestas

A pesar de las funcionalidades implementadas, la solución presenta algunas limitaciones y áreas de mejora potencial:

- **Idioma**: Actualmente, el sistema puede no funcionar correctamente con artículos en idiomas distintos al inglés o español. Se podría explorar la posibilidad de agregar soporte para otros idiomas.
- **Precisión de la Extracción de Entidades**: La precisión de la extracción de entidades nombradas podría mejorarse mediante el uso de modelos de aprendizaje más avanzados y entrenados específicamente para el dominio de las noticias.
- **Recomendaciones Personalizadas**: Se podría implementar un sistema de recomendación más avanzado que tenga en cuenta los intereses y preferencias del usuario para sugerir noticias más relevantes y personalizadas.

Se anima a los contribuyentes y usuarios del proyecto a proponer y trabajar en mejoras adicionales que ayuden a hacer el sistema más robusto y efectivo en la extracción de información de noticias en línea.

Para obtener más detalles sobre la implementación y el funcionamiento del sistema, consulte la documentación en el código fuente y siéntase libre de contribuir con sus ideas y sugerencias.

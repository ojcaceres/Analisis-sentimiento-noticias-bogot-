[![es](https://img.shields.io/badge/lang-es-yellow.svg)](https://github.com/ojcaceres/Analisis-sentimiento-noticias-bogot-/blob/main/README.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ojcaceres/Analisis-sentimiento-noticias-bogot-/blob/main/README.en.md)

# Análisis de Sentimiento de Noticias de Bogotá

Este proyecto se centra en la transcripción y análisis de sentimientos de fragmentos de noticias relacionadas con Bogotá, obtenidos de videos publicados en línea por diversos noticieros (principalmente en YouTube). Los resultados se almacenan en archivos Excel para facilitar su análisis y visualización posterior.

## Contenido del Repositorio

- **Carpetas:**
  - `Caracol`: Contiene scripts adaptados a los fragmentos de noticias de Caracol TV que:
    - Transcriben los fragmentos de noticias almacenados en Google Cloud Storage utilizando la API de Google Cloud Speech-to-Text.
    - Realizan el análisis de sentimiento de las transcripciones empleando la API de Google Cloud Natural Language.
    - Almacenan los resultados en archivos Excel.
  - `CityTv`: Incluye scripts con la misma lógica que la carpeta anterior, adaptados a los fragmentos de noticias de CityTv.
  - `RCN t`: Contiene scripts que siguen el mismo procedimiento (transcripción, análisis de sentimiento y almacenamiento en Excel) para las noticias de RCN Televisión.

- **Archivos principales:**
  - `ensayo_taller_final.ipynb`: Un notebook de Jupyter que carga y procesa los datos resultantes del análisis de sentimiento de cada noticiero, generando gráficos y una nube de palabras con los términos más mencionados.
  - `resultados.png` y `resultados2.png`: Imágenes con los resultados gráficos del análisis de sentimiento.
  - `LICENSE`: Licencia MIT que define los términos de uso del proyecto.
  - `README.md`: Este archivo, con una descripción general del proyecto.

## Descripción del Proyecto

El objetivo principal es analizar el sentimiento de las noticias relacionadas con Bogotá desde diferentes medios de comunicación. Para lograrlo, el proyecto se divide en las siguientes etapas:

1. **Recolección de datos:** Extracción de fragmentos de noticias desde videos publicados en línea (YouTube).
2. **Transcripción de noticias:** Conversión del contenido de los videos en texto utilizando la API de Google Cloud Speech-to-Text.
3. **Análisis de sentimiento:** Empleo de la API de Google Cloud Natural Language para determinar la polaridad de las noticias (positiva, negativa o neutral).
4. **Almacenamiento de resultados:** Guardado de los resultados en archivos Excel para su posterior revisión.
5. **Visualización:** Creación de gráficos que representan la distribución de los sentimientos y generación de una nube de palabras con los términos más frecuentes.

## Instalación y Uso

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/ojcaceres/Analisis-sentimiento-noticias-bogot-.git
   `

2. **Navega al directorio del proyecto:**
   ```bash
   cd Analisis-sentimiento-noticias-bogot-
   ```

3. **Instala las dependencias:**
   Asegúrate de tener instalado Python y pip. Luego ejecuta:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las credenciales de Google Cloud:**
   Este proyecto utiliza servicios de Google Cloud para la transcripción y el análisis de sentimientos. Asegúrate de tener una cuenta activa, habilitar las APIs necesarias y descargar la clave de servicio (JSON). Luego, establece la variable de entorno con la ruta a tu credencial:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="ruta/a/tu/credencial.json"
   ```

5. **Ejecuta el notebook de Jupyter:**
   Abre el notebook para revisar y ejecutar el código paso a paso:
   ```bash
   jupyter notebook "ensayo_taller_final.ipynb"
   ```

## Estructura del Código

### Transcripción de Audios

El siguiente fragmento muestra cómo se realiza la transcripción de audios utilizando la API de Google Cloud Speech-to-Text. Este proceso convierte fragmentos de audio almacenados en Google Cloud Storage a texto, guardando las transcripciones localmente.

```python
from google.cloud import speech_v1 as speech

def transcribir_audio(ruta_audio, ruta_destino):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=ruta_audio)
    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        language_code="es-CO"
    )
    response = client.long_running_recognize(config=config, audio=audio)
    response = response.result(timeout=1200)
    with open(ruta_destino, "w", encoding='utf-8') as t:
        for parrafo in response.results:
            transcripcion = parrafo.alternatives[0].transcript
            t.write(f'{transcripcion} ')
```

### Análisis de Sentimiento

Para el análisis de sentimiento se hace uso de la API de Google Cloud Natural Language. El siguiente fragmento de código ilustra cómo obtener la polaridad (score) y la magnitud del sentimiento presente en el texto:

```python
from google.cloud import language_v1
import spacy

nlp = spacy.load('es_core_news_sm')

def analizar_sentimiento(texto):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=texto, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    score = response.document_sentiment.score
    magnitud = response.document_sentiment.magnitude
    return score, magnitud
```

### Almacenamiento de Resultados

Los resultados del análisis se guardan en un archivo Excel para su posterior análisis y visualización utilizando `pandas`:

```python
import pandas as pd

def guardar_resultados(datos, nombre_archivo):
    df = pd.DataFrame(datos)
    df.to_excel(nombre_archivo, index=False)
```

### Visualización y Nube de Palabras

El notebook `ensayo_taller_final.ipynb` procesa y grafica los datos resultantes del análisis de sentimiento. Además, genera una nube de palabras con los términos más mencionados en las noticias transcritas:

```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Suponiendo que 'texto' contiene el texto concatenado de todas las noticias
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Nube de palabras - Noticias Bogotá")
plt.show()
```

Este código genera una nube de palabras a partir del texto agregado de todas las transcripciones, ayudando a visualizar las palabras más frecuentes en las noticias analizadas.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un **Issue** o un **Pull Request** con tus sugerencias, correcciones o mejoras. Antes de contribuir, revisa las normas internas del proyecto y asegúrate de que tus aportes estén alineados con el objetivo general del proyecto.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Para más información, dudas o colaboración, contactarse a través de:

- Correo: oj.caceres@uniandes.edu.co
- LinkedIn: https://www.linkedin.com/in/oswaldo-jose-caceres-leal/

---


[![es](https://img.shields.io/badge/lang-es-yellow.svg)](https://github.com/ojcaceres/Analisis-sentimiento-noticias-bogot-/blob/main/README.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ojcaceres/Analisis-sentimiento-noticias-bogot-/blob/main/README.en.md)

# Bogotá News Sentiment Analysis

This project focuses on the transcription and sentiment analysis of news segments related to Bogotá, obtained from online videos published by various news outlets (mainly on YouTube). The results are stored in Excel files to facilitate subsequent analysis and visualization.

## Repository Contents

- **Folders:**
  - `Caracol`: Contains scripts adapted for news segments from Caracol TV that:
    - Transcribe news segments stored in Google Cloud Storage using the Google Cloud Speech-to-Text API.
    - Perform sentiment analysis on the transcriptions using the Google Cloud Natural Language API.
    - Store the results in Excel files.
  - `CityTv`: Includes scripts following the same logic as the above folder, adapted for CityTv news segments.
  - `RCN t`: Contains scripts that follow the same procedure (transcription, sentiment analysis, and Excel storage) for RCN Televisión news segments.

- **Main files:**
  - `ensayo_taller_final.ipynb`: A Jupyter notebook that loads and processes the sentiment analysis results from each news outlet, generating charts and a word cloud with the most mentioned terms.
  - `resultados.png` and `resultados2.png`: Images showing graphical results of the sentiment analysis.
  - `LICENSE`: MIT License defining the project’s terms of use.
  - `README.md`: This file, providing a general project overview.

## Project Description

The main objective is to analyze the sentiment of Bogotá-related news from different media outlets. The project is divided into the following stages:

1. **Data Collection:** Extracting news segments from online videos (YouTube).
2. **News Transcription:** Converting video content into text using the Google Cloud Speech-to-Text API.
3. **Sentiment Analysis:** Using the Google Cloud Natural Language API to determine the polarity of the news (positive, negative, or neutral).
4. **Results Storage:** Saving the analysis results in Excel files for later review.
5. **Visualization:** Creating charts to represent the distribution of sentiments and generating a word cloud with the most frequent terms.

## Installation and Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ojcaceres/Analisis-sentimiento-noticias-bogot-.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd Analisis-sentimiento-noticias-bogot-
   ```

3. **Install dependencies:**
   Make sure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials:**
   This project uses Google Cloud services for transcription and sentiment analysis. Ensure you have an active account, have enabled the necessary APIs, and downloaded the service key (JSON). Then set the environment variable pointing to your credential:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credential.json"
   ```

5. **Run the Jupyter notebook:**
   Open the notebook to review and execute the code step-by-step:
   ```bash
   jupyter notebook "ensayo_taller_final.ipynb"
   ```

## Code Structure

### Audio Transcription

The following snippet demonstrates how audio transcription is performed using the Google Cloud Speech-to-Text API. This process converts audio segments stored in Google Cloud Storage into text, saving the transcriptions locally.

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

### Sentiment Analysis

For sentiment analysis, the project uses the Google Cloud Natural Language API. The following code snippet shows how to obtain the polarity (score) and magnitude of the sentiment present in the text:

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

### Storing Results

The analysis results are saved in an Excel file for later analysis and visualization using `pandas`:

```python
import pandas as pd

def guardar_resultados(datos, nombre_archivo):
    df = pd.DataFrame(datos)
    df.to_excel(nombre_archivo, index=False)
```

### Visualization and Word Cloud

The `ensayo_taller_final.ipynb` notebook processes and plots the sentiment analysis data. It also generates a word cloud of the most frequently mentioned terms in the transcribed news:

```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Assuming 'texto' contains the concatenated text of all news articles
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud - Bogotá News")
plt.show()
```

This code produces a word cloud from the aggregated text of all transcriptions, helping visualize the most frequently used words in the analyzed news segments.
```

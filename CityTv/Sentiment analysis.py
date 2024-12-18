# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:25:22 2022

@author: Oswaldo Cáceres
"""

import os
import pandas as pd
from google.cloud import language_v1
from pandas import ExcelWriter
import spacy
import operator

nlp = spacy.load('es_core_news_sm')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "inserte la ruta de su credencial aquí"

data = pd.DataFrame(columns=['noticiero', 'año', 'mes', 'dia', 'id_audio', 'clasificacion', 'score', 'subjetividad',
                             'palabra_frecuente', 'frecuencia_palabra', 'n_score'])
noticiero = "CityTv"
dir_transcripciones = "./transcripciones"


def store_result(annotations, año, mes, dia, frecuencias, id_audio):
    n_score = 0.0
    n_sentences = 0
    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print("la oración tiene n_score de: {}".format(sentence_sentiment))
        if sentence_sentiment < 0.0:
            n_score += sentence_sentiment
            n_sentences += 1
    if n_sentences > 0:
        n_score = n_score / n_sentences

    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    if(len(annotations.sentences) > 0):
        subjetividad = magnitude / len(annotations.sentences)
    else:
        subjetividad = 0
    print(
        "Overall Sentiment: score of {} with n_score of {} and {} of subjetividad".format(score, n_score, subjetividad)
    )

    if score > 0.15:
        clasificacion = "POSITIVA"
    elif (score < -0.15) | ((score >= -0.15) & (score <= 0.15) & (subjetividad >= 0.15) & (n_score <= -0.15)):
        clasificacion = "NEGATIVA"
    else:
        clasificacion = "NEUTRA"

    i = 0
    for palabra, frecuencia in frecuencias:
        data.loc[len(data.index)] = [noticiero, año, mes, dia, id_audio, clasificacion, score, subjetividad,
                                     palabra, frecuencia, n_score]
        i += 1
        if i == 5:
            break


def analyze(file_name, año, mes, dia, id_audio):
    # Read the data
    with open(file_name, "r", encoding='utf-8') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()
    """Run a relevant words obtainer on text within a passed filename."""
    doc = nlp(content)
    lemmas = [token.lemma_.lower() for token in doc if not token.is_punct | token.is_stop ]
    palabras = [t for t in lemmas if len(t) > 3 and t.isalpha() and t != 'bogotá']

    diccionario_frecuencias = {}
    for palabra in palabras:
        if palabra in diccionario_frecuencias:
            diccionario_frecuencias[palabra] += 1
        else:
            diccionario_frecuencias[palabra] = 1

    lista_sorted = sorted(diccionario_frecuencias.items(), key=operator.itemgetter(1), reverse=True)

    """Run a sentiment analysis request on text within a passed filename."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=content, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    annotations = client.analyze_sentiment(request={"document": document})

    # store the results
    store_result(annotations, año, mes, dia, lista_sorted, id_audio)


def crear_dataframe_trascripciones():
    archivos = os.listdir(dir_transcripciones)
    for dir_año in archivos:
        ruta_año = os.path.join(dir_transcripciones, dir_año)
        if os.path.isdir(ruta_año):
            for dir_mes in os.listdir(ruta_año):
                ruta_mes = os.path.join(ruta_año, dir_mes)
                if os.path.isdir(ruta_mes):
                    for dir_dia in os.listdir(ruta_mes):
                        ruta_dia = os.path.join(ruta_mes, dir_dia)
                        if os.path.isdir(ruta_dia):
                            for index, transcript in enumerate(os.listdir(ruta_dia)):
                                ruta_transcript = os.path.join(ruta_dia, transcript)
                                if os.path.isfile(ruta_transcript):
                                    analyze(ruta_transcript, dir_año, dir_mes, dir_dia, index+1)

    with ExcelWriter(
            "CityTvDB.xlsx"
    ) as writer:
        data.to_excel(writer, index=False)


crear_dataframe_trascripciones()

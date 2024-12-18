import io
import os
import re

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage
from deepmultilingualpunctuation import PunctuationModel

model = PunctuationModel(model='kredor/punctuate-all')

#configurando la credencial de Google
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'inserte la ruta de su credencial aquí'
#clave del storage de google cloud
key_storage = "inserte la ruta de su credencial aquí"
dirAudios = "gs://ojcaceres/transcripts"
dir_transcripciones= "./transcripciones"

#configuración de la API
config = speech.RecognitionConfig(
        encoding='MP3',
        sample_rate_hertz=44100,
        language_code="es-CO"
     )

def speech_to_text(config, rutaAudio, rutaDestino):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=rutaAudio)
    response = client.long_running_recognize(config=config, audio=audio)
    print(f"The transcription of the audio is in progress...")
    response = response.result(timeout=1200)
    with open(rutaDestino, "w", encoding='utf-8') as t:
        for parrafo in response.results:
            best_alternative = parrafo.alternatives[0]
            trascripcion = best_alternative.transcript
            trascripcion = model.restore_punctuation(text=trascripcion)
            t.write('{} '.format(trascripcion))
            confidence = best_alternative.confidence
            print(f"Confidence of the paragraph's transcription: {confidence:.0%}")
    print(f"Transcription saved in: {rutaDestino}")



def creacionDeTranscripciones():
    clientStorage = storage.Client.from_service_account_json(json_credentials_path=key_storage)
    BUCKET_NAME = 'ojcaceres'
    blobs = clientStorage.list_blobs(BUCKET_NAME, prefix='transcripts')
    for archivo in blobs:
        if "." in archivo.name:
            parametros = archivo.name.split("/")
            año = parametros[1]
            mes = parametros[2]

            if (año == '2018') & (mes == 'Marzo'):
                dia = parametros[3]
                audio = parametros[4]
                # crea los directorios para guardar las transcripciones
                os.makedirs(dir_transcripciones + '/{}/{}/{}'.format(año, mes, dia.split(" ")[1]), exist_ok=True)
                # ruta dónde está el audio
                rutaAudio = dirAudios + '/{}/{}/{}/{}'.format(año, mes, dia, audio)
                #ruta dónde se guarda el archivo
                rutaDestino = dir_transcripciones + '/{}/{}/{}/{}.txt'.format(año, mes, dia.split(" ")[1], audio.split(".")[0])

                speech_to_text(config, rutaAudio, rutaDestino)

creacionDeTranscripciones()


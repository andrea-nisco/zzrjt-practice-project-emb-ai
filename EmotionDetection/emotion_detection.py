import requests
import json

def emotion_detector(text_to_analyze):
    # 1. Controllo base: se il testo è nullo o vuoto
    if not text_to_analyze or text_to_analyze.strip() == "":
        return {
            'anger': None, 'disgust': None, 'fear': None, 
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyze } }
    
    response = requests.post(url, json=myobj, headers=header)
    
    # 2. Se Watson risponde male (es. 400), restituisci i None
    if response.status_code != 200:
        return {
            'anger': None, 'disgust': None, 'fear': None, 
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }
    
    # 3. Parsing del JSON
    formatted_response = json.loads(response.text)
    
    # 4. Estrazione sicura
    if 'emotionPredictions' in formatted_response and len(formatted_response['emotionPredictions']) > 0:
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        result = {
            'anger': emotions['anger'],
            'disgust': emotions['disgust'],
            'fear': emotions['fear'],
            'joy': emotions['joy'],
            'sadness': emotions['sadness']
        }
        dominant_emotion = max(result, key=result.get)
        result['dominant_emotion'] = dominant_emotion
        return result
    else:
        # Fallback se non ci sono predizioni
        return {
            'anger': None, 'disgust': None, 'fear': None, 
            'joy': None, 'sadness': None, 'dominant_emotion': None
        }
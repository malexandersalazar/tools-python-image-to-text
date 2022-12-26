import sys as _s

import pytesseract as pyt
import cv2
import os
import spacy
import pandas as pd
from sklearn.model_selection import ParameterGrid

pyt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
gpu = spacy.prefer_gpu()

text_scores = []

def get_grayscaled(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def get_thresholded(image, block_size, c):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c)

def process(img_file, lang, block_size, c):
    img = cv2.imread(img_file)

    thresholded_img = get_thresholded(get_grayscaled(img),block_size,c)

    if(lang == 'es'):
        tess_lang = 'spa'
    elif(lang == 'en'):
        tess_lang = 'eng'
    else:
        raise Exception('Not supported language')

    return pyt.image_to_string(thresholded_img, tess_lang)

def run(img_file,lang):
    params = {
        'blockSize': [13,21,55,89,233],
        'C': [2,3,5,8,13,21],
    }

    if(lang == 'es'):
        nlp = spacy.load("es_core_news_md")
    elif(lang == 'en'):
        nlp = spacy.load("en_core_web_md")
    else:
        raise Exception('Not supported language')

    for config in ParameterGrid(params):
        block_size = config['blockSize']
        c = config['C']

        text_result = process(img_file, lang, block_size,c)

        tokens = nlp(text_result)
        df = pd.DataFrame([(w.text, w.pos_) for w in tokens],columns=['text','word_type'])

        nouns = df[df['word_type']=='NOUN']
        verbs = df[df['word_type']=='VERB']
        propernames = df[df['word_type']=='PROPN']
        adjetives = df[df['word_type']=='ADJ']
        prepositions = df[df['word_type']=='ADP']
        verbs = df[df['word_type']=='VERB']
        pronouns = df[df['word_type']=='PRON']
        conjunctions = df[df['word_type']=='CCONJ']

        text_score = len(nouns) + len(verbs) + len(propernames) + len(adjetives) + len(prepositions) + len(verbs) + len(pronouns) + len(conjunctions)
        text_scores.append((text_result,text_score))

    scores_df = pd.DataFrame(text_scores, columns=['text_result','text_score'])
    text_final_result = scores_df.sort_values('text_score', ascending=False).reset_index(drop=True)['text_result'][0]
    print(text_final_result)


if __name__ == "__main__":
    img_file = _s.argv[1]
    lang = 'en'

    if len(_s.argv) == 3:
        lang = _s.argv[2]
    
    run(img_file,lang)
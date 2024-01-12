import argparse

parser=argparse.ArgumentParser(
    description='A Python tool based on OpenCV, Tesseract OCR and spaCy for reading and recognize the text in an image from Windows.',
    epilog='github.com/malexandersalazar/tools-python-image-to-text')
parser.add_argument('folder', type=str, help='W:/malexandersalazar/tools-python-image-to-text/raw')
parser.add_argument('-l','--lang', choices=['en','es'], default='en', type=str, help='specifies the lang in which the reader should be executed, "en" for english and "es" for spanish (default: "en")')
args=parser.parse_args()

FOLDER = args.folder
LANG = args.lang

import os
import pytz
from glob import glob
from itertools import product
from datetime import datetime as DateTime

import cv2
import spacy
import pandas as pd
import pytesseract as pyt

pyt.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
gpu = spacy.prefer_gpu()

def get_grayscaled(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def get_thresholded(image, block_size, c):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c)

def dict_configs(d):
    for vcomb in product(*d.values()):
        yield dict(zip(d.keys(), vcomb))

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

def run(imgs_folder,lang):
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

    img_files = glob(imgs_folder + '/*.png') + glob(imgs_folder + '/*.jpg') + glob(imgs_folder + '/*.jpeg')

    for img_file in img_files:
        print(f'Reading {os.path.basename(img_file)}...')

        text_scores = []

        for config in dict_configs(params):
            block_size = config['blockSize']
            c = config['C']

            text_result = process(img_file,lang,block_size,c)

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
            text_scores.append((block_size,c, text_result,text_score))

        scores_df = pd.DataFrame(text_scores, columns=['block_size','c','text_result','text_score'])
        sorted_scores_df = scores_df.sort_values('text_score', ascending=False).reset_index(drop=True)
        text_final_result = sorted_scores_df['text_result'][0]

        with open("results.txt", "a", encoding='utf-8') as f:
            now = DateTime.now(pytz.timezone('America/Lima'))
            log_content = f"========================================================\n[{now.strftime('%Y-%m-%d %H:%M')}]\n\n{text_final_result}\n"
            f.write(log_content)

        top_df = sorted_scores_df[['block_size', 'c']][:3]

        if os.path.exists('log.csv'):
            old_df = pd.read_csv('log.csv', encoding='utf-8')
            new_df = pd.concat([old_df, top_df])
        else:
            new_df = top_df

        new_df.to_csv('log.csv',index=False, encoding='utf-8')

run(FOLDER,LANG)
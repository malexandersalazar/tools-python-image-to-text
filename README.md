# Image to text tool

![alt text](/img/variants.PNG "Image to text tool")

 A Python tool based on OpenCV, Tesseract OCR and spaCy for reading and recognize the text in an image from Windows.

 This script processes the image generating 30 variants using OpenCV adaptiveThreshold to then measure with spaCy the relevance and number of words obtained by Tesseract OCR and choose the best reading.

## Installation

### Tesseract OCR

The latest installers for Windows can be downloaded [here](https://github.com/UB-Mannheim/tesseract/wiki).

For more information about languages supported in different versions of Tesseract visit the following [link](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html).

### spaCy

To enable spaCy we must download the pre-trained models as indicated on its official [site](https://spacy.io/models).

>  pip install -U spacy

Installing English:

>  python -m spacy download en_core_web_md

Installing Spanish:

>  python -m spacy download es_core_news_md

### Image to text tool

Just copy the `itt.py` script located in the dist folder and update the Tesseract path if necessary.

```
import pytesseract as pyt

pyt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```

## Getting Started

To use the script we only have to indicate the path of the image that we want to read.

> python itt.py D:\Workspaces\malexandersalazar\tools-python-image-to-text\img\source.jpg

You can also set the language as a parameter. For now it only supports English and Spanish.

> python itt.py D:\Workspaces\malexandersalazar\tools-python-image-to-text\img\source.jpg en

If we want to support more languages we must install the necessary spaCy models and make sure that Tesseract OCR can support them as well.

## Dependencies

* python (== 3.8.15)
* pytesseract (== 0.3.10)
* cv2 (== 4.6.0)
* spacy (== 3.4.4)
* pandas (== 1.5.2)
* sklearn (== 1.2.0)

## License

This project is licenced under the [MIT License][1].

[1]: https://opensource.org/licenses/mit-license.html "The MIT License | Open Source Initiative"
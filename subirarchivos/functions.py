import codecs
import textract
from chardet.universaldetector import UniversalDetector
import os


DETECTOR = UniversalDetector()

def convert_to_utf8(filename):
    global DETECTOR
    DETECTOR.reset()
    with open(filename, 'rb') as f:
        start = f.read(3)
        f.seek(0)
        for line in f:
            DETECTOR.feed(line)
            if DETECTOR.done:
                break
    DETECTOR.close()
    encoding = DETECTOR.result["encoding"]
    if encoding != "UTF-8":
        os.system('iconv -f %s -t UTF-8 "%s" > "%s.utf8"'%(encoding, filename, filename))
        os.system('mv "%s.utf8" "%s"'%(filename, filename))
    elif start == codecs.BOM_UTF8:
            os.system('tail --bytes=+4 "%s" > "%s.utf8wobom"'%(filename, filename))
            os.system('mv "%s.utf8wobom" "%s"'%(filename, filename))

def convert_to_txt(filename):
    data = ""
    try:
        data = textract.process(filename)
    except textract.exceptions.ExtensionNotSupported:
        fname = filename.split("/")[-1]
        raise osv.except_osv("Error", u"%s no es un tipo de archivo soportado"%fname)
    if data:
        with open(filename + ".txt", "wb") as f:
            f.write(data)
    else:
        fname = filename.split("/")[-1]
        raise osv.except_osv("Error", u"No se pudo extraer texto del archivo %s"%fname)

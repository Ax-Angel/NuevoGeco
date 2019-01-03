import codecs
import textract
from chardet.universaldetector import UniversalDetector
import os
import freeling
import sys

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

def ProcessSentences(ls, out_name):
    # for each sentence in list
    with open(out_name, 'a') as file:
        file.write('Palabra\t'+'Candidatos\t'+'Etiqueta\n')
        for s in ls :
            # for each word in sentence
            for w in s :
                # print word form  
                file.write(w.get_form()+"\t")
                # print possible analysis in word, output lemma and tag

                for a in w :
                    file.write("("+a.get_lemma()+","+a.get_tag()+")")
                file.write("\t")
                #  print analysis selected by the tagger 
                file.write("("+w.get_lemma()+","+w.get_tag()+")\n")
 

def my_maco_options(lang,lpath) :
    opt = freeling.maco_options(lang);
    opt.UserMapFile = "";
    opt.LocutionsFile = lpath + "locucions.dat"; 
    opt.AffixFile = lpath + "afixos.dat";
    opt.ProbabilityFile = lpath + "probabilitats.dat"; 
    opt.DictionaryFile = lpath + "dicc.src";
    opt.NPdataFile = lpath + "np.dat"; 
    opt.PunctuationFile = lpath + "../common/punct.dat"; 
    return opt;

def tagger(file_url, out_name):
    freeling.util_init_locale("default");
    ipath = "/usr/local";
    lpath = ipath + "/share/freeling/" + "es" + "/"
    tk=freeling.tokenizer(lpath+"tokenizer.dat");
    sp=freeling.splitter(lpath+"splitter.dat"); 
    morfo=freeling.maco(my_maco_options("es",lpath));
    morfo.set_active_options (False,  # UserMap 
                              True,  # NumbersDetection,  
                              True,  # PunctuationDetection,   
                              True,  # DatesDetection,    
                              True,  # DictionarySearch,  
                              True,  # AffixAnalysis,  
                              False, # CompoundAnalysis, 
                              True,  # RetokContractions,
                              True,  # MultiwordsDetection,  
                              True,  # NERecognition,     
                              False, # QuantitiesDetection,  
                              True); # ProbabilityAssignment                 

    tagger = freeling.hmm_tagger(lpath+"tagger.dat",True,2)
    file = open(file_url, "r") 
    text = file.read()
    lw = tk.tokenize(text)
    ls = sp.split(lw)
    ls = morfo.analyze(ls)
    ls = tagger.analyze(ls)  
    ProcessSentences(ls, out_name)
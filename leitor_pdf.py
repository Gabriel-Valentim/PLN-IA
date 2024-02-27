import PyPDF2
import nltk

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def retira_stop_words(texto):
    
    words_in_quote = word_tokenize(texto, "english", False)
    #print("--------")
    #print(words_in_quote)
    print("--------")
    stop_wrds = set(stopwords.words("english"))
    filtered_list = []
    
    stop_words = nltk.corpus.stopwords.words("english")
    #********
    cont = 0
    for palavra in texto.split():
        if palavra.lower() not in stop_words:
            arquivo_saida.write(palavra + " ")
            cont = cont + 1
        if cont%7 == 0:
             arquivo_saida.write("\n")
             cont = 1
    #*****************
    
    #RETIRANDO STOP_WORDS
    for word in words_in_quote:
        if word.casefold() not in stop_wrds:
            filtered_list.append(word.lower())
    print(filtered_list)

    return filtered_list



def fazendo_lemmatizing(filtered_list):

    lemmatized_words = []
    for word in filtered_list:
        lemmatized_words.append(lemmatizer.lemmatize(word, "v")) #v é para retirar o formato dos verbos

    #lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_list]
    
    #print(lemmatized_words)
    return lemmatized_words
    print("--------")


def fazendo_stemming(filtered_list):

    stemmed_words = []
    for words in filtered_list:
        stemmed_words.append(stemmer.stem(words))
    
    return stemmed_words
    print(stemmed_words)
    print("--------")


arquivo_pdf = open("artigos/artigo.pdf", 'rb')
arquivo_saida = open("arquivo_saida.txt", 'w')

pdf = PyPDF2.PdfReader(arquivo_pdf)

# Acessar a página pelo índice
pagina = pdf.pages[0]  # Para acessar a primeira página, use o índice 0

texto = pagina.extract_text()  # Extrair o texto da página

print(texto)

filtered_list = retira_stop_words(texto)

lemmatize_wrd = fazendo_lemmatizing(filtered_list)

#stemmed_wrd = fazendo_stemming(lemmatize_wrd)

arquivo_pdf.close()
arquivo_saida.close()

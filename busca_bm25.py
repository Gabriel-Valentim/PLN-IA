import PyPDF2
import nltk
import re
import heapq
import json

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import trigrams

from rank_bm25 import BM25Okapi

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


def retira_referencias(texto):

    words_in_quote = word_tokenize(texto, "english", False)
    texto_sem_referencia = []
    referencias = False

    for words in words_in_quote:
        if words == "References" or words == "REFERENCES":
            break
        else:
           texto_sem_referencia.append(words)


    return texto_sem_referencia

def remove_stop_words(texto):
    
    stop_wrds = set(stopwords.words("english"))
    filtered_list = []
    
    #RETIRANDO STOP_WORDS
    for word in texto:
        if word.casefold() not in stop_wrds:
            if word != "–" :
                filtered_list.append(word.casefold())
    
    filtered_list = [re.sub('[-%,.!?;*:|()\[|\]“”]', '', word) for word in filtered_list]

    while '' in filtered_list:
        filtered_list.pop(filtered_list.index(''))

    #print(filtered_list)
    return filtered_list


def busca_bm25(word, corpus):
    tokenized_word  = word.split(" ")
    print(tokenized_word)
    #verificar essa função pode estar errada, ver de tentar fazer um for para ele percorrer cara lista de palavras 
    bm25 = BM25Okapi(corpus)
    print(bm25)
    doc_scores = bm25.get_scores(tokenized_word)
    print(doc_scores)
    bm25.get_top_n(tokenized_word, corpus, n=1)
    

def main():

    termo_pesquisa = ""

    while True:
        try:
            termo_pesquisa = str(input("Digite uma palavra para buscar: "))
            break
        except ValueError:
            print("Entrada inválida.")

    contador = 0
    lista_artigos = []

    arquivo_saida = open("string_tokenized.txt", "w")

    while contador < 10:

        nome_arquivo = f"artigos/artigo{contador}.pdf"
        print(nome_arquivo)
        arquivo_pdf = open(nome_arquivo, 'rb')
        pdf = PyPDF2.PdfReader(arquivo_pdf)

        texto_completo = ""

        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            texto_completo += texto_pagina

        #print(texto_completo)
        texto_sem_referencia = retira_referencias(texto_completo)
        filtered_list = remove_stop_words(texto_sem_referencia)

        #arquivo_saida.write(str(filtered_list))    NÃO FUNCIONA
        lista_artigos.append(filtered_list)
        
        arquivo_pdf.close()
        
        contador+=1


    with open("string_tokenized.json", "w") as arquivo:
            json.dump(lista_artigos, arquivo)

    #print(lista_artigos) 

    busca_bm25(termo_pesquisa, lista_artigos)
    
    arquivo_saida.close()

if __name__ == "__main__":
  main()
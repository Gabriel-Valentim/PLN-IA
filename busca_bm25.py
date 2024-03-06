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
            if word != "–" :
                filtered_list.append(word.casefold())
    
    filtered_list = [re.sub('[-%,.!?;*:|()\[|\]“”]', '', word) for word in filtered_list]

    while '' in filtered_list:
        filtered_list.pop(filtered_list.index(''))

    return filtered_list


def busca_bm25(word, corpus):
    tokenized_word  = word.split(" ")

    bm25 = BM25Okapi(corpus)

    doc_scores = bm25.get_scores(tokenized_word)
    print(f"TF: {doc_scores}")
    bm25.get_top_n(tokenized_word, corpus, n=1)
    calcula_idf(doc_scores)

   



def calcula_idf(doc_scores):
    classificacao_idf = ""
    score_idf = 0
    contador = 0
    for score in doc_scores:
        if score != 0:
            print(f"Artigo {contador}: {round(score,3)}")
        score_idf += score
        contador += 1
    
    score_idf = score_idf / len(doc_scores)

    if round(score_idf,3) >= 0.65:
        classificacao_idf = "IDF baixo, palavra comum."
    else:
        classificacao_idf = "IDF alto, termo raro."
    
    print(classificacao_idf)



    

def main():

    termo_pesquisa = ""

    while True:
        try:
            print("**************************************")
            print("**                                  **")
            print("**                                  **")
            print("**                                  **")
            print("**        Digite uma palavra        **")
            print("**            para buscar           **")
            print("**                                  **")
            print("**                                  **")
            print("**                                  **")
            termo_pesquisa = str(input("=> "))
            print("**                                  **")
            print("**                                  **")
            print("**                                  **")
            print("**                                  **")
            print("**************************************")
            break
        except ValueError:
            print("Entrada inválida.")

    contador = 0
    lista_artigos = []

    arquivo_saida = open("string_tokenized.txt", "w")

    while contador < 10:

        nome_arquivo = f"artigos/artigo{contador}.pdf"
        print(f"Lendo: {nome_arquivo}")
        arquivo_pdf = open(nome_arquivo, 'rb')
        pdf = PyPDF2.PdfReader(arquivo_pdf)

        texto_completo = ""

        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            texto_completo += texto_pagina

        #print(texto_completo)
        texto_sem_referencia = retira_referencias(texto_completo)
        filtered_list = remove_stop_words(texto_sem_referencia)

        #arquivo_saida.write(str(filtered_list))    NAO FUNCIONA
        lista_artigos.append(filtered_list)
        
        arquivo_pdf.close()
        
        contador+=1


    with open("string_tokenized.json", "w") as arquivo:
            json.dump(lista_artigos, arquivo)


    busca_bm25(termo_pesquisa, lista_artigos)
    
    arquivo_saida.close()

if __name__ == "__main__":
  main()
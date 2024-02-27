import PyPDF2
import nltk
import re
import heapq

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
arquivo_saida = open("arquivo_saida.txt", 'w')

def retira_stop_words(texto):
    
    words_in_quote = word_tokenize(texto, "english", False)
    stop_wrds = set(stopwords.words("english"))
    filtered_list = []
    
    #RETIRANDO STOP_WORDS
    for word in words_in_quote:
        if word.casefold() not in stop_wrds:
            if word != "–" :
                filtered_list.append(word.casefold())
    
    filtered_list = [re.sub('[-%,.!?;*:|()\[|\]“”]', '', word) for word in filtered_list]

    while '' in filtered_list:
        filtered_list.pop(filtered_list.index(''))

    print(filtered_list)
    return filtered_list



def fazendo_lemmatizing(filtered_list):

    #funcao para descobrir se a palavra é um verbo, substantivo, ou adjetivo e após isso fazer a lematizacao
    tagged_words = nltk.pos_tag(filtered_list)
    lemmatized_words = []
    
    for word, tag in tagged_words:
        if "VB" in tag:
            lemmatized_words.append(lemmatizer.lemmatize(word, "v")) #V é para retirar o formato dos verbos
        elif "NN" in tag:
            lemmatized_words.append(lemmatizer.lemmatize(word, "n")) #N é para retirar o formato dos substantivos
        elif "JJ" in tag:
            lemmatized_words.append(lemmatizer.lemmatize(word, "a")) #A é para retirar o formato dos adjetivos
        else:
             lemmatized_words.append(word)

    #print(lemmatized_words)
    return lemmatized_words


def fazendo_stemming(filtered_list):

    stemmed_words = []
    for words in filtered_list:
        stemmed_words.append(stemmer.stem(words))
    
    return stemmed_words


def termos_mais_citados(filtered_list):
    word_counts = {}

    for word in filtered_list:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    
    most_common_words = heapq.nlargest(10, word_counts.items(), key=lambda x: x[1])
    
    identificador = 1
    print("\n10 TERMOS MAIS CITADOS:")
    for word, count in most_common_words:
        
        print(identificador,"°:", f"{word}: {count}")
        identificador += 1
        


def main():

    nome_artigo = ""

    while True:
        try:
            numero_artigo = int(input("Digite o número do artigo (0-9): "))
            if 0 <= numero_artigo < 10:
                if numero_artigo == 0:
                    nome_artigo = "artigos/artigo.pdf"
                elif numero_artigo == 1:
                    nome_artigo = "artigos/artigo2.pdf"
                elif numero_artigo == 2:
                    nome_artigo = "artigos/artigo3.pdf"
                elif numero_artigo == 3:
                    nome_artigo = "artigos/artigo4.pdf"
                elif numero_artigo == 4:
                    nome_artigo = "artigos/artigo5.pdf"
                elif numero_artigo == 5:
                    nome_artigo = "artigos/artigo6.pdf"
                elif numero_artigo == 6:
                    nome_artigo = "artigos/artigo7.pdf"
                elif numero_artigo == 7:
                    nome_artigo = "artigos/artigo8.pdf"
                elif numero_artigo == 8:
                    nome_artigo = "artigos/artigo9.pdf"
                elif numero_artigo == 9:
                    nome_artigo = "artigos/artigo10.pdf"
                break
            else:
                print("Número inválido. Digite um número entre 0 e 9.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    arquivo_pdf = open(nome_artigo, 'rb')
    

    pdf = PyPDF2.PdfReader(arquivo_pdf)

    # Acessar a página pelo índice
    #pagina = pdf.pages[0]  # Para acessar a primeira página, use o índice 0

    #texto = pdf.extract_text()  # Extrair o texto da página
    texto_completo = ""

    for pagina in pdf.pages:
        texto_pagina = pagina.extract_text()
        texto_completo += texto_pagina
        print(texto_completo)


    tokenized_list = retira_stop_words(texto_completo)

    lemmatize_wrd = fazendo_lemmatizing(tokenized_list)

    #stemmed_wrd = fazendo_stemming(lemmatize_wrd)

    termos_mais_citados(tokenized_list)

    arquivo_pdf.close()
    arquivo_saida.close()

if __name__ == "__main__":
  main()
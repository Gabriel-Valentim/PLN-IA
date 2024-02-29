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
from nltk.util import trigrams

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
arquivo_saida = open("arquivo_saida.txt", 'w')


def retira_referencias(texto):

    words_in_quote = word_tokenize(texto, "english", False)
    texto_sem_referencia = []
    referencias_texto = []
    referencias = False

    for words in words_in_quote:
        if words == "References" or words == "REFERENCES":
            referencias = True
        elif referencias == False:
            texto_sem_referencia.append(words)
        else:
            referencias_texto.append(words)


    return texto_sem_referencia, referencias_texto



def retira_stop_words(texto):
    
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



def extrai_objetivo(texto):
    # Expressão regular para encontrar a frase inicial e tudo até o primeiro ponto final.
    possiveis_objetivos = ['this study aimed', 'in this research']
    texto_objetivo = ""

    # Encontrar a posição do resumo (abstract)
    inicio_abstract = texto.find("abstract")
    if inicio_abstract != -1:
        # Encontrar o final do resumo (abstract)
        fim_abstract = texto.find("introduction", inicio_abstract)
        if fim_abstract != -1:
            texto_abstract = texto[inicio_abstract+len("abstract"):fim_abstract].strip()
        else:
            texto_abstract = texto[inicio_abstract+len("abstract"):].strip()

    # Encontrar a posição da introdução (introduction)
    inicio_introduction = texto.find("introduction")
    if inicio_introduction != -1:
        # Encontrar o final da introdução (introduction)
        fim_introduction = texto.find("ii.", inicio_introduction)
        if fim_introduction != -1:
            texto_introduction = texto[inicio_introduction+len("introduction"):fim_introduction].strip()
        else:
            texto_introduction = texto[inicio_introduction+len("introduction"):].strip()

    # Procurar o objetivo no resumo (abstract)
    for objetivo in possiveis_objetivos:
        match_abstract = re.search(re.escape(objetivo) + '(.*?)\.', texto_abstract, flags=re.IGNORECASE | re.DOTALL)
        match_introduction = re.search(re.escape(objetivo) + '(.*?)\.', texto_introduction, flags=re.IGNORECASE | re.DOTALL)
        if match_abstract:
            texto_objetivo = match_abstract.group(0)
            break
        elif match_introduction:
            texto_objetivo = match_introduction.group(0)
            break

    print("==========================")
    print(texto_objetivo)
    print("==========================")

    return texto_objetivo


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
    texto_aux = ""

    for pagina in pdf.pages:
        texto_pagina = pagina.extract_text()
        texto_completo += texto_pagina
        texto_aux += texto_pagina.lower()
        


    print(texto_aux)
    obj = extrai_objetivo(texto_aux)

    texto_sem_referencia, referencias = retira_referencias(texto_completo)

    tokenized_list = retira_stop_words(texto_sem_referencia)

    lemmatize_wrd = fazendo_lemmatizing(tokenized_list)

    #stemmed_wrd = fazendo_stemming(lemmatize_wrd)

    termos_mais_citados(tokenized_list)

    arquivo_pdf.close()
    arquivo_saida.close()

if __name__ == "__main__":
  main()
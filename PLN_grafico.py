import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
import PyPDF2
import nltk
import re
import heapq
import matplotlib.pyplot as plt

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS


lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# Inicializar o Tkinter
root = tk.Tk()
root.title("Extrator de Informações de Artigos")
root.geometry("400x200")

# Funções para extrair informações do PDF
def extrair_informacoes():
    nome_artigo = arquivo_combobox.get()
    if nome_artigo == "":
        messagebox.showerror("Erro", "Por favor, selecione um artigo.")
        return

    arquivo_pdf = open(nome_artigo, 'rb')
    pdf = PyPDF2.PdfReader(arquivo_pdf)

    # Extrair texto do PDF
    texto_completo = ""
    texto_aux = ""
    for pagina in pdf.pages:
        texto_pagina = pagina.extract_text()
        texto_completo += texto_pagina
        texto_aux += texto_pagina.lower()

    obj = extrai_objetivo(texto_aux)
    met = extrai_metodologia(texto_aux)
    prob = extrai_problema(texto_aux)
    contrib = find_contribution(texto_aux)

    texto_sem_referencia, referencias = retira_referencias(texto_completo)
    tokenized_list = retira_stop_words(texto_sem_referencia)

    termos_mais_citados(tokenized_list)

    arquivo_pdf.close()

    # Abrir nova janela para mostrar informações
    mostrar_resultados(obj, met, prob, contrib)
    salvar_dados(obj, met, prob, contrib, referencias)

def mostrar_resultados(obj, met, prob, contrib):
    resultados_window = tk.Toplevel(root)
    resultados_window.title("Informações do Artigo")
    resultados_window.geometry("600x400")

    label_obj = tk.Label(resultados_window, text="Objetivo:")
    label_obj.pack()
    text_obj = tk.Text(resultados_window, height=5, wrap=tk.WORD)
    text_obj.insert(tk.END, obj)
    text_obj.pack()

    label_met = tk.Label(resultados_window, text="Metodologia:")
    label_met.pack()
    text_met = tk.Text(resultados_window, height=5, wrap=tk.WORD)
    text_met.insert(tk.END, met)
    text_met.pack()

    label_prob = tk.Label(resultados_window, text="Problema:")
    label_prob.pack()
    text_prob = tk.Text(resultados_window, height=5, wrap=tk.WORD)
    text_prob.insert(tk.END, prob)
    text_prob.pack()

    label_contrib = tk.Label(resultados_window, text="Contribuições:")
    label_contrib.pack()
    text_contrib = tk.Text(resultados_window, height=5, wrap=tk.WORD)
    text_contrib.insert(tk.END, contrib)
    text_contrib.pack()

def extrair_termos_citados():
    nome_artigo = arquivo_combobox.get()
    if nome_artigo == "":
        messagebox.showerror("Erro", "Por favor, selecione um artigo.")
        return

    arquivo_pdf = open(nome_artigo, 'rb')
    pdf = PyPDF2.PdfReader(arquivo_pdf)

    # Extrair texto do PDF
    texto_completo = ""
    texto_aux = ""
    for pagina in pdf.pages:
        texto_pagina = pagina.extract_text()
        texto_completo += texto_pagina
        texto_aux += texto_pagina.lower()

    texto_sem_referencia, referencias = retira_referencias(texto_completo)
    tokenized_list = retira_stop_words(texto_sem_referencia)

    termos_mais_citados(tokenized_list)

    arquivo_pdf.close()



# GUI
label_artigo = tk.Label(root, text="Selecione o artigo:")
label_artigo.pack()

artigos = ["artigos/artigo0.pdf", "artigos/artigo1.pdf", "artigos/artigo2.pdf",
           "artigos/artigo3.pdf", "artigos/artigo4.pdf", "artigos/artigo5.pdf",
           "artigos/artigo6.pdf", "artigos/artigo7.pdf", "artigos/artigo8.pdf",
           "artigos/artigo9.pdf"]  # Adicione mais artigos conforme necessário
arquivo_combobox = ttk.Combobox(root, values=artigos, width=30)
arquivo_combobox.pack()

botao_extrair = tk.Button(root, text="Extrair Informações", command=extrair_informacoes)
botao_extrair.pack()


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
        if(len(word) == 1 or str.isdigit(word) or word == "et" or word == "al" or word == "td"):
            continue
        else:    
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
    
    most_common_words = heapq.nlargest(10, word_counts.items(), key=lambda x: x[1])
    
    palavras = {}
    identificador = 1
    print("\n10 TERMOS MAIS CITADOS:")
    for word, count in most_common_words:
        
        print(f"{identificador}°: {word}: {count}")
        palavras[word] = count
        identificador += 1

    wordcloud = WordCloud(background_color="white").generate_from_frequencies(palavras)

    wordcloud.to_file('wordcloud_common_words.png')

    # Exibir a nuvem de palavras
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()



def extrai_objetivo(texto):
    # Expressão regular para encontrar a frase inicial e tudo até o primeiro ponto final.
    possiveis_objetivos = ['this study', 'in this research', 'this paper', ' in this work']
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



def extrai_problema(texto):
    possiveis_problemas = ['problem', 'issue', 'challenge', 'limitation', 'drawback', 'constraint']
    texto_problema = ""

    # Encontrar a posição do resumo (abstract)
    inicio_abstract = texto.find("abstract")
    if inicio_abstract != -1:
        # Encontrar o final do resumo (abstract)
        fim_abstract = texto.find("introduction", inicio_abstract)
        if fim_abstract != -1:
            texto_abstract = texto[inicio_abstract+len("abstract"):fim_abstract].strip()
        else:
            texto_abstract = texto[inicio_abstract+len("abstract"):].strip()

    # Procurar o problema no resumo (abstract)
    for problema in possiveis_problemas:
        matches = re.finditer(re.escape(problema), texto_abstract, flags=re.IGNORECASE)
        for match in matches:
            inicio = texto_abstract.rfind(".", 0, match.start()) + 1
            fim = texto_abstract.find(".", match.end()) + 1
            texto_problema += texto_abstract[inicio:fim]


    if texto_problema == "":
        inicio_introduction = texto.find("introduction")
        if inicio_introduction != -1:
            fim_introduction = texto.find("ii.", inicio_introduction)
            if fim_introduction != -1:
                texto_introduction = texto[inicio_introduction+len("introduction"):fim_introduction].strip()
            else:
                texto_introduction = texto[inicio_introduction+len("introduction"):].strip()

        for problema in possiveis_problemas:
            matches = re.finditer(re.escape(problema), texto_introduction, flags=re.IGNORECASE)
            for match in matches:
                inicio = texto_introduction.rfind(".", 0, match.start()) + 1
                fim = texto_introduction.find(".", match.end()) + 1
                texto_problema += texto_introduction[inicio:fim]



    print("==========================")
    print(f"problema: \n {texto_problema}")
    print("==========================")

    return texto_problema


def extrai_metodologia(texto):
    possiveis_metodologias = ['method', 'approach', 'strategy', 'technique']
    texto_metodologia = ""

    # Encontrar a posição do resumo (abstract)
    inicio_abstract = texto.find("abstract")
    if inicio_abstract != -1:
        # Encontrar o final do resumo (abstract)
        fim_abstract = texto.find("introduction", inicio_abstract)
        if fim_abstract != -1:
            texto_abstract = texto[inicio_abstract+len("abstract"):fim_abstract].strip()
        else:
            texto_abstract = texto[inicio_abstract+len("abstract"):].strip()
    else:
        texto_abstract = ""

    # Procurar a metodologia no resumo (abstract) ou na introdução
    for metodologia in possiveis_metodologias:
        matches = re.finditer(re.escape(metodologia), texto_abstract, flags=re.IGNORECASE)
        for match in matches:
            inicio = texto_abstract.rfind(".", 0, match.start()) + 1
            fim = texto_abstract.find(".", match.end()) + 1
            texto_metodologia += texto_abstract[inicio:fim]

    
    # Se não encontrar a palavra "method" no abstract, buscar na introdução
    if texto_metodologia == "":
        inicio_introduction = texto.find("introduction")
        if inicio_introduction != -1:
            fim_introduction = texto.find("ii.", inicio_introduction)
            if fim_introduction != -1:
                texto_introduction = texto[inicio_introduction+len("introduction"):fim_introduction].strip()
            else:
                texto_introduction = texto[inicio_introduction+len("introduction"):].strip()

        for metodologia in possiveis_metodologias:
            matches = re.finditer(re.escape(metodologia), texto_introduction, flags=re.IGNORECASE)
            for match in matches:
                inicio = texto_introduction.rfind(".", 0, match.start()) + 1
                fim = texto_introduction.find(".", match.end()) + 1
                texto_metodologia += texto_introduction[inicio:fim]


    print("==========================")
    print(f"metodologia \n {texto_metodologia}")
    print("==========================")

    return texto_metodologia

def find_contribution(texto_completo):
    key_wrd = ['contribu']
    texto_contribuition = []

    for word in key_wrd:
        matches = re.finditer(re.escape(word), texto_completo, flags=re.IGNORECASE)
        if matches:
            for match in matches:
                inicio = texto_completo.rfind(".", 0, match.start()) + 1
                fim = texto_completo.find(".", match.end()) + 1
                texto_contribuition.append(texto_completo[inicio:fim])
    
    if texto_contribuition:
        cleaned_phrases = []

        for phrase in texto_contribuition:
            cleaned_phrases.append(re.sub(r"\n", "", phrase))
        
        print("** CONTRIBUICOES **")
        print(cleaned_phrases)
        print("** ************* **")
        return cleaned_phrases
    else:
        print("NAO FOI POSSIVEL ENCONTRAR AS CONTRIBUICOES")
        return []  # Retorna uma lista vazia se não encontrar contribuições


def salvar_dados(obj, met, prob, contrib, referencias):
    try:
        nome_arquivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Arquivos de texto", "*.txt")])
        
        tam_contrib = len(contrib)
        cont = 0
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(f"Objetivo: {obj};;\n")
            arquivo.write(f"Metodologia: {met};;\n")
            arquivo.write(f"Problema: {prob};;\n")
            arquivo.write("Contribuicoes:\n")
            for c in contrib:
                cont += 1
                arquivo.write(f"{c}\n")
                if cont == tam_contrib:
                    arquivo.write(";;\n")
                    cont = 0
            arquivo.write(f"Referencias: {referencias} ;;\n")
            #for ref in referencias:
            #    arquivo.write(f"{ref}\n")
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar os dados: {str(e)}")


# Executar o loop principal do Tkinter
root.mainloop()
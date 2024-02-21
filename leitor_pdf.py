import PyPDF2
import nltk

nltk.download('stopwords')

def retira_stop_words(texto):
    
    stop_words = nltk.corpus.stopwords.words("english")
    cont = 0
    for palavra in texto.split():
        if palavra.lower() not in stop_words:
            arquivo_saida.write(palavra + " ")
            cont = cont + 1
        if cont%7 == 0:
             arquivo_saida.write("\n")
             cont = 1


arquivo_pdf = open("artigos/artigo.pdf", 'rb')
arquivo_saida = open("arquivo_saida.txt", 'w')

pdf = PyPDF2.PdfReader(arquivo_pdf)

# Acessar a página pelo índice
pagina = pdf.pages[0]  # Para acessar a primeira página, use o índice 0

texto = pagina.extract_text()  # Extrair o texto da página

print(texto)

retira_stop_words(texto)

arquivo_pdf.close()
arquivo_saida.close()

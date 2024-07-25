import os
from docx import Document

# Verificar se o arquivo modelo.docx existe na pasta atual
if not os.path.exists('modelo.docx'):
    print("O arquivo modelo.docx não foi encontrado.")
else:
    # Função para substituir texto no documento
    def replace_text_in_doc(doc, replacements):
        for paragraph in doc.paragraphs:
            for key, value in replacements.items():
                if key in paragraph.text:
                    paragraph.text = paragraph.text.replace(key, value)

    # Carrega o documento modelo
    doc = Document('modelo.docx')

    # Define os textos a serem substituídos
    replacements = {
        '{nome}': 'Alexsander',
        '{valor}': '700,00'
    }

    # Substitui os textos no documento
    replace_text_in_doc(doc, replacements)

    # Salva o novo documento com as substituições feitas
    doc.save('documento_final.docx')
    print("O documento foi salvo como documento_final.docx")

import os
from docx import Document
import time


data = {
    "data": "2023-03-08",
    "destinatario": "Público",
    "titulo": "Treinamento Avançado em Prestação de Serviços e Produtos",
    "objetivo": "Ampliar e aprimorar o conhecimento e habilidades técnicas dos profissionais envolvidos na prestação de serviços e produtos, visando otimizar o atendimento ao cliente e fortalecer a competitividade da organização.",
    "periodo": "10 dias corridos (com base na carga horária total)",
    "detalhamento_proposta": [
        {
            "titulo_etapa": "Módulo 1: Fundamentos de Atendimento ao Cliente",
            "carga_horaria_necessaria": "20 horas",
            "publico_alvo": "Profissionais de atendimento, gestores e supervisores",
            "objetivo_da_etapa": "Aprimorar as competências de comunicação, relacionamento interpessoal e resolução de conflitos, visando proporcionar um atendimento excepcional ao cliente.",
            "conteudo_programatico": [
                "Técnicas de comunicação eficaz",
                "Empatia e escuta ativa",
                "Gestão de conflitos e reclamações",
                "Atendimento personalizado e segmentado",
                "Avaliação e mensuração do atendimento",
            ],
        },
    ],
    "carga_horaria_total": "65 horas",
    "valor_investimento": "R$ 5.000,00",
}

replacements = {
    "{data}": "data",
    "{destinatario}": "destinatario",
    "{titulo}": "titulo",
    "{objetivo}": "objetivo",
    "{periodo}": "periodo",
    "{carga_horaria_total}": "carga_horaria_total",
    "{valor_investimento}": "valor_investimento",
    # "{detalhamento_proposta}": "detalhamento_proposta",
}


def replace_text_in_doc(doc, replacements, data_json):
    for paragraph in doc.paragraphs:
        for key, value in replacements.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, data_json[value])
        



def generate_doc(data_json):
    doc = Document("modelo.docx")

    replace_text_in_doc(doc, replacements, data_json)
    file_name = f"{time.time()}.docx"
    doc.save(file_name)
    content_file = open(file_name, "rb")
    return content_file



from docx import Document
import time
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Inches
from docx.shared import Pt


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

REPLACEMENTS = {
    "{data}": "data",
    "{cliente}": "cliente",
    "{destinatario}": "destinatario",
    "{titulo}": "titulo",
    "{objetivo}": "objetivo",
    "{periodo}": "periodo",
    "{carga_horaria_total}": "carga_horaria_total",
    "{valor_investimento}": "valor_investimento",
}

SCHEMA_DETALHAMENTO_PROPOSTA = {
    "carga_horaria_necessaria": "Carga Horária",
    "publico_alvo": "Público-alvo",
    "objetivo_da_etapa": "Objetivo",
    "conteudo_programatico": "Conteúdo Programático (ementa)",
}


def replace_text_in_doc(doc, data_json):
    replace_paragraph(doc, data_json)
    if data_json.get("detalhamento_proposta"):
        insert_detalhamento_da_proposta(doc, data_json.get("detalhamento_proposta"))


def replace_paragraph(doc, data_json):
    for paragraph in doc.paragraphs:
        for key, value in REPLACEMENTS.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, data_json[value])


def insert_detalhamento_da_proposta(doc, detalhamento_proposta: list):
    table = doc.tables[2]
    for detalhe in detalhamento_proposta:
        for key, value in detalhe.items():
            if key == "titulo_etapa":
                insert_line_merge(table, value)
                continue
            insert_line_information(table, SCHEMA_DETALHAMENTO_PROPOSTA[key], value)


def insert_line_merge(table, text):
    merged_row = table.add_row()
    merged_row.cells[0].text = text
    merged_row.cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def insert_line_information(table, key, value):
    new_row = table.add_row()
    new_row._element.add_tc()

    new_row.cells[0].text = key
    if isinstance(value, list):
        for item in value:
            new_row.cells[1].add_paragraph(f"• {item}")
    else:
        new_row.cells[1].text = value

    table_width = Inches(6)
    cell_1_width = int(table_width * 0.2)
    cell_2_width = int(table_width * 0.8)
    new_row.cells[0].width = cell_1_width
    new_row.cells[1].width = cell_2_width


def generate_doc(data_json):
    doc = Document("modelo.docx")
    replace_text_in_doc(doc, data_json)
    file_name = f"{time.time()}.docx"
    doc.save(file_name)
    content_file = open(file_name, "rb")
    return content_file


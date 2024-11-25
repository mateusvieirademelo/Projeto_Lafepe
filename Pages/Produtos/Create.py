import streamlit as st
import datetime
from datetime import date
import controllers.ProdutoController as Produtocontroller
import models.Produto as produto
import pandas as pd
import pyodbc


def insert_database(itens):
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-H123T9I7\SQLEXPRESS;'
        'DATABASE=Lafepe03;'
        'UID=leonardo;'
        'PWD=leonardo30'
    )
    cursor = connection.cursor()

    for index, row in itens.iterrows():
        # Convertendo a data para o formato correto
        row['datta'] = pd.to_datetime(row['datta'], format='%d/%m/%Y').strftime('%Y-%m-%d')
        cursor.execute(
            "INSERT INTO consolidacao (codigo_mp, descricao, estoque, und, quarentena, datta) VALUES (?, ?, ?, ?, ?, ?)",
            row['codigo_mp'], row['descricao'], row['estoque'], row['und'], row['quarentena'], row['datta']
        )

    connection.commit()
    cursor.close()
    connection.close()


def Create():
    idAlteracao = st._get_query_params().get("codigo_mp")
    produtoRecuperado = None
    if idAlteracao:
        idAlteracao = idAlteracao[0]
        produtoRecuperado = Produtocontroller.SelecionarByCodigo(idAlteracao)
        st._set_query_params(
            codigo_mp=[produtoRecuperado.codigo_mp]
        )
        st.title("Alterar Insumo")
    else:
        st.title("Cadastrar Insumo")

    with st.form(key="include_produto"):
        if produtoRecuperado is None:
            listUnd = ["Kg", "L", "Und", "Mh"]
            input_codigo = st.text_input(label="Codigo matéria prima")
            input_descricao = st.text_input(label="Descrição do produto (Opcional)")
            input_estoque = st.number_input(label='Quantidade em estoque')
            input_und = st.selectbox("Selecione a unidade de medida", listUnd)
            input_quarentena = st.number_input(label="Quarentena", step=1)
            input_datta = st.date_input("Validade", value=datetime.date.today(), format="DD/MM/YYYY")
        else:
            input_codigo = st.text_input(label="Codigo matéria prima", value=produtoRecuperado.codigo_mp)
            input_descricao = st.text_input(label="Descrição do produto (Opcional)", value=produtoRecuperado.descricao)
            input_estoque = st.number_input(label='Quantidade em estoque', value=produtoRecuperado.estoque)
            input_und = st.selectbox("Selecione a unidade de medida", ["Kg", "L", "Und", "Mh"], index=["Kg", "L", "Und", "Mh"].index(produtoRecuperado.und))
            input_quarentena = st.number_input(label="Quarentena", step=1, value=produtoRecuperado.quarentena)
            input_datta = st.date_input("Validade", value=produtoRecuperado.datta, format="DD/MM/YYYY")

        input_button_submit = st.form_submit_button("Enviar")

        if input_button_submit:
            novo_produto = produto.Produto(input_codigo, input_descricao, input_estoque, input_und, input_quarentena, input_datta)
            try:
                if produtoRecuperado is None:
                    Produtocontroller.Incluir(novo_produto)
                    st.success("Produto cadastrado com sucesso!")
                    verifica_alerta(input_datta)
                else:
                    Produtocontroller.Alterar(novo_produto)
                    st.success("Produto alterado com sucesso!")
            except ValueError as e:
                st.error(e)

    # Adicionando a funcionalidade de upload de arquivo
    st.markdown("---")
    st.header("Upload de Arquivo Excel")
    uploaded_file = st.file_uploader("Faça upload de um arquivo Excel", type=["xls", "xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        insert_database(df)
        st.success("Os dados foram inseridos no banco de dados com sucesso!")

# Função principal para verificar e disparar alerta
def dias_ate_data(data_alvo):
    hoje = date.today()
    delta = data_alvo - hoje
    return delta.days

def verifica_alerta(data_alvo):
    dias_restantes = dias_ate_data(data_alvo)
    if dias_restantes == 30:
        st.warning("ALERTA: Faltam 30 dias para data de Validade!")
    return dias_restantes

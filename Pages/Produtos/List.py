import streamlit as st
from datetime import datetime, date
import controllers.ProdutoController as Produtocontroller
import Pages.Produtos.Create as PagesCriarProduto
import plotly.express as px
import pandas as pd
import models.Produto as produto

#Se o insumo estiver menor ou igual a 30 dias, a validade vai fica vermelho pra destacar
def highlight_date(datta):
    delta = datta - date.today()
    if delta.days <= 30:
        return 'color: red'
    else:
        return ''

def List():
    # Verifica se tem um código_mp no estado da sessão para edição
    codigo_mp_edicao = st.session_state.get('codigo_mp', None)

    # Adiciona filtro por mês
    meses = ["Todos", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    mes_selecionado = st.selectbox("Filtrar por mês de validade", meses)

    if codigo_mp_edicao:
        # Recuperar o produto pelo código_mp
        produtoRecuperado = Produtocontroller.SelecionarByCodigo(codigo_mp_edicao)

        if produtoRecuperado:
            st.title("Alterar Insumos")
            with st.form(key="edit_produto"):
                st.write(f"Código MP: {produtoRecuperado.codigo_mp}")  # Exibe o código MP sem permitir a edição
                input_descricao = st.text_input(label="Descrição do produto (Opcional)", value=produtoRecuperado.descricao)
                input_estoque = st.number_input(label='Quantidade em estoque', value=float(produtoRecuperado.estoque))
                input_und = st.selectbox("Selecione a unidade de medida", ["Kg", "L", "Und", "Mh"], index=["Kg", "L", "Und", "Mh"].index(produtoRecuperado.und))
                input_quarentena = st.number_input(label="Quarentena", step=1, value=int(produtoRecuperado.quarentena))
                input_datta = st.date_input("Validade", value=produtoRecuperado.datta, format="DD/MM/YYYY")
                
                input_button_submit = st.form_submit_button("Salvar Alterações")

                if input_button_submit:
                    produtoEditado = produto.Produto(produtoRecuperado.codigo_mp, input_descricao, input_estoque, input_und, input_quarentena, input_datta)
                    Produtocontroller.Alterar(produtoEditado)
                    st.success("Produto alterado com sucesso!")
                    st.session_state.pop('codigo_mp', None)  # Limpa o código MP do estado da sessão
                    st.rerun()
        return

    # Exibição da lista de produtos
    st.title("Lista de Insumos")
    colms = st.columns((1, 1, 1, 1, 1, 1, 1, 1))
    campos = ['Codigo MP', 'Descrição', 'Estoque', 'Und', 'Quarenten', 'Validade', 'Excluir', 'Alterar']
    for col, campo_nome in zip(colms, campos):
        col.write(campo_nome)
    
    # Filtrando produtos pelo mês selecionado
    produtos = Produtocontroller.SelecionarTodos()
    if mes_selecionado != "Todos":
        mes_index = meses.index(mes_selecionado)
        produtos = [item for item in produtos if item.datta.month == mes_index]
        
    for item in produtos:
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((1, 1, 1, 1, 1, 1, 1, 1))
        
        col1.write(item.codigo_mp)
        col2.write(item.descricao)
        col3.write(item.estoque)
        col4.write(item.und)
        col5.write(item.quarentena)
        validade_formatada = item.datta.strftime("%d/%m/%Y")
        col6.markdown(f'<p style="{highlight_date(item.datta)}">{validade_formatada}</p>', unsafe_allow_html=True)

        
        button_space_excluir = col7.empty()
        on_click_excluir = button_space_excluir.button('Excluir', key='btnExcluir' + str(item.codigo_mp))
        button_space_alterar = col8.empty()
        on_click_alterar = button_space_alterar.button('Alterar', key='btnAlterar' + str(item.codigo_mp))

        if on_click_excluir:
            Produtocontroller.Excluir(item.codigo_mp)
            st.rerun()
        
        if on_click_alterar:
            st.session_state['codigo_mp'] = item.codigo_mp
            st.rerun()

    # Criar e exibir o gráfico
    costumerList = []
    for item in produtos:
        costumerList.append([item.codigo_mp, item.descricao, item.estoque, item.und, item.quarentena, item.datta])

    df = pd.DataFrame(
        costumerList,
        columns=['codigo_mp', 'descricao', 'estoque', 'und', 'quarentena', 'datta']
    )

    tipo_grafico = st.selectbox('Escolha o tipo de gráfico', ['Barra', 'Pizza', 'Linha', 'Dispersão', 'Área', 'Caixa', 'Histograma'])
    if tipo_grafico == 'Barra':
        fig = px.bar(df, x='descricao', y='estoque', title='Estoque por Insumo')
    elif tipo_grafico == 'Pizza':
        fig = px.pie(df, values='estoque', names='descricao', title='Distribuição do Estoque por Insumo')
    elif tipo_grafico == 'Linha':
        fig = px.line(df, x='descricao', y='estoque', title='Estoque por Insumo ao Longo do Tempo')
    elif tipo_grafico == 'Dispersão':
        fig = px.scatter(df, x='descricao', y='estoque', title='Estoque por Insumo (Dispersão)')
    elif tipo_grafico == 'Área':
        fig = px.area(df, x='descricao', y='estoque', title='Estoque por Insumo (Área)')
    elif tipo_grafico == 'Caixa':
        fig = px.box(df, x='descricao', y='estoque', title='Distribuição do Estoque por Insumo (Box Plot)')
    elif tipo_grafico == 'Histograma':
        fig = px.histogram(df, x='estoque', title='Distribuição do Estoque')

    st.plotly_chart(fig)

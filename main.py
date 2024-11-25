import streamlit as st
from os import write
import datetime
import controllers.ProdutoController as Produtocontroller
import models.Produto as produto
import pandas as pd
import plotly.express as px
import Pages.Produtos.Create as PagesCriarProduto
import Pages.Produtos.List as PagesListaProduto

  
Page_produto = st.sidebar.selectbox(
    'Produto', ['Incluir', 'Consultar'], 0)

if Page_produto == 'Consultar':
   PagesListaProduto.List()
    
elif Page_produto == 'Incluir':
    PagesCriarProduto.Create()


 
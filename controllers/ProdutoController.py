import string
from typing import List
import services.database as db;
import models.Produto as produto;
import numpy as np

def Incluir(consolidacao):
    cursor = db.cnxn.cursor()
    cursor.execute("SELECT COUNT(*) FROM CONSOLIDACAO WHERE codigo_mp = ?", consolidacao.codigo_mp)
    count = cursor.fetchone()[0]
    
    if count == 0:
        cursor.execute("""
        INSERT INTO CONSOLIDACAO (codigo_mp, descricao, estoque, und, quarentena, datta) 
        VALUES (?,?,?,?,?,?)""",
        consolidacao.codigo_mp, consolidacao.descricao, consolidacao.estoque, consolidacao.und, consolidacao.quarentena, consolidacao.datta)
        db.cnxn.commit()
    else:
        raise ValueError(f"Código MP {consolidacao.codigo_mp} já existe. Não é possível inserir duplicata.")



def SelecionarByCodigo(codigo_mp):
    db.cursor.execute("SELECT * FROM CONSOLIDACAO WHERE codigo_mp = ?", codigo_mp)
    row = db.cursor.fetchone()

    if row:
        return produto.Produto(row[0], row[1], row[2], row[3], row[4], row[5])
    else:
        return None

def Excluir(codigo_mp):
    count = db.cnxn.cursor().execute("""
    DELETE FROM CONSOLIDACAO WHERE codigo_mp = ?""", codigo_mp).rowcount
    db.cnxn.commit()
    
def Alterar(produto):
    count = db.cursor.execute("""
    UPDATE consolidacao
    SET codigo_mp = ?, descricao = ?, estoque = ?, und = ?, quarentena = ?, datta = ?
    WHERE codigo_mp = ?
    """,
    produto.codigo_mp, produto.descricao, produto.estoque, produto.und, produto.quarentena, produto.datta, produto.codigo_mp).rowcount
    db.cnxn.commit()


def SelecionarTodos():
    db.cursor.execute("SELECT * FROM CONSOLIDACAO")
    costumerList = []

    for row in db.cursor.fetchall():
        costumerList.append(produto.Produto(row[0], row[1], row[2], row[3], row[4], row[5]))

    return costumerList
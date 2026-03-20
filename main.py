import streamlit as st
import upload as up
import pandas as pd
#from slugify import slugify

def processar_planilha(arquivo):
    st.markdown(f'### -> Produção Megaferro')
    progresso = st.progress(0, 'Lendo arquivo...')

    try: 
        data_frame = pd.read_excel(arquivo, header=2, skipfooter=1)
    except Exception as e:
        progresso.empty()
        st.error(f'Erro ao abrir arquivo. Erro: {e}')
        return

    progresso.progress(1/4, 'Validando planilha...')

    try:
        up.validar_planilha(
            data_frame, 
            ["Data Produção", "OP", "Produto","Qtd. Lote"],
            ['Data Produção' ]
        )
    except Exception as e:
        progresso.empty()
        st.error(f'Planilha inválida. Erro: {e}')
        return
    
    #data_frame.columns = [slugify(column, separator='_') for column in data_frame.columns.to_list()]
    
    progresso.progress(2/4, 'Filtrando Registros...')

    try:
        novos_dados = up.filtrar_novos_dados(data_frame, "producao_megaferro", 'OP')
    except Exception as e:
        progresso.empty()
        st.error(f'Erro ao se conectar ao banco de dados. Erro: {e}')
        return

    if novos_dados.empty:
        progresso.empty()
        st.warning('Não há dados novos na planilha')
        return

    progresso.progress(3/4, 'Enviando Dados...')

    try:
        up.adicionar_registros(novos_dados, 'producao_megaferro')
        progresso.progress(4/4, 'Finalizado!')
        progresso.empty()
        st.success(f'Base de dados atualizada com sucesso! {len(novos_dados)} registros adicionados')
    except Exception as e:
        progresso.empty()
        st.warning(f'Houve um erro ao enviar dados. Erro: {e}')
        return

def page_upload():
    st.write("# Produção Megaferro")
    col1, col2 = st.columns(2, gap='large')

    with col1:
        st.header("Enviar para o banco de dados", divider=True)

        planilha = st.file_uploader("**Planilha Produção Megaferro**", ['xlsx', 'xls'])

        botao = st.button('Enviar')

    with col2:
        st.header('Logs', divider=True)

        if planilha and botao:
            processar_planilha(planilha)      

def main():
    st.set_page_config(layout='wide', page_title="Logística Megaferro - Industria")
    page_upload()

if __name__ == "__main__":
    main()
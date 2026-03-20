import pandas as pd
from decouple import config
from sqlalchemy import create_engine, inspect

URL_DB = config('URL_DB')

def validar_planilha(data_frame: pd.DataFrame, colunas_esperadas: list[str], colunas_data: list[str] = []) -> None:
    if data_frame.empty:
        raise ValueError('Planilha Vazia')

    if list(data_frame.columns) != colunas_esperadas:
        raise TypeError('Colunas Incompatíveis')
    
    for coluna in colunas_data:
        if not pd.api.types.is_datetime64_any_dtype(data_frame[coluna]):
            raise TypeError(f'A coluna {coluna} precisa ser do tipo Data e Hora')

def filtrar_novos_dados(data_frame: pd.DataFrame, tabela: str, unico_col: str = "nro_unico") -> pd.DataFrame:
    engine = create_engine(URL_DB)
    inspector = inspect(engine)

    if inspector.has_table(tabela): 
        query = f'SELECT {unico_col} FROM {tabela};'
        pedidos_registrados = pd.read_sql_query(query, engine)
    else:
        pedidos_registrados = pd.DataFrame({unico_col: []})

    df_filtrado = data_frame[~data_frame[unico_col].isin(pedidos_registrados[unico_col])]

    return df_filtrado

def adicionar_registros(data_frame: pd.DataFrame, nome_tabela: str):
    engine = create_engine(URL_DB)  
    data_frame.to_sql(nome_tabela, engine, if_exists='append', index=False)
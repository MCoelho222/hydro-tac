import pandas as pd
import numpy as np
# from src.app.challenge import removerepeateddates
from src.app.utils.challenge import removerepeateddates


def read_bes(df, comun_cols, pt_colname, params):
    dfcols = comun_cols
    dfcols.extend(params)
    main_df = df[comun_cols]
    pts = main_df[pt_colname].drop_duplicates()
    pts = pts.reset_index(drop=True)

    for param in params:
        param_df = pd.DataFrame(columns=comun_cols)
        for idx in pts.index:
            print(pts.loc[idx])
            allparams_pt_df = main_df[main_df[pt_colname] == pts.loc[idx]]
            params_df_cols = comun_cols
            params_df_cols.append(param)
            param_pt_df = allparams_pt_df[params_df_cols]
            param_pt_df = removerepeateddates(param_pt_df, 'Data', param)
            param_df = param_df.merge(param_pt_df, how='outer', on='Data')
        print(param_df)
            


    # print(pts)


 
    return

if __name__ == "__main__":

    df = pd.read_excel('Anexo VI - Resultados analíticos gerais – qualidade das águas superficiais.xlsx', sheet_name='Sheet2')
    comun_cols = ['Data', 'Parâmetro', 'mare']
    params = ['Fósforo total', 'Sulfato']

    read_bes(df, comun_cols, 'Parâmetro', params)
    

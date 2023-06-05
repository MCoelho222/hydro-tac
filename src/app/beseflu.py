import pandas as pd
import numpy as np
from src.app.utils.challenge import removerepeateddates


def read_beseflu(df, comun_cols, pt_colname, params, risco, mode):
    dfcols = comun_cols[:]
    dfcols.extend(params)
    main_df = df[dfcols]
    pts = main_df[pt_colname].drop_duplicates()
    pts = pts.reset_index(drop=True)
    for idx in pts.index:
        if pts.loc[idx] == 'VMP' or pts.loc[idx] == 'Unidade':
            pts = pts.drop(idx)
    
    units = {}
    vmps = {}
    overallmax = {}
    for param in params:
        param_col = main_df[param]
        values_list = param_col.values.tolist()[::-1]
        units[param] = values_list[0]
        if values_list[0][1:] == 'g/L' and values_list[0][0] != 'm' and values_list[0][0] != 'k':
            try:
                units[param] = 'mg/L'
                param_col = param_col.apply(lambda x: x/1000.)      
            except:
                pass
        
        vmps[param] = values_list[1]
        if mode == 'sup':
            if param == 'pH':
                vmps[param] = '6 a 9'
                units[param] = 'pH'
            if param == 'Sulfato':
                vmps[param] = 250.
            if param == 'Fósforo total':
                vmps[param] = 0.1
   
    pts = pts.reset_index(drop=True)
   
    
    eflu_dfs = {}
    with pd.ExcelWriter(f'dataframes\{risco}\{mode.upper()}_{risco.lower()}_BES.xlsx') as writer1:
        for param in params:

            params_df_cols = comun_cols
            params_df_cols.append(param)
            
            param_df = pd.DataFrame(columns=['Data'])
            for idx in pts.index:
                
                pointdf = pd.DataFrame()
                allparams_pt_df = main_df[main_df[pt_colname] == pts.loc[idx]]
                if len(allparams_pt_df) == 0:
                    continue
                param_pt_df = allparams_pt_df[params_df_cols]
                param_pt_df[param] = pd.to_numeric(param_pt_df[param], errors='coerce')
                param_pt_df = param_pt_df.dropna()
                maxvalue = param_pt_df[param].max()
                overallmax[param] = maxvalue
                if len(param_pt_df) >= 2:
                    param_pt_df = removerepeateddates(param_pt_df, 'Data', result_col=param)
                    
                pointdf['Data'] = param_pt_df['Data']
                pointdf[pts.loc[idx]] = param_pt_df[param]
                param_df = param_df.merge(pointdf, how='outer', on='Data')
                
            if len(param_df) > 0:
                ind = params_df_cols.index(param)

                x = []
                for i in range(len(param_df)):
                    x.append(vmps[param])
                y = np.array(x)
                param_df['VMP'] = y
                vmp_col = list(np.ones(len(param_df)))
                for i in range(len(vmp_col)):
                    vmp_col[i] = units[param]
                param_df['Unidade'] = np.array(vmp_col)
                
                params_df_cols.pop(ind)
                param_df = removerepeateddates(param_df, 'Data', param='month')
                param_df['Data'] = pd.to_datetime(param_df['Data'], format="%m-%Y")
                param_df = param_df.sort_values(by='Data', ascending=True)
                param_df = param_df.reset_index(drop=True)
                param_df.to_excel(writer1, sheet_name=param)
                eflu_dfs[param] = param_df
        

    return {'dataframes': eflu_dfs, 'overallmax': overallmax, 'params': params}

if __name__ == "__main__":

    from src.app.utils.graphs import besplotmare, besplotall
    
    # RISCO 12
    # df = pd.read_excel('data/Anexo VI - Resultados analíticos gerais – qualidade das águas superficiais.xlsx', sheet_name='Sheet2')
    # sup_params = ['Fósforo total', 'Sulfato']
    
    # RISCO 13
    df = pd.read_excel('data/Anexo VI - Resultados analíticos gerais – qualidade das águas superficiais.xlsx', sheet_name='Sheet2')
    # df = pd.read_excel('data/Transposta_SE_11082022_copy.xlsx', sheet_name='Sheet1')
    sup_params = ['Sulfato', 'Sódio total', 'pH']
    # sed_params = ['Alumínio', 'Ferro']
    comun_cols = ['Data', 'Parâmetro', 'mare']
    sup_baseline = {'risk13': {'Alumínio dissolvido': 0.21, 'Ferro dissolvido': 0.47, 'Sólidos dissolvidos totais': 123}, 'risk17': {'Sulfato': 3.09, 'Sódio total': 4.9, 'pH': 5.22}}
    # sed_baseline = {'risk13': {'Alumínio': {'max': 20217, 'med': 3389}, 'Ferro': {'max': 67240, 'med': 6894}}}
    # sed_period = '31-08-2020 a 26-04-2022'
    sup_period = '19-08-2020 a 16-12-2021'
    risco = 'RISCO_17'
    mode = 'sup'
    figtitle_mares = f'RCA PCA Alunorte ({sup_period}) - pontos com maré'
    figtitle = f'RCA PCA Alunorte ({sup_period})'
    toplot = read_beseflu(df, comun_cols, 'Parâmetro', sup_params, risco, mode)
    besplotall(toplot['dataframes']['media_mares'], toplot['overallmax'], figtitle, sup_baseline['risk17'], mode, risco, 'best')
    besplotmare(toplot['dataframes']['permares'], toplot['overallmax'], figtitle_mares, sup_baseline['risk17'], mode, risco)
    
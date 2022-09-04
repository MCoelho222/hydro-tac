import pandas as pd
import numpy as np
from src.app.utils.challenge import removerepeateddates
from src.app.utils.graphs import hydroplots


def read_bes(df, comun_cols, pt_colname, params, risco):
    dfcols = comun_cols[:]
    dfcols.extend(params)
    # print(dfcols)
    main_df = df[dfcols]
    # print(main_df.columns.tolist())
    pts = main_df[pt_colname].drop_duplicates()
    pts = pts.reset_index(drop=True)
    # print(pts)
    for idx in pts.index:
        if pts.loc[idx] == 'VMP' or pts.loc[idx] == 'Unidade':
            pts = pts.drop(idx)
    
    mare = main_df['mare'].drop_duplicates()
    mare = mare.reset_index(drop=True)
    for i in range(len(mare)):
        cell_value = mare.loc[i]
        mare.loc[i] = cell_value.split('-')[-1]

    mare = mare.drop_duplicates()
    mare = mare.reset_index(drop=True)
    mare = mare.loc[:9]
    mares = mare.values.tolist()
    units = {}
    vmps = {}
    overallmax = {}
    for param in params:
        df_max = main_df[param].loc[:len(main_df) - 3]
        df_max = pd.to_numeric(df_max, errors='coerce')
        df_max = df_max.dropna()
        maxvalue = df_max.max()
        overallmax[param] = maxvalue
    print(overallmax)
    for param in params:
        param_col = main_df[param]
        values_list = param_col.values.tolist()[::-1]
        units[param] = values_list[0]
        vmps[param] = values_list[1]
        if values_list[0][1:] == 'g/L' and values_list[0][0] != 'm' and values_list[0][0] != 'k':
            print('CHANGE UNITS')
            try:
                units[param] = 'mg/L'
                param_col = param_col.apply(lambda x: x/1000.)      
            except:
                pass
        if param == 'pH':
            vmps[param] = '6 a 9'
            units[param] = 'pH'
        if param == 'Sulfato':
            vmps[param] = 250.
        if param == 'Fósforo total':
            vmps[param] = 0.1
    print(units)
    print(vmps)
   
    pts = pts.reset_index(drop=True)
    alltidesdfs = {}
    for tide in mares:
        param_mare_df = main_df[main_df['mare'] == tide]
        tides_dfs = {}
        for param in params:
            with pd.ExcelWriter(f'dataframes\RISCO_12\{param}_{risco}_BES_{tide}.xlsx') as writer1:
                print('heyehey')
                params_df_cols = comun_cols
                
                params_df_cols.append(param)
                
                param_df = pd.DataFrame(columns=['Data'])
                for idx in pts.index:
                    
                    pointdf = pd.DataFrame()
                    allparams_pt_df = param_mare_df[param_mare_df[pt_colname] == pts.loc[idx]]
                    if len(allparams_pt_df) == 0:
                        continue
                    
                    param_pt_df = allparams_pt_df.loc[:, allparams_pt_df.columns.isin(params_df_cols)]
                    param_pt_df = pd.to_numeric(param_pt_df, errors='coerce')
                    param_pt_df = param_pt_df.dropna()
                    print('HEY', len(param_pt_df))
                    if len(param_pt_df) >= 2:
                        param_pt_df = removerepeateddates(param_pt_df, 'Data', param)
                   
                    pointdf['Data'] = param_pt_df['Data']
                    pointdf[pts.loc[idx]] = param_pt_df[param]
                    param_df = param_df.merge(pointdf, how='outer', on='Data')
                    
                if len(param_df) > 0:
                    param_df = param_df.sort_values(by='Data', ascending=True)
                    param_df = param_df.reset_index(drop=True)
                    ind = params_df_cols.index(param)
                    param_df['VMP'] = vmps[param] * np.ones(len(param_df))
                    vmp_col = list(np.ones(len(param_df)))
                    for i in range(len(vmp_col)):
                        vmp_col[i] = units[param]
                    param_df['Unidade'] = np.array(vmp_col)

                    print(param_df['Unidade'])
                    params_df_cols.pop(ind)

                    param_df.to_excel(writer1, sheet_name=param)
                    tides_dfs[param] = param_df
        alltidesdfs[tide] = tides_dfs

    
    
    mediamares_dfs = {}
    with pd.ExcelWriter(f'dataframes\RISCO_12\{risco}_BES_media_mares.xlsx') as writer2:
        for param in params:
            params_df_cols = comun_cols
            
            params_df_cols.append(param)
            
            param_df = pd.DataFrame(columns=['Data'])
            for idx in pts.index:
                
                pointdf = pd.DataFrame()
                allparams_pt_df = main_df[main_df[pt_colname] == pts.loc[idx]]
                if len(allparams_pt_df) == 0:
                    continue
                
                param_pt_df = allparams_pt_df.loc[:, allparams_pt_df.columns.isin(params_df_cols)]
                param_pt_df = param_pt_df.dropna()
                
                param_pt_df = removerepeateddates(param_pt_df, 'Data', param)
                
                pointdf['Data'] = param_pt_df['Data']
                pointdf[pts.loc[idx]] = param_pt_df[param]
                param_df = param_df.merge(pointdf, how='outer', on='Data')
                param_df = param_df.sort_values(by='Data', ascending=True)
                param_df = param_df.reset_index(drop=True)
            ind = params_df_cols.index(param)
            param_df['VMP'] = vmps[param] * np.ones(len(param_df))
            vmp_col = list(np.ones(len(param_df)))
            for i in range(len(vmp_col)):
                vmp_col[i] = units[param]
            param_df['Unidade'] = np.array(vmp_col)

            print(param_df['Unidade'])
            params_df_cols.pop(ind)

            param_df.to_excel(writer2, sheet_name=param)
            mediamares_dfs[param] = param_df
        
                # asd
        # print(param_df)
            


    # print(pts)


 
    return {'dataframes': {'media_mares': mediamares_dfs, 'permares': alltidesdfs}, 'overallmax': overallmax}

if __name__ == "__main__":

    df = pd.read_excel('Anexo VI - Resultados analíticos gerais – qualidade das águas superficiais.xlsx', sheet_name='Sheet2')
    comun_cols = ['Data', 'Parâmetro', 'mare']
    params = ['Fósforo total', 'Sulfato']

    toplot = read_bes(df, comun_cols, 'Parâmetro', params, 'RISCO_12')
    hydroplots(toplot['dataframes']['mediamares'], toplot['overallmax'], 'BES_media_mares', 'RCA PCA Alunorte média entre marés', 'RISCO_12', 'upper right')
    
import pandas as pd
import numpy as np
from src.app.utils.challenge import removerepeateddates
# from src.app.utils.graphs import hydroplots
from src.app.utils import ordered_bes_sites
from src.app.beseflu import read_beseflu



def read_bes(df, comun_cols, pt_colname, params, risco, mode):
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
        
        try:
            mare_ = cell_value.split('-')[-1]
            if len(mare_) > 0:
                mare.loc[i] = mare_
            else:
                pass
        except:
            pass
    mare = mare.drop_duplicates()
    # print(mare)
    # asd
    mare = mare.reset_index(drop=True)
    mare = mare.drop(len(mare) - 1)
    mares = mare.values.tolist()
    todasmares = mare.values.tolist()
    ind = mares.index('sem_mare')
    mares.pop(ind)
    # print(mare)
    # asd
    
    units = {}
    vmps = {}
    for param in params:
        param_col = main_df[param]
        values_list = param_col.values.tolist()[::-1]
        units[param] = values_list[0]
        if values_list[0][1:] == 'g/L' and values_list[0][0] != 'm' and values_list[0][0] != 'k':
            print('CHANGE UNITS')
            try:
                units[param] = 'mg/L'
                param_col = param_col.apply(lambda x: x/1000.)
                main_df[param] = param_col   
            except:
                pass
        
        vmps[param] = values_list[1]
        if mode == 'sup':
            if param == 'pH':
                vmps[param] = '6 a 9'
                units[param] = 'pH'
            if param == 'Sulfato':
                vmps[param] = 250.
            if param == 'F??sforo total':
                vmps[param] = 0.1
    # print(units)
    overallmax = {}
    for param in params:
        df_max = main_df[param].loc[:len(main_df) - 3]
        df_max = pd.to_numeric(df_max, errors='coerce')
        df_max = df_max.dropna()
        maxvalue = df_max.max()
        overallmax[param] = maxvalue
    # print(overallmax)
    # print(overallmax)
    # asd
    # print(vmps)
    pts = pts.reset_index(drop=True)
    # print(pts)
    alltidesdfs = {}
    for tide in mares:
        
        # unique_mares = main_df['mare'].drop_duplicates()
        # mare = mare.reset_index(drop=True)
        mare_col = main_df['mare']
        for i in range(len(mare_col)):
            cell_value = mare_col.loc[i]
            try:
                mare_ = cell_value.split('-')[-1]
                if len(mare_) > 0:
                    main_df.loc[i, 'mare'] = mare_
                else:
                    pass
            except:
                pass

        param_mare_df = main_df[main_df['mare'] == tide]
       
        tides_dfs = {}
        for param in params:
            with pd.ExcelWriter(f'dataframes\{risco}\Arcadis\{mode.upper()}_{param}_{risco}_BES_{tide}.xlsx') as writer1:

                params_df_cols = comun_cols
                params_df_cols.append(param)
                
                param_df = pd.DataFrame(columns=['Data'])
                for idx in pts.index:
                    
                    pointdf = pd.DataFrame()
                    allparams_pt_df = param_mare_df[param_mare_df[pt_colname] == pts.loc[idx]]
                    if len(allparams_pt_df) == 0:
                        continue
                    # print(params_df_cols)
                    param_pt_df = allparams_pt_df[params_df_cols]
                    param_pt_df[param] = pd.to_numeric(param_pt_df[param], errors='coerce')
                    param_pt_df = param_pt_df.dropna()
                    # print('HEY', len(param_pt_df))
                    if len(param_pt_df) >= 2:
                        param_pt_df = removerepeateddates(param_pt_df, 'Data', result_col=param)
                      
                    pointdf['Data'] = param_pt_df['Data']
                    pointdf[pts.loc[idx]] = param_pt_df[param]
                    param_df = param_df.merge(pointdf, how='outer', on='Data')
                    
                if len(param_df) > 0:
                    # print(tide)
                    # print(param)
                    # print(param_df[['Data', 'SUP47']].values.tolist())
                    # asd
                    ind = params_df_cols.index(param)

                    if mode == 'sed':
                        x = []
                        for i in range(len(param_df)):
                            x.append(vmps[param])
                        y = np.array(x)
                        param_df['VMP'] = y
                    else:
                        try:
                            param_df['VMP'] = vmps[param] * np.ones(len(param_df))
                        except:
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
                    order = [31, 33, 9, 7, 3, 6, 2, 37, 5, 1, 4, 8, 36, 32, 52, 47, 48, 40, 41, 14, 42, 43, 15, 25, 26]
                    tidal_cols = param_df.columns.tolist()[1:-2]
                    
                    ordered_tidal_cols = ordered_bes_sites(order, tidal_cols)   
                    cols_order1 = ['Data']
                    sups1 = []
                    if mode == 'sup':
                        for i in range(len(ordered_tidal_cols)):
                            num1 = str(ordered_tidal_cols[i])
                            if len(num1) == 1:
                                sups1.append('SUP0' + num1)
                            else:
                                sups1.append('SUP' + num1)
                    if mode == 'sed':
                        for i in range(len(ordered_tidal_cols)):
                            num1 = str(ordered_tidal_cols[i])
                            if len(num1) == 1:
                                sups1.append('SED0' + num1)
                            else:
                                sups1.append('SED' + num1)
                    sups1.append('VMP')
                    sups1.append('Unidade')
                    cols_order1.extend(sups1)
                    param_df = param_df[cols_order1]
                    param_df = removerepeateddates(param_df, 'Data', param='month')
                    param_df['Data'] = pd.to_datetime(param_df['Data'], format="%m-%Y")
                    param_df = param_df.sort_values(by='Data', ascending=True)
                    param_df = param_df.reset_index(drop=True)
                    param_df.to_excel(writer1, sheet_name=param)
                    tides_dfs[param] = param_df
        alltidesdfs[tide] = tides_dfs
    

    mediamares_dfs = {}
    with pd.ExcelWriter(f'dataframes\{risco}\Arcadis\{mode.upper()}_{risco}_BES_max_mares.xlsx') as writer2:
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
                param_pt_df[param] = pd.to_numeric(param_pt_df[param], errors='coerce')
                param_pt_df = param_pt_df.dropna()
                
                param_pt_df = removerepeateddates(param_pt_df, 'Data', param)
                
                pointdf['Data'] = param_pt_df['Data']
                pointdf[pts.loc[idx]] = param_pt_df[param]
                param_df = param_df.merge(pointdf, how='outer', on='Data')
                param_df = param_df.sort_values(by='Data', ascending=True)
                param_df = param_df.reset_index(drop=True)
            ind = params_df_cols.index(param)
            if mode == 'sed':
                x = []
                for i in range(len(param_df)):
                    x.append(vmps[param])
                y = np.array(x)
                param_df['VMP'] = y
            else:
                try:
                    param_df['VMP'] = vmps[param] * np.ones(len(param_df))
                except:
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
      
            order = [35, 30, 23, 18, 44, 54, 27, 28, 21, 20, 55, 46, 45, 19, 56, 16, 17, 22, 49, 50, 51, 52, 10, 11, 12, 40, 41, 14, 42, 43, 15, 47, 24, 53, 25, 26, 38, 9, 31, 34, 29, 33, 7, 3, 6, 2, 37, 5, 1, 4, 8, 36, 32, 48]
            tidal_cols1 = param_df.columns.tolist()[1:-2]       
            ordered_tidal_cols1 = ordered_bes_sites(order, tidal_cols1)
            cols_order = ['Data']
            sups = []
            if mode == 'sup':
                for i in range(len(ordered_tidal_cols1)):
                    num = str(ordered_tidal_cols1[i])
                    if len(num) == 1:
                        sups.append('SUP0' + num)
                    else:
                        sups.append('SUP' + num)
            if mode == 'sed':
                for i in range(len(ordered_tidal_cols1)):
                    num = str(ordered_tidal_cols1[i])
                    if len(num) == 1:
                        sups.append('SED0' + num)
                    else:
                        sups.append('SED' + num)
            sups.append('VMP')
            sups.append('Unidade')
            cols_order.extend(sups)
    
            param_df = param_df[cols_order]
            param_df.to_excel(writer2, sheet_name=param)
            mediamares_dfs[param] = param_df
 
    return {'dataframes': {'media_mares': mediamares_dfs, 'permares': alltidesdfs}, 'overallmax': overallmax, 'mares': mares, 'params': params}

if __name__ == "__main__":

    from src.app.utils.graphs import besplotmare, besplotall
    
    # RISCO 12
    # df = pd.read_excel('Anexo VI - Resultados anal??ticos gerais ??? qualidade das ??guas superficiais.xlsx', sheet_name='Sheet2')
    
    # sup_params = ['F??sforo total', 'Sulfato']
    # besdf = pd.read_excel('Anexo II - Resultados anal??ticos gerais - efluentes.xlsx', sheet_name='Sheet1')
    # RISCO 13
    # df = pd.read_excel('Anexo VI - Resultados anal??ticos gerais ??? qualidade das ??guas superficiais.xlsx', sheet_name='Sheet2')
    df = pd.read_excel('Transposta_SE_11082022_copy.xlsx', sheet_name='Sheet1')
    # sup_params = ['Sulfato', 'S??dio total', 'pH']
    
    #RISCO 07
    sup_params = ['S??lidos dissolvidos totais', 'Coliformes Termotolerantes', 'pH', 'DBO', 'OD', '??leos e Graxas', 'F??sforo total', 'B??rio total', 'Cromo total', 'Van??dio total', 'Zinco total', 'Ars??nio total', 'Mangan??s total', 'Chumbo total', 'Ferro dissolvido', 'Alum??nio dissolvido', 'Merc??rio total', 'S??dio total', 'Sulfato total', 'Sil??cio total']

    eflu_params = ['S??lidos sediment??veis', 'Temperatura', 'S??lidos dissolvidos totais', 'pH', '??leos e graxas minerais', '??leos e graxas vegetais e animais', 'Oxig??nio dissolvido', 'DBO']
    # sed_params = ['Alum??nio', 'Ferro']
    #RISCO 07
    sed_params = ['Ars??nio', 'Alum??nio', 'Ferro', 'Cromo', 'Chumbo', 'F??sforo', 'B??rio', 'Van??dio', 'Cobalto', 'Merc??rio', 'Mangan??s', 'S??dio', 'Sulfato', 'Zinco', 'S??lica']

    comun_cols = ['Data', 'Par??metro', 'mare']
    eflu_comun_cols = ['Data', 'Par??metro']
    
    sup_baseline = {'risk13': {'Alum??nio dissolvido': 0.21, 'Ferro dissolvido': 0.47, 'S??lidos dissolvidos totais': 123}, 'risk17': {'Sulfato': 3.09, 'S??dio total': 4.9, 'pH': 5.22}, 'risk07': {'S??lidos dissolvidos totais': 123, 'Alum??nio dissolvido': 0.21, 'Ferro dissolvido': 0.47, 'Sulfato total': 3.09, 'S??dio total': 4.9, 'pH': 5.22, 'Coliformes Termotolerantes': 160, 'DBO': 3.44, 'OD': 4.31, '??leos e Graxas': 0.0, 'F??sforo total': 0.06, 'B??rio total': 0.04, 'Van??dio total': 0.01, 'Zinco total': 0.08, 'Ars??nio total': 0.066, 'Mangan??s total': 0.09, 'Chumbo total': 0.02, 'Merc??rio total': 0.0002, 'Cromo total': 0.01, 'Sil??cio total': 4.38}}
    
    sed_baseline = {'risk13': {'Alum??nio': {'max': 20217, 'med': 3389}, 'Ferro': {'max': 67240, 'med': 7488}}, 'risk07': {'Ars??nio': {'max': 13.6, 'med': 1.39}, 'Alum??nio': {'max': 20217, 'med': 3389}, 'Ferro': {'max': 67240, 'med': 7488}, 'Chumbo': {'max': 7.85, 'med': 3.06}, 'F??sforo': {'max': 313, 'med': 55}, 'B??rio': {'max': 69.8, 'med': 5.75}, 'Van??dio': {'max': 256, 'med': 18.2}, 'Merc??rio': {'max': 0.08, 'med': 0.0242}, 'Mangan??s': {'max': 1796, 'med': 58.5}, 'S??dio': {'max': 126, 'med': 73.7}, 'Sulfato': {'max': 6.650, 'med': 2.37}, 'Zinco': {'max': 27.1, 'med': 9.15}, 'Cromo': {'max':138, 'med': 9.98}, 'Cobalto': {'max':3.84, 'med': 1.63}, 'S??lica': {'max':8.7, 'med': 4.37}}}
    
    
    sed_period = '31-08-2020 a 26-04-2022'
    sup_period = '19-08-2020 a 16-12-2021'
    eflu_period = '26-08-2020 a 08-09-2021'
    
    
    risco = 'RISCO_07'
    mode = 'sed'
    figtitle_mares = f'RCA PCA Alunorte ({sed_period}) - pontos com mar??'
    figtitle = f'RCA PCA Alunorte ({sed_period})'
    toplot = read_bes(df, comun_cols, 'Par??metro', sed_params, risco, mode)
    # toplot = read_beseflu(besdf, eflu_comun_cols, 'Par??metro', eflu_params, risco, mode)
    # besplotall(toplot['dataframes'], toplot['overallmax'], figtitle, mode, risco, leg_position='best')
    besplotall(toplot['dataframes']['media_mares'], toplot['overallmax'], figtitle, mode, risco, sed_baseline['risk07'], 'best')
    besplotmare(toplot['dataframes']['permares'], toplot['overallmax'], figtitle_mares, sed_baseline['risk07'], mode, risco)
    
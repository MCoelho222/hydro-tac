import pandas as pd
import numpy as np
from src.app.utils.challenge import removerepeateddates
# from src.app.utils.graphs import hydroplots
# from src.app.utils import ordered_bes_sites



def read_beseflu(df, comun_cols, pt_colname, params, risco, mode):
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
    
    units = {}
    vmps = {}
    overallmax = {}
    # for param in params:
    #     df_max = main_df[param].loc[:len(main_df) - 3]
    #     df_max = pd.to_numeric(df_max, errors='coerce')
    #     df_max = df_max.dropna()
    #     maxvalue = df_max.max()
    #     overallmax[param] = maxvalue
        
    # print(overallmax)
    for param in params:
        param_col = main_df[param]
        values_list = param_col.values.tolist()[::-1]
        units[param] = values_list[0]
        if values_list[0][1:] == 'g/L' and values_list[0][0] != 'm' and values_list[0][0] != 'k':
            # print('CHANGE UNITS')
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
                # print(params_df_cols)
                param_pt_df = allparams_pt_df[params_df_cols]
                param_pt_df[param] = pd.to_numeric(param_pt_df[param], errors='coerce')
                param_pt_df = param_pt_df.dropna()
                maxvalue = param_pt_df[param].max()
                overallmax[param] = maxvalue
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
                # order = [31, 33, 9, 7, 3, 6, 2, 37, 5, 1, 4, 8, 36, 32, 52, 47, 48, 40, 41, 14, 42, 43, 15, 25, 26]
                # tidal_cols = param_df.columns.tolist()[1:-2]
                
                # ordered_tidal_cols = ordered_bes_sites(order, tidal_cols)   
                # cols_order1 = ['Data']
                # sups1 = []
                # if mode == 'sup':
                #     for i in range(len(tidal_cols)):
                #         num1 = str(tidal_cols[i])
                #         if len(num1) == 1:
                #             sups1.append('SUP0' + num1)
                #         else:
                #             sups1.append('SUP' + num1)
                # if mode == 'sed':
                #     for i in range(len(ordered_tidal_cols)):
                #         num1 = str(ordered_tidal_cols[i])
                #         if len(num1) == 1:
                #             sups1.append('SED0' + num1)
                #         else:
                #             sups1.append('SED' + num1)
                # sups1.append('VMP')
                # sups1.append('Unidade')
                # cols_order1.extend(sups1)
                # param_df = param_df[cols_order1]
                param_df = removerepeateddates(param_df, 'Data', param='month')
                param_df['Data'] = pd.to_datetime(param_df['Data'], format="%m-%Y")
                param_df = param_df.sort_values(by='Data', ascending=True)
                param_df = param_df.reset_index(drop=True)
                param_df.to_excel(writer1, sheet_name=param)
                eflu_dfs[param] = param_df
        

    # mediamares_dfs = {}
    # with pd.ExcelWriter(f'dataframes\{risco}\Arcadis\{mode.upper()}_{risco}_BES_max_mares.xlsx') as writer2:
    #     for param in params:
    #         params_df_cols = comun_cols
            
    #         params_df_cols.append(param)
            
    #         param_df = pd.DataFrame(columns=['Data'])
    #         for idx in pts.index:
                
    #             pointdf = pd.DataFrame()
    #             allparams_pt_df = main_df[main_df[pt_colname] == pts.loc[idx]]
    #             if len(allparams_pt_df) == 0:
    #                 continue
                
    #             param_pt_df = allparams_pt_df.loc[:, allparams_pt_df.columns.isin(params_df_cols)]
    #             param_pt_df[param] = pd.to_numeric(param_pt_df[param], errors='coerce')
    #             param_pt_df = param_pt_df.dropna()
                
    #             param_pt_df = removerepeateddates(param_pt_df, 'Data', param)
                
    #             pointdf['Data'] = param_pt_df['Data']
    #             pointdf[pts.loc[idx]] = param_pt_df[param]
    #             param_df = param_df.merge(pointdf, how='outer', on='Data')
    #             param_df = param_df.sort_values(by='Data', ascending=True)
    #             param_df = param_df.reset_index(drop=True)
    #         ind = params_df_cols.index(param)
    #         if mode == 'sed':
    #             x = []
    #             for i in range(len(param_df)):
    #                 x.append(vmps[param])
    #             y = np.array(x)
    #             param_df['VMP'] = y
    #         else:
    #             try:
    #                 param_df['VMP'] = vmps[param] * np.ones(len(param_df))
    #             except:
    #                 x = []
    #                 for i in range(len(param_df)):
    #                     x.append(vmps[param])
    #                 y = np.array(x)
    #                 param_df['VMP'] = y
    #         vmp_col = list(np.ones(len(param_df)))
    #         for i in range(len(vmp_col)):
    #             vmp_col[i] = units[param]
    #         param_df['Unidade'] = np.array(vmp_col)

    #         params_df_cols.pop(ind)
    #         param_df = removerepeateddates(param_df, 'Data', param='month')
    #         param_df['Data'] = pd.to_datetime(param_df['Data'], format="%m-%Y")
    #         param_df = param_df.sort_values(by='Data', ascending=True)
    #         param_df = param_df.reset_index(drop=True)
      
    #         order = [35, 30, 23, 18, 44, 54, 27, 28, 21, 20, 55, 46, 45, 19, 56, 16, 17, 22, 49, 50, 51, 52, 10, 11, 12, 40, 41, 14, 42, 43, 15, 47, 24, 53, 25, 26, 38, 9, 31, 34, 29, 33, 7, 3, 6, 2, 37, 5, 1, 4, 8, 36, 32, 48]
    #         tidal_cols1 = param_df.columns.tolist()[1:-2]       
    #         ordered_tidal_cols1 = ordered_bes_sites(order, tidal_cols1)
    #         cols_order = ['Data']
    #         sups = []
    #         if mode == 'sup':
    #             for i in range(len(ordered_tidal_cols1)):
    #                 num = str(ordered_tidal_cols1[i])
    #                 if len(num) == 1:
    #                     sups.append('SUP0' + num)
    #                 else:
    #                     sups.append('SUP' + num)
    #         if mode == 'sed':
    #             for i in range(len(ordered_tidal_cols1)):
    #                 num = str(ordered_tidal_cols1[i])
    #                 if len(num) == 1:
    #                     sups.append('SED0' + num)
    #                 else:
    #                     sups.append('SED' + num)
    #         sups.append('VMP')
    #         sups.append('Unidade')
    #         cols_order.extend(sups)
    
    #         param_df = param_df[cols_order]
    #         param_df.to_excel(writer2, sheet_name=param)
    #         mediamares_dfs[param] = param_df
    # print(overallmax)
    return {'dataframes': eflu_dfs, 'overallmax': overallmax, 'params': params}

if __name__ == "__main__":

    from src.app.utils.graphs import besplotmare, besplotall
    
    # RISCO 12
    # df = pd.read_excel('Anexo VI - Resultados analíticos gerais – qualidade das águas superficiais.xlsx', sheet_name='Sheet2')
    # sup_params = ['Fósforo total', 'Sulfato']
    
    # RISCO 13
    df = pd.read_excel('Anexo VI - Resultados analíticos gerais – qualidade das águas superficiais.xlsx', sheet_name='Sheet2')
    # df = pd.read_excel('Transposta_SE_11082022_copy.xlsx', sheet_name='Sheet1')
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
    toplot = read_bes(df, comun_cols, 'Parâmetro', sup_params, risco, mode)
    besplotall(toplot['dataframes']['media_mares'], toplot['overallmax'], figtitle, sup_baseline['risk17'], mode, risco, 'best')
    besplotmare(toplot['dataframes']['permares'], toplot['overallmax'], figtitle_mares, sup_baseline['risk17'], mode, risco)
    
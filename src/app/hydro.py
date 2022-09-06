import pandas as pd
import numpy as np
from src.app.utils import replace_as_lastcols
from src.app.utils.challenge import removerepeateddates

def hydroalunorte(risco, df, cols, str_filters, mode, val_filters=None, ts=None):
    """-----------------------------------------------------------------------------------------------------
    PARAMS
    --------------------------------------------------------------------------------------------------------
    df            => pandas dataframe to be filtered
    cols          => list, ['col_name1', 'col_name2',...]
    str_filters   => dict, {'col_name1': 'filter_value1',...}
                    The values of the dict are strings that will be used as filters.
    val_filters   => dict, {'col_name1': 'filter_type1',...}
                    The values of the dict are the type of filter to be used.
    ts            => dict, {'owner': (owner_colname, (owner_name)), 'site': (site_colname, (sites,)), 'params': ('params',), 'date': ('date_colname', (date_start, date_end))}
    -------------------------------------------------------------------------------------------------------
    RETURN => dict: {'df': filtered dataframe, 'empty_df_causes': ['filter_value1', ..., filter_type1', ...]}
    ------------------------------------------------------------------------------------------------------"""
    
    df_cols = df.loc[:, cols]
   
    param_col = str_filters['param'][0] 
    params = str_filters['param'][1] 
    vmp_col = 'VMP'
    unit_col = ts['unit'][0]
    result_col = ts['result'][0]
    river_col = str_filters['river'][0]
    rivers = str_filters['river'][1]
    site_col = ts['site'][0]
   
    if 'date' in ts:
        date_col = ts['date'][0]
        # period = ts['date'][1] # tuple

    if val_filters:
        
        for key in val_filters.keys():

            num_type = val_filters[key]
            if 'nan' in num_type:
                df_cols.loc[:, key] = pd.to_numeric(df_cols[key], errors='coerce')
                df_cols.dropna()
                if len(df_cols) == 0:
                    return {'df': df_cols, 'empty_df_causes': 'nan'}
            if 'positive' in num_type:
                df_cols = df_cols[df_cols[key] >= 0.]
                if len(df_cols) == 0:
                    return {'df': df_cols, 'empty_df_causes': 'positive'}
    
    df_cols = df_cols.reset_index(drop=True)
    for i in range(len(df_cols)):
        cell_value = df_cols.loc[i, result_col]
        cell_unit = df_cols.loc[i, unit_col]
        cell_vmp = df_cols.loc[i, vmp_col]
        cell_param = df_cols.loc[i, param_col]
        cell_river = df_cols.loc[i, river_col]
        # mu = '\u03BC'
        try:
            if cell_unit[1:] == 'g/L' and cell_unit[0] != 'm' and cell_unit[0] != 'k':
              
                df_cols.loc[i, result_col] = cell_value/1000.
                df_cols.loc[i, unit_col] = 'mg/L'
                df_cols.loc[i, vmp_col] = cell_vmp/1000
        except:
            pass

        if cell_param == 'pH' and cell_river in rivers:

            df_cols.loc[i, vmp_col] = '6 a 9'
            df_cols.loc[i, unit_col] = 'pH'
        if cell_param == 'Sulfato' and cell_river in rivers:
            df_cols.loc[i, vmp_col] = 250.
        if cell_param == 'Fósforo Total' and cell_river in rivers:
            df_cols.loc[i, vmp_col] = 0.1
    
    overallmax = {}
    
    for key in str_filters.keys():
        df_new = pd.DataFrame(columns=cols)
        colname = str_filters[key][0]
        colvalues = str_filters[key][1]

        if colname not in cols:
            return {'error': f'col {key[0]} does not exist'}
        if len(colvalues) > 0:
           
            for val in colvalues:
                filtered = df_cols[df_cols[colname] == val]
             
                if len(filtered) > 0:
                    df_new = pd.concat([df_new, filtered], axis=0, ignore_index=True)
              
            df_cols = df_new.copy(deep=True)
            if len(df_cols) == 0:
                return {'dataframes': df_cols, 'empty_df_cause': val}
    
    for param in params:
        df_max = df_cols[df_cols[param_col] == param]
        maxvalue = df_max[result_col].max()
        overallmax[param] = maxvalue
            
    if not ts:
        return {'dataframes': df_cols}
    perriverdfs = {}
    allriversmaxvals = {}
    param_ts = {}
    for param in params:
        param_tsdf = pd.DataFrame(columns=['Data', unit_col, vmp_col])
        param_filtered = df_cols[df_cols[param_col] == param]
        param_filtered = param_filtered.reset_index(drop=True)

        if len(param_filtered) == 0:
            continue

        rivermaxvals = {}
        river_ts = {}
        for river in rivers:

            river_df = param_filtered[param_filtered[river_col] == river]
        
            if len(river_df) > 0:

                unique_sites = []
                sites = river_df[site_col]
                
                for ind in sites.index:
                    
                    site_name = sites[ind]
                    if site_name not in unique_sites:
                        unique_sites.append(site_name)
            else:
                continue
                        
            maxvalue = river_df[result_col].max()
            # print('PASSEI')
            rivermaxvals[river] = maxvalue
            river_sites_df = pd.DataFrame(columns=['Data', unit_col, vmp_col])
            
            for site in unique_sites:
                
                site_filtered = river_df[river_df[site_col] == site]
                site_filtered = site_filtered.reset_index(drop=True)
                if len(site_filtered) == 0:
                    continue
                
                param_sitedf = pd.DataFrame()

                if len(site_filtered) >= 2:
                   
                    site_filtered = removerepeateddates(site_filtered, date_col, result_col)
        
                param_sitedf['Data'] = site_filtered[date_col]
                param_sitedf[site] = site_filtered[result_col]
                param_sitedf[unit_col] = site_filtered[unit_col]
                param_sitedf[vmp_col] = site_filtered[vmp_col]
                river_sites_df = river_sites_df.merge(param_sitedf, how='outer', on=['Data', unit_col, vmp_col])
                river_sites_df = river_sites_df.sort_values(by='Data', ascending=True)
                river_sites_df = river_sites_df.reset_index(drop=True)
                river_sites_df = replace_as_lastcols(river_sites_df, (vmp_col, unit_col))
   
            river_ts[river] = river_sites_df
            param_tsdf = param_tsdf.merge(river_sites_df, how='outer', on=['Data', unit_col, vmp_col])
            param_tsdf = param_tsdf.sort_values(by='Data', ascending=True)
            param_tsdf = param_tsdf.reset_index(drop=True)
            param_tsdf = replace_as_lastcols(param_tsdf, (vmp_col, unit_col))
        
        allriversmaxvals[param] = rivermaxvals
        perriverdfs[param] = river_ts      
        param_ts[param] = param_tsdf
        
    with pd.ExcelWriter(f'dataframes\{risco}\Hydro\{mode.upper()}_{risco}_monit_cont.xlsx') as writer1:
        for param in param_ts.keys():

            param_ts[param].to_excel(writer1, sheet_name=param)

    parammaxvals = {}
   
    for param in allriversmaxvals.keys():
      
        maxparam = []
        for riv in allriversmaxvals[param].keys():
            finalmax = allriversmaxvals[param][riv]
            maxparam.append(finalmax)
        maxparam2 = np.array(maxparam)
        
        parammaxvals[param] = np.max(maxparam2)
    # print(parammaxvals)    


    return {'dataframes': {'perparam':param_ts, 'perriver': perriverdfs}, 'maximos': allriversmaxvals, 'overallmax': parammaxvals} 
   
if __name__ == "__main__":

    from src.app.utils.graphs import hydroplots

    df = pd.read_excel('BD_hydro_rev120_22-07-2022.xlsm', sheet_name='Versão 120_GS')

    risk_params = {'risk12': ('Fósforo Total', 'Sulfato', 'Enxofre'), 'risk17': ('Sulfato', 'Sódio', 'Sódio Total', 'pH')}
   
    risk_title = 'RISCO_12'
    mode = 'sup'
    risk = risk_params['risk12']
    cols_hydro = ['Código do ponto', 'Local', 'Data Coleta', 'Parâmetro', 'Valor', 'Unidade', 'VMP']
    rivers = ('Rio Murucupi', 'Rio Pará', 'Igarapé Tauá', 'Igarapé Pramajozinho', 'Igarapé Água Verde')
    ts_dict = {'site': ('Código do ponto', ()), 'date': ('Data Coleta', ()), 'result': ('Valor', ()), 'unit': ('Unidade', ())}
    str_filter_dict = {'param': ('Parâmetro', risk), 'river': ('Local', rivers)}
    val_filter_dict = {'Valor': ('positive', 'nan')}

    dfs = hydroalunorte(risk_title, df, cols_hydro, str_filter_dict, mode, val_filters=val_filter_dict, ts=ts_dict)

    hydroplots(dfs['dataframes']['perparam'], dfs['overallmax'], 'monit_cont', 'monitoramento contínuo', risk_title, 'best')
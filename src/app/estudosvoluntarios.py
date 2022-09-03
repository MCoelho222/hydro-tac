import pandas as pd
import numpy as np
from src.app.utils import sort_str_endswithnum
from src.app.utils import replace_as_lastcols
from src.app.challenge import removerepeateddates

def estudosvolun(risco, rivername, df, cols, str_filters, allrivers, val_filters=None, ts=None):
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
    tide_col = ts['tide'][0] 
    tide_cond = ts['tide'][1]
    sample_col = ts['sample'][0]
    vmp_col = 'VMP'
    unit_col = ts['unit'][0]
    result_col = ts['result'][0]
    site_col = str_filters['site'][0]
    owner_col = str_filters['owner'][0]
    pt_col = ts['site'][0]
    owners = str_filters['owner'][1]
   
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
        cell_site = df_cols.loc[i, site_col]
        # mu = '\u03BC'

        if cell_unit[1:] == 'g/L' and cell_unit[0] != 'm' and cell_unit[0] != 'k':
            df_cols.loc[i, result_col] = cell_value/1000.
            df_cols.loc[i, unit_col] = 'mg/L'
            try:
                df_cols.loc[i, vmp_col] = cell_vmp/1000
            except:
                pass

        if cell_param == 'pH' and cell_site in allrivers:
            df_cols.loc[i, vmp_col] = '6 a 9'
            df_cols.loc[i, unit_col] = 'pH'
        if cell_param == 'Sulfato' and cell_site in allrivers:
            df_cols.loc[i, vmp_col] = 250.
        if cell_param == 'Fósforo Total' and cell_site in allrivers:
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
                filtered = filtered.reset_index(drop=True)
               
                if key == 'param':
                    max_df = pd.DataFrame(columns=cols)
                    for river in allrivers:
                       
                        river_filtered = filtered[filtered[site_col] == river]
                        if len(river_filtered) > 0:
                            max_df = pd.concat([max_df, river_filtered], axis=0, ignore_index=True)
                    max_val = max_df[result_col].max()

                    overallmax[val] = max_val
                
                if len(filtered) > 0:
                    df_new = pd.concat([df_new, filtered], axis=0, ignore_index=True)
                   
            df_cols = df_new.copy(deep=True)
            if len(df_cols) == 0:
                return {'dataframes': df_cols, 'empty_df_cause': val}
    
    if not ts:
        return {'dataframes': df_cols}
        
    owners_dfs = {}
    owners_sites = {}
    for owner in owners:
        
        owner_df = df_cols[df_cols[owner_col] == owner]
       
        if len(owner_df) > 0:
            owners_dfs[owner] = owner_df
            unique_sites = []
            sites = owner_df[pt_col]
            
            for ind in sites.index:
              
                site_name = sites[ind]
                if site_name not in unique_sites:
                    unique_sites.append(site_name)
                owners_sites[owner] = unique_sites
           
            if owner == 'Geoklock' or owner == 'Enviro-Tec' or owner == 'SGW':
                ordered_sites = sort_str_endswithnum(unique_sites, '-')
                owners_sites[owner] = ordered_sites
             
    
    timeseries = {}
    ownermaxvals = {}
    for site_own in owners_sites.keys():
        own_df = owners_dfs[site_own]

        for param in params:
            maxdf = own_df[own_df[param_col] == param]
            maxvalue = maxdf[result_col].max()
            ownermaxvals[param] = maxvalue

        tidaldf = {}
        for tide in tide_cond[site_own]:
          
            tide_df = own_df[own_df[tide_col] == tide]
         
            if len(tide_df) == 0:
                continue    
            params_df = {}
            tsparams = tide_df[param_col].values.tolist()
            for param in tsparams:
              
                owner_tsdf = pd.DataFrame(columns=['Data', unit_col, vmp_col])
                owner_tsdf['Data'] = pd.to_datetime(owner_tsdf['Data'])
                owner_tsdf.set_index('Data')
             
                for site in owners_sites[site_own]:
              
                    if site in tide_df[pt_col].values.tolist():
                        site_filtered = tide_df[tide_df[pt_col] == site]
        
                        if site_own == 'Enviro-Tec':
                            site_filtered = site_filtered[site_filtered[sample_col] == 1]
            
                        owner_sitedf = pd.DataFrame()
                     
                        param_filtered = site_filtered[site_filtered[param_col] == param]
                        param_filtered = param_filtered.reset_index(drop=True)

                        if len(param_filtered) >= 2:
                            param_filtered = removerepeateddates(param_filtered, date_col, result_col)
                           
                        if len(param_filtered) > 0:
                            
                            owner_sitedf['Data'] = pd.to_datetime(param_filtered[date_col])
                            owner_sitedf[site] = param_filtered[result_col]
                            owner_sitedf[unit_col] = param_filtered[unit_col]
                            owner_sitedf[vmp_col] = param_filtered[vmp_col]
                            owner_sitedf.set_index('Data')
                            owner_tsdf = owner_tsdf.merge(owner_sitedf, how='outer', on=['Data', unit_col, vmp_col])
                        
                owner_tsdf = replace_as_lastcols(owner_tsdf, ('VMP', 'Unidade'))
                owner_tsdf = owner_tsdf.sort_values(by='Data', ascending=True)
                owner_tsdf = owner_tsdf.reset_index(drop=True)

                params_df[param] = owner_tsdf
                tidaldf[tide] = params_df

            timeseries[site_own] = tidaldf
        
        if len(timeseries) > 0:
            for owner in timeseries.keys():
                for tidal in timeseries[owner].keys():
                    with pd.ExcelWriter(f'dataframes\{risco}\{owner}_{rivername.upper()}_{tidal}_{risco}.xlsx') as writer:
                        for tsdf in timeseries[owner][tidal].keys():
                            timeseries[owner][tidal][tsdf].to_excel(writer, sheet_name=tsdf)
    # print(timeseries)
    return {'dataframes': timeseries, 'ownermax': ownermaxvals, 'overallmax': overallmax} 

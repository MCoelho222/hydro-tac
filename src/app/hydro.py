import pandas as pd
import numpy as np
from src.app.utils import replace_as_lastcols

def hydroalunorte(risco, df, cols, str_filters, val_filters=None, ts=None):
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

    river_ts = {}
    allriversmaxvals = {}
    for river in rivers:
       
        river_df = df_cols[df_cols[river_col] == river]
     
        if len(river_df) > 0:

            unique_sites = []
            sites = river_df[site_col]
            
            for ind in sites.index:
                
                site_name = sites[ind]
                if site_name not in unique_sites:
                    unique_sites.append(site_name)

        param_ts = {}

        rivermaxvals = {}
        for param in params:

            param_filtered = river_df[river_df[param_col] == param]
            param_filtered = param_filtered.reset_index(drop=True)
            if len(param_filtered) == 0:
                continue
            maxvalue = param_filtered[result_col].max()
            rivermaxvals[param] = maxvalue
            param_tsdf = pd.DataFrame(columns=['Data', unit_col, vmp_col])
            # param_tsdf['Data'] = pd.to_datetime(param_tsdf['Data'])
            param_tsdf.set_index('Data')
            
            for site in unique_sites:
                
                site_filtered = param_filtered[param_filtered[site_col] == site].copy(deep=True)
                site_filtered = site_filtered.reset_index(drop=True)
                if len(site_filtered) == 0:
                    continue
                
                param_sitedf = pd.DataFrame(columns=['Data'])
                   
                # param_filtered = site_filtered[site_filtered[param_col] == param]

                if len(site_filtered) >= 2:

                    for i in range(len(site_filtered) - 1):

                        year1 = site_filtered.loc[i, date_col].year
                        month1 = site_filtered.loc[i, date_col].month
                        if len(str(month1)) == 1:
                            month1 = f'0{site_filtered.loc[i, date_col].month}'
                        day1 = site_filtered.loc[i, date_col].day
                        if len(str(day1)) == 1:
                            day1 = f'0{site_filtered.loc[i, date_col].day}'
                        
                        date_before = np.datetime64(f'{year1}-{month1}-{day1}')
                        print('BEFORE', date_before)
                        year2 = site_filtered.loc[i + 1, date_col].year
                        month2 = site_filtered.loc[i + 1, date_col].month
                        if len(str(month2)) == 1:
                            month2 = f'0{site_filtered.loc[i + 1, date_col].month}'
                        day2 = site_filtered.loc[i + 1, date_col].day
                        if len(str(day2)) == 1:
                            day2 = f'0{site_filtered.loc[i + 1, date_col].day}'
                        
                        date_next = np.datetime64(f'{year2}-{month2}-{day2}')
                        print('NEXT', date_next)
                        if date_next == date_before:
                            print('MATCH', date_next, date_before)
                            avg = site_filtered.loc[i: i + 2, result_col].mean()
                            print('AVG', avg)
                            site_filtered.loc[i + 1, result_col] = avg
                            # if date_before.astype('datetime64[Y]').astype(int) + 1970 == 2019:
                            #     print('AVG', avg)
                            #     print(date_before, date_next)
                            #     print(len(site_filtered))
                            print(len(site_filtered))
                            site_filtered = site_filtered.drop(i)
                            print(len(site_filtered))
                            # if date_before.astype('datetime64[Y]').astype(int) + 1970 == 2019:
                            #     print(len(site_filtered))
                
                          # print(site_filtered)
                # if site == 'RPJ':

                #     print(site_filtered.info())            # fknkbnjgknb
                #     print(site_filtered)            # fknkbnjgknb
                if len(site_filtered) > 0:
                            
                    # param_sitedf['Data'] = pd.to_datetime(site_filtered[date_col])
                    param_sitedf['Data'] = site_filtered[date_col]
                    param_sitedf[site] = site_filtered[result_col]
                    param_sitedf[unit_col] = site_filtered[unit_col]
                    param_sitedf[vmp_col] = site_filtered[vmp_col]
                    param_sitedf.set_index('Data')
                    param_tsdf = param_tsdf.merge(param_sitedf, how='outer', on=['Data', unit_col, vmp_col])
                    if param == 'Sulfato':
                        print(river)
                        print(param)
                        print(site)
                        print(param_tsdf)
                    param_tsdf = param_tsdf.reset_index(drop=True)
            
            param_tsdf = replace_as_lastcols(param_tsdf, (vmp_col, unit_col))
            param_ts[param] = param_tsdf
        
        if len(param_ts) > 0:    
            river_ts[river] = param_ts
        allriversmaxvals[river] = rivermaxvals
    param_allrivers_df = {}
    for param in params:
        param_allrivers_tsdf = pd.DataFrame(columns=['Data', unit_col, vmp_col])
        param_allrivers_tsdf.set_index('Data')

        for river in river_ts.keys():
            for riverparam in river_ts[river].keys():
                if riverparam == param:

                    param_allrivers_tsdf = param_allrivers_tsdf.merge(river_ts[river][riverparam], how='outer', on=['Data', unit_col, vmp_col])
                    param_allrivers_tsdf = param_allrivers_tsdf.reset_index(drop=True)

        param_allrivers_tsdf = replace_as_lastcols(param_allrivers_tsdf, (vmp_col, unit_col))
        param_allrivers_tsdf = param_allrivers_tsdf.sort_values(by='Data', ascending=True)
        
        if len(param_allrivers_tsdf) > 0:
            param_allrivers_df[param] = param_allrivers_tsdf

    for river in river_ts.keys():
        with pd.ExcelWriter(f'dataframes\{risco}\{river}_{risco}_monit_cont.xlsx') as writer:
            for tsdf in river_ts[river].keys():
                river_ts[river][tsdf].to_excel(writer, sheet_name=tsdf)

    with pd.ExcelWriter(f'dataframes\{risco}\{risco}_monit_cont.xlsx') as writer:
        for param in param_allrivers_df.keys():
            param_allrivers_df[param].to_excel(writer, sheet_name=param)
    
    # print(river_ts)
    # print(param_allrivers_df)
    # print(rivermaxvals)
    # print(overallmax)
    return {'dataframes': {'perparam':param_allrivers_df, 'perriver': river_ts}, 'maximos': rivermaxvals, 'overallmax': overallmax} 
   
        
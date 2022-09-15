import pandas as pd
import numpy as np
from src.app.utils.challenge import removerepeateddates
from src.app.utils import replace_as_lastcols


def eflu_etei(df, cols, params, pts, risco, mode, owner, renames=None):
    
    main_df = df[cols]
    # print(params)
    datecol = 'Data da coleta'
    resultcol = 'Resultado'
    paramcol = 'Parâmetros'     
    ptcol = 'Ponto'
    unitcol = 'Unidade'
    vmpcol = 'VMP'
    if owner == 'hydro':
        datecol = 'Data Coleta'
        resultcol = 'Valor'
        paramcol = 'Parâmetro'     
        ptcol = 'Código do ponto'
        unitcol = 'Unidade'
        vmpcol = 'VMP'
    tsdfs = {}
    with pd.ExcelWriter(f'dataframes\{risco}\{mode.upper()}_{risco.lower()}_{owner.upper()}.xlsx') as writer:

        for param in params:
            # print(param)
            
            param_df = main_df[main_df[paramcol] == param]
            # print(len(param_df))

            if len(param_df) == 0:
                continue
           
            param_tsdf = pd.DataFrame(columns=['Data', unitcol, vmpcol])
            param_tsdf['Data'] = pd.to_datetime(param_tsdf['Data'])
            param_tsdf.set_index('Data')
            for pt in pts:
                # print(pt)
                pt_df = param_df[param_df[ptcol] == pt]
                pt_df.loc[:, resultcol] = pd.to_numeric(pt_df[resultcol], errors='coerce')
                pt_df.dropna()

                if len(pt_df) > 0 and pt_df[resultcol].max() > 0:
                    # print(pt)
                    pt_df = pt_df.reset_index(drop=True)
                    # print(len(pt_df))
                    pt_df.loc[:, resultcol] = pd.to_numeric(pt_df[resultcol], errors='coerce')
                    # print(len(pt_df))
                    pt_df = pt_df[pt_df[resultcol] >= 0.]
                    # print(len(pt_df))
                    pt_df = pt_df.reset_index(drop=True)
                    pt_tsdf = pd.DataFrame()
                    for i in range(len(pt_df)):
                        cell_value = pt_df.loc[i, resultcol]
                        cell_unit = pt_df.loc[i, unitcol]
                        cell_vmp = pt_df.loc[i, vmpcol]
                        # mu = '\u03BC'
                        if cell_unit[1:] == 'g/L' and cell_unit[0] != 'm' and cell_unit[0] != 'k':
                            pt_df.loc[i, resultcol] = cell_value/1000.
                            pt_df.loc[i, unitcol] = 'mg/L'
                            try:
                                pt_df.loc[i, vmpcol] = cell_vmp/1000
                            except:
                                pass
                    
                    pt_tsdf['Data'] = pd.to_datetime(pt_df[datecol])
                    if renames:
                        pt_tsdf[renames[pt]] = pt_df[resultcol]
                    else:
                        pt_tsdf[pt] = pt_df[resultcol]
                    pt_tsdf[unitcol] = pt_df[unitcol]
                    pt_tsdf[vmpcol] = pt_df[vmpcol]
                    pt_tsdf.set_index('Data')
                    param_tsdf = param_tsdf.merge(pt_tsdf, how='outer', on=['Data', unitcol, vmpcol])
            if len(param_tsdf) > 0:
                param_tsdf.set_index('Data')      
                param_tsdf = replace_as_lastcols(param_tsdf, ('VMP', 'Unidade'))
                orderedcols = ['Data']
                df_cols = param_tsdf.columns.tolist()
                ind = df_cols.index('Data')
                df_cols.pop(ind)
                orderedcols.extend(df_cols)
                param_tsdf = param_tsdf[orderedcols]
                param_tsdf = removerepeateddates(param_tsdf, 'Data')
                param_tsdf = param_tsdf.sort_values(by='Data', ascending=True)
                param_tsdf = param_tsdf.reset_index(drop=True)
                tsdfs[param] = param_tsdf
                param_tsdf.to_excel(writer, sheet_name=param)
 
    return tsdfs
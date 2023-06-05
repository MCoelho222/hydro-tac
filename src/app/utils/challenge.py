import pandas as pd
import numpy as np

def removerepeateddates(df, date_col, result_col=None, param=None):
 
    dfc = df
    dfc = dfc.sort_values(by=date_col, ascending=True)
    dfc = dfc.reset_index(drop=True)
    cols = df.columns.tolist()
    avg_cols = cols[1: len(cols) - 2]
    if len(dfc) >= 2:
      
        todrop = []
        for i in range(len(dfc) - 1):
            year1 = dfc.loc[i, date_col].year
            month1 = dfc.loc[i, date_col].month
            if len(str(month1)) == 1:
                month1 = f'0{dfc.loc[i, date_col].month}'
            day1 = dfc.loc[i, date_col].day
            if len(str(day1)) == 1:
                day1 = f'0{dfc.loc[i, date_col].day}'
            
            date_before = np.datetime64(f'{year1}-{month1}-{day1}')
            year2 = dfc.loc[i + 1, date_col].year
            month2 = dfc.loc[i + 1, date_col].month
            if len(str(month2)) == 1:
                month2 = f'0{dfc.loc[i + 1, date_col].month}'
            day2 = dfc.loc[i + 1, date_col].day
            if len(str(day2)) == 1:
                day2 = f'0{dfc.loc[i + 1, date_col].day}'
            
            date_next = np.datetime64(f'{year2}-{month2}-{day2}')
            if date_next == date_before:
                if result_col != None:
                    rowsmax = dfc.loc[i: i + 1, result_col]
                    avg = rowsmax.max()
                    dfc.loc[i + 1, result_col] = avg
                else:
                    rowsmax = dfc.loc[i: i + 1, avg_cols]
                    avg = rowsmax.max()
                    dfc.loc[i + 1, avg_cols] = avg

                todrop.append(i)
        if param == 'month':
           
            for i in range(len(dfc) - 1):
                year1 = dfc.loc[i, date_col].year
                month1 = dfc.loc[i, date_col].month
                if len(str(month1)) == 1:
                    month1 = f'0{dfc.loc[i, date_col].month}'
                day1 = dfc.loc[i, date_col].day
                if len(str(day1)) == 1:
                    day1 = f'0{dfc.loc[i, date_col].day}'
                
                date_before = np.datetime64(f'{year1}-{month1}')
                year2 = dfc.loc[i + 1, date_col].year
                month2 = dfc.loc[i + 1, date_col].month
                if len(str(month2)) == 1:
                    month2 = f'0{dfc.loc[i + 1, date_col].month}'
                day2 = dfc.loc[i + 1, date_col].day
                if len(str(day2)) == 1:
                    day2 = f'0{dfc.loc[i + 1, date_col].day}'
                
                date_next = np.datetime64(f'{year2}-{month2}')
                if date_next == date_before:
                    if result_col != None:
                        rowsmax = dfc.loc[i: i + 1, result_col]
                        avg = rowsmax.max()
                        dfc.loc[i + 1, result_col] = avg
                    else:
                        rowsmax = dfc.loc[i: i + 1, avg_cols]
                        avg = rowsmax.max()
                        dfc.loc[i + 1, avg_cols] = avg

                    todrop.append(i)
        
        if len(todrop) > 0:
            for dropind in todrop:
                for idx in dfc.index:
                    if dropind == idx:
                        dfc = dfc.drop(idx)
    return dfc


def mergedfs(dfs, cols):
    mergeddf = pd.DataFrame(columns=cols)
    for df in dfs:
        df_cols = df.columns.tolist()
        df1 = removerepeateddates(df, 'Data', df_cols[1], df_cols[1])
        mergeddf = mergeddf.merge(df1, how='outer', on=cols)
    mergeddf.to_excel('dataframes\challenge.xlsx')

    return mergeddf
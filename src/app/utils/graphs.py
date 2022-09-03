import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import matplotlib.dates as mdates
from src.app.utils import replace_as_lastcols

mpl.rcParams['axes.linewidth'] = 0.5

def voluntariosplot(df, overallmax, rivername, risco, leg_position):
  
    if len(df) == 0:
        print('hdhfkfngkjnbgbgb')
        return {'error': 'empty dataframe'}
    owners = list(df.keys())
    name = ''
    allparams = set([])
    for item in owners:
        name = item
        owner = df[item]
        for tide in owner.keys():

            params = list(owner[tide].keys())
            for j in range(len(params)):
                allparams.add(params[j])
    
    all_tides = df[name].keys()
    list_all_tides = list(all_tides)
    markers = ['o', '^', '*']
    colors= ['tab:orange', 'gray', 'k', 'r', 'brown', 'lime', 'blue', 'm', 'c', 'deeppink', 'y']
    marker = {}
    for i in range(len(list_all_tides)):
        marker[list_all_tides[i]] = markers[i]
    
    for param in allparams:
        ylabel = ''
        xlabels = []
        figsize = (6.6, 3.3)
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)

        counter = 0
        for tide in all_tides:

            try:
                paramdf = df[name][tide][param]
                counter += 1
            except KeyError:
                if counter == 0:
                    continue
                if counter == 1:
                    paramdf = pd.DataFrame()
                
            if len(paramdf) > 0:
                
                paramdf = replace_as_lastcols(paramdf, ('VMP', 'Unidade'))
                
                vmp_col = paramdf['VMP']
                vmp = vmp_col.max()
                paramdf_cols = list(paramdf.columns)
                pop_ind = paramdf_cols.index('VMP')
                paramdf_cols.pop(pop_ind)
                paramdf = paramdf[paramdf_cols] 
                cols2 = paramdf.columns.tolist()
                unit = cols2.pop()
                ylabel = paramdf[unit].loc[0]
                
                xlabels = cols2[1:]
                # dff = paramdf[cols2].sort_values(by='Data', ascending=True)
                for i in range(len(paramdf)):
                    
                    ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], marker=marker[tide], s=30,  label=f"{paramdf.loc[i, 'Data'].day}-{paramdf.loc[i, 'Data'].month}-{paramdf.loc[i, 'Data'].year} {tide}", color=colors[i]) 
        try:
            vmp_col.loc[0] > 0
            ax.axhline(vmp_col.loc[0],  label='VMP', linewidth=0.5, linestyle='dashed', color='r')
        except:
            if param == 'pH':
                try:
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=0.5, color='r')
                    ax.axhline(supflim, linewidth=0.5, color='r')
                except:
                    pass
            pass
        
        plt.title(f'{param} - {rivername.title()} ({name.upper()})', fontsize=11)
        plt.xlabel('Pontos', fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
      
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
     
        if len(xlabels) > 3:
            for x in xlabels:
                try:
                    label = x.split(' - ')
                    if label[-1] == '(Antes)' or label[-1] == '(Depois)':
                        fig.autofmt_xdate()
                except:
                    continue
            
        if len(xlabels) > 10:
            plt.xticks(rotation=90)
        try:
            if param != 'pH':
                if overallmax[param] > vmp:
                    plt.ylim(0., overallmax[param] * 1.1)
            if param == 'pH':
                ph = vmp_col.loc[0].split(' ')[-1]
                if overallmax[param] > int(ph):
                    plt.ylim(0., overallmax[param] * 1.1)
        except TypeError:
            plt.ylim(0., overallmax[param] * 1.1)
        
        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        leg = ax.legend(handles, labels, loc=leg_position, fontsize=7, framealpha=0.4)
        leg.get_frame().set_linewidth(0.0)
        # ax.legend(loc='best', fontsize=7, frameon=False)
        plt.tight_layout()
        plt.savefig(f'graphs\{risco}\{param.upper()}_{rivername}_{name}.svg')
        plt.show()
    
    return allparams

def hydroplots(df, overallmax, figfilename, figtitle, risco, leg_position):
  
    if len(df) == 0:
        return {'error': 'empty dataframe'}
    overallmax['Fósforo Total'] = 0.99
    for param in df.keys():
        
        paramdf = df[param]
        vmp_col = paramdf['VMP']
        vmp = vmp_col.max()
        paramdf = replace_as_lastcols(paramdf, ('VMP', 'Unidade'))  
        paramdf_cols = list(paramdf.columns)
        pop_ind = paramdf_cols.index('VMP')
        paramdf_cols.pop(pop_ind)
        paramdf = paramdf[paramdf_cols] 
        
        cols2 = paramdf.columns.tolist()
        unit = cols2.pop()
        ylabel = paramdf[unit].loc[0]
        
        ts = cols2[1:]
        # dff = paramdf[cols2].sort_values(by='Data', ascending=True)
        
        figsize = (7, 3.5)
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)
        colors= ['tab:orange', 'gray', 'k', 'r', 'brown', 'burlywood', 'blue', 'm', 'c', 'deeppink', 'y']
        sizes = [32, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8]
        colors = colors[::-1]
        # for ts in ts_names:
        for i in range(len(ts)):

            ax.scatter(paramdf[cols2[0]], paramdf[ts[i]], s=sizes[i], label=ts[i], color=colors[i], alpha=0.8) 
        try:
            vmp_col.loc[0] > 0
            ax.axhline(vmp_col.loc[0],  label='VMP', linewidth=0.5, linestyle='dashed', color='r')
        except:
            if param == 'pH':
                try:
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=0.5, color='r')
                    ax.axhline(supflim, linewidth=0.5, color='r')
                except:
                    pass
            pass
        
        plt.title(f'{param} - {figtitle.title()}', fontsize=11)
        plt.xlabel('Data', fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
      
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
        fig.autofmt_xdate()
              
        try:
            if param != 'pH':
                if overallmax[param] > vmp:
                    plt.ylim(0., overallmax[param] * 1.1)
                if param == 'pH':
                    ph = vmp_col.loc[0].split(' ')[-1]
                    if overallmax[param] > int(ph):
                        plt.ylim(0., overallmax[param] * 1.1)
        except TypeError:
            plt.ylim(0., overallmax[param] * 1.1)

        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        leg = ax.legend(handles, labels, loc=leg_position, fontsize=8, framealpha=0.4)
        leg.get_frame().set_linewidth(0.0)
        
        # ax.legend(loc='best', fontsize=7, frameon=False)
        plt.tight_layout()
        plt.savefig(f'graphs\{risco}\{param.upper()}_{figfilename}.svg', dpi=1200)
        plt.show()
       
    return
    



            




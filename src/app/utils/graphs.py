import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import matplotlib.dates as mdates
from src.app.utils import replace_as_lastcols
import numpy as np

mpl.rcParams['axes.linewidth'] = 0.5


def voluntariosplot(df, overallmax, rivername, risco, baseline, mode, leg_position):
    if len(df) == 0:
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
    list_all_tides = list(all_tides)[::-1]
    markers = ['o', '^', '*']
    colors= ['tab:orange', 'gray', 'k', 'r', 'brown', 'lime', 'blue', 'm', 'c', 'deeppink', 'y']
    marker = {}
    for i in range(len(list_all_tides)):
        marker[list_all_tides[i]] = markers[i]
    
    if mode == 'sed' and name == 'Geoklock':
        list_all_tides = list_all_tides[::-1]
    for param in allparams:
        ylabel = ''
        xxlabels = set([])
        figsize = (6.8, 3.6)
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)

        counter = 0
        if mode == 'sed':
            ax.axhline(baseline[param]['max'],  label='Baseline/background (max)', linewidth=0.5, linestyle='dashed', color='k')
            ax.axhline(baseline[param]['med'],  label='Baseline/background (mediana)', linewidth=1., linestyle='dashed', color='b')
        if mode == 'sup':
            try:
                ax.axhline(baseline[param],  label='Baseline/background (max)', linewidth=0.5, linestyle='dashed', color='k')
            except KeyError:
                pass
        for tide in list_all_tides:

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
                if vmp == '6 a 9' or vmp =='6.0 a 9.0':
                    vmp = int(vmp.split(' ')[-1])
                paramdf_cols = list(paramdf.columns)

                maxcols = paramdf_cols[1:]
                colmax = []
                for i in range(len(maxcols)):
                    tomax = pd.to_numeric(paramdf[maxcols[i]], errors='coerce')
                    tomax = tomax.dropna()
                    if len(tomax) > 0:
                        try:
                            maxval = tomax.max()
                        except:
                            continue
                        
                        colmax.append(maxval)
                colmax2 = np.array(colmax)
                maxmax = np.max(colmax2)

                pop_ind = paramdf_cols.index('VMP')
                paramdf_cols.pop(pop_ind)
                paramdf = paramdf[paramdf_cols] 
                cols2 = paramdf.columns.tolist()
                unit = cols2.pop()
                ylabel = paramdf[unit].loc[0]
                
                xlabels = cols2[1:]
                for i in range(len(xlabels)):
                    xxlabels.add(xlabels[i])
                for i in range(len(paramdf)):
                    
                    ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], marker=marker[tide], s=30,  label=f"{paramdf.loc[i, 'Data'].day}-{paramdf.loc[i, 'Data'].month}-{paramdf.loc[i, 'Data'].year} {tide}", color=colors[i]) 
        try:
            vmp_col.loc[0] > 0
            if mode == 'sed': 
                if name == 'Geoklock':
                    label = 'EPA-RSL'
                if name == 'Enviro-Tec':
                    label = 'CONAMA 420/2009'
                if name == 'SGW':
                    label = 'CONAMA 454/2012'
                ax.axhline(vmp_col.loc[0],  label=label, linewidth=1., linestyle='dashed', color='r')
            else:
                label = 'VMP'
                ax.axhline(vmp_col.loc[0],  label=label, linewidth=1., linestyle='dashed', color='r')

        except:
            if param == 'pH':
                try:
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=1., linestyle='dashed', color='r')
                    ax.axhline(supflim, linewidth=1., color='r', linestyle='dashed')
                except:
                    pass
            pass
        
        plt.title(f'{param} - {rivername.title()}', fontsize=9)
        plt.xlabel('Pontos', fontsize=9)
        plt.ylabel(ylabel, fontsize=9)
      

        if len(xxlabels) > 3:
            for x in xlabels:
                try:
                    label = x.split(' - ')
                    if label[-1] == '(Antes)' or label[-1] == '(Depois)':
                        fig.autofmt_xdate()
                except:
                    continue
            
        if len(xxlabels) > 7:
            plt.xticks(rotation=90)
        if mode == 'sed':
            toptop = baseline[param]['max']
        else:
            try:
                toptop = baseline[param]
            except KeyError:
                toptop = 0

        if toptop > maxmax and toptop > overallmax[param]:
            plt.ylim(0., toptop * 1.0500)
        else:
            if overallmax[param] > maxmax and param != 'Sólidos dissolvidos totais':
                plt.ylim(0., overallmax[param] * 1.0500)
            else:
                try:
                    if maxmax > vmp:
                        plt.ylim(0., maxmax * 1.0500)
                    else:
                        plt.ylim(0., vmp * 1.0500)
                except:
                    plt.ylim(0., maxmax * 1.0500)

        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        leg = ax.legend(handles, labels, fontsize=7, loc=leg_position, framealpha=0.4, ncol=2)
        leg.get_frame().set_linewidth(1.0)
        plt.tight_layout()
        plt.savefig(f'graphs\{risco}\{name}\{mode.upper()}_{param}_{rivername}_{name}.svg')
        plt.show()
    
    return allparams


def hydroplots(df, overallmax, figfilename, figtitle, risco, baseline, mode, graphtype=None, leg_position=None):
  
    if len(df) == 0:
        return {'error': 'empty dataframe'}
    for param in df.keys():
       
        paramdf = df[param]
        if param != 'pH':
            paramdf['VMP'] = pd.to_numeric(paramdf['VMP'], errors='coerce')
        vmp_col = paramdf['VMP']
        vmp = vmp_col.max()
        if vmp == '6 a 9' or vmp =='6.0 a 9.0':
            vmp = int(vmp.split(' ')[-1])
        paramdf_cols = list(paramdf.columns)

        maxcols = paramdf_cols[1:]
        colmax = []
        for i in range(len(maxcols)):
            tomax = pd.to_numeric(paramdf[maxcols[i]], errors='coerce')
            tomax = tomax.dropna()
            if len(tomax) > 0:
                try:
                    maxval = tomax.max()
                except:
                    continue
                
                colmax.append(maxval)
        colmax2 = np.array(colmax)
        maxmax = np.max(colmax2)
        paramdf = replace_as_lastcols(paramdf, ('VMP', 'Unidade'))  
        paramdf_cols = list(paramdf.columns)
        pop_ind = paramdf_cols.index('VMP')
        paramdf_cols.pop(pop_ind)
        paramdf = paramdf[paramdf_cols] 
        
        cols2 = paramdf.columns.tolist()
        unit = cols2.pop()
        ylabel = paramdf[unit].loc[0]
        
        ts = cols2[1:]
        ordered = []
        order = ['RMN', 'RMEC', 'RMCC', 'IT', 'IPJ', 'IAV']
        for i in range(len(order)):
            if order[i] in ts:
                ordered.append(order[i])
        data = []
        for i in range(len(ordered)):
            colvalue = paramdf[ordered[i]]
            colvalue = colvalue.dropna()
            values = colvalue.values.tolist()
            data.append(values)
        figsize = (7, 4)
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)
        colors= ['goldenrod', 'gold', 'k', 'chocolate', 'darkorange', 'orangered', 'dimgray', 'darkgray', 'lightgray', 'royalblue', 'cornflowerblue', 'deepskyblue']
        if graphtype == 'boxplot':
            ax.boxplot(data, labels=ordered)
        else:
            for i in range(len(ts)):

                ax.scatter(paramdf[cols2[0]], paramdf[ts[i]], s=31, label=ts[i], color=colors[i])
        try:
            vmp_col.loc[0] > 0
            if param != 'pH' and param != 'Sódio total' and param != 'Sílica total':
                ax.axhline(vmp_col.loc[0],  label='VMP', linewidth=1., linestyle='dashed', color='r')
        except:
            if param == 'pH':
                try:
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=1., color='r', linestyle='dashed')
                    ax.axhline(supflim, linewidth=1., color='r', linestyle='dashed')
                except:
                    pass
            pass
        try:
            ax.axhline(baseline[param],  label='Baseline/background (max)', linewidth=0.5, linestyle='dashed', color='k')
        except:
            pass
        
        
        plt.title(f'{param} - {figtitle.title()}', fontsize=9)
        if graphtype == 'boxplot':
            plt.xlabel('Pontos', fontsize=10)
        else:
            plt.xlabel('Data', fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
      
        if graphtype != 'boxplot':
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
            fig.autofmt_xdate()

        if mode == 'sed':
            toptop = baseline[param]['max']
        else:
            try:
                toptop = baseline[param]
            except:
                pass
        try: 
            if toptop > maxmax and toptop > overallmax[param]:
                plt.ylim(0., toptop * 1.0500)
            else:
                if overallmax[param] > maxmax:
                    plt.ylim(0., overallmax[param] * 1.0500)
                else:
                    try:
                        if maxmax > vmp:
                            plt.ylim(0., maxmax * 1.0500)
                        else:
                            plt.ylim(0., vmp * 1.0500)
                    except:
                        plt.ylim(0., maxmax * 1.0500)
        except:
            if overallmax[param] > maxmax:
                plt.ylim(0., overallmax[param] * 1.0500)
            else:
                try:
                    if maxmax > vmp:
                        plt.ylim(0., maxmax * 1.0500)
                    else:
                        plt.ylim(0., vmp * 1.0500)
                except:
                    plt.ylim(0., maxmax * 1.0500)

        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        leg = ax.legend(handles, labels, fontsize=7, loc=leg_position, framealpha=0.4, ncol=3)
        leg.get_frame().set_linewidth(1.0)
        
        plt.tight_layout()

        if graphtype == 'boxplot':
            plt.savefig(f'graphs\{risco}\Hydro\{graphtype}_{mode.upper()}_{param}_{figfilename}.svg', dpi=1200)
        else:
            plt.savefig(f'graphs\{risco}\Hydro\{mode.upper()}_{param}_{figfilename}.svg', dpi=1200)
        plt.show()
       
    return
    
def besplotmare(df, overallmax, figtitle, baseline, mode, risco, leg_position=None):
    if len(df) == 0:
        print('hdhfkfngkjnbgbgb')
        return {'error': 'empty dataframe'}

    tides = list(df.keys())
    allparams = set([])
    for tide in tides:
       
        params = list(df[tide].keys())
        for j in range(len(params)):
            allparams.add(params[j])
    
    markers = ['o', '^', '*', 's', 'D', 'v', 'X', 'h', 'p', 'x']
    marker = {}
    for i in range(len(tides)):
        marker[tides[i]] = markers[i]
    
    for param in allparams:
        ylabel = ''
        allxlabels = []
        figsize = (11, 5.5)
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)

        counter = 0
        for tide in tides:

            try:
                paramdf = df[tide][param]
                counter += 1
            except KeyError:
                if counter == 0:
                    continue
                if counter == 1:
                    paramdf = pd.DataFrame()
                
            if len(paramdf) > 0:
                
                vmp_col = paramdf['VMP']
                vmp = vmp_col.max()
                if vmp == '6 a 9' or vmp =='6.0 a 9.0':
                    vmp = int(vmp.split(' ')[-1])
                paramdf_cols = list(paramdf.columns)

                maxcols = paramdf_cols[1:]
                colmax = []
                for i in range(len(maxcols)):
                    tomax = pd.to_numeric(paramdf[maxcols[i]], errors='coerce')
                    tomax = tomax.dropna()
                    if len(tomax) > 0:
                        try:
                            maxval = tomax.max()
                        except:
                            continue
                        
                        colmax.append(maxval)
                colmax2 = np.array(colmax)
                maxmax = np.max(colmax2)

                pop_ind = paramdf_cols.index('VMP')
                paramdf_cols.pop(pop_ind)
                paramdf = paramdf[paramdf_cols] 
                cols2 = paramdf.columns.tolist()
                unit = cols2.pop()

                ylabel = paramdf[unit].loc[0]
                
                xlabels = cols2[1:]
                allxlabels.append(xlabels)
                for i in range(len(paramdf)):
                    ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], marker=marker[tide], s=30,  label=f"{paramdf.loc[i, 'Data'].month}-{paramdf.loc[i, 'Data'].year} {tide}") 
        
        try:
            vmp_col.loc[0] > 0
            if mode == 'sed':
                ax.axhline(vmp_col.loc[0],  label='CONAMA 454/2012', linewidth=1., linestyle='dashed', color='r')
            else:
                ax.axhline(vmp_col.loc[0],  label='VMP', linewidth=1., linestyle='dashed', color='r')
        except:
            if param == 'pH':
                try:
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=1., color='r', linestyle='dashed')
                    ax.axhline(supflim, linewidth=1., color='r', linestyle='dashed')
                except:
                    pass
            pass
        try:
            if mode == 'sed':
                ax.axhline(baseline[param]['max'],  label='Baseline/background (max)', linewidth=0.5, linestyle='dashed', color='k')
                ax.axhline(baseline[param]['med'],  label='Baseline/background (mediana)', linewidth=1., linestyle='dashed', color='b')
            if mode == 'sup':
                ax.axhline(baseline[param],  label='Baseline/background (max)', linewidth=0.5, linestyle='dashed', color='k')
        except:
            pass
        plt.title(f'{param} - {figtitle}', fontsize=9)
        plt.xlabel('Pontos', fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
        y0, ymax = plt.ylim()
        if ymax > maxmax and ymax > overallmax[param]:
            ywidth = ymax - 0.0000
        else:
            if overallmax[param] > maxmax:
                ywidth = overallmax[param] - 0.0000
            else:
                ywidth = maxmax - 0.000
        yloc = ywidth * 0.7
        print('Y MAX', ymax)
        print('ywidth', ywidth)
        print('MAXMAX', maxmax)
        print('YLOC', yloc)

        lcolor = 'grey'
        
        if mode == 'sup':
            plt.text(19, yloc, 'Murucupi', fontsize=8, color='k')
            plt.text(6, yloc, 'Pará', fontsize=8, color='k')
            plt.text(22, yloc, 'Dendê', fontsize=8, color='k')
            plt.axvline(16, 0., 1, color=lcolor, linewidth=1.)
            plt.axvline(22, 0., 1, color=lcolor, linewidth=1.)
        if mode == 'sed':
            plt.text(17, yloc, 'Murucupi', fontsize=8, color='k')
            plt.text(6, yloc, 'Pará', fontsize=8, color='k')
            plt.text(19, yloc, 'Dendê', fontsize=8, color='k')
            plt.axvline(16, 0., 1, color=lcolor, linewidth=1.)
            plt.axvline(19, 0., 1, color=lcolor, linewidth=1.)

        if len(xlabels) > 10:
            plt.xticks(rotation=90)
        
        if mode == 'sed':
            toptop = baseline[param]['max']
        else:
            toptop = baseline[param]

        if toptop > maxmax and toptop > overallmax[param]:
            plt.ylim(0., toptop * 1.0500)
        else:
            if overallmax[param] > maxmax:
                plt.ylim(0., overallmax[param] * 1.0500)
            else:
                try:
                    if maxmax > vmp:
                        plt.ylim(0., maxmax * 1.0500)
                    else:
                        plt.ylim(0., vmp * 1.0500)
                except:
                    plt.ylim(0., maxmax * 1.0500)
        
        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        # sort both labels and handles by labels

        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        leg = ax.legend(handles, labels, fontsize=6, framealpha=0.4, ncol=3, loc='best')
        leg.get_frame().set_linewidth(1.0)
        plt.tight_layout()
        plt.savefig(f'graphs\{risco}\Arcadis\{mode.upper()}_{param}_BES_mares.svg')
        plt.show()
    
    return


def besplotall(df, overallmax, figtitle, mode, risco, baseline=None, leg_position=None):

    if len(df) == 0:
        return {'error': 'empty dataframe'}
    
    params = list(df.keys())
   
    for param in params:
        print(overallmax)
        ylabel = ''
        xlabels = []
        if mode == 'eflu':
            figsize = (9, 4.5)
        else:
            figsize = (11, 5.5)
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)

        paramdf = df[param]
        
        vmp_col = paramdf['VMP']

        vmp = vmp_col.max()
        if vmp == '6 a 9' or vmp =='6.0 a 9.0':
            vmp = int(vmp.split(' ')[-1])
        print(param)
        print('VMP MAX', vmp)
        paramdf_cols = list(paramdf.columns)
        
        maxcols = paramdf_cols[1:]
        colmax = []
        for i in range(len(maxcols)):
            tomax = pd.to_numeric(paramdf[maxcols[i]], errors='coerce')
            tomax = tomax.dropna()
            if len(tomax) > 0:
                try:
                    maxval = tomax.max()
                except:
                    continue
                
                colmax.append(maxval)
        colmax2 = np.array(colmax)
        maxmax = np.max(colmax2)
        
        pop_ind = paramdf_cols.index('VMP')
        paramdf_cols.pop(pop_ind)
        paramdf = paramdf[paramdf_cols] 
        cols2 = paramdf.columns.tolist()
        unit = cols2.pop()
        ylabel = paramdf[unit].loc[0]
        xlabels = cols2[1:]
        for i in range(len(paramdf)):
            
            ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], s=30,  label=f"{paramdf.loc[i, 'Data'].month}-{paramdf.loc[i, 'Data'].year}") 
            # ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], s=25, color='tab:orange') 
        
        try:
            vmp_col.loc[0] > 0
            ax.axhline(vmp_col.loc[0],  label='VMP', linewidth=1., linestyle='dashed', color='r')
        except:
            if param == 'pH':
                try:
                    print('VMP', vmp_col.loc[0])
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=1., color='r', linestyle='dashed')
                    ax.axhline(supflim, linewidth=1., color='r', linestyle='dashed')
                except:
                    pass
            pass
        if baseline:
            try:
                if mode =='sed':
                    ax.axhline(baseline[param]['max'],  label='Baseline/background (max)', linewidth=0.5, linestyle='dashed', color='k')
                    ax.axhline(baseline[param]['med'],  label='Baseline/background (mediana)', linewidth=1., linestyle='dashed', color='b')
                if mode =='sup':
                    ax.axhline(baseline[param],  label='Baseline/background (max)', linewidth=0.5, linestyle='dashed', color='k')
            except:
                pass
        plt.title(f'{param} - {figtitle}', fontsize=9)
        plt.xlabel('Pontos', fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
        y0, ymax = plt.ylim()
        if ymax > maxmax and ymax > overallmax[param]:
            ywidth = ymax - 0.0000
        else:
            if overallmax[param] > maxmax:
                ywidth = overallmax[param] - 0.0000
            else:
                ywidth = maxmax - 0.000
        yloc = ywidth*0.70
        yloc2 = ywidth*0.40
        yloc3 = ywidth*0.30
        yloc4 = ywidth*0.35
        yloc5 = ywidth*0.20
        print('Y MAX', ymax)
        print('ywidth', ywidth)
        print('MAXMAX', maxmax)
        print('YLOC', yloc)
        lcolor = 'grey'
        line = 1.
        ig_size = 7
        if mode == 'sup':
            plt.text(8, yloc, 'Barcarena', fontsize=8, color='k')
            plt.text(24, yloc, 'Murucupi', fontsize=8, color='k')
            plt.text(33, yloc, 'Dendê', fontsize=8, color='k')
            plt.text(45, yloc, 'Pará', fontsize=8, color='k')
            plt.axvline(21, 0, 1, color=lcolor, linewidth=line)
            plt.axvline(31, 0, 1, color=lcolor, linewidth=line)
            plt.axvline(38, 0, 1, color=lcolor, linewidth=line)
        
            plt.text(3, yloc2, 'Tauá', fontsize=ig_size, color=lcolor)
            plt.text(6, yloc3, 'Pramajó', fontsize=ig_size, color=lcolor)
            plt.text(8, yloc4, 'Pramajozinho', fontsize=ig_size, color=lcolor)
            plt.text(10, yloc5, 'Pramajó', fontsize=ig_size, color=lcolor)
            plt.text(11, yloc2, 'Tauá', fontsize=ig_size, color=lcolor)
            plt.text(15, yloc3, 'Água Verde', fontsize=ig_size, color=lcolor)
            plt.axvline(3, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(6, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(8, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(10, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(11, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(15, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
        if mode == 'sed':
            plt.text(6, yloc, 'Barcarena', fontsize=8, color='k')
            plt.text(15, yloc, 'Murucupi', fontsize=8, color='k')
            plt.text(21, yloc, 'Dendê', fontsize=8, color='k')
            plt.text(30, yloc, 'Pará', fontsize=8, color='k')
            plt.axvline(14, 0, 1, color=lcolor, linewidth=line)
            plt.axvline(20, 0, 1, color=lcolor, linewidth=line)
            plt.axvline(23, 0, 1, color=lcolor, linewidth=line)
        
            plt.text(2, yloc2, 'Tauá', fontsize=ig_size, color=lcolor)
            plt.text(3, yloc3, 'Pramajó', fontsize=ig_size, color=lcolor)
            plt.text(6, yloc4, 'Pramajozinho', fontsize=ig_size, color=lcolor)
            plt.text(7, yloc2, 'Tauá', fontsize=ig_size, color=lcolor)
            plt.text(9, yloc3, 'Água Verde', fontsize=ig_size, color=lcolor)
            plt.axvline(2, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(3, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(6, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(7, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(9, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(11, 0, 1, linestyle='dashed', color=lcolor, linewidth=0.5)
        if mode == 'eflu':
            plt.text(0, yloc2, 'Entrada ETE',  fontsize=ig_size, color=lcolor)
            plt.text(1, yloc3, 'Saída ETE',  fontsize=ig_size, color=lcolor)
            plt.text(2, yloc4, 'Saída caixa de mistura Área 82',  fontsize=ig_size, color=lcolor)
            plt.text(4, yloc5, 'Calha Parshall',  fontsize=ig_size, color=lcolor)
            plt.text(5, yloc2, 'Canal de lançamento',  fontsize=ig_size, color=lcolor)
            plt.axvline(0, 0, 1, color=lcolor, linewidth=0.5)
            plt.axvline(1, 0, 1, color=lcolor, linewidth=0.5)
            plt.axvline(2, 0, 1, color=lcolor, linewidth=0.5)
            plt.axvline(4, 0, 1, color=lcolor, linewidth=0.5)
            plt.axvline(5, 0, 1, color=lcolor, linewidth=0.5)

        if len(xlabels) > 10:
            plt.xticks(rotation=90)
        if overallmax[param] > maxmax:
            plt.ylim(0., overallmax[param] * 1.0500)
        else:
            try:
                if maxmax > vmp:
                    plt.ylim(0., maxmax * 1.0500)
                else:
                    plt.ylim(0., vmp * 1.0500)
            except:
                plt.ylim(0., maxmax * 1.0500)
        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        leg = ax.legend(handles, labels, fontsize=6, framealpha=0.4,
                         loc='best', ncol=3)
        leg.get_frame().set_linewidth(1.0)
        
        plt.tight_layout()
        if mode == 'eflu':
            plt.savefig(f'graphs\{risco}\{mode.upper()}_{param}_BES.svg')
        else:
            plt.savefig(f'graphs\{risco}\Arcadis\{mode.upper()}_{param}_BES_mare_max.svg')
        plt.show()
    
    return
def efluplot(df, figtitle, mode, risco, graphtype=None, owner=None, leg_position=None):
    
    if len(df) == 0:
        return {'error': 'empty dataframe'}
    
    params = list(df.keys())
   
    for param in params:
        ylabel = ''
        xlabels = []
        figsize = (6.6, 3.3)
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)

        paramdf = df[param]
        vmp_col = paramdf['VMP']
        paramdf_cols = list(paramdf.columns)
        pop_ind = paramdf_cols.index('VMP')
        paramdf_cols.pop(pop_ind)
        paramdf = paramdf[paramdf_cols] 
        cols2 = paramdf.columns.tolist()
        unit = cols2.pop()
        ylabel = paramdf[unit].loc[0]
        
        xlabels = cols2[1:]
        data = []
        for i in range(len(xlabels)):
            colvalue = paramdf[xlabels[i]]
            colvalue = colvalue.dropna()
            values = colvalue.values.tolist()
            print(values)
            data.append(values)
        colors = ['tab:orange', 'gray', 'k', 'brown']
        if owner == 'hydro':
            if graphtype == 'boxplot':
                ax.boxplot(data, labels=xlabels)
            else:
                for i in range(len(xlabels)):
                    ax.scatter(paramdf[cols2[0]], paramdf[xlabels[i]], s=30, label=xlabels[i], color=colors[i])
        else:
            for i in range(len(paramdf)):
                
                ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], s=30,  label=f"{paramdf.loc[i, 'Data'].day}-{paramdf.loc[i, 'Data'].month}-{paramdf.loc[i, 'Data'].year}") 
                # ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], s=25, color='tab:orange') 
        try:
            vmp_col.loc[0] > 0
            ax.axhline(vmp_col.loc[0],  label='VMP', linewidth=1., linestyle='dashed', color='r')
        except:
            if param == 'pH':
                try:
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=1., color='r', linestyle='dashed')
                    ax.axhline(supflim, linewidth=1., color='r', linestyle='dashed')

                except:
                    pass
            pass
        if owner == 'hydro':
            if graphtype != 'boxplot':
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
        y0, ymax = plt.ylim()
        plt.ylim(0., ymax * 1.05)
        if len(xlabels) > 10:
            plt.xticks(rotation=90)

        plt.title(f'{param} - {figtitle}', fontsize=9)
        if owner == 'hydro' and graphtype != 'boxplot':
            plt.xlabel('Data', fontsize=10)
        else:
            plt.xlabel('Pontos', fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
        
        if len(xlabels) > 10:
            plt.xticks(rotation=90)
       
        ax.tick_params(axis='both', which='major', labelsize=6)
        if graphtype != 'boxplot':
            handles, labels = ax.get_legend_handles_labels()
            # sort both labels and handles by labels
            labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
            leg = ax.legend(handles, labels, fontsize=6, framealpha=0.4,
                            loc=leg_position, ncol=1)
        else:
            leg = ax.legend(loc=leg_position, fontsize=6, framealpha=0.4,frameon=False, ncol=1)
        leg.get_frame().set_linewidth(0.0)
        
        plt.tight_layout()
        if graphtype != 'boxplot' and graphtype != None:
            plt.savefig(f'graphs\{risco}\{graphtype}_{mode.upper()}_{param}_{owner}.svg')
        else:
            plt.savefig(f'graphs\{risco}\{mode.upper()}_{param}_{owner}.svg')
        plt.show()
    
    return


       




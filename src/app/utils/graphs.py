import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import matplotlib.dates as mdates
from src.app.utils import replace_as_lastcols
# from src.app.utils import sort_bes
# import matplotlib as mpl
# mpl.rc('image', cmap='gray')


mpl.rcParams['axes.linewidth'] = 0.5

def voluntariosplot(df, overallmax, rivername, risco, baseline, mode, leg_position):
    # if mode == 'sed':
    #     overallmax['Alumínio'] = 120000
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
        figsize = (6.6, 3.4)
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)

        counter = 0
        ax.axhline(baseline[param],  label='Baseline/background (max)', linewidth=1., linestyle='dashed', color='k')
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
                # paramdf['EPA-RSL'] = paramdf.loc[:, 'VMP']
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
            if mode == 'sed': 
                if name == 'Geoklock':
                    label = 'EPA-RSL'
                if name == 'Enviro-Tec':
                    label = 'CONAMA 420/2009'
                if name == 'SGW':
                    label = 'CONAMA 454/2012'
            else:
                label = 'VMP'
                if mode == 'sup':
                    ax.axhline(vmp_col.loc[0],  label=label, linewidth=1., linestyle='dashed', color='r')

        except:
            if param == 'pH':
                try:
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=1., color='r')
                    ax.axhline(supflim, linewidth=1., color='r')
                except:
                    pass
            pass
        
        plt.title(f'{param} - {rivername.title()} ({name.upper()})', fontsize=9)
        plt.xlabel('Pontos', fontsize=9)
        plt.ylabel(ylabel, fontsize=9)
      
        # plt.xticks(fontsize=9)
        # plt.yticks(fontsize=9)
     
        if len(xlabels) > 3:
            for x in xlabels:
                try:
                    label = x.split(' - ')
                    if label[-1] == '(Antes)' or label[-1] == '(Depois)':
                        fig.autofmt_xdate()
                except:
                    continue
            
        if len(xlabels) > 7:
            plt.xticks(rotation=90)
        try:
            if param != 'pH' and param != 'Sólidos dissolvidos totais':
                if overallmax[param] > vmp:
                    plt.ylim(0., overallmax[param] * 1.05)
            if param == 'pH':
                ph = vmp_col.loc[0].split(' ')[-1]
                if overallmax[param] > int(ph):
                    plt.ylim(0., overallmax[param] * 1.05)
        except TypeError:
            plt.ylim(0., overallmax[param] * 1.05)
        if mode == 'sed' and param == 'Alumínio':
            plt.ylim(0, 120000)
        if mode == 'sed' and param == 'Ferro':
            plt.ylim(0, 70000)
        
        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        leg = ax.legend(handles, labels, fontsize=7, loc=leg_position, framealpha=0.4)
        leg.get_frame().set_linewidth(0.0)
        # ax.legend(loc='best', fontsize=7, frameon=False)
        plt.tight_layout()
        plt.savefig(f'graphs\{risco}\{name}\{mode.upper()}_{param}_{rivername}_{name}.svg')
        plt.show()
    
    return allparams

def hydroplots(df, overallmax, figfilename, figtitle, risco, baseline, mode, leg_position):
  
    if len(df) == 0:
        return {'error': 'empty dataframe'}
    # overallmax['Fósforo Total'] = 0.5
    for param in df.keys():
        print(param)
        paramdf = df[param]
        paramdf['VMP'] = pd.to_numeric(paramdf['VMP'], errors='coerce')
        vmp_col = paramdf['VMP']
        print(vmp_col)
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
        
        figsize = (6.6, 3.3)
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)
        colors= ['goldenrod', 'gold', 'k', 'chocolate', 'darkorange', 'orangered', 'dimgray', 'darkgray', 'lightgray', 'royalblue', 'cornflowerblue', 'deepskyblue']
        # , 'tab:orange', 'gray', 'k', 'r', 'brown', 'burlywood', 'blue', 'm', 'c', 'deeppink', 'y']
        # sizes = [32, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8]
        # colors = colors[::-1]
        # for ts in ts_names:
        for i in range(len(ts)):

            ax.scatter(paramdf[cols2[0]], paramdf[ts[i]], s=31, label=ts[i], color=colors[i]) 
        try:
            vmp_col.loc[0] > 0
            ax.axhline(vmp_col.loc[0],  label='VMP', linewidth=1., linestyle='dashed', color='r')
        except:
            if param == 'pH':
                try:
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=1., color='r')
                    ax.axhline(supflim, linewidth=1., color='r')
                except:
                    pass
            pass
        ax.axhline(baseline[param],  label='Baseline/background (max)', linewidth=1., linestyle='dashed', color='k')
        
        
        plt.title(f'{param} - {figtitle.title()}', fontsize=9)
        plt.xlabel('Data', fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
      
        # plt.xticks(fontsize=9)
        # plt.yticks(fontsize=9)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
        fig.autofmt_xdate()
              
        try:
            if param != 'pH':
                if overallmax[param] > vmp:
                    plt.ylim(0., overallmax[param] * 1.05)
                if param == 'pH':
                    ph = vmp_col.loc[0].split(' ')[-1]
                    if overallmax[param] > int(ph):
                        plt.ylim(0., overallmax[param] * 1.05)
        except TypeError:
            plt.ylim(0., overallmax[param] * 1.05)

        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        leg = ax.legend(handles, labels, fontsize=6, loc=leg_position, framealpha=0.4, ncol=3)
        leg.get_frame().set_linewidth(0.0)
        
        # ax.legend(loc='best', fontsize=7, frameon=False)
        plt.tight_layout()
        plt.savefig(f'graphs\{risco}\Hydro\{mode.upper()}_{param}_{figfilename}.svg', dpi=1200)
        plt.show()
       
    return
    
def besplotmare(df, overallmax, figtitle, baseline, mode, risco, leg_position=None):
    # overallmax['Fósforo total'] = 0.5
    if len(df) == 0:
        print('hdhfkfngkjnbgbgb')
        return {'error': 'empty dataframe'}
    tides = list(df.keys())
    # ind = tides.index('sem_mare')
    # tides.pop(ind)
    allparams = set([])
    for tide in tides:
       
        params = list(df[tide].keys())
        for j in range(len(params)):
            allparams.add(params[j])
    
    markers = ['o', '^', '*', 's', 'D', 'v', 'X', 'h', 'p', 'x']
    # colors= ['tab:orange', 'gray', 'k', 'r', 'brown', 'lime', 'blue', 'm', 'c', 'deeppink', 'y']
    marker = {}
    for i in range(len(tides)):
        # print(len(tides), len(markers))
        marker[tides[i]] = markers[i]
    
    for param in allparams:
        ylabel = ''
        allxlabels = []
        figsize = (9, 4.5)
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
                
                # paramdf = replace_as_lastcols(paramdf, ('VMP', 'Unidade'))
                
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
                allxlabels.append(xlabels)
                # dff = paramdf[cols2].sort_values(by='Data', ascending=True)
                for i in range(len(paramdf)):
                    # if tide == 'mare_alta':
                    #     color = 'tab:orange'
                    # if tide == 'mare_vazante':
                    #     color = 'gray'
                    # ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], marker=marker[tide], s=30, color=color)
                    # if i == len(paramdf) - 1:
                        # ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], marker=marker[tide], s=30, label=tide, color=color)

                    ax.scatter(cols2[1:], paramdf.loc[i, cols2[1:]], marker=marker[tide], s=30,  label=f"{paramdf.loc[i, 'Data'].month}-{paramdf.loc[i, 'Data'].year} {tide}") 
        
                # print('HEYHEYEHEYEHEY')
        # sortedpoints = sort_bespts(allxlabels)
        try:
            vmp_col.loc[0] > 0
            ax.axhline(vmp_col.loc[0],  label='VMP', linewidth=1., linestyle='dashed', color='r')
        except:
            if param == 'pH':
                try:
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=1., color='r')
                    ax.axhline(supflim, linewidth=1., color='r')
                except:
                    pass
            pass
        ax.axhline(baseline[param],  label='Baseline/background (max)', linewidth=1., linestyle='dashed', color='k')
        plt.title(f'{param} - {figtitle}', fontsize=9)
        plt.xlabel('Pontos', fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
        y0, ymax = plt.ylim()
        print(param)
        print(ymax)
        ywidth = ymax - y0
        yloc = ywidth * 0.8
        if param == 'Sólidos dissolvidos totais':
            yloc = ywidth * 0.5

        lcolor = 'lightgrey'
        
        if mode == 'sup':
            plt.text(19, yloc, 'Murucupi', fontsize=8, color='k')
            plt.text(6, yloc, 'Pará', fontsize=8, color='k')
            plt.axvline(16, y0, ymax, color=lcolor, linewidth=1.)
        if mode == 'sed':
            plt.text(17, yloc, 'Murucupi', fontsize=8, color='k')
            plt.text(6, yloc, 'Pará', fontsize=8, color='k')
            plt.axvline(16, y0, ymax, color=lcolor, linewidth=1.)

        if len(xlabels) > 10:
            plt.xticks(rotation=90)
        
        try:
            if param != 'pH':
                if overallmax[param] > vmp:
                    plt.ylim(0., overallmax[param] * 1.05)
            if param == 'pH':
                ph = vmp_col.loc[0].split(' ')[-1]
                if overallmax[param] > int(ph):
                    plt.ylim(0., overallmax[param] * 1.05)
        except TypeError:
            plt.ylim(0., overallmax[param] * 1.05)
       

        
        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        # sort both labels and handles by labels

        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        # asd
        leg = ax.legend(handles, labels, fontsize=6, framealpha=0.4, ncol=4, loc='upper left')
        leg.get_frame().set_linewidth(0.0)
        # ax.legend(loc='best', fontsize=7, frameon=False)
        # plt.tight_layout(rect=(0, 0.1, 1, 1))
        plt.tight_layout()
        plt.savefig(f'graphs\{risco}\Arcadis\{mode.upper()}_{param}_BES_por_mares.svg')
        plt.show()
    
    return


def besplotall(df, overallmax, figtitle, baseline, mode, risco, leg_position=None):
    # overallmax['Fósforo total'] = 0.5
    
    if len(df) == 0:
        return {'error': 'empty dataframe'}
    
    params = list(df.keys())
   
    for param in params:
        ylabel = ''
        xlabels = []
        figsize = (10, 5)
        # fig, ax = plt.subplots()
        fig, ax = plt.subplots(figsize=figsize)
        plt.grid(axis = 'y', linewidth=0.1)

        paramdf = df[param]
        
        vmp_col = paramdf['VMP']
        vmp = vmp_col.max()
        paramdf_cols = list(paramdf.columns)
        pop_ind = paramdf_cols.index('VMP')
        paramdf_cols.pop(pop_ind)
        paramdf = paramdf[paramdf_cols] 
        cols2 = paramdf.columns.tolist()
        unit = cols2.pop()
        # print(unit)
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
                    inflim = float(vmp_col.loc[0].split(' ')[0])
                    supflim = float(vmp_col.loc[0].split(' ')[-1])
                    ax.axhline(inflim,  label='VMP', linewidth=1., color='r')
                    ax.axhline(supflim, linewidth=1., color='r')
                except:
                    pass
            pass
        ax.axhline(baseline[param],  label='Baseline/background (max)', linewidth=1., linestyle='dashed', color='k')
        plt.title(f'{param} - {figtitle}', fontsize=9)
        plt.xlabel('Pontos', fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
        y0, ymax = plt.ylim()
        ywidth = ymax - y0
        yloc = ywidth*0.60
        yloc2 = ywidth*0.40
        yloc3 = ywidth*0.30
        yloc4 = ywidth*0.35
        yloc5 = ywidth*0.20
        lcolor = 'lightgrey'
        line = 1.
        if mode == 'sup':
            plt.text(8, yloc, 'Barcarena', fontsize=8, color='k')
            plt.text(24, yloc, 'Murucupi', fontsize=8, color='k')
            plt.text(33, yloc, 'Dendê', fontsize=8, color='k')
            plt.text(45, yloc, 'Pará', fontsize=8, color='k')
            plt.axvline(21, y0, ymax, color=lcolor, linewidth=line)
            plt.axvline(31, y0, ymax, color=lcolor, linewidth=line)
            plt.axvline(38, y0, ymax, color=lcolor, linewidth=line)
        
            plt.text(3, yloc2, 'Tauá', fontsize=6, color=lcolor)
            plt.text(6, yloc3, 'Pramajó', fontsize=6, color=lcolor)
            plt.text(8, yloc4, 'Pramajozinho', fontsize=6, color=lcolor)
            plt.text(10, yloc5, 'Pramajó', fontsize=6, color=lcolor)
            plt.text(11, yloc2, 'Tauá', fontsize=6, color=lcolor)
            plt.text(15, yloc3, 'Água Verde', fontsize=6, color=lcolor)
            plt.axvline(3, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(6, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(8, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(10, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(11, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(15, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
        if mode == 'sed':
            plt.text(6, yloc, 'Barcarena', fontsize=8, color='k')
            plt.text(15, yloc, 'Murucupi', fontsize=8, color='k')
            plt.text(21, yloc, 'Dendê', fontsize=8, color='k')
            plt.text(30, yloc, 'Pará', fontsize=8, color='k')
            plt.axvline(14, y0, ymax, color=lcolor, linewidth=line)
            plt.axvline(20, y0, ymax, color=lcolor, linewidth=line)
            plt.axvline(23, y0, ymax, color=lcolor, linewidth=line)
        
            plt.text(2, yloc2, 'Tauá', fontsize=6, color=lcolor)
            plt.text(3, yloc3, 'Pramajó', fontsize=6, color=lcolor)
            plt.text(6, yloc4, 'Pramajozinho', fontsize=6, color=lcolor)
            plt.text(7, yloc2, 'Tauá', fontsize=6, color=lcolor)
            plt.text(9, yloc3, 'Água Verde', fontsize=6, color=lcolor)
            plt.axvline(2, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(3, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(6, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(7, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(9, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            plt.axvline(11, y0, ymax, linestyle='dashed', color=lcolor, linewidth=0.5)
            

        # plt.xticks(fontsize=9)
        # plt.yticks(fontsize=9)
            
        if len(xlabels) > 10:
            plt.xticks(rotation=90)
        try:
            if param != 'pH':
                if overallmax[param] > vmp:
                    plt.ylim(0., overallmax[param] * 1.05)
            if param == 'pH':
                ph = vmp_col.loc[0].split(' ')[-1]
                if overallmax[param] > int(ph):
                    plt.ylim(0., overallmax[param] * 1.05)
        except TypeError:
            plt.ylim(0., overallmax[param] * 1.05)
        
        ax.tick_params(axis='both', which='major', labelsize=8)
        handles, labels = ax.get_legend_handles_labels()
        # sort both labels and handles by labels
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        leg = ax.legend(handles, labels, fontsize=7, framealpha=0.4,
                         loc='upper left', ncol=4)
        leg.get_frame().set_linewidth(0.0)
        # ax.legend(loc='best', fontsize=7, frameon=False)
        # ax.set_xticklabels(xlabels, fontsize=8)
        
        plt.tight_layout()
        # plt.tight_layout(rect=(0, 0.1, 1, 1))
        plt.savefig(f'graphs\{risco}\Arcadis\{mode.upper()}_{param}_BES_media_entre_mares.svg')
        plt.show()
    
    return


            




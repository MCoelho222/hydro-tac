import pandas as pd
from src.app.estudosvoluntarios import estudosvolun
from src.app.hydro import hydroalunorte
from src.app.utils.graphs import voluntariosplot, hydroplots


if __name__ == "__main__":

    
    # ASUP
    df = pd.read_excel('data/estudos_vonluntarios_agua_superficial_revc.xlsx', sheet_name='Água Superficial')
    # SED
    # df = pd.read_excel('data/estudos_voluntarios_sedimento_REVC.xlsx', sheet_name='Sedimento')

    # df = pd.read_excel('data/BD_hydro_rev120_22-07-2022.xlsm', sheet_name='Versão 120_GS')
    
    cols_volun = ['Empresa responsável', 'Local', 'Ponto', 'Data da coleta', 'Maré', 'Parâmetros', 'Resultado', 'Unidade', 'VMP', 'Legislação']

    # murucupi = ['Rio Murucupi', 'Pontos de amostragem proximos a Bacia do Rio Murucupi', 'Igarapé Murucupi - Braço Superior Oeste (Entre a Refinaria e o DRS-1)', 'Igarapé Murucupi - Unificação dos Braços', 'Rio Igarapé Murucupi']
    murucupi = ['Rio Murucupi']
    
    para = ['Rio Pará',]
    # para = ['Rio Pará', 'Qualidade Hídrica - Rio Pará a Montante', 'Rio Pará e dos Efluentes da Alunorte', 'rio Pará a jusante', 'rio Pará a montante', 'Rio Pará - Litoral Sul - Oeste/Noroete da Refinaria', 'Rio Pará - Litoral Sul']

    pramajo = ['Igarapé Pramajó',]
    # pramajo = ['Igarapé Pramajó', 'Igarapé Pramajó  - Área Background, Fora da Influência das Operações Industriais da HYDRO ALUNORTE', 'Rio Igarapé Pramajó']

    pramajozinho = ['Igarapé Pramajozinho',]
    # pramajozinho = ['Igarapé Pramajozinho', 'Igarapé Pramajozinho - Sul do DRS-1', 'Igarapés  Pramajozinho - Sul do DRS-1', 'Igarapé Pramajozinho']

    taua = ['Igarapé Tauá',]
    # taua = ['Igarapé Tauá', 'Igarapé Tauá - Braço Superior Sul - Área Background, Fora da Influência das Operações Industriais da HYDRO ALUNORTE', 'Igarapé Tauá - Unificação dos Braços - Sudeste do DRS-2', 'Igarapé Tauá - Braço Sul - Área Background', 'Igarapé Tauá - Braço Norte - Sul do DRS-2', 'Rio  Igarapé Tauá', 'Igarapé Tauá (próximo a foz)', 'Igarapé Tauá (a jusante do Pramajó)']

    aguaverde = ['Igarapé Água Verde',]
    # aguaverde = ['Igarapé Água Verde', 'Igarapé Água Verde - Norte do DRS-2', 'Rio Igarapé Água Verde']
    
    # barcarena = ['Rio Barcarena até Furo do Arrozal', 'Rio Barcarena', 'Ponto rio  Barcarena', 'Barcarena']

    allrivers_names = [murucupi, para, pramajo, pramajozinho, taua, aguaverde]
    allrivers = []
    for i in range(len(allrivers_names)):
        for j in range(len(allrivers_names[i])):
            allrivers.append(allrivers_names[i][j])
    
    rivers_name = {'murucupi': murucupi, 'para': para, 'pramajo': pramajo, 'pramajozinho': pramajozinho, 'taua': taua, 'aguaverde': aguaverde}
   
    
    ts_dict = {'site': ('Ponto', ()), 'date': ('Data da coleta', ()), 'result': ('Resultado', ()), 'unit': ('Unidade', ()), 'tide': ('Maré', {'Geoklock': ('Cheia', 'Vazante', 'sem_info_mare'), 'Enviro-Tec': ('Sem maré', 'Maré'), 'SGW': ('Enchente', 'Vazante', 'Sem maré')}), 'sample': ('Amostra', (1,))}

    # rivername = 'murucupi'

   
    positions = {'taua': 'best', 'murucupi': 'best', 'pramajo': 'best', 'pramajozinho': 'best', 'aguaverde': 'best', 'para': 'best'}
   
    
    figtitles = ['Rio Murucupi', 'Rio Pará', 'Igarapé Tauá', 'Igarapé Pramajó', 'Igarapé Pramajozinho', 'Igarapé Água Verde']
    
    sed_risk_params = {'risk13': ('Alumínio', 'Ferro'), 'risk07': ('Arsênio', 'Alumínio', 'Ferro', 'Cromo', 'Chumbo', 'Fósforo', 'Bário', 'Vanádio', 'Silício', 'Cobalto', 'Mercúrio', 'Manganês', 'Sódio', 'Sulfato', 'Zinco')}
    
    sup_risk_params = {'risk12': ('Fósforo total', 'Sulfato total', 'Enxofre'), 'risk17': ('Sulfato total', 'Sódio total', 'pH'), 'risk13': ('Alumínio dissolvido', 'Ferro dissolvido', 'Sólidos dissolvidos totais'), 'risk07': ('Sólidos dissolvidos totais', 'Coliformes Termotolerantes', 'pH', 'DBO', 'OD', 'Óleos e Graxas', 'Fósforo total', 'Bário total', 'Cromo total', 'Vanádio total', 'Zinco total', 'Arsênio total', 'Manganês total', 'Chumbo total', 'Ferro dissolvido', 'Alumínio dissolvido', 'Mercúrio total', 'Sódio total', 'Sulfato total')} # 'Sílica total'

    sup_baseline = {'risk13': {'Alumínio dissolvido': 0.21, 'Ferro dissolvido': 0.47, 'Sólidos dissolvidos totais': 123}, 'risk17': {'Sulfato': 3.09, 'Sódio total': 4.9, 'pH': 5.22}, 'risk12': {'Fósforo total': 0.06, 'Sulfato': 3.09}, 'risk07': {'Sólidos dissolvidos totais': 123, 'Alumínio dissolvido': 0.21, 'Ferro dissolvido': 0.47, 'Sulfato total': 3.09, 'Sódio total': 4.9, 'pH': 5.8, 'Coliformes Termotolerantes': 160, 'DBO': 3.44, 'OD': 4.9, 'Óleos e Graxas': 0.0, 'Fósforo total': 0.03, 'Bário total': 0.03, 'Vanádio total': 0.01, 'Zinco total': 0.08, 'Arsênio total': 0.066, 'Manganês total': 0.04, 'Chumbo total': 0.02, 'Mercúrio total': 0.0002, 'Cromo total': 0.05}}
    
    sed_baseline = {'risk13': {'Alumínio': {'max': 20217, 'med': 3389}, 'Ferro': {'max': 21622, 'med': 7488}}, 'risk07': {'Arsênio': {'max': 4.64, 'med': 1.39}, 'Alumínio': {'max': 20217, 'med': 3389}, 'Ferro': {'max': 21622, 'med': 7488}, 'Chumbo': {'max': 6.01, 'med': 3.06}, 'Fósforo': {'max': 313, 'med': 55}, 'Bário': {'max': 69.8, 'med': 9.27}, 'Vanádio': {'max': 93.3, 'med': 18.2}, 'Mercúrio': {'max': 0.08, 'med': 0.04}, 'Manganês': {'max': 1796, 'med': 63.4}, 'Sódio': {'max': 126, 'med': 73.7}, 'Sulfato': {'max': 6.650, 'med': 2.3}, 'Zinco': {'max': 27.1, 'med': 13.3}, 'Cromo': {'max':28.1, 'med': 9.98}, 'Cobalto': {'max':3.84, 'med': 1.54}, 'Sílica': {'max':8.7, 'med': 4.37}}}
    
    rivers = ['murucupi', 'para', 'taua', 'pramajo', 'pramajozinho', 'aguaverde']
    # rivers = ['murucupi',]
    # owners = ['Enviro-Tec',]
    owners = ['Geoklock', 'Enviro-Tec', 'SGW']
    risk_title = 'RISCO_13'
    # risk_title = 'TESTE'
    mode = 'sup'
    sup_risk = sup_risk_params['risk13']
    
    sed_risk = sed_risk_params['risk13']
    
    
        
    # for j in range(len(owners)):

    # str_filter_dict = {'param': ('Parâmetros', sup_risk), 'site': ('Local', figtitles), 'owner': ('Empresa responsável', ('Enviro-Tec',))}

    # val_filter_dict = {'Resultado': ('positive', 'nan')}

    # ts_df = estudosvolun(risk_title, 'resume', df, cols_volun, str_filter_dict, allrivers, owners, mode, val_filters=val_filter_dict, ts=ts_dict)
    # if len(ts_df['dataframes']) > 0:
    #     voluntariosplot(ts_df['dataframes'], ts_df['overallmax'], 'águas superficiais', risk_title, sup_baseline['risk17'], mode, 'best')
    
    
    
    for i in range(len(rivers)):
        
        for j in range(len(owners)):

            str_filter_dict = {'param': ('Parâmetros', sup_risk), 'site': ('Local', rivers_name[rivers[i]]), 'owner': ('Empresa responsável', (owners[j],))}

            val_filter_dict = {'Resultado': ('positive', 'nan')}
        
            ts_df = estudosvolun(risk_title, rivers[i], df, cols_volun, str_filter_dict, allrivers, owners, mode, val_filters=val_filter_dict, ts=ts_dict)
            if len(ts_df['dataframes']) > 0:
                voluntariosplot(ts_df['dataframes'], ts_df['overallmax'], figtitles[i], risk_title, sup_baseline['risk13'], mode, positions[rivers[i]])
   

    # cols_hydro = ['Código do ponto', 'Local', 'Data Coleta', 'Parâmetro', 'Valor', 'Unidade', 'VMP']
    # rivers = ('Rio Murucupi', 'Rio Pará', 'Igarapé Tauá', 'Igarapé Pramajozinho', 'Igarapé Água Verde')
    # ts_dict = {'site': ('Código do ponto', ()), 'date': ('Data Coleta', ()), 'result': ('Valor', ()), 'unit': ('Unidade', ())}
    # str_filter_dict = {'param': ('Parâmetro', sup_risk), 'river': ('Local', rivers)}
    # val_filter_dict = {'Valor': ('positive', 'nan')}

    # dfs = hydroalunorte(risk_title, df, cols_hydro, str_filter_dict, mode, val_filters=val_filter_dict, ts=ts_dict)
    # print(dfs)
    # hydroplots(dfs['dataframes']['perparam'], dfs['overallmax'], 'monit_cont', 'monitoramento contínuo', risk_title, sup_baseline['risk13'], mode, leg_position='best')
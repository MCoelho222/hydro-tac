import pandas as pd
from src.app.estudosvoluntarios import estudosvolun
from src.app.hydro import hydroalunorte
from src.app.utils.graphs import voluntariosplot, hydroplots


if __name__ == "__main__":
    
    # df = pd.read_excel('estudos_vonluntarios_agua superficial_reva_original.xlsx', sheet_name='agua_sup')
    df = pd.read_excel('BD_hydro_rev120_22-07-2022.xlsm', sheet_name='Versão 120_GS')
    
    cols_volun = ['Empresa responsável', 'Local', 'Matriz', 'Ponto', 'Amostra', 'Data da coleta', 'Maré', 'Parâmetros', 'Resultado', 'Unidade', 'VMP', 'Legislação']

    murucupi = ['Rio Murucupi', 'Pontos de amostragem proximos a Bacia do Rio Murucupi', 'Igarapé Murucupi - Braço Superior Oeste (Entre a Refinaria e o DRS-1)', 'Igarapé Murucupi - Unificação dos Braços', 'Rio Igarapé Murucupi']
    
    para = ['Rio Pará', 'Qualidade Hídrica - Rio Pará a Montante', 'Rio Pará e dos Efluentes da Alunorte', 'rio Pará a jusante', 'rio Pará a montante', 'Rio Pará - Litoral Sul - Oeste/Noroete da Refinaria', 'Rio Pará - Litoral Sul']

    pramajo = ['Igarapé Pramajó  - Área Background, Fora da Influência das Operações Industriais da HYDRO ALUNORTE', 'Rio Igarapé Pramajó']

    pramajozinho = ['Igarapé Pramajozinho', 'Igarapé Pramajozinho - Sul do DRS-1', 'Igarapés  Pramajozinho - Sul do DRS-1', 'Igarapé Pramajozinho']

    taua = ['Igarapé Tauá', 'Igarapé Tauá - Braço Superior Sul - Área Background, Fora da Influência das Operações Industriais da HYDRO ALUNORTE', 'Igarapé Tauá - Unificação dos Braços - Sudeste do DRS-2', 'Igarapé Tauá - Braço Sul - Área Background', 'Igarapé Tauá - Braço Norte - Sul do DRS-2', 'Rio  Igarapé Tauá', 'Igarapé Tauá (próximo a foz)', 'Igarapé Tauá (a jusante do Pramajó)']

    aguaverde = ['Igarapé Água Verde - Norte do DRS-2', 'Rio Igarapé Água Verde']
    
    barcarena = ['Rio Barcarena até Furo do Arrozal', 'Rio Barcarena', 'Ponto rio  Barcarena', 'Barcarena']

    allrivers_names = [murucupi, para, pramajo, pramajozinho, taua, aguaverde, barcarena]
    allrivers = []
    for i in range(len(allrivers_names)):
        for j in range(len(allrivers_names[i])):
            allrivers.append(allrivers_names[i][j])
    
    rivers_name = {'murucupi': murucupi, 'para': para, 'pramajo': pramajo, 'pramajozinho': pramajozinho, 'taua': taua, 'aguaverde': aguaverde, 'barcarena': barcarena}
   
    
    # ts_dict = {'site': ('Ponto', ()), 'date': ('Data da coleta', ()), 'result': ('Resultado', ()), 'unit': ('Unidade', ()), 'tide': ('Maré', {'Geoklock': ('Cheia', 'Vazante'), 'Enviro-Tec': ('Sem maré', 'Maré'), 'SGW': ('Enchente', 'Vazante', 'Sem maré')}), 'sample': ('Amostra', (1,))}

    rivername = 'murucupi'

   
    positions = {'taua': 'upper right', 'murucupi': 'best', 'pramajo': 'upper right', 'pramajozinho': 'upper right', 'aguaverde': 'upper right', 'para': 'upper left'}
   
    
    figtitles = ['Rio Murucupi', 'Rio Pará', 'Igarapé Tauá', 'Igarapé Pramajó', 'Igarapé Pramajozinho', 'Igarapé Água Verde']
    risk_params = {'risk12': ('Fósforo Total', 'Sulfato', 'Enxofre'), 'risk17': ('Sulfato', 'Sódio', 'Sódio Total', 'pH')}
    # rivers = ['murucupi', 'para', 'taua', 'pramajo', 'pramajozinho', 'aguaverde']
    owners = ['Geoklock', 'Enviro-Tec', 'SGW']
    risk_title = 'RISCO_12'
    
    risk = risk_params['risk12']
    
    # for i in range(len(rivers)):
        
    #     for j in range(len(owners)):

    #         str_filter_dict = {'param': ('Parâmetros', risk), 'site': ('Local', rivers_name[rivers[i]]), 'owner': ('Empresa responsável', (owners[j],))}

    #         val_filter_dict = {'Resultado': ('positive', 'nan')}
        
    #         ts_df = estudosvolun(risk_title, rivers[i], df, cols_volun, str_filter_dict, allrivers, val_filters=val_filter_dict, ts=ts_dict)
    #         # print(ts_df['overallmax'])
    #         # print(ts_df['ownermax'])
    #         if len(ts_df['dataframes']) > 0:
    #             voluntariosplot(ts_df['dataframes'], ts_df['overallmax'], figtitles[i], risk_title, positions[rivers[i]])
   

    cols_hydro = ['Código do ponto', 'Local', 'Data Coleta', 'Parâmetro', 'Valor', 'Unidade', 'VMP']
    rivers = ('Rio Murucupi', 'Rio Pará', 'Igarapé Tauá', 'Igarapé Pramajozinho', 'Igarapé Água Verde')
    ts_dict = {'site': ('Código do ponto', ()), 'date': ('Data Coleta', ()), 'result': ('Valor', ()), 'unit': ('Unidade', ())}
    str_filter_dict = {'param': ('Parâmetro', risk), 'river': ('Local', rivers)}
    val_filter_dict = {'Valor': ('positive', 'nan')}

    dfs = hydroalunorte(risk_title, df, cols_hydro, str_filter_dict, val_filters=val_filter_dict, ts=ts_dict)

    hydroplots(dfs['dataframes']['perparam'], dfs['overallmax'], 'monit_cont', 'monitoramento contínuo', risk_title, 'best')
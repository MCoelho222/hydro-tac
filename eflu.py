from src.app.estudosvoluntarios import estudosvolun
from src.app.utils.graphs import hydroplots
from src.app.hydro import hydroalunorte
from src.app.alleflus import eflu_etei
from src.app.utils.graphs import efluplot
from src.app.beseflu import read_beseflu

import pandas as pd

if __name__ == "__main__":

    volundf = pd.read_excel('estudos_voluntarios_efluentes_REVC.xlsx', sheet_name='Efluente')
    # hydrodf = pd.read_excel('data/BD_hydro_rev120_22-07-2022.xlsm', sheet_name='Versão 120_GS')
    # besdf = pd.read_excel('data/Anexo II - Resultados analíticos gerais - efluentes.xlsx', sheet_name='Sheet1')
    volunpts = ['ETE-01','ETEI-01']
    hydropts = ['Canal de Lançamento', 'Calha Parshall', 'ETE-1', '82C-2ABC']
    voluncols = ['Ponto', 'Data da coleta', 'Parâmetros', 'Resultado', 'Unidade', 'VMP']
    hydrocols = ['Código do ponto', 'Data Coleta', 'Parâmetro', 'Valor', 'Unidade', 'VMP']
    hydro_eflu_risk_params = {'risk6': ('Sólidos dissolvidos totais', 'Óleos e Graxas Total', 'Óleos e Graxas Mineral', 'Óleos Vegetais e Gorduras Animais ','Temperatura', 'Sólidos Sedimentáveis', 'pH', 'DBO', 'OD', 'Sulfato')}
    volun_eflu_risk_params = {'risk6': ('Sólidos dissolvidos totais', 'Óleo Mineral', 'Óleo Vegetal e Animal', 'Temperatura', 'Sólidos sedimentáveis', 'pH', 'DBO', 'OD', 'Sulfato')}
    mode = 'eflu'
    risk = 'RISCO_06'
    volun_renames = {'ETE-01': 'ETE-01 (sanit. bruto)' ,'ETEI-01': 'ETEI-01 (efl. tratado)'}
    hydro_renames = {'Canal de Lançamento': 'Canal Lançamento (efl. tratado)', 'Calha Parshall': 'C. Parshall (efl. tratado)', 'ETE-1': 'ETE-1 (efl. sanit. bruto)', '82C-2ABC': '82C-2ABC (efl. ind. bruto)'}
    # ylims = {'Sólidos dissolvidos totais': 1, 'óleos e graxas':1 , 'Temperatura':1 , 'Sólidos sedimentáveis':1 , 'pH':1 , 'DBO': 1, 'OD': 1}
    
    volunplot = eflu_etei(volundf, voluncols, volun_eflu_risk_params['risk6'], volunpts, risk, mode, 'estudos_voluntarios', volun_renames)
    
    # hydroplot = eflu_etei(hydrodf, hydrocols, hydro_eflu_risk_params['risk6'], hydropts, risk, mode, 'hydro', renames=hydro_renames)
    
    efluplot(volunplot, 'Efluentes', mode, risk, owner='estudos_voluntarios')
    # efluplot(hydroplot, 'Efluentes', mode, risk, 'boxplot', owner='hydro', leg_position='best')



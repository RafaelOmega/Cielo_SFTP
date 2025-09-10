import pandas as pd
from IPython.display import display
from .RegistroBase import RegistroBase


class Registro0(RegistroBase):
    def __init__(self):
        super().__init__("0")

    def processar_linha(self, linha, mostrar=True):
        dados = {
            "tipo_registro": linha[0:1].strip(),
            "estabelecimento_matriz": linha[1:11].strip(),
            "data_processamento": self.formatar_data(linha[11:19].strip()),
            "periodo_inicial": self.formatar_data(linha[19:27].strip()),
            "periodo_final": self.formatar_data(linha[27:35].strip()),
            "sequencia": linha[35:42].strip(),
            # "empresa_adquirente": linha[42:47].strip(),
            "opcao_extrato": linha[47:49].strip(),
            "transmissao": linha[49:50].strip(),
            # "caixa_postal": linha[50:70].strip(),
            "versao_layout": linha[70:73].strip(),
            # "uso_cielo": linha[73:250].strip(),
        }

        df_registro_0 = pd.DataFrame([dados])

        if mostrar:
            display(df_registro_0)

        return df_registro_0

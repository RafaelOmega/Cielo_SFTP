import pandas as pd
from IPython.display import display
from .RegistroBase import RegistroBase


class RegistroC(RegistroBase):
    def __init__(self):
        super().__init__("C")

    def processar_linha(self, linha, mostrar=True):
        dados = {
            "tipo_registro": linha[0:1].strip(),
            "banco": linha[1:5].strip(),
            "agencia": linha[5:10].strip(),
            "conta": linha[10:30].strip(),
            "sinal_valor_depositado": linha[30:31].strip(),
            "valor_depositado": self.formatar_valor(linha[31:44]),
            "uso_cielo": linha[44:250].strip(),
        }

        df_registro_C = pd.DataFrame([dados])

        if mostrar:
            display(df_registro_C)

        return df_registro_C

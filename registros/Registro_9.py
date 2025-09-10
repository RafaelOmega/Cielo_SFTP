import pandas as pd
from IPython.display import display
from .RegistroBase import RegistroBase


class Registro9(RegistroBase):
    def __init__(self):
        super().__init__("9")

    def processar_linha(self, linha, mostrar=True):
        dados = {
            # Identificação básica
            "tipo_registro": linha[0:1].strip(),
            "total_registros": self.formatar_inteiro(linha[1:12]),
            "sinal_valor_liquido": linha[12:13].strip(),
            "valor_liquido_soma_registros": self.formatar_valor(linha[13:30]),
            "quantidade_total_registros_tipo_E": self.formatar_inteiro(linha[30:41]),
            "sinal_valor_bruto_soma_registros": linha[41:42].strip(),
            "valor_bruto_soma_registros": self.formatar_valor(linha[42:59]),
            "sinal_valor_liquido_valores_cedidos_negociacao": linha[59:60].strip(),
            "somatoria_valor_liquido_valores_cedidos_negociacao": self.formatar_valor(linha[60:77]),
            "sinal_valor_liquido_valores_dados_garantia_gravames": linha[77:78].strip(),
            "somatoria_valor_liquido_valores_dados_garantia_gravames": self.formatar_valor(linha[78:95]),
            "uso_cielo": linha[95:250].strip(),
        }

        df_registro_9 = pd.DataFrame([dados])

        if mostrar:
            display(df_registro_9)

        return df_registro_9

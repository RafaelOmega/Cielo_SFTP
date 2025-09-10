import pandas as pd
from IPython.display import display
from .RegistroBase import RegistroBase


class RegistroA(RegistroBase):
    def __init__(self):
        super().__init__("A")

    def processar_linha(self, linha, mostrar=True):
        dados = {
            "tipo_registro": linha[0:1].strip(),
            "data_negociacao": self.formatar_data_compacta(linha[1:7]),
            "data_pagamento": self.formatar_data_compacta(linha[7:13]),
            "cpf_cnpj": self.formatar_cpf_cnpj(linha[13:27]),
            "prazo_medio": linha[27:30].strip(),
            "taxa_nominal": self.formatar_taxa(linha[30:35]),
            "sinal_valor_bruto": linha[35:36].strip(),
            "valor_bruto": self.formatar_valor(linha[36:49]),
            "sinal_valor_liquido": linha[49:50].strip(),
            "valor_liquido": self.formatar_valor(linha[50:63]),
            "numero_negociacao_registradora": linha[63:83].strip(),
            "forma_pagamento": linha[83:86].strip(),
            "taxa_efetiva_negociacao": self.formatar_taxa(linha[86:91]),
            "uso_cielo": linha[91:250].strip(),
        }

        df_registro_A = pd.DataFrame([dados])

        if mostrar:
            display(df_registro_A)

        return df_registro_A

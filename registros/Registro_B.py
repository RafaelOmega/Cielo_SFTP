import pandas as pd
from IPython.display import display
from .RegistroBase import RegistroBase


class RegistroB(RegistroBase):
    def __init__(self):
        super().__init__("B")

    def processar_linha(self, linha, mostrar=True):
        dados = {
            "tipo_registro": linha[0:1].strip(),
            "data_negociacao": self.formatar_data_compacta(linha[1:7]),
            "data_vencimento_original": self.formatar_data_compacta(linha[7:13]),
            "cpf_cnpj": linha[13:27].strip(),
            "bandeira": linha[27:30].strip(),
            "tipo_liquidacao": linha[30:33].strip(),
            "sinal_valor_bruto": linha[33:34].strip(),
            "valor_bruto": self.formatar_valor(linha[34:47]),
            "sinal_valor_liquido": linha[47:48].strip(),
            "valor_liquido": self.formatar_valor(linha[48:61]),
            "taxa_efetiva": self.formatar_taxa(linha[61:66]),
            "instituicao_financeira": linha[66:116].strip(),
            "numero_estabelecimento": linha[116:126].strip(),
            "sinal_valor_desconto": linha[126:127].strip(),
            "valor_desconto": self.formatar_valor(linha[127:140]),
            "uso_cielo": linha[140:250].strip(),
        }

        df_registro_B = pd.DataFrame([dados])

        if mostrar:
            display(df_registro_B)

        return df_registro_B

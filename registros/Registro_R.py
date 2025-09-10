from .RegistroBase import RegistroBase


class RegistroR(RegistroBase):
    def __init__(self):
        super().__init__("R")

    def processar_linha(self, linha):
        return {
            "tipo_registro": linha[0:1].strip(),
            "estabelecimento_submissor": linha[1:11].strip(),
            "cpf_cnpj_titular_movimento": linha[11:25].strip(),
            "bandeira": linha[25:28].strip(),
            "matriz_pagamento": linha[28:38].strip(),
            "sinal_valor_reserva": linha[38:39].strip(),
            "valor_reserva": self.formatar_valor(linha[39:52]),
            "chave_ur": linha[52:152].strip(),
            "data_vencimento_original": self.formatar_data(linha[152:160]),
            "numero_estabelecimento_pagamento": linha[160:170].strip(),
            "uso_cielo": linha[170:222].strip(),
        }

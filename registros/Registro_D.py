import pandas as pd
from IPython.display import display
from .RegistroBase import RegistroBase


class RegistroD(RegistroBase):
    def __init__(self):
        super().__init__("D")

    def processar_linha(self, linha, mostrar=True):
        dados = {
            "tipo_registro": linha[0:1].strip(),
            "estabelecimento_submissor": linha[1:11].strip(),
            # "cpf_cnpj_titular": self.formatar_cpf_cnpj(linha[11:25]),
            # "cpf_cnpj_titular_movimento": self.formatar_cpf_cnpj(linha[25:39]),
            # "cpf_cnpj_recebedor": self.formatar_cpf_cnpj(linha[39:53]),
            "bandeira": self.formatar_bandeira(linha[53:56]),
            "tipo_liquidacao": self.forma_pgto(linha[56:59]),
            # "matriz_pagamento": linha[59:69].strip(),
            "status_pagamento": self.status_pagamento(linha[69:71]),
            # "sinal_valor_bruto": linha[71:72].strip(),
            "valor_bruto": self.formatar_valor(linha[72:85]),
            # "sinal_taxa_administrativa": linha[85:86].strip(),
            "valor_taxa_administrativa": self.formatar_valor(linha[86:99]),
            # "sinal_valor_liquido": linha[99:100].strip(),
            "valor_liquido": self.formatar_valor(linha[100:113]),
            "banco": linha[113:117].strip(),
            "agencia": linha[117:122].strip(),
            "conta": linha[122:142].strip(),
            "digito_conta": linha[142:143].strip(),
            "quantidade_lancamentos_ur": self.formatar_inteiro(linha[143:149]),
            "tipo_lancamento": self.tipo_lancamento(linha[149:151]),
            "chave_ur": linha[151:251].strip(),
            "tipo_lancamento_original": self.tipo_lancamento(linha[251:253]),
            "tipo_antecipacao": self.tipo_antecipacao(linha[253:254]),
            "numero_antecipacao": linha[254:263].strip(),
            "taxa_antecipacao": linha[263:267].strip(),
            "data_pagamento": self.formatar_data_br(linha[267:275]),
            "data_envio_banco": self.formatar_data_br(linha[275:283]),
            "data_vencimento_original": self.formatar_data_br(linha[283:291]),
            # "numero_estabelecimento_pgto": linha[291:301].strip(),
            "indicativo_lancamento_pendente": linha[301:302].strip(),
            "indicativo_reenvio_pgto": linha[302:303].strip(),
            "indicativo_negociacao_gravame": linha[303:304].strip(),
            # "cpf_cnpj_negociador": self.formatar_cpf_cnpj(linha[304:318]),
            "indicativo_saldo_aberto": linha[318:319].strip(),
            "uso_cielo": linha[319:400].strip(),
        }

        df_registro_D = pd.DataFrame([dados])

        if mostrar:
            display(df_registro_D)

        return df_registro_D

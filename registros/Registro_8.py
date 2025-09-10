import pandas as pd
from IPython.display import display
from .RegistroBase import RegistroBase


class Registro8(RegistroBase):
    def __init__(self):
        super().__init__("8")

    def processar_linha(self, linha, mostrar=True):
        dados = {
            # Identificação básica
            "tipo_registro": linha[0:1].strip(),
            "estabelecimento_submissor": linha[1:11].strip(),
            "tipo_transacao": linha[11:13].strip(),
            "data_transacao": self.formatar_data(linha[13:19]),
            "hora_transacao": linha[19:25].strip(),
            "id_pix": linha[25:61].strip(),
            "nsu_doc": linha[61:67].strip(),
            "data_pagamento": self.formatar_data(linha[67:73]),
            "sinal_valor_bruto": linha[73:74].strip(),
            "valor_bruto": self.formatar_valor(linha[74:87]),
            "sinal_taxa_administrativa": linha[87:88].strip(),
            "valor_taxa_administrativa": linha[88:101].strip(),
            "sinal_valor_liquido": linha[101:102].strip(),
            "valor_liquido": linha[102:115].strip(),
            "banco": linha[115:119].strip(),
            "agencia": linha[119:124].strip(),
            "conta": linha[124:144].strip(),
            "data_captura_transacao": linha[144:150].strip(),
            "taxa_administrativa": linha[150:155].strip(),
            "tarifa_administrativa": linha[155:159].strip(),
            "canal_venda": linha[159:161].strip(),
            "numero_logico_terminal": linha[161:169].strip(),
            "data_transacao_original": linha[169:175].strip(),
            "hora_transacao_original": linha[175:181].strip(),
            "id_pix_original": linha[181:217].strip(),
            "indicativo_troco_saque": linha[217:219].strip(),
            "origem_ajuste": linha[219:221].strip(),
            "identificador_transferencia_automatica": linha[221:222].strip(),
            "status_transferencia_conta_pagamento": linha[222:224].strip(),
            "data_pagamento_conta_cielo": linha[224:230].strip(),
            "nsu_doc": linha[230:238].strip(),
            "identificador_transferencia_programada": linha[238:239].strip(),
            "tx_id": linha[239:275].strip(),
            "id_recorrencia": linha[275:311].strip(),
            "uso_cielo": linha[311:400].strip(),
        }

        df_registro_8 = pd.DataFrame([dados])

        if mostrar:
            display(df_registro_8)

        return df_registro_8

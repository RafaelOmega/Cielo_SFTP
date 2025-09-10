class RegistroBase:
    """
    Classe base para todos os registros.
    Define a estrutura comum e métodos básicos.
    """

    def __init__(self, tipo_registro):
        """
        Inicializa o registro com o tipo de registro.
        """
        self.tipo_registro = tipo_registro

    @staticmethod
    def formatar_data(data_aaaammdd):
        """
        Converte uma data no formato AAAAMMDD para DD/MM/AAAA.
        """
        if len(data_aaaammdd) == 8 and data_aaaammdd.isdigit():
            ano = data_aaaammdd[:4]
            mes = data_aaaammdd[4:6]
            dia = data_aaaammdd[6:8]
            return f"{dia}/{mes}/{ano}"
        else:
            return data_aaaammdd  # Retorna o valor original se não for uma data válida

    @staticmethod
    def formatar_data_adm(data_aaaaddmm):
        """
        Converte uma data no formato AAAAMMDD para DD/MM/AAAA.
        """
        if len(data_aaaaddmm) == 8 and data_aaaaddmm.isdigit():
            ano = data_aaaaddmm[:4]
            dia = data_aaaaddmm[4:6]
            mes = data_aaaaddmm[6:8]
            return f"{dia}/{mes}/{ano}"
        else:
            return data_aaaaddmm  # Retorna o valor original se não for uma data válida

    @staticmethod
    def formatar_hora(hora_hhmmss):
        """
        Converte uma hora no formato HHMMSS para HH:MM:SS.
        """
        if len(hora_hhmmss) == 6 and hora_hhmmss.isdigit():
            hora = hora_hhmmss[:2]
            minuto = hora_hhmmss[2:4]
            segundo = hora_hhmmss[4:6]
            return f"{hora}:{minuto}:{segundo}"
        else:
            return hora_hhmmss  # Retorna o valor original se não for uma hora válida

    @staticmethod
    def formatar_data_br(data_ddmmaaaa):
        """
        Converte uma data no formato AAAAMMDD para DD/MM/AAAA.
        """
        if len(data_ddmmaaaa) == 8 and data_ddmmaaaa.isdigit():
            dia = data_ddmmaaaa[:2]
            mes = data_ddmmaaaa[2:4]
            ano = data_ddmmaaaa[4:8]
            return f"{dia}/{mes}/{ano}"
        else:
            return data_ddmmaaaa  # Retorna o valor original se não for uma data válida

    @staticmethod
    def formatar_cpf_cnpj(cpf_cnpj):
        """
        Formata um CPF ou CNPJ com base no número de dígitos.
        - Se tiver 11 dígitos, formata como CPF: 000.000.000-00
        - Se tiver 14 dígitos, formata como CNPJ: 00.000.000/0000-00
        - Caso contrário, retorna o valor original.
        """
        cpf_cnpj = cpf_cnpj.strip()  # Remove espaços em branco
        if len(cpf_cnpj) == 11 and cpf_cnpj.isdigit():  # CPF
            return f"{cpf_cnpj[:3]}.{cpf_cnpj[3:6]}.{cpf_cnpj[6:9]}-{cpf_cnpj[9:]}"
        elif len(cpf_cnpj) == 14 and cpf_cnpj.isdigit():  # CNPJ
            return f"{cpf_cnpj[:2]}.{cpf_cnpj[2:5]}.{cpf_cnpj[5:8]}/{cpf_cnpj[8:12]}-{cpf_cnpj[12:]}"
        else:
            return cpf_cnpj  # Retorna o valor original se não for CPF ou CNPJ válido

    @staticmethod
    def formatar_bandeira(codigo_bandeira):
        """
        Formata o código da bandeira para o nome correspondente.
        - 001: Visa
        - 002: MasterCard
        - Outros códigos podem ser adicionados conforme necessário.
        """
        bandeiras = {
            "001": "Visa",
            "002": "Mastercard",
            "003": "Amex",
            "006": "Sorocred",
            "007": "Elo",
            "009": "Diners",
            "011": "Agiplan",
            "015": "Banescard",
            "023": "Cabal",
            "029": "Credsystem",
            "035": "Explanada",
            "040": "Hipercard",
            "060": "JCB",
            "064": "Credz",
            "072": "Hiper",
            "075": "Ourocard",
            "888": "Pix",
        }
        return bandeiras.get(codigo_bandeira.strip(), codigo_bandeira)

    @staticmethod
    def forma_pgto(codigo_forma):
        formas = {
            "000": "não identificado",
            "001": "débito",
            "002": "crédito",
            "003": "parcelado",
            "004": "voucher",
        }
        return formas.get(codigo_forma.strip(), codigo_forma)

    @staticmethod
    def tipo_precificacao(codigo_tipo):
        tipos = {
            "00000": "Não se aplica",
            "00001": "Aluguel",
            "00002": "Cielo Facilita",
            "00003": "Venda",
            "00012": "Dedicado",
            "00021": "TAP White label",
            "00022": "TAP Bradesco",
            "00023": "TAP Banco do Brasil",
            "00024": "Cielo TAP",
            "00026": "Conecta",
            "00032": "Venda pelo WhatsApp",
            "00033": "Link de pagamento",
            "00035": "Checkout",
            "00036": "API E-commerce",
            "00037": "BNDES",
            "00041": "IATA/EDI",
            "00045": "Agro",
            "00046": "Não se aplica"
        }
        return tipos.get(codigo_tipo.strip(), codigo_tipo)

    @staticmethod
    def tipo_antecipacao(codigo_antecipacao):
        antecipacao = {
            "0": "Movimento Normal",
            "1": "Movimento Antecipado",
            "2": "Movimento Cedido",
            "": "Não identificado",
        }
        return antecipacao.get(codigo_antecipacao.strip(), codigo_antecipacao)

    @staticmethod
    def grupo_cartoes(codigo_grupo_cartoes):
        grupo_cartoes = {
            "00": "Serviço não atribuído",
            "01": "Cartão emitido no Brasil",
            "02": "Cartão emitido no exterior",
            "03": "MDR por Tipo de Cartão - Inicial",
            "04": "MDR por Tipo de Cartão - Intermediário",
            "05": "MDR por Tipo de Cartão – Superior",
        }
        return grupo_cartoes.get(codigo_grupo_cartoes.strip(), codigo_grupo_cartoes)

    @staticmethod
    def canal_venda(codigo_canal_venda):
        canal_venda = {
            "000": "Cielo Lio",
            "001": "POS (Point of Sale)",
            "002": "Mobile",
            "003": "Manual",
            "004": "URA/CVA",
            "005": "EDI/Remessa (Troca de dados)",
            "006": "GDS/IATA",
            "007": "E-commerce",
            "008": "TEF/PDV",
            "009": "Pedágio",
            "010": "Central de atendimento (BackOffice)",
            "011": "Central de atendimento",
            "012": "Chargeback",
            "013": "Ouvidoria",
            "014": "Massivo",
            "015": "Digitado",
            "099": "Não identificado",
            " ": "Não identificado",
            "998": "Não se aplica",
        }
        return canal_venda.get(codigo_canal_venda.strip(), codigo_canal_venda)

    @staticmethod
    def tipo_lancamento(codigo_lancamento):
        lancamento = {
            "01": "Venda débito",
            "02": "Venda crédito",
            "03": "Venda parcelada",
            "04": "Ajuste a débito",
            "05": "Ajuste a crédito",
            "06": "Cancelamento de venda",
            "07": "Reversão de cancelamento de venda",
            "08": "Contestação do portador do cartão",
            "09": "Reversão de contestação do portador do cartão",
            "10": "Aluguel de máquina",
            "11": "Valor cedido em negociação",
            "13": "Débito de recebíveis dados como garantia (gravame)",
            "14": "Crédito de recebíveis dados como garantia (gravame)",
            "15": "Débito de compensação de valores em agenda financeira",
            "16": "Crédito de compensação de valores em agenda financeira",
            "17": "Devolução de crédito de valor cedido em negociação",
            "18": "Devolução de débito de valor cedido em negociação",
            "19": "Devolução de crédito de recebíveis dados como garantia (gravame)",
            "20": "Devolução de débito de recebíveis dados como garantia (gravame)",
            "23": "Débito de penhora por decisão judicial",
            "26": "Devolução de débito de penhora por decisão judicial",
            "27": "Débito de cancelamento/contestação sobre negociação cancelada",
            "28": "Crédito de cancelamento/contestação sobre negociação cancelada",
            "35": "Compensação a débito devido lançamento em garantia (gravame)",
            "36": "Compensação a crédito devido lançamento em garantia (gravame)",
            "37": "Compensação à débito devido lançamento de penhora",
            "38": "Compensação à crédito devido lançamento de penhora",
            "39": "Compensação à débito devido lançamento de cessão",
            "40": "Compensação à crédito devido lançamento de cessão",
            "42": "Venda Voucher",
        }
        return lancamento.get(codigo_lancamento.strip(), codigo_lancamento)

    @staticmethod
    def forma_pagamento(codigo_forma):
        formas_pagamento = {
            "001": "Agiplan crédito à vista",
            "002": "Agiplan parcelado loja",
            "003": "Banescard crédito à vista",
            "004": "Banescard parcelado loja",
            "005": "Esplanada crédito à vista",
            "006": "Credz crédito à vista",
            "007": "Esplanada parcelado loja",
            "008": "Credz parcelado loja",
            "009": "Elo Crediário",
            "010": "Credito a vista",
            "011": "Debito a vista",
            "012": "Parcelado Emissor",
            "013": "Elo Construcard",
            "014": "Elo Agro Débito",
            "015": "Elo Agro Custeio",
            "016": "Elo Agro Investimento",
            "017": "Elo Agro Custeio + Débito",
            "018": "Elo Agro Investimento + Débito",
            "019": "Discover crédito à vista",
            "020": "Diners crédito à vista",
            "021": "Diners parcelado loja",
            "022": "Visa Agro Custeio + Débito",
            "023": "Visa Agro Investimento + Débito",
            "024": "FCO Investimento",
            "025": "Agro Electron Agro Custeio",
            "026": "Agro Electron Agro Investimento",
            "027": "Visa FCO Giro",
            "028": "Visa creditário no crédito",
            "029": "Visa parcelado cliente",
            "030": "Pre-pago debito",
            "031": "Pre-pago credito",
            "032": "Credito a vista",
            "033": "Visa débito conversor de moeda",
            "034": "Pré-pago Visa Carnê",
            "035": "Visa Saque com cartão de Débito",
            "036": "Flex Car Visa Vale",
            "037": "Credsystem crédito à vista",
            "038": "Credsystem parcelado loja",
            "039": "Visa crédito à vista",
            "040": "Debito a vista",
            "041": "Debito a vista",
            "042": "Visa parcelado loja",
            "043": "Credito a vista",
            "044": "Alelo Refeição",
            "045": "Alelo Alimentação",
            "046": "Alelo Multibenefícios",
            "058": "Alelo Auto",
            "060": "Sorocred débito à vista",
            "061": "Sorocred crédito à vista",
            "062": "Sorocred parcelado loja",
            "064": "Visa Crediário",
            "065": "Alelo Refeição",
            "066": "Alelo Alimentação",
            "067": "Visa Capital de Giro",
            "068": "Visa Crédito Imobiliário",
            "069": "Alelo Cultura",
            "070": "Credito a vista",
            "071": "Debito a vista",
            "072": "Credito parcelado loja",
            "073": "Pré-pago Visa Cash (Visa Vale pedágio)",
            "075": "Visa Voucher",
            "079": "Pagamento Carnê Visa Eléctron",
            "080": "Visa Crédito Conversor de Moeda",
            "081": "Mastercard Crédito Especializado (*)",
            "082": "Credito a vista",
            "083": "Amex parcelado loja",
            "084": "Amex parcelado banco",
            "089": "Elo Crédito Imobiliário",
            "091": "Elo Crédito Especializado (*)",
            "094": "Banescard Débito",
            "096": "Cabal crédito à vista",
            "097": "Cabal débito à vista",
            "098": "Cabal parcelado loja",
            "107": "Pré-pago Mastar Card Carnê",
            "110": "Pre-pago credito",
            "111": "Pre-pago debito",
            "161": "Hiper crédito à vista",
            "162": "Hiper débito à vista",
            "163": "Hiper parcelado loja",
            "164": "Hipercard crédito à vista",
            "165": "Hipercard parcelado loja",
            "200": "Verdecard crédito a vista",
            "201": "Verdecard parcelado loja",
            "202": "Nutricash Alimentação",
            "203": "Nutricash Refeição",
            "204": "Nutricash Multibenefícios",
            "205": "Nutricash Combustível",
            "206": "Ben Alimentação",
            "207": "Ben Refeição",
            "215": "Voucher MasterCard",
            "269": "Pré-pago Elo Carnê",
            "270": "Pre-pago credito",
            "271": "Pre-pago debito",
            "275": "Elo Multibenefícios",
            "278": "Elo Transporte",
            "282": "Pré-pago Amex Crédito",
            "314": "Ourocard Agro débito",
            "315": "Ourocard Agro custeio",
            "316": "Ourocard Agro investimento",
            "317": "Ourocard Agro custeio + débito",
            "318": "Ourocard Agro investimento + débito",
            "321": "Mastercard creditário no crédito",
            "322": "Mastercard parcelado cliente",
            "324": "Elo parcelado cliente",
            "330": "Elo creditário no crédito",
            "342": "Mastercard Pedágio",
            "377": "Elo Carnê",
            "378": "Mastercard Carnê",
            "380": "Credito conversor moedas",
            "433": "Credito parcelado loja",
        }
        return formas_pagamento.get(codigo_forma.strip(), codigo_forma)

    @staticmethod
    def status_pagamento(status_pgto):
        status = {
            "00": "Agendado",
            "03": "Enviado ao banco",
            "45": "Enviado ao banco",
            "54": "Enviado ao banco",
            "04": "Pago",
            "05": "Pago",
            "10": "Pago",
            "11": "Pago",
            "31": "Pago",
            "32": "Pago",
            "98": "Pago",
            "99": "Pago",
            "06": "Rejeitado pelo banco",
            "07": "Reenviado ao banco",
            "46": "Debitado em conta",
            "47": "Debitado em conta",
            "58": "Pago via negociação",
            "42": "Débito Pendente",
            "48": "Débito Pendente",
        }
        return status.get(status_pgto.strip(), status_pgto)

    @staticmethod
    def formatar_valor(valor, formatar_como_texto=False):
        valor = valor.strip()
        if valor.startswith('-'):
            sinal = -1
            valor = valor[1:]
        else:
            sinal = 1

        if valor.isdigit():
            valor_numerico = sinal * (int(valor) / 100)
            if formatar_como_texto:
                valor_formatado = f"{valor_numerico:,.2f}".replace(
                    ",", "X").replace(".", ",").replace("X", ".")
                return valor_formatado
            else:
                return valor_numerico
        return 0.0 if not formatar_como_texto else "0,00"

    @staticmethod
    def formatar_inteiro(valor, formatar_como_texto=False):
        """
        Formata valores inteiros (sem casas decimais)
        Exemplo: "00000012345" → 12345
                "-00000012345" → -12345
        """
        valor = valor.strip()
        if valor.startswith('-'):
            sinal = -1
            valor = valor[1:]
        else:
            sinal = 1

        if valor.isdigit():
            valor_numerico = sinal * int(valor)
            if formatar_como_texto:
                # Formata como texto com separadores de milhar
                valor_formatado = f"{valor_numerico:,}".replace(",", ".")
                return valor_formatado
            else:
                return valor_numerico
        return 0 if not formatar_como_texto else "0"

    @staticmethod
    def formatar_tipo_lancamento(tipo_lancamento):
        """
        Formata o código da bandeira para o nome correspondente.
        - 001: Visa
        - 002: MasterCard
        - Outros códigos podem ser adicionados conforme necessário.
        """
        lancamento = {
            "01": "Debito a vista",
            "02": "Credito a vista",
            "03": "Credito parcelado loja",
            "04": "Ajuste a débito",
            "05": "Ajuste a crédito",
            "06": "Cancelamento de venda",
            "07": "Reversão de cancelamento de venda",
            "08": "Contestação do portador do cartão",
            "09": "Reversão de contestação do portador do cartão",
            "10": "Aluguel de máquina",
            "11": "Valor cedido em negociação",
            "13": "Débito de recebíveis dados como garantia (gravame)",
            "14": "Crédito de recebíveis dados como garantia (gravame)",
            "15": "Débito de compensação de valores em agenda financeira",
            "16": "Crédito de compensação de valores em agenda financeira",
            "17": "Devolução de crédito de valor cedido em negociação",
            "18": "Devolução de débito de valor cedido em negociação",
            "19": "Devolução de crédito de recebíveis dados como garantia (gravame)",
            "20": "Devolução de débito de recebíveis dados como garantia (gravame)",
            "23": "Débito de penhora por decisão judicial",
            "26": "Devolução de débito de penhora por decisão judicial",
            "27": "Débito de cancelamento/contestação sobre negociação cancelada",
            "28": "Crédito de cancelamento/contestação sobre negociação cancelada",
            "35": "Compensação a débito devido lançamento em garantia (gravame)",
            "36": "Compensação a crédito devido lançamento em garantia (gravame)",
            "37": "Compensação à débito devido lançamento de penhora",
            "38": "Compensação à crédito devido lançamento de penhora",
            "39": "Compensação à débito devido lançamento de cessão",
            "40": "Compensação à crédito devido lançamento de cessão",
            "42": "Venda Voucher",
        }
        return lancamento.get(tipo_lancamento.strip(), tipo_lancamento)

    def processar_linha(self, linha):
        """
        Método abstrato para processar uma linha do arquivo.
        Deve ser implementado pelas subclasses.
        """
        raise NotImplementedError(
            "Método processar_linha deve ser implementado nas subclasses."
        )

    @staticmethod
    def formatar_valor_trailer(valor_str):
        """Converte string de 17 dígitos para valor decimal (2 casas) - específico para trailer"""
        valor_str = valor_str.strip()
        if valor_str and len(valor_str) == 17:
            return float(valor_str) / 100
        return 0.0

    @staticmethod
    def formatar_taxa(taxa_str):
        """
        Converte taxa (5 dígitos com 3 casas decimais) para formato brasileiro.
        Exemplo: "00123" -> "0,123"
        """
        taxa_str = taxa_str.strip()
        if taxa_str and len(taxa_str) == 5 and taxa_str.isdigit():
            valor = float(taxa_str) / 1000
            return f"{valor:0.3f}".replace('.', ',')
        return "0,000"

    @staticmethod
    def formatar_data_compacta(data_str):
        """Converte AAMMDD para DD/MM/AAAA (específico para Pix)"""
        data_str = data_str.strip()
        if len(data_str) == 6 and data_str.isdigit():
            return f"{data_str[4:6]}/{data_str[2:4]}/20{data_str[0:2]}"
        return data_str

    @staticmethod
    def formatar_data_pix(data_str):
        """Converte AAMMDD para DD/MM/AAAA (alias para formatar_data_compacta)"""
        return RegistroBase.formatar_data_compacta(data_str)

# 📡 Cielo SFTP Automação

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)  
![License](https://img.shields.io/badge/license-MIT-green)  
![Status](https://img.shields.io/badge/status-active-success)

Automatize o download, processamento e análise de arquivos da **Cielo** via **SFTP**.  
Este projeto conecta-se ao servidor, baixa os relatórios, interpreta os registros padronizados (layout Cielo) e organiza os dados para análise.

---

## ✨ Funcionalidades

- 🔑 Conexão automática ao servidor **SFTP da Cielo**  
- ⬇️ Download de arquivos de forma segura e prática  
- 📂 Processamento dos registros do layout da Cielo  
- 📊 Organização dos dados para relatórios e análises  
- ⚡ Execução automatizada via `.bat` ou scripts Python  

---

## 📦 Estrutura do Projeto

```
Cielo_SFTP_Atualização/
├── versao_final.py              # Script principal
├── versao_final.ipynb           # Versão notebook (testes/experimentos)
├── Cielo_SFTP.bat               # Execução automatizada no Windows
├── requirements.txt             # Dependências do projeto
└── registros/                   # Classes de registros Cielo
    ├── RegistroBase.py
    ├── Registro_0.py
    ├── Registro_A.py
    ├── Registro_B.py
    ├── Registro_C.py
    ├── Registro_D.py
    ├── Registro_E.py
    ├── Registro_R.py
    ├── Registro_8.py
    ├── Registro_9.py
    └── __init__.py
```

---

## 🚀 Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/RafaelOmega/Cielo_SFTP.git
cd Cielo_SFTP
pip install -r requirements.txt
```

---

## ▶️ Uso

### 1. Execução direta em Python
```bash
python versao_final.py
```

### 2. Execução via batch (Windows)
Basta dar **duplo clique** em `Cielo_SFTP.bat` ou rodar:
```bash
Cielo_SFTP.bat
```

### 3. Jupyter Notebook
Se preferir explorar/ajustar:
```bash
jupyter notebook versao_final.ipynb
```

---

## ⚙️ Configuração

Certifique-se de configurar corretamente as variáveis de ambiente ou credenciais do servidor **SFTP da Cielo** antes de executar o script.  
No Windows (PowerShell):

```bash
$env:SFTP_HOST="servidor.cielo.com"
$env:SFTP_PORT="22"
$env:SFTP_USERNAME="usuario"
$env:SFTP_PASSWORD="senha"
```

---

## 🤝 Contribuindo

Contribuições são super bem-vindas!  
Para colaborar:

1. Faça um fork do projeto  
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)  
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)  
4. Faça o push da branch (`git push origin feature/nova-funcionalidade`)  
5. Abra um Pull Request 🎉  

---

## 📜 Licença

Este projeto está sob a licença MIT.  
Sinta-se livre para usar, modificar e distribuir.

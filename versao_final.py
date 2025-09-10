# %%
import shutil
import paramiko
import os
import pandas as pd
from IPython.display import display
from registros import (
    Registro0,
    RegistroD,
    RegistroE,
    Registro8,
    Registro9,
    RegistroA,
    RegistroB,
    RegistroC,
    RegistroR,
)
from sqlalchemy import create_engine
from unidecode import unidecode
from sqlalchemy import create_engine, text
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

print("Bibliotecas importadas com sucesso!")
print("Variáveis de ambiente carregadas do arquivo .env")

# %%
# === Obter variáveis de ambiente do Windows ===
hostname = os.getenv("SFTP_HOST")
port = int(os.getenv("SFTP_PORT", 22))
username = os.getenv("SFTP_USERNAME")
password = os.getenv("SFTP_PASSWORD")

# Remove espaços extras
if hostname:
    hostname = hostname.strip()
if username:
    username = username.strip()
if password:
    password = password.strip() if password else None

# Verificar se todas as variáveis foram definidas
if not all([hostname, username, password]):
    raise ValueError("Uma ou mais variáveis de ambiente não foram definidas.")

# Caminho da pasta local
local_folder = "arquivos"
os.makedirs(local_folder, exist_ok=True)
print(f"Pasta '{local_folder}' pronta.")

# Criar instância do cliente SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Tentando conectar em {hostname}:{port} como {username}...")

    # Conectar ao servidor SFTP
    ssh.connect(hostname, port, username, password)
    print("Conexão SSH estabelecida com sucesso!")

    # Abrir sessão SFTP
    with ssh.open_sftp() as sftp:
        print("Sessão SFTP aberta com sucesso!")

        # Entrar na pasta 'arquivos' do servidor
        remote_dir = "./arquivos"
        print(f"Acessando diretório remoto: {remote_dir}")

        # Listar arquivos no diretório remoto
        files = sftp.listdir(remote_dir)
        print("Arquivos no diretório remoto:")

        for file in files:
            print(" -", file)

            # remote_file_path = os.path.join(".", file)
            remote_file_path = f"{remote_dir}/{file}"
            local_file_path = os.path.join(local_folder, file)

            # Baixar arquivo
            sftp.get(remote_file_path, local_file_path)
            print(f"Arquivo '{file}' copiado para '{local_file_path}'")

            # Remover arquivo remoto após baixar
            sftp.remove(remote_file_path)
            print(f"Arquivo '{file}' removido do servidor.")

except paramiko.AuthenticationException:
    print("Erro de autenticação! Verifique usuário/senha ou chave privada.")
except paramiko.SSHException as ssh_err:
    print(f"Erro SSH: {ssh_err}")
except Exception as e:
    print(f"Erro inesperado: {e}")
finally:
    ssh.close()
    print("Conexão SSH fechada.")

# %%
print("🔍 INVESTIGAÇÃO COMPLETA DA PASTA:")
print(f"Pasta local: {os.path.abspath(local_folder)}")

# Listar TUDO que está na pasta
print("\n📋 Conteúdo completo da pasta:")
conteudo = os.listdir(local_folder)
for i, item in enumerate(conteudo, 1):
    caminho_completo = os.path.join(local_folder, item)
    if os.path.isfile(caminho_completo):
        tamanho = os.path.getsize(caminho_completo)
        print(f"  {i:2d}. 📄 {item} ({tamanho} bytes)")
    else:
        print(f"  {i:2d}. 📁 {item}/ (pasta)")

# Filtrar apenas arquivos CIELO
arquivos_cielo = []
for item in conteudo:
    caminho_completo = os.path.join(local_folder, item)
    if os.path.isfile(caminho_completo) and item.startswith("CIELO"):
        arquivos_cielo.append(item)

print(f"\n🎯 Arquivos CIELO encontrados: {len(arquivos_cielo)}")
for i, arquivo in enumerate(arquivos_cielo, 1):
    file_type = arquivo[5:7] if len(arquivo) >= 7 else "??"
    print(f"  {i:2d}. {arquivo} (Tipo: {file_type})")

# Verificar extensões
print(f"\n🔎 Extensões dos arquivos CIELO:")
extensoes = {}
for arquivo in arquivos_cielo:
    ext = os.path.splitext(arquivo)[1].lower()
    extensoes[ext] = extensoes.get(ext, 0) + 1

for ext, count in extensoes.items():
    print(f"  {ext}: {count} arquivos")

# %%
# Célula para processar registros do tipo 0 (Cabeçalho) separados por tipo de arquivo
print("📊 PROCESSANDO REGISTROS TIPO 0 (CABEÇALHO) POR TIPO DE ARQUIVO...")

# DataFrames separados por tipo de arquivo
df_registro_0_03 = pd.DataFrame()  # Para arquivos tipo 03
df_registro_0_04 = pd.DataFrame()  # Para arquivos tipo 04
df_registro_0_15 = pd.DataFrame()  # Para arquivos tipo 15
df_registro_0_09 = pd.DataFrame()  # Para arquivos tipo 09

processador_0 = Registro0()

for arquivo in arquivos_cielo:
    caminho_arquivo = os.path.join(local_folder, arquivo)

    # Identificar o tipo de arquivo (03, 04, 15, 09)
    # Pega os caracteres 5 e 6 (ex: "03", "04", etc.)
    tipo_arquivo = arquivo[5:7]

    print(f"📁 Processando arquivo: {arquivo} (Tipo: {tipo_arquivo})")

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            linhas = file.readlines()

            for i, linha in enumerate(linhas):
                linha = linha.strip()
                if not linha:
                    continue

                # Verificar se é registro tipo 0
                if linha.startswith('0'):
                    try:
                        df_linha = processador_0.processar_linha(
                            linha, mostrar=False)
                        df_linha['arquivo_origem'] = arquivo
                        df_linha['tipo_arquivo'] = tipo_arquivo

                        # Adicionar ao DataFrame correspondente ao tipo de arquivo
                        if tipo_arquivo == '03':
                            if df_registro_0_03.empty:
                                df_registro_0_03 = df_linha
                            else:
                                df_registro_0_03 = pd.concat(
                                    [df_registro_0_03, df_linha], ignore_index=True)

                        elif tipo_arquivo == '04':
                            if df_registro_0_04.empty:
                                df_registro_0_04 = df_linha
                            else:
                                df_registro_0_04 = pd.concat(
                                    [df_registro_0_04, df_linha], ignore_index=True)

                        elif tipo_arquivo == '15':
                            if df_registro_0_15.empty:
                                df_registro_0_15 = df_linha
                            else:
                                df_registro_0_15 = pd.concat(
                                    [df_registro_0_15, df_linha], ignore_index=True)

                        elif tipo_arquivo == '09':
                            if df_registro_0_09.empty:
                                df_registro_0_09 = df_linha
                            else:
                                df_registro_0_09 = pd.concat(
                                    [df_registro_0_09, df_linha], ignore_index=True)

                    except Exception as e:
                        print(f"⚠️  Erro na linha {i+1}: {e}")

    except Exception as e:
        print(f"❌ Erro no arquivo {arquivo}: {e}")

# Exibir resultados
print("\n" + "="*60)
print("📈 RESULTADOS REGISTRO 0 POR TIPO DE ARQUIVO:")
print("="*60)

print(f"\n✅ Registro 0 - Arquivos Tipo 03: {len(df_registro_0_03)} linhas")
if not df_registro_0_03.empty:
    display(df_registro_0_03)
else:
    print("   Nenhum registro encontrado")

print(f"\n✅ Registro 0 - Arquivos Tipo 04: {len(df_registro_0_04)} linhas")
if not df_registro_0_04.empty:
    display(df_registro_0_04)
else:
    print("   Nenhum registro encontrado")

print(f"\n✅ Registro 0 - Arquivos Tipo 15: {len(df_registro_0_15)} linhas")
if not df_registro_0_15.empty:
    display(df_registro_0_15)
else:
    print("   Nenhum registro encontrado")

print(f"\n✅ Registro 0 - Arquivos Tipo 09: {len(df_registro_0_09)} linhas")
if not df_registro_0_09.empty:
    display(df_registro_0_09)
else:
    print("   Nenhum registro encontrado")

# Estatísticas finais
print("\n" + "="*60)
print("📊 ESTATÍSTICAS FINAIS REGISTRO 0:")
print("="*60)
print(f"Total Tipo 03: {len(df_registro_0_03)} registros")
print(f"Total Tipo 04: {len(df_registro_0_04)} registros")
print(f"Total Tipo 15: {len(df_registro_0_15)} registros")
print(f"Total Tipo 09: {len(df_registro_0_09)} registros")
print(f"TOTAL GERAL: {len(df_registro_0_03) + len(df_registro_0_04) + len(df_registro_0_15) + len(df_registro_0_09)} registros")

# %%
# Célula para criar arquivo Excel com os resultados do Registro 0 (sobrescrevendo)
print("💾 SALVANDO RESULTADOS DO REGISTRO 0 EM EXCEL...")

# Criar caminho dinâmico para a pasta resultados_analise
diretorio_atual = os.getcwd()  # Pega o diretório atual de execução
pasta_resultados = os.path.join(diretorio_atual, "resultados_analise")

# Garantir que a pasta existe
os.makedirs(pasta_resultados, exist_ok=True)
print(f"📁 Pasta de resultados: {pasta_resultados}")

# Nome fixo do arquivo (será sobrescrito sempre)
nome_arquivo = "registro_0_analise.xlsx"
caminho_completo = os.path.join(pasta_resultados, nome_arquivo)

# Criar um ExcelWriter para salvar múltiplas abas
with pd.ExcelWriter(caminho_completo, engine='openpyxl') as writer:
    # Salvar cada DataFrame em uma aba diferente
    if not df_registro_0_03.empty:
        df_registro_0_03.to_excel(writer, sheet_name='Tipo_03', index=False)
        print("✅ Aba 'Tipo_03' salva")
    else:
        # Criar aba vazia para manter a estrutura
        pd.DataFrame().to_excel(writer, sheet_name='Tipo_03', index=False)
        print("ℹ️  Aba 'Tipo_03' criada (vazia)")

    if not df_registro_0_04.empty:
        df_registro_0_04.to_excel(writer, sheet_name='Tipo_04', index=False)
        print("✅ Aba 'Tipo_04' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Tipo_04', index=False)
        print("ℹ️  Aba 'Tipo_04' criada (vazia)")

    if not df_registro_0_15.empty:
        df_registro_0_15.to_excel(writer, sheet_name='Tipo_15', index=False)
        print("✅ Aba 'Tipo_15' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Tipo_15', index=False)
        print("ℹ️  Aba 'Tipo_15' criada (vazia)")

    if not df_registro_0_09.empty:
        df_registro_0_09.to_excel(writer, sheet_name='Tipo_09', index=False)
        print("✅ Aba 'Tipo_09' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Tipo_09', index=False)
        print("ℹ️  Aba 'Tipo_09' criada (vazia)")

    # Criar uma aba de resumo
    resumo_data = {
        'Tipo_Arquivo': ['03', '04', '15', '09', 'TOTAL'],
        'Quantidade_Registros': [
            len(df_registro_0_03),
            len(df_registro_0_04),
            len(df_registro_0_15),
            len(df_registro_0_09),
            len(df_registro_0_03) + len(df_registro_0_04) +
            len(df_registro_0_15) + len(df_registro_0_09)
        ],
        'Status': [
            'Encontrados' if len(df_registro_0_03) > 0 else 'Não encontrados',
            'Encontrados' if len(df_registro_0_04) > 0 else 'Não encontrados',
            'Encontrados' if len(df_registro_0_15) > 0 else 'Não encontrados',
            'Encontrados' if len(df_registro_0_09) > 0 else 'Não encontrados',
            'Consolidado'
        ]
    }
    df_resumo = pd.DataFrame(resumo_data)
    df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
    print("✅ Aba 'Resumo' salva")

print(f"🎯 Arquivo Excel criado/atualizado com sucesso!")
print(f"📊 Local: {caminho_completo}")
print(
    f"📋 Total de registros salvos: {len(df_registro_0_03) + len(df_registro_0_04) + len(df_registro_0_15) + len(df_registro_0_09)}")

# Verificar se o arquivo foi criado
if os.path.exists(caminho_completo):
    tamanho_arquivo = os.path.getsize(caminho_completo)
    print(f"💾 Tamanho do arquivo: {tamanho_arquivo} bytes")
else:
    print("❌ Erro: Arquivo não foi criado!")

# Mostrar caminho completo para fácil acesso
print(f"\\n🔗 Caminho completo do arquivo:")
print(f"   {caminho_completo}")

# %%
# # Célula para processar registros do tipo 8 (PIX) separados por tipo de arquivo
# print("📊 PROCESSANDO REGISTROS TIPO 8 (PIX) POR TIPO DE ARQUIVO...")

# # DataFrames separados por tipo de arquivo
# df_registro_8_03 = pd.DataFrame()  # Para arquivos tipo 03
# df_registro_8_04 = pd.DataFrame()  # Para arquivos tipo 04
# df_registro_8_15 = pd.DataFrame()  # Para arquivos tipo 15
# df_registro_8_09 = pd.DataFrame()  # Para arquivos tipo 09

# processador_8 = Registro8()

# for arquivo in arquivos_cielo:
#     caminho_arquivo = os.path.join(local_folder, arquivo)

#     # Identificar o tipo de arquivo (03, 04, 15, 09)
#     # Pega os caracteres 5 e 6 (ex: "03", "04", etc.)
#     tipo_arquivo = arquivo[5:7]

#     print(f"📁 Processando arquivo: {arquivo} (Tipo: {tipo_arquivo})")

#     try:
#         with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#             linhas = file.readlines()

#             for i, linha in enumerate(linhas):
#                 linha = linha.strip()
#                 if not linha:
#                     continue

#                 # Verificar se é registro tipo 8
#                 if linha.startswith('8'):
#                     try:
#                         df_linha = processador_8.processar_linha(
#                             linha, mostrar=False)
#                         df_linha['arquivo_origem'] = arquivo
#                         df_linha['tipo_arquivo'] = tipo_arquivo

#                         # Adicionar ao DataFrame correspondente ao tipo de arquivo
#                         if tipo_arquivo == '03':
#                             if df_registro_8_03.empty:
#                                 df_registro_8_03 = df_linha
#                             else:
#                                 df_registro_8_03 = pd.concat(
#                                     [df_registro_8_03, df_linha], ignore_index=True)

#                         elif tipo_arquivo == '04':
#                             if df_registro_8_04.empty:
#                                 df_registro_8_04 = df_linha
#                             else:
#                                 df_registro_8_04 = pd.concat(
#                                     [df_registro_8_04, df_linha], ignore_index=True)

#                         elif tipo_arquivo == '15':
#                             if df_registro_8_15.empty:
#                                 df_registro_8_15 = df_linha
#                             else:
#                                 df_registro_8_15 = pd.concat(
#                                     [df_registro_8_15, df_linha], ignore_index=True)

#                         elif tipo_arquivo == '09':
#                             if df_registro_8_09.empty:
#                                 df_registro_8_09 = df_linha
#                             else:
#                                 df_registro_8_09 = pd.concat(
#                                     [df_registro_8_09, df_linha], ignore_index=True)

#                     except Exception as e:
#                         print(f"⚠️  Erro na linha {i+1}: {e}")

#     except Exception as e:
#         print(f"❌ Erro no arquivo {arquivo}: {e}")

# # Exibir resultados
# print("\n" + "="*60)
# print("📈 RESULTADOS REGISTRO 8 (PIX) POR TIPO DE ARQUIVO:")
# print("="*60)

# print(f"\n✅ Registro 8 - Arquivos Tipo 03: {len(df_registro_8_03)} linhas")
# if not df_registro_8_03.empty:
#     display(df_registro_8_03.head(3))  # Mostrando apenas as primeiras linhas
# else:
#     print("   Nenhum registro encontrado")

# print(f"\n✅ Registro 8 - Arquivos Tipo 04: {len(df_registro_8_04)} linhas")
# if not df_registro_8_04.empty:
#     display(df_registro_8_04.head(3))
# else:
#     print("   Nenhum registro encontrado")

# print(f"\n✅ Registro 8 - Arquivos Tipo 15: {len(df_registro_8_15)} linhas")
# if not df_registro_8_15.empty:
#     display(df_registro_8_15.head(3))
# else:
#     print("   Nenhum registro encontrado")

# print(f"\n✅ Registro 8 - Arquivos Tipo 09: {len(df_registro_8_09)} linhas")
# if not df_registro_8_09.empty:
#     display(df_registro_8_09.head(3))
# else:
#     print("   Nenhum registro encontrado")

# # Estatísticas finais
# print("\n" + "="*60)
# print("📊 ESTATÍSTICAS FINAIS REGISTRO 8 (PIX):")
# print("="*60)
# print(f"Total Tipo 03: {len(df_registro_8_03)} registros")
# print(f"Total Tipo 04: {len(df_registro_8_04)} registros")
# print(f"Total Tipo 15: {len(df_registro_8_15)} registros")
# print(f"Total Tipo 09: {len(df_registro_8_09)} registros")
# print(f"TOTAL GERAL: {len(df_registro_8_03) + len(df_registro_8_04) + len(df_registro_8_15) + len(df_registro_8_09)} registros")

# %%
# # Célula para salvar resultados do Registro 8 em Excel
# print("💾 SALVANDO RESULTADOS DO REGISTRO 8 (PIX) EM EXCEL...")

# # Usar a mesma pasta de resultados
# pasta_resultados = os.path.join(os.getcwd(), "resultados_analise")
# os.makedirs(pasta_resultados, exist_ok=True)

# # Nome fixo do arquivo para registro 8
# nome_arquivo_8 = "registro_8_pix_analise.xlsx"
# caminho_completo_8 = os.path.join(pasta_resultados, nome_arquivo_8)

# # Criar um ExcelWriter para salvar múltiplas abas
# with pd.ExcelWriter(caminho_completo_8, engine='openpyxl') as writer:
#     # Salvar cada DataFrame em uma aba diferente
#     if not df_registro_8_03.empty:
#         df_registro_8_03.to_excel(
#             writer, sheet_name='PIX_Tipo_03', index=False)
#         print("✅ Aba 'PIX_Tipo_03' salva")
#     else:
#         pd.DataFrame().to_excel(writer, sheet_name='PIX_Tipo_03', index=False)
#         print("ℹ️  Aba 'PIX_Tipo_03' criada (vazia)")

#     if not df_registro_8_04.empty:
#         df_registro_8_04.to_excel(
#             writer, sheet_name='PIX_Tipo_04', index=False)
#         print("✅ Aba 'PIX_Tipo_04' salva")
#     else:
#         pd.DataFrame().to_excel(writer, sheet_name='PIX_Tipo_04', index=False)
#         print("ℹ️  Aba 'PIX_Tipo_04' criada (vazia)")

#     if not df_registro_8_15.empty:
#         df_registro_8_15.to_excel(
#             writer, sheet_name='PIX_Tipo_15', index=False)
#         print("✅ Aba 'PIX_Tipo_15' salva")
#     else:
#         pd.DataFrame().to_excel(writer, sheet_name='PIX_Tipo_15', index=False)
#         print("ℹ️  Aba 'PIX_Tipo_15' criada (vazia)")

#     if not df_registro_8_09.empty:
#         df_registro_8_09.to_excel(
#             writer, sheet_name='PIX_Tipo_09', index=False)
#         print("✅ Aba 'PIX_Tipo_09' salva")
#     else:
#         pd.DataFrame().to_excel(writer, sheet_name='PIX_Tipo_09', index=False)
#         print("ℹ️  Aba 'PIX_Tipo_09' criada (vazia)")

#     # Criar uma aba de resumo
#     resumo_data = {
#         'Tipo_Arquivo': ['03', '04', '15', '09', 'TOTAL'],
#         'Quantidade_Registros_PIX': [
#             len(df_registro_8_03),
#             len(df_registro_8_04),
#             len(df_registro_8_15),
#             len(df_registro_8_09),
#             len(df_registro_8_03) + len(df_registro_8_04) +
#             len(df_registro_8_15) + len(df_registro_8_09)
#         ],
#         'Status': [
#             'Encontrados' if len(df_registro_8_03) > 0 else 'Não encontrados',
#             'Encontrados' if len(df_registro_8_04) > 0 else 'Não encontrados',
#             'Encontrados' if len(df_registro_8_15) > 0 else 'Não encontrados',
#             'Encontrados' if len(df_registro_8_09) > 0 else 'Não encontrados',
#             'Consolidado'
#         ]
#     }
#     df_resumo = pd.DataFrame(resumo_data)
#     df_resumo.to_excel(writer, sheet_name='Resumo_PIX', index=False)
#     print("✅ Aba 'Resumo_PIX' salva")

# print(f"🎯 Arquivo Excel do Registro 8 criado/atualizado com sucesso!")
# print(f"📊 Local: {caminho_completo_8}")
# print(
#     f"📋 Total de registros PIX salvos: {len(df_registro_8_03) + len(df_registro_8_04) + len(df_registro_8_15) + len(df_registro_8_09)}")

# # Verificar se o arquivo foi criado
# if os.path.exists(caminho_completo_8):
#     tamanho_arquivo = os.path.getsize(caminho_completo_8)
#     print(f"💾 Tamanho do arquivo: {tamanho_arquivo} bytes")
# else:
#     print("❌ Erro: Arquivo não foi criado!")

# print(f"\\n🔗 Caminho completo do arquivo:")
# print(f"   {caminho_completo_8}")

# %%
# Célula para processar registros do tipo 9 (Rodapé) separados por tipo de arquivo
print("📊 PROCESSANDO REGISTROS TIPO 9 (RODAPÉ) POR TIPO DE ARQUIVO...")

# DataFrames separados por tipo de arquivo
df_registro_9_03 = pd.DataFrame()  # Para arquivos tipo 03
df_registro_9_04 = pd.DataFrame()  # Para arquivos tipo 04
df_registro_9_15 = pd.DataFrame()  # Para arquivos tipo 15
df_registro_9_09 = pd.DataFrame()  # Para arquivos tipo 09

processador_9 = Registro9()

for arquivo in arquivos_cielo:
    caminho_arquivo = os.path.join(local_folder, arquivo)

    # Identificar o tipo de arquivo (03, 04, 15, 09)
    # Pega os caracteres 5 e 6 (ex: "03", "04", etc.)
    tipo_arquivo = arquivo[5:7]

    print(f"📁 Processando arquivo: {arquivo} (Tipo: {tipo_arquivo})")

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            linhas = file.readlines()

            for i, linha in enumerate(linhas):
                linha = linha.strip()
                if not linha:
                    continue

                # Verificar se é registro tipo 9 (RODAPÉ)
                if linha.startswith('9'):
                    try:
                        df_linha = processador_9.processar_linha(
                            linha, mostrar=False)
                        df_linha['arquivo_origem'] = arquivo
                        df_linha['tipo_arquivo'] = tipo_arquivo

                        # Adicionar ao DataFrame correspondente ao tipo de arquivo
                        if tipo_arquivo == '03':
                            if df_registro_9_03.empty:
                                df_registro_9_03 = df_linha
                            else:
                                df_registro_9_03 = pd.concat(
                                    [df_registro_9_03, df_linha], ignore_index=True)

                        elif tipo_arquivo == '04':
                            if df_registro_9_04.empty:
                                df_registro_9_04 = df_linha
                            else:
                                df_registro_9_04 = pd.concat(
                                    [df_registro_9_04, df_linha], ignore_index=True)

                        elif tipo_arquivo == '15':
                            if df_registro_9_15.empty:
                                df_registro_9_15 = df_linha
                            else:
                                df_registro_9_15 = pd.concat(
                                    [df_registro_9_15, df_linha], ignore_index=True)

                        elif tipo_arquivo == '09':
                            if df_registro_9_09.empty:
                                df_registro_9_09 = df_linha
                            else:
                                df_registro_9_09 = pd.concat(
                                    [df_registro_9_09, df_linha], ignore_index=True)

                    except Exception as e:
                        print(f"⚠️  Erro na linha {i+1}: {e}")

    except Exception as e:
        print(f"❌ Erro no arquivo {arquivo}: {e}")

# Exibir resultados
print("\n" + "="*60)
print("📈 RESULTADOS REGISTRO 9 (RODAPÉ) POR TIPO DE ARQUIVO:")
print("="*60)

print(f"\n✅ Registro 9 - Arquivos Tipo 03: {len(df_registro_9_03)} linhas")
if not df_registro_9_03.empty:
    display(df_registro_9_03)
else:
    print("   Nenhum registro encontrado")

print(f"\n✅ Registro 9 - Arquivos Tipo 04: {len(df_registro_9_04)} linhas")
if not df_registro_9_04.empty:
    display(df_registro_9_04)
else:
    print("   Nenhum registro encontrado")

print(f"\n✅ Registro 9 - Arquivos Tipo 15: {len(df_registro_9_15)} linhas")
if not df_registro_9_15.empty:
    display(df_registro_9_15)
else:
    print("   Nenhum registro encontrado")

print(f"\n✅ Registro 9 - Arquivos Tipo 09: {len(df_registro_9_09)} linhas")
if not df_registro_9_09.empty:
    display(df_registro_9_09)
else:
    print("   Nenhum registro encontrado")

# Estatísticas finais
print("\n" + "="*60)
print("📊 ESTATÍSTICAS FINAIS REGISTRO 9 (RODAPÉ):")
print("="*60)
print(f"Total Tipo 03: {len(df_registro_9_03)} registros")
print(f"Total Tipo 04: {len(df_registro_9_04)} registros")
print(f"Total Tipo 15: {len(df_registro_9_15)} registros")
print(f"Total Tipo 09: {len(df_registro_9_09)} registros")
print(f"TOTAL GERAL: {len(df_registro_9_03) + len(df_registro_9_04) + len(df_registro_9_15) + len(df_registro_9_09)} registros")

# %%
# Célula para salvar resultados do Registro 9 em Excel
print("💾 SALVANDO RESULTADOS DO REGISTRO 9 (RODAPÉ) EM EXCEL...")

# Usar a mesma pasta de resultados
pasta_resultados = os.path.join(os.getcwd(), "resultados_analise")
os.makedirs(pasta_resultados, exist_ok=True)

# Nome fixo do arquivo para registro 9
nome_arquivo_9 = "registro_9_rodape_analise.xlsx"
caminho_completo_9 = os.path.join(pasta_resultados, nome_arquivo_9)

# Criar um ExcelWriter para salvar múltiplas abas
with pd.ExcelWriter(caminho_completo_9, engine='openpyxl') as writer:
    # Salvar cada DataFrame em uma aba diferente
    if not df_registro_9_03.empty:
        df_registro_9_03.to_excel(
            writer, sheet_name='Rodape_Tipo_03', index=False)
        print("✅ Aba 'Rodape_Tipo_03' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Rodape_Tipo_03', index=False)
        print("ℹ️  Aba 'Rodape_Tipo_03' criada (vazia)")

    if not df_registro_9_04.empty:
        df_registro_9_04.to_excel(
            writer, sheet_name='Rodape_Tipo_04', index=False)
        print("✅ Aba 'Rodape_Tipo_04' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Rodape_Tipo_04', index=False)
        print("ℹ️  Aba 'Rodape_Tipo_04' criada (vazia)")

    if not df_registro_9_15.empty:
        df_registro_9_15.to_excel(
            writer, sheet_name='Rodape_Tipo_15', index=False)
        print("✅ Aba 'Rodape_Tipo_15' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Rodape_Tipo_15', index=False)
        print("ℹ️  Aba 'Rodape_Tipo_15' criada (vazia)")

    if not df_registro_9_09.empty:
        df_registro_9_09.to_excel(
            writer, sheet_name='Rodape_Tipo_09', index=False)
        print("✅ Aba 'Rodape_Tipo_09' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Rodape_Tipo_09', index=False)
        print("ℹ️  Aba 'Rodape_Tipo_09' criada (vazia)")

    # Criar uma aba de resumo
    resumo_data = {
        'Tipo_Arquivo': ['03', '04', '15', '09', 'TOTAL'],
        'Quantidade_Registros_Rodape': [
            len(df_registro_9_03),
            len(df_registro_9_04),
            len(df_registro_9_15),
            len(df_registro_9_09),
            len(df_registro_9_03) + len(df_registro_9_04) +
            len(df_registro_9_15) + len(df_registro_9_09)
        ],
        'Status': [
            'Encontrados' if len(df_registro_9_03) > 0 else 'Não encontrados',
            'Encontrados' if len(df_registro_9_04) > 0 else 'Não encontrados',
            'Encontrados' if len(df_registro_9_15) > 0 else 'Não encontrados',
            'Encontrados' if len(df_registro_9_09) > 0 else 'Não encontrados',
            'Consolidado'
        ]
    }
    df_resumo = pd.DataFrame(resumo_data)
    df_resumo.to_excel(writer, sheet_name='Resumo_Rodape', index=False)
    print("✅ Aba 'Resumo_Rodape' salva")

print(f"🎯 Arquivo Excel do Registro 9 (RODAPÉ) criado/atualizado com sucesso!")
print(f"📊 Local: {caminho_completo_9}")
print(
    f"📋 Total de registros de rodapé salvos: {len(df_registro_9_03) + len(df_registro_9_04) + len(df_registro_9_15) + len(df_registro_9_09)}")

# Verificar se o arquivo foi criado
if os.path.exists(caminho_completo_9):
    tamanho_arquivo = os.path.getsize(caminho_completo_9)
    print(f"💾 Tamanho do arquivo: {tamanho_arquivo} bytes")
else:
    print("❌ Erro: Arquivo não foi criado!")

print(f"\n🔗 Caminho completo do arquivo:")
print(f"   {caminho_completo_9}")

# %%
# # Célula para processar registros do tipo A (Resumo de Negociação) - apenas arquivos 15
# print("📊 PROCESSANDO REGISTROS TIPO A (RESUMO NEGOCIAÇÃO) - APENAS ARQUIVOS 15...")

# # DataFrame para registro A (só existe em arquivos 15)
# df_registro_A_15 = pd.DataFrame()

# processador_A = RegistroA()

# for arquivo in arquivos_cielo:
#     caminho_arquivo = os.path.join(local_folder, arquivo)

#     # Identificar o tipo de arquivo
#     tipo_arquivo = arquivo[5:7]

#     # Processar apenas arquivos tipo 15 (onde o registro A existe)
#     if tipo_arquivo == '15':
#         print(f"📁 Processando arquivo: {arquivo} (Tipo: {tipo_arquivo})")

#         try:
#             with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#                 linhas = file.readlines()

#                 for i, linha in enumerate(linhas):
#                     linha = linha.strip()
#                     if not linha:
#                         continue

#                     # Verificar se é registro tipo A
#                     if linha.startswith('A'):
#                         try:
#                             df_linha = processador_A.processar_linha(
#                                 linha, mostrar=False)
#                             df_linha['arquivo_origem'] = arquivo
#                             df_linha['tipo_arquivo'] = tipo_arquivo

#                             if df_registro_A_15.empty:
#                                 df_registro_A_15 = df_linha
#                             else:
#                                 df_registro_A_15 = pd.concat(
#                                     [df_registro_A_15, df_linha], ignore_index=True)

#                         except Exception as e:
#                             print(f"⚠️  Erro na linha {i+1}: {e}")

#         except Exception as e:
#             print(f"❌ Erro no arquivo {arquivo}: {e}")
#     else:
#         print(
#             f"⏭️  Pulando arquivo {arquivo} (Tipo: {tipo_arquivo}) - Registro A só existe em arquivos 15")

# # Exibir resultados
# print("\n" + "="*70)
# print("📈 RESULTADOS REGISTRO A (RESUMO NEGOCIAÇÃO) - ARQUIVOS 15:")
# print("="*70)

# print(f"\n✅ Registro A - Arquivos Tipo 15: {len(df_registro_A_15)} linhas")
# if not df_registro_A_15.empty:
#     display(df_registro_A_15)
# else:
#     print("   Nenhum registro encontrado")

# # Estatísticas finais
# print("\n" + "="*70)
# print("📊 ESTATÍSTICAS FINAIS REGISTRO A:")
# print("="*70)
# print(f"Total Registros A (Tipo 15): {len(df_registro_A_15)} registros")

# %%
# # Célula para salvar resultados do Registro A em Excel
# print("💾 SALVANDO RESULTADOS DO REGISTRO A (RESUMO NEGOCIAÇÃO) EM EXCEL...")

# # Usar a mesma pasta de resultados
# pasta_resultados = os.path.join(os.getcwd(), "resultados_analise")
# os.makedirs(pasta_resultados, exist_ok=True)

# # Nome fixo do arquivo para registro A
# nome_arquivo_A = "registro_A_negociacao_analise.xlsx"
# caminho_completo_A = os.path.join(pasta_resultados, nome_arquivo_A)

# # Criar um ExcelWriter para salvar
# with pd.ExcelWriter(caminho_completo_A, engine='openpyxl') as writer:
#     # Salvar DataFrame do tipo 15
#     if not df_registro_A_15.empty:
#         df_registro_A_15.to_excel(
#             writer, sheet_name='Negociacao_Tipo_15', index=False)
#         print("✅ Aba 'Negociacao_Tipo_15' salva")
#     else:
#         pd.DataFrame().to_excel(writer, sheet_name='Negociacao_Tipo_15', index=False)
#         print("ℹ️  Aba 'Negociacao_Tipo_15' criada (vazia)")

#     # Criar uma aba de resumo
#     resumo_data = {
#         'Tipo_Arquivo': ['15', 'TOTAL'],
#         'Quantidade_Registros_Negociacao': [
#             len(df_registro_A_15),
#             len(df_registro_A_15)
#         ],
#         'Status': [
#             'Encontrados' if len(df_registro_A_15) > 0 else 'Não encontrados',
#             'Consolidado'
#         ]
#     }
#     df_resumo = pd.DataFrame(resumo_data)
#     df_resumo.to_excel(writer, sheet_name='Resumo_Negociacao', index=False)
#     print("✅ Aba 'Resumo_Negociacao' salva")

# print(f"🎯 Arquivo Excel do Registro A criado/atualizado com sucesso!")
# print(f"📊 Local: {caminho_completo_A}")
# print(f"📋 Total de registros de negociação salvos: {len(df_registro_A_15)}")

# # Verificar se o arquivo foi criado
# if os.path.exists(caminho_completo_A):
#     tamanho_arquivo = os.path.getsize(caminho_completo_A)
#     print(f"💾 Tamanho do arquivo: {tamanho_arquivo} bytes")
# else:
#     print("❌ Erro: Arquivo não foi criado!")

# print(f"\n🔗 Caminho completo do arquivo:")
# print(f"   {caminho_completo_A}")

# %%
# # Célula para processar registros do tipo B (Detalhe Negociação) - apenas arquivos 15
# print("📊 PROCESSANDO REGISTROS TIPO B (DETALHE NEGOCIAÇÃO) - APENAS ARQUIVOS 15...")

# # DataFrame para registro B (só existe em arquivos 15)
# df_registro_B_15 = pd.DataFrame()

# processador_B = RegistroB()

# for arquivo in arquivos_cielo:
#     caminho_arquivo = os.path.join(local_folder, arquivo)

#     # Identificar o tipo de arquivo
#     tipo_arquivo = arquivo[5:7]

#     # Processar apenas arquivos tipo 15 (onde o registro B existe)
#     if tipo_arquivo == '15':
#         print(f"📁 Processando arquivo: {arquivo} (Tipo: {tipo_arquivo})")

#         try:
#             with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#                 linhas = file.readlines()

#                 for i, linha in enumerate(linhas):
#                     linha = linha.strip()
#                     if not linha:
#                         continue

#                     # Verificar se é registro tipo B
#                     if linha.startswith('B'):
#                         try:
#                             df_linha = processador_B.processar_linha(
#                                 linha, mostrar=False)
#                             df_linha['arquivo_origem'] = arquivo
#                             df_linha['tipo_arquivo'] = tipo_arquivo

#                             if df_registro_B_15.empty:
#                                 df_registro_B_15 = df_linha
#                             else:
#                                 df_registro_B_15 = pd.concat(
#                                     [df_registro_B_15, df_linha], ignore_index=True)

#                         except Exception as e:
#                             print(f"⚠️  Erro na linha {i+1}: {e}")

#         except Exception as e:
#             print(f"❌ Erro no arquivo {arquivo}: {e}")
#     else:
#         print(
#             f"⏭️  Pulando arquivo {arquivo} (Tipo: {tipo_arquivo}) - Registro B só existe em arquivos 15")

# # Exibir resultados
# print("\n" + "="*70)
# print("📈 RESULTADOS REGISTRO B (DETALHE NEGOCIAÇÃO) - ARQUIVOS 15:")
# print("="*70)

# print(f"\n✅ Registro B - Arquivos Tipo 15: {len(df_registro_B_15)} linhas")
# if not df_registro_B_15.empty:
#     # Mostrar primeiras 5 linhas por ser detalhado
#     display(df_registro_B_15.head(5))
# else:
#     print("   Nenhum registro encontrado")

# # Estatísticas finais
# print("\n" + "="*70)
# print("📊 ESTATÍSTICAS FINAIS REGISTRO B:")
# print("="*70)
# print(f"Total Registros B (Tipo 15): {len(df_registro_B_15)} registros")

# %%
# # Célula para salvar resultados do Registro B em Excel
# print("💾 SALVANDO RESULTADOS DO REGISTRO B (DETALHE NEGOCIAÇÃO) EM EXCEL...")

# # Usar a mesma pasta de resultados
# pasta_resultados = os.path.join(os.getcwd(), "resultados_analise")
# os.makedirs(pasta_resultados, exist_ok=True)

# # Nome fixo do arquivo para registro B
# nome_arquivo_B = "registro_B_detalhe_negociacao_analise.xlsx"
# caminho_completo_B = os.path.join(pasta_resultados, nome_arquivo_B)

# # Criar um ExcelWriter para salvar
# with pd.ExcelWriter(caminho_completo_B, engine='openpyxl') as writer:
#     # Salvar DataFrame do tipo 15
#     if not df_registro_B_15.empty:
#         df_registro_B_15.to_excel(
#             writer, sheet_name='Detalhe_Negociacao_15', index=False)
#         print("✅ Aba 'Detalhe_Negociacao_15' salva")
#     else:
#         pd.DataFrame().to_excel(writer, sheet_name='Detalhe_Negociacao_15', index=False)
#         print("ℹ️  Aba 'Detalhe_Negociacao_15' criada (vazia)")

#     # Criar uma aba de resumo
#     resumo_data = {
#         'Tipo_Arquivo': ['15', 'TOTAL'],
#         'Quantidade_Registros_Detalhe_Negociacao': [
#             len(df_registro_B_15),
#             len(df_registro_B_15)
#         ],
#         'Status': [
#             'Encontrados' if len(df_registro_B_15) > 0 else 'Não encontrados',
#             'Consolidado'
#         ]
#     }
#     df_resumo = pd.DataFrame(resumo_data)
#     df_resumo.to_excel(
#         writer, sheet_name='Resumo_Detalhe_Negociacao', index=False)
#     print("✅ Aba 'Resumo_Detalhe_Negociacao' salva")

# print(f"🎯 Arquivo Excel do Registro B criado/atualizado com sucesso!")
# print(f"📊 Local: {caminho_completo_B}")
# print(
#     f"📋 Total de registros de detalhe de negociação salvos: {len(df_registro_B_15)}")

# # Verificar se o arquivo foi criado
# if os.path.exists(caminho_completo_B):
#     tamanho_arquivo = os.path.getsize(caminho_completo_B)
#     print(f"💾 Tamanho do arquivo: {tamanho_arquivo} bytes")
# else:
#     print("❌ Erro: Arquivo não foi criado!")

# print(f"\n🔗 Caminho completo do arquivo:")
# print(f"   {caminho_completo_B}")

# %%
# # Célula para processar registros do tipo C (Conta Recebimento) - apenas arquivos 15
# print("📊 PROCESSANDO REGISTROS TIPO C (CONTA RECEBIMENTO) - APENAS ARQUIVOS 15...")

# # DataFrame para registro C (só existe em arquivos 15)
# df_registro_C_15 = pd.DataFrame()

# processador_C = RegistroC()

# for arquivo in arquivos_cielo:
#     caminho_arquivo = os.path.join(local_folder, arquivo)

#     # Identificar o tipo de arquivo
#     tipo_arquivo = arquivo[5:7]

#     # Processar apenas arquivos tipo 15 (onde o registro C existe)
#     if tipo_arquivo == '15':
#         print(f"📁 Processando arquivo: {arquivo} (Tipo: {tipo_arquivo})")

#         try:
#             with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#                 linhas = file.readlines()

#                 for i, linha in enumerate(linhas):
#                     linha = linha.strip()
#                     if not linha:
#                         continue

#                     # Verificar se é registro tipo C
#                     if linha.startswith('C'):
#                         try:
#                             df_linha = processador_C.processar_linha(
#                                 linha, mostrar=False)
#                             df_linha['arquivo_origem'] = arquivo
#                             df_linha['tipo_arquivo'] = tipo_arquivo

#                             if df_registro_C_15.empty:
#                                 df_registro_C_15 = df_linha
#                             else:
#                                 df_registro_C_15 = pd.concat(
#                                     [df_registro_C_15, df_linha], ignore_index=True)

#                         except Exception as e:
#                             print(f"⚠️  Erro na linha {i+1}: {e}")

#         except Exception as e:
#             print(f"❌ Erro no arquivo {arquivo}: {e}")
#     else:
#         print(
#             f"⏭️  Pulando arquivo {arquivo} (Tipo: {tipo_arquivo}) - Registro C só existe em arquivos 15")

# # Exibir resultados
# print("\n" + "="*70)
# print("📈 RESULTADOS REGISTRO C (CONTA RECEBIMENTO) - ARQUIVOS 15:")
# print("="*70)

# print(f"\n✅ Registro C - Arquivos Tipo 15: {len(df_registro_C_15)} linhas")
# if not df_registro_C_15.empty:
#     display(df_registro_C_15)
# else:
#     print("   Nenhum registro encontrado")

# # Estatísticas finais
# print("\n" + "="*70)
# print("📊 ESTATÍSTICAS FINAIS REGISTRO C:")
# print("="*70)
# print(f"Total Registros C (Tipo 15): {len(df_registro_C_15)} registros")

# %%
# # Célula para salvar resultados do Registro C em Excel
# print("💾 SALVANDO RESULTADOS DO REGISTRO C (CONTA RECEBIMENTO) EM EXCEL...")

# # Usar a mesma pasta de resultados
# pasta_resultados = os.path.join(os.getcwd(), "resultados_analise")
# os.makedirs(pasta_resultados, exist_ok=True)

# # Nome fixo do arquivo para registro C
# nome_arquivo_C = "registro_C_conta_recebimento_analise.xlsx"
# caminho_completo_C = os.path.join(pasta_resultados, nome_arquivo_C)

# # Criar um ExcelWriter para salvar
# with pd.ExcelWriter(caminho_completo_C, engine='openpyxl') as writer:
#     # Salvar DataFrame do tipo 15
#     if not df_registro_C_15.empty:
#         df_registro_C_15.to_excel(
#             writer, sheet_name='Conta_Recebimento_15', index=False)
#         print("✅ Aba 'Conta_Recebimento_15' salva")
#     else:
#         pd.DataFrame().to_excel(writer, sheet_name='Conta_Recebimento_15', index=False)
#         print("ℹ️  Aba 'Conta_Recebimento_15' criada (vazia)")

#     # Criar uma aba de resumo
#     resumo_data = {
#         'Tipo_Arquivo': ['15', 'TOTAL'],
#         'Quantidade_Registros_Conta_Recebimento': [
#             len(df_registro_C_15),
#             len(df_registro_C_15)
#         ],
#         'Status': [
#             'Encontrados' if len(df_registro_C_15) > 0 else 'Não encontrados',
#             'Consolidado'
#         ]
#     }
#     df_resumo = pd.DataFrame(resumo_data)
#     df_resumo.to_excel(
#         writer, sheet_name='Resumo_Conta_Recebimento', index=False)
#     print("✅ Aba 'Resumo_Conta_Recebimento' salva")

# print(f"🎯 Arquivo Excel do Registro C criado/atualizado com sucesso!")
# print(f"📊 Local: {caminho_completo_C}")
# print(
#     f"📋 Total de registros de conta de recebimento salvos: {len(df_registro_C_15)}")

# # Verificar se o arquivo foi criado
# if os.path.exists(caminho_completo_C):
#     tamanho_arquivo = os.path.getsize(caminho_completo_C)
#     print(f"💾 Tamanho do arquivo: {tamanho_arquivo} bytes")
# else:
#     print("❌ Erro: Arquivo não foi criado!")

# print(f"\n🔗 Caminho completo do arquivo:")
# print(f"   {caminho_completo_C}")

# %%
# Célula para processar registros do tipo D (UR Agenda) - apenas arquivos 04 e 09
print("📊 PROCESSANDO REGISTROS TIPO D (UR AGENDA) - APENAS ARQUIVOS 04 E 09...")

# DataFrames separados por tipo de arquivo
df_registro_D_04 = pd.DataFrame()  # Para arquivos tipo 04
df_registro_D_09 = pd.DataFrame()  # Para arquivos tipo 09

processador_D = RegistroD()

for arquivo in arquivos_cielo:
    caminho_arquivo = os.path.join(local_folder, arquivo)

    # Identificar o tipo de arquivo
    tipo_arquivo = arquivo[5:7]

    # Processar apenas arquivos tipo 04 e 09 (onde o registro D existe)
    if tipo_arquivo in ['04', '09']:
        print(f"📁 Processando arquivo: {arquivo} (Tipo: {tipo_arquivo})")

        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                linhas = file.readlines()

                for i, linha in enumerate(linhas):
                    linha = linha.strip()
                    if not linha:
                        continue

                    # Verificar se é registro tipo D
                    if linha.startswith('D'):
                        try:
                            df_linha = processador_D.processar_linha(
                                linha, mostrar=False)
                            df_linha['arquivo_origem'] = arquivo
                            df_linha['tipo_arquivo'] = tipo_arquivo

                            # Adicionar ao DataFrame correspondente ao tipo de arquivo
                            if tipo_arquivo == '04':
                                if df_registro_D_04.empty:
                                    df_registro_D_04 = df_linha
                                else:
                                    df_registro_D_04 = pd.concat(
                                        [df_registro_D_04, df_linha], ignore_index=True)

                            elif tipo_arquivo == '09':
                                if df_registro_D_09.empty:
                                    df_registro_D_09 = df_linha
                                else:
                                    df_registro_D_09 = pd.concat(
                                        [df_registro_D_09, df_linha], ignore_index=True)

                        except Exception as e:
                            print(f"⚠️  Erro na linha {i+1}: {e}")

        except Exception as e:
            print(f"❌ Erro no arquivo {arquivo}: {e}")
    else:
        print(
            f"⏭️  Pulando arquivo {arquivo} (Tipo: {tipo_arquivo}) - Registro D só existe em arquivos 04 e 09")

# Exibir resultados
print("\n" + "="*70)
print("📈 RESULTADOS REGISTRO D (UR AGENDA) POR TIPO DE ARQUIVO:")
print("="*70)

print(f"\n✅ Registro D - Arquivos Tipo 04: {len(df_registro_D_04)} linhas")
if not df_registro_D_04.empty:
    display(df_registro_D_04.head(3))  # Mostrar primeiras linhas
else:
    print("   Nenhum registro encontrado")

print(f"\n✅ Registro D - Arquivos Tipo 09: {len(df_registro_D_09)} linhas")
if not df_registro_D_09.empty:
    display(df_registro_D_09.head(3))  # Mostrar primeiras linhas
else:
    print("   Nenhum registro encontrado")

# Estatísticas finais
print("\n" + "="*70)
print("📊 ESTATÍSTICAS FINAIS REGISTRO D:")
print("="*70)
print(f"Total Tipo 04: {len(df_registro_D_04)} registros")
print(f"Total Tipo 09: {len(df_registro_D_09)} registros")
print(
    f"TOTAL GERAL: {len(df_registro_D_04) + len(df_registro_D_09)} registros")

# %%
# Célula para salvar resultados do Registro D em Excel
print("💾 SALVANDO RESULTADOS DO REGISTRO D (UR AGENDA) EM EXCEL...")

# Usar a mesma pasta de resultados
pasta_resultados = os.path.join(os.getcwd(), "resultados_analise")
os.makedirs(pasta_resultados, exist_ok=True)

# Nome fixo do arquivo para registro D
nome_arquivo_D = "registro_D_ur_agenda_analise.xlsx"
caminho_completo_D = os.path.join(pasta_resultados, nome_arquivo_D)

# Criar um ExcelWriter para salvar múltiplas abas
with pd.ExcelWriter(caminho_completo_D, engine='openpyxl') as writer:
    # Salvar cada DataFrame em uma aba diferente
    if not df_registro_D_04.empty:
        df_registro_D_04.to_excel(
            writer, sheet_name='UR_Agenda_Tipo_04', index=False)
        print("✅ Aba 'UR_Agenda_Tipo_04' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='UR_Agenda_Tipo_04', index=False)
        print("ℹ️  Aba 'UR_Agenda_Tipo_04' criada (vazia)")

    if not df_registro_D_09.empty:
        df_registro_D_09.to_excel(
            writer, sheet_name='UR_Agenda_Tipo_09', index=False)
        print("✅ Aba 'UR_Agenda_Tipo_09' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='UR_Agenda_Tipo_09', index=False)
        print("ℹ️  Aba 'UR_Agenda_Tipo_09' criada (vazia)")

    # Criar uma aba de resumo
    resumo_data = {
        'Tipo_Arquivo': ['04', '09', 'TOTAL'],
        'Quantidade_Registros_UR_Agenda': [
            len(df_registro_D_04),
            len(df_registro_D_09),
            len(df_registro_D_04) + len(df_registro_D_09)
        ],
        'Status': [
            'Encontrados' if len(df_registro_D_04) > 0 else 'Não encontrados',
            'Encontrados' if len(df_registro_D_09) > 0 else 'Não encontrados',
            'Consolidado'
        ]
    }
    df_resumo = pd.DataFrame(resumo_data)
    df_resumo.to_excel(writer, sheet_name='Resumo_UR_Agenda', index=False)
    print("✅ Aba 'Resumo_UR_Agenda' salva")

print(f"🎯 Arquivo Excel do Registro D criado/atualizado com sucesso!")
print(f"📊 Local: {caminho_completo_D}")
print(
    f"📋 Total de registros UR Agenda salvos: {len(df_registro_D_04) + len(df_registro_D_09)}")

# Verificar se o arquivo foi criado
if os.path.exists(caminho_completo_D):
    tamanho_arquivo = os.path.getsize(caminho_completo_D)
    print(f"💾 Tamanho do arquivo: {tamanho_arquivo} bytes")
else:
    print("❌ Erro: Arquivo não foi criado!")

print(f"\n🔗 Caminho completo do arquivo:")
print(f"   {caminho_completo_D}")

# %%
# Célula para processar registros do tipo E (Detalhe Lançamento) - arquivos 03, 04, 09
print("📊 PROCESSANDO REGISTROS TIPO E (DETALHE LANÇAMENTO) - ARQUIVOS 03, 04, 09...")

# DataFrames separados por tipo de arquivo
df_registro_E_03 = pd.DataFrame()  # Para arquivos tipo 03
df_registro_E_04 = pd.DataFrame()  # Para arquivos tipo 04
df_registro_E_09 = pd.DataFrame()  # Para arquivos tipo 09

processador_E = RegistroE()

for arquivo in arquivos_cielo:
    caminho_arquivo = os.path.join(local_folder, arquivo)

    # Identificar o tipo de arquivo
    tipo_arquivo = arquivo[5:7]

    # Processar apenas arquivos tipo 03, 04 e 09 (onde o registro E existe)
    if tipo_arquivo in ['03', '04', '09']:
        print(f"📁 Processando arquivo: {arquivo} (Tipo: {tipo_arquivo})")

        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                linhas = file.readlines()

                for i, linha in enumerate(linhas):
                    linha = linha.strip()
                    if not linha:
                        continue

                    # Verificar se é registro tipo E
                    if linha.startswith('E'):
                        try:
                            df_linha = processador_E.processar_linha(
                                linha, mostrar=False)
                            df_linha['arquivo_origem'] = arquivo
                            df_linha['tipo_arquivo'] = tipo_arquivo

                            # Adicionar ao DataFrame correspondente ao tipo de arquivo
                            if tipo_arquivo == '03':
                                if df_registro_E_03.empty:
                                    df_registro_E_03 = df_linha
                                else:
                                    df_registro_E_03 = pd.concat(
                                        [df_registro_E_03, df_linha], ignore_index=True)

                            elif tipo_arquivo == '04':
                                if df_registro_E_04.empty:
                                    df_registro_E_04 = df_linha
                                else:
                                    df_registro_E_04 = pd.concat(
                                        [df_registro_E_04, df_linha], ignore_index=True)

                            elif tipo_arquivo == '09':
                                if df_registro_E_09.empty:
                                    df_registro_E_09 = df_linha
                                else:
                                    df_registro_E_09 = pd.concat(
                                        [df_registro_E_09, df_linha], ignore_index=True)

                        except Exception as e:
                            print(f"⚠️  Erro na linha {i+1}: {e}")

        except Exception as e:
            print(f"❌ Erro no arquivo {arquivo}: {e}")
    else:
        print(
            f"⏭️  Pulando arquivo {arquivo} (Tipo: {tipo_arquivo}) - Registro E só existe em arquivos 03, 04 e 09")

# 🔄 NOVO: FILTRAR LINHAS E REMOVER COLUNA sinal_valor_bruto
print("\n🔍 FILTRANDO REGISTROS E REMOVENDO COLUNA sinal_valor_bruto...")


def filtrar_registro_E(df):
    if not df.empty:
        # Contar linhas antes do filtro
        linhas_antes = len(df)

        # Filtrar linhas: remover onde sinal_valor_bruto = "-" E tipo_lancamento é "Aluguel de máquina" ou "Cancelamento de venda"
        condicao_remover = (
            (df['sinal_valor_bruto'] == '-') &
            (df['tipo_lancamento'].isin(
                ['Aluguel de máquina', 'Cancelamento de venda']))
        )

        # Manter as linhas que NÃO atendem à condição de remoção
        df_filtrado = df[~condicao_remover].copy()

        # Remover a coluna sinal_valor_bruto
        if 'sinal_valor_bruto' in df_filtrado.columns:
            df_filtrado = df_filtrado.drop(columns=['sinal_valor_bruto'])

        linhas_depois = len(df_filtrado)
        linhas_removidas = linhas_antes - linhas_depois

        print(f"   ↳ Linhas removidas: {linhas_removidas}")
        return df_filtrado
    return df


# Aplicar filtro para cada DataFrame
df_registro_E_03 = filtrar_registro_E(df_registro_E_03)
df_registro_E_04 = filtrar_registro_E(df_registro_E_04)
df_registro_E_09 = filtrar_registro_E(df_registro_E_09)

# Exibir resultados
print("\n" + "="*70)
print("📈 RESULTADOS REGISTRO E (DETALHE LANÇAMENTO) POR TIPO DE ARQUIVO:")
print("="*70)

print(f"\n✅ Registro E - Arquivos Tipo 03: {len(df_registro_E_03)} linhas")
if not df_registro_E_03.empty:
    display(df_registro_E_03.head(3))  # Mostrar primeiras linhas
else:
    print("   Nenhum registro encontrado")

print(f"\n✅ Registro E - Arquivos Tipo 04: {len(df_registro_E_04)} linhas")
if not df_registro_E_04.empty:
    display(df_registro_E_04.head(3))  # Mostrar primeiras linhas
else:
    print("   Nenhum registro encontrado")

print(f"\n✅ Registro E - Arquivos Tipo 09: {len(df_registro_E_09)} linhas")
if not df_registro_E_09.empty:
    display(df_registro_E_09.head(3))  # Mostrar primeiras linhas
else:
    print("   Nenhum registro encontrado")

# Estatísticas finais
print("\n" + "="*70)
print("📊 ESTATÍSTICAS FINAIS REGISTRO E:")
print("="*70)
print(f"Total Tipo 03: {len(df_registro_E_03)} registros")
print(f"Total Tipo 04: {len(df_registro_E_04)} registros")
print(f"Total Tipo 09: {len(df_registro_E_09)} registros")
print(
    f"TOTAL GERAL: {len(df_registro_E_03) + len(df_registro_E_04) + len(df_registro_E_09)} registros")

# %%
# Célula para salvar resultados do Registro E em Excel
print("💾 SALVANDO RESULTADOS DO REGISTRO E (DETALHE LANÇAMENTO) EM EXCEL...")

# Usar a mesma pasta de resultados
pasta_resultados = os.path.join(os.getcwd(), "resultados_analise")
os.makedirs(pasta_resultados, exist_ok=True)

# Nome fixo do arquivo para registro E
nome_arquivo_E = "registro_E_detalhe_lancamento_analise.xlsx"
caminho_completo_E = os.path.join(pasta_resultados, nome_arquivo_E)

# Criar um ExcelWriter para salvar múltiplas abas
with pd.ExcelWriter(caminho_completo_E, engine='openpyxl') as writer:
    # Salvar cada DataFrame em uma aba diferente
    if not df_registro_E_03.empty:
        df_registro_E_03.to_excel(
            writer, sheet_name='Detalhe_Lancamento_03', index=False)
        print("✅ Aba 'Detalhe_Lancamento_03' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Detalhe_Lancamento_03', index=False)
        print("ℹ️  Aba 'Detalhe_Lancamento_03' criada (vazia)")

    if not df_registro_E_04.empty:
        df_registro_E_04.to_excel(
            writer, sheet_name='Detalhe_Lancamento_04', index=False)
        print("✅ Aba 'Detalhe_Lancamento_04' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Detalhe_Lancamento_04', index=False)
        print("ℹ️  Aba 'Detalhe_Lancamento_04' criada (vazia)")

    if not df_registro_E_09.empty:
        df_registro_E_09.to_excel(
            writer, sheet_name='Detalhe_Lancamento_09', index=False)
        print("✅ Aba 'Detalhe_Lancamento_09' salva")
    else:
        pd.DataFrame().to_excel(writer, sheet_name='Detalhe_Lancamento_09', index=False)
        print("ℹ️  Aba 'Detalhe_Lancamento_09' criada (vazia)")

    # Criar uma aba de resumo
    resumo_data = {
        'Tipo_Arquivo': ['03', '04', '09', 'TOTAL'],
        'Quantidade_Registros_Detalhe_Lancamento': [
            len(df_registro_E_03),
            len(df_registro_E_04),
            len(df_registro_E_09),
            len(df_registro_E_03) + len(df_registro_E_04) + len(df_registro_E_09)
        ],
        'Status': [
            'Encontrados' if len(df_registro_E_03) > 0 else 'Não encontrados',
            'Encontrados' if len(df_registro_E_04) > 0 else 'Não encontrados',
            'Encontrados' if len(df_registro_E_09) > 0 else 'Não encontrados',
            'Consolidado'
        ]
    }
    df_resumo = pd.DataFrame(resumo_data)
    df_resumo.to_excel(
        writer, sheet_name='Resumo_Detalhe_Lancamento', index=False)
    print("✅ Aba 'Resumo_Detalhe_Lancamento' salva")

print(f"🎯 Arquivo Excel do Registro E criado/atualizado com sucesso!")
print(f"📊 Local: {caminho_completo_E}")
print(
    f"📋 Total de registros de detalhe de lançamento salvos: {len(df_registro_E_03) + len(df_registro_E_04) + len(df_registro_E_09)}")

# Verificar se o arquivo foi criado
if os.path.exists(caminho_completo_E):
    tamanho_arquivo = os.path.getsize(caminho_completo_E)
    print(f"💾 Tamanho do arquivo: {tamanho_arquivo} bytes")
else:
    print("❌ Erro: Arquivo não foi criado!")

print(f"\n🔗 Caminho completo do arquivo:")
print(f"   {caminho_completo_E}")

# %%
# # Célula para processar registros do tipo R (Reserva Financeira) - apenas arquivos 03 e 09
# print("📊 PROCESSANDO REGISTROS TIPO R (RESERVA FINANCEIRA) - APENAS ARQUIVOS 03 E 09...")

# # DataFrames separados por tipo de arquivo
# df_registro_R_03 = pd.DataFrame()  # Para arquivos tipo 03
# df_registro_R_09 = pd.DataFrame()  # Para arquivos tipo 09

# processador_R = RegistroR()

# for arquivo in arquivos_cielo:
#     caminho_arquivo = os.path.join(local_folder, arquivo)

#     # Identificar o tipo de arquivo
#     tipo_arquivo = arquivo[5:7]

#     # Processar apenas arquivos tipo 03 e 09 (onde o registro R existe)
#     if tipo_arquivo in ['03', '09']:
#         print(f"📁 Processando arquivo: {arquivo} (Tipo: {tipo_arquivo})")

#         try:
#             with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#                 linhas = file.readlines()

#                 for i, linha in enumerate(linhas):
#                     linha = linha.strip()
#                     if not linha:
#                         continue

#                     # Verificar se é registro tipo R
#                     if linha.startswith('R'):
#                         try:
#                             df_linha = processador_R.processar_linha(
#                                 linha, mostrar=False)
#                             df_linha['arquivo_origem'] = arquivo
#                             df_linha['tipo_arquivo'] = tipo_arquivo

#                             # Adicionar ao DataFrame correspondente ao tipo de arquivo
#                             if tipo_arquivo == '03':
#                                 if df_registro_R_03.empty:
#                                     df_registro_R_03 = df_linha
#                                 else:
#                                     df_registro_R_03 = pd.concat(
#                                         [df_registro_R_03, df_linha], ignore_index=True)

#                             elif tipo_arquivo == '09':
#                                 if df_registro_R_09.empty:
#                                     df_registro_R_09 = df_linha
#                                 else:
#                                     df_registro_R_09 = pd.concat(
#                                         [df_registro_R_09, df_linha], ignore_index=True)

#                         except Exception as e:
#                             print(f"⚠️  Erro na linha {i+1}: {e}")

#         except Exception as e:
#             print(f"❌ Erro no arquivo {arquivo}: {e}")
#     else:
#         print(
#             f"⏭️  Pulando arquivo {arquivo} (Tipo: {tipo_arquivo}) - Registro R só existe em arquivos 03 e 09")

# # Exibir resultados
# print("\n" + "="*70)
# print("📈 RESULTADOS REGISTRO R (RESERVA FINANCEIRA) POR TIPO DE ARQUIVO:")
# print("="*70)

# print(f"\n✅ Registro R - Arquivos Tipo 03: {len(df_registro_R_03)} linhas")
# if not df_registro_R_03.empty:
#     display(df_registro_R_03)
# else:
#     print("   Nenhum registro encontrado")

# print(f"\n✅ Registro R - Arquivos Tipo 09: {len(df_registro_R_09)} linhas")
# if not df_registro_R_09.empty:
#     display(df_registro_R_09)
# else:
#     print("   Nenhum registro encontrado")

# # Estatísticas finais
# print("\n" + "="*70)
# print("📊 ESTATÍSTICAS FINAIS REGISTRO R:")
# print("="*70)
# print(f"Total Tipo 03: {len(df_registro_R_03)} registros")
# print(f"Total Tipo 09: {len(df_registro_R_09)} registros")
# print(
#     f"TOTAL GERAL: {len(df_registro_R_03) + len(df_registro_R_09)} registros")

# %%
# # Célula para salvar resultados do Registro R em Excel
# print("💾 SALVANDO RESULTADOS DO REGISTRO R (RESERVA FINANCEIRA) EM EXCEL...")

# # Usar a mesma pasta de resultados
# pasta_resultados = os.path.join(os.getcwd(), "resultados_analise")
# os.makedirs(pasta_resultados, exist_ok=True)

# # Nome fixo do arquivo para registro R
# nome_arquivo_R = "registro_R_reserva_financeira_analise.xlsx"
# caminho_completo_R = os.path.join(pasta_resultados, nome_arquivo_R)

# # Criar um ExcelWriter para salvar múltiplas abas
# with pd.ExcelWriter(caminho_completo_R, engine='openpyxl') as writer:
#     # Salvar cada DataFrame em uma aba diferente
#     if not df_registro_R_03.empty:
#         df_registro_R_03.to_excel(
#             writer, sheet_name='Reserva_Financeira_03', index=False)
#         print("✅ Aba 'Reserva_Financeira_03' salva")
#     else:
#         pd.DataFrame().to_excel(writer, sheet_name='Reserva_Financeira_03', index=False)
#         print("ℹ️  Aba 'Reserva_Financeira_03' criada (vazia)")

#     if not df_registro_R_09.empty:
#         df_registro_R_09.to_excel(
#             writer, sheet_name='Reserva_Financeira_09', index=False)
#         print("✅ Aba 'Reserva_Financeira_09' salva")
#     else:
#         pd.DataFrame().to_excel(writer, sheet_name='Reserva_Financeira_09', index=False)
#         print("ℹ️  Aba 'Reserva_Financeira_09' criada (vazia)")

#     # Criar uma aba de resumo
#     resumo_data = {
#         'Tipo_Arquivo': ['03', '09', 'TOTAL'],
#         'Quantidade_Registros_Reserva_Financeira': [
#             len(df_registro_R_03),
#             len(df_registro_R_09),
#             len(df_registro_R_03) + len(df_registro_R_09)
#         ],
#         'Status': [
#             'Encontrados' if len(df_registro_R_03) > 0 else 'Não encontrados',
#             'Encontrados' if len(df_registro_R_09) > 0 else 'Não encontrados',
#             'Consolidado'
#         ]
#     }
#     df_resumo = pd.DataFrame(resumo_data)
#     df_resumo.to_excel(
#         writer, sheet_name='Resumo_Reserva_Financeira', index=False)
#     print("✅ Aba 'Resumo_Reserva_Financeira' salva")

# print(f"🎯 Arquivo Excel do Registro R criado/atualizado com sucesso!")
# print(f"📊 Local: {caminho_completo_R}")
# print(
#     f"📋 Total de registros de reserva financeira salvos: {len(df_registro_R_03) + len(df_registro_R_09)}")

# # Verificar se o arquivo foi criado
# if os.path.exists(caminho_completo_R):
#     tamanho_arquivo = os.path.getsize(caminho_completo_R)
#     print(f"💾 Tamanho do arquivo: {tamanho_arquivo} bytes")
# else:
#     print("❌ Erro: Arquivo não foi criado!")

# print(f"\n🔗 Caminho completo do arquivo:")
# print(f"   {caminho_completo_R}")

# %%
# Célula para enviar Registro E - Tipo 03 para PostgreSQL
print("🚀 ENVIANDO REGISTRO E - TIPO 03 PARA POSTGRESQL...")

try:
    # Configurações de conexão com PostgreSQL
    db_config = {
        'dbname': os.getenv('DB_NAME', 'estoque'),
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }

    # Verificar se as variáveis obrigatórias estão definidas
    if not all([db_config['user'], db_config['password']]):
        raise ValueError(
            "Variáveis DB_USERNAME ou DB_PASSWORD não definidas no arquivo .env")

    print(
        f"🔗 Conectando ao PostgreSQL: {db_config['user']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}")

    # Criar engine do SQLAlchemy
    connection_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(connection_string)

    # Nome da tabela no PostgreSQL
    table_name = 'cielo_sftp'

    # Verificar se o DataFrame não está vazio
    if not df_registro_E_03.empty:
        print(f"📊 Preparando {len(df_registro_E_03)} registros para envio...")

        # Limpar nomes de colunas (remover acentos e caracteres especiais)
        df_registro_E_03.columns = [unidecode(col).lower().replace(' ', '_').replace('/', '_').replace('-', '_')
                                    for col in df_registro_E_03.columns]

        # ✅ ABORDAGEM SIMPLES: SEMPRE SUBSTITUIR (CRIA SE NÃO EXISTIR)
        df_registro_E_03.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',  # ✅ Substitui se existir, cria se não existir
            index=False,
            method='multi',
            chunksize=1000
        )
        # append
        print(f"✅ Tabela '{table_name}' criada/substituída com sucesso!")
        print(f"   📋 Total de registros inseridos: {len(df_registro_E_03)}")

        # ✅ VERIFICAÇÃO SIMPLIFICADA (sem execute)
        # Podemos confiar que o to_sql funcionou, mas vamos fazer uma verificação simples
        print(f"   ✅ Processo de inserção concluído com sucesso!")

        # Verificação opcional usando pandas
        try:
            # Ler apenas a contagem diretamente com pandas
            count_query = f"SELECT COUNT(*) as total FROM {table_name}"
            count_df = pd.read_sql_query(count_query, engine)
            count_in_db = count_df['total'].iloc[0]
            print(f"   🔍 Registros confirmados no banco: {count_in_db}")
        except:
            print(
                "   ⚠️  Verificação de contagem não foi possível, mas os dados foram inseridos")

    else:
        print("ℹ️  Nenhum dado para enviar - DataFrame vazio")

except ImportError:
    print("❌ Erro: Biblioteca psycopg2 não instalada. Instale com: pip install psycopg2-binary")
except Exception as e:
    print(f"❌ Erro ao conectar/enviar para PostgreSQL: {e}")

# %%
# ============================
# Mover arquivos processados para a pasta 'processados'
# ============================
print("\n📂 MOVENDO ARQUIVOS PROCESSADOS PARA A PASTA 'processados'...")


pasta_arquivos = os.path.join(os.getcwd(), "arquivos")
pasta_processados = os.path.join(pasta_arquivos, "processados")

# Criar a pasta 'processados' caso não exista
os.makedirs(pasta_processados, exist_ok=True)

if os.path.exists(pasta_arquivos):
    for nome in os.listdir(pasta_arquivos):
        caminho_antigo = os.path.join(pasta_arquivos, nome)

        # Ignorar diretórios (inclusive a própria pasta 'processados')
        if os.path.isdir(caminho_antigo):
            continue

        # Novo caminho dentro da pasta 'processados'
        caminho_novo = os.path.join(pasta_processados, nome)

        # Mover o arquivo
        shutil.move(caminho_antigo, caminho_novo)
        print(f"✅ Movido: {nome} -> processados/{nome}")
else:
    print("⚠️ A pasta 'arquivos' não existe.")

import sys
import os
import logging
import subprocess

libs_path = os.path.join(os.path.dirname(__file__), 'libs')
sys.path.insert(0, libs_path)

try:
    import pdfplumber
    import markdownify
except ImportError:
    print("📦 Instalando dependências localmente...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "--target=./libs", "pdfplumber", "markdownify"
    ])
    print("✅ Instalação concluída. Continuando...\n")
    import pdfplumber
    import markdownify

logging.getLogger("pdfminer").setLevel(logging.ERROR)
logging.getLogger("pdfplumber").setLevel(logging.ERROR)
logging.getLogger("PyPDF2").setLevel(logging.ERROR)

os.makedirs('pdf', exist_ok=True)
os.makedirs('markdown', exist_ok=True)

arquivos_pdf = [f for f in os.listdir('pdf') if f.lower().endswith('.pdf')]

if not arquivos_pdf:
    print("📂 A pasta 'pdf/' está vazia. Coloque arquivos .pdf e execute novamente.")
    sys.exit()

os.system("clear")

for nome_arquivo in arquivos_pdf:
    caminho_pdf = os.path.join('pdf', nome_arquivo)
    nome_md = os.path.splitext(nome_arquivo)[0] + '.md'
    caminho_md = os.path.join('markdown', nome_md)

    if os.path.exists(caminho_md):
        print(f'ℹ️  Já convertido: {nome_md}')
        continue

    print(f'🔄 Convertendo: {nome_arquivo}')
    with pdfplumber.open(caminho_pdf) as pdf:
        total = len(pdf.pages)
        texto = ''
        for i, page in enumerate(pdf.pages):
            texto += page.extract_text() or ''
            progresso = int(((i + 1) / total) * 100)
            if progresso % 10 == 0 or progresso == 100:
                print(f'   Progresso: {progresso}%', end='\r')

    if not texto.strip():
        print(f'\n⚠️  Aviso: o arquivo \"{nome_arquivo}\" está vazio ou sem texto extraível. Ignorado.')
        continue

    markdown = markdownify.markdownify(texto, heading_style="ATX")

    with open(caminho_md, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f'\n✅ Concluído: {nome_md}')
import re
import subprocess

def extract_urls_and_run_linkfinder(wordlist_path):
    # Lista para armazenar os caminhos completos das URLs
    paths = []

    # Regex para extrair o caminho completo da URL
    regex = r"https?://[^\s]+"

    # Comando para executar o linkfinder
    linkfinder_command = "python linkfinder.py -i {} -o results.html"

    # Abrir o arquivo wordlist e aplicar o regex em cada linha
    with open(wordlist_path, 'r') as file:
        for line in file:
            match = re.search(regex, line)
            if match:
                url = match.group()
                # Executa o linkfinder para a URL atual
                subprocess.run(linkfinder_command.format(url), shell=True)
                paths.append(url)

    return paths

# Exemplo de uso:
wordlist_path = "subd_up.txt"  # Substitua pelo caminho real da sua wordlist
paths = extract_urls_and_run_linkfinder(wordlist_path)
for path in paths:
    print(path)

import subprocess
import os
import re
import sys

def subfinder(dmn, r_lim=100, n_thrds=100):
    subs = []  # Lista para armazenar os subdomínios encontrados
    subf_cmd = [
        "subfinder",
        "-d", dmn,
        "-rl", str(r_lim),
        "-t", str(n_thrds),
        "--recursive",
        "-nW",
        "-silent"
    ]

    temp_file = "tmp_subs.txt"
    try:
        # Executando o comando Subfinder e salvando a saída em um arquivo temporário
        with open(temp_file, 'w') as f:
            subprocess.run(subf_cmd, check=True, stdout=f, stderr=subprocess.PIPE, text=True)
        
        # Ordenando e removendo duplicatas do arquivo temporário
        subprocess.run(["sort", "-o", temp_file, temp_file])
        subprocess.run(["uniq", "-i", "-u", temp_file])  # Removendo a opção '-o'

        # Lendo o arquivo temporário para obter os subdomínios únicos
        with open(temp_file, 'r') as f:
            subs = f.read().split('\n')

    except Exception as e:
        print(f"Erro ao executar o subfinder: {e}")
        sys.exit(1)
    finally:
        # Removendo o arquivo temporário
        os.remove(temp_file)

    return subs  # Retorna a lista de subdomínios encontrados

def httpx(subs, output_file):
    if not subs:
        print("Nenhum subdomínio encontrado.")
        sys.exit(1)

    # Escrevendo os subdomínios em um arquivo temporário
    temp_file = "tmp_subs_httpx.txt"
    with open(temp_file, 'w') as f:
        f.write('\n'.join(subs))

    httpx_cmd = [
        "httpx",
        "-l", temp_file,
        "-title", "-wc", "-sc", "-cl", "-location", "-web-server", "-asn",
        "-fc", "404",
        "-o", output_file,
        "-silent"
    ]

    try:
        # Executando o comando HTTPX
        subprocess.run(httpx_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Erro ao executar o httpx: {e}")
        sys.exit(1)
    finally:
        # Removendo o arquivo temporário
        os.remove(temp_file)

def extract_domain(url):
    url = url.strip().rstrip('/')
    match = re.match(r'https?://(?:www\.)?([^/]+\.[a-zA-Z0-9.-]+)', url)  # Ajuste no padrão de regex
    if match:
        return match.group(1)
    else:
        return ""  # Retorna uma string vazia se a extração falhar

def extract_full_urls(httpx_output, output_file):
    with open(output_file, 'w') as f:
        for line in httpx_output:
            full_url = line.split()[0]
            f.write(full_url + '\n')

def gen_wayback(wordlist_file, output_file):
    wayback_cmd = ["waybackurls", "<", wordlist_file, ">>", output_file]
    try:
        # Executando o comando waybackurls < wordlist_file >> output_file
        subprocess.run(" ".join(wayback_cmd), shell=True, check=True)
    except Exception as e:
        print(f"Erro ao executar waybackurls: {e}")
        sys.exit(1)

def paramspider(wordlist_file, output_file):
    paramspider_cmd = ["paramspider", "-d", wordlist_file, "-o", output_file]
    try:
        # Executando o comando paramspider -d wordlist_file -o output_file
        subprocess.run(paramspider_cmd, check=True)
    except Exception as e:
        print(f"Erro ao executar paramspider: {e}")
        sys.exit(1)

def gf_xss(wordlist_file, output_file):
    gf_cmd = [
        "cat", wordlist_file,
        "|", "gf", "xss",
        "|", "sed", "'s/=.*/=/'",
        "|", "sed", "'s/URL: //'",
        ">", output_file
    ]
    try:
        # Executando o comando cat wordlist | gf xss | sed 's/=.*/=/' | sed 's/URL: //' > xss.txt
        subprocess.run(" ".join(gf_cmd), shell=True, check=True)
    except Exception as e:
        print(f"Erro ao executar gf xss: {e}")
        sys.exit(1)

def rem_duplicates(wordlist_file):
    try:
        # Ordenando e removendo duplicatas do arquivo temporário
        subprocess.run(["sort", "-o", wordlist_file, wordlist_file])
        subprocess.run(["uniq", "-i", "-u", wordlist_file])  # Removendo a opção '-o'
    except Exception as e:
        print(f"Erro ao remover duplicatas: {e}")
        sys.exit(1)

def run_linkfinder(urls_file, output_file):
    with open(urls_file, 'r') as f:
        urls = f.readlines()

    for url in urls:
        linkfinder_cmd = [
            "python", "linkfinder.py",
            "-i", url.strip(),
            "-o", output_file
        ]
        try:
            subprocess.run(linkfinder_cmd, check=True)
        except Exception as e:
            print(f"Erro ao executar linkfinder para {url}: {e}")
            sys.exit(1)

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "-d":
        print("Uso: python3 main.py -d <domínio>")
        sys.exit(1)

    domain = sys.argv[2]

    # Encontrar subdomínios
    subdomains = subfinder(domain)  # Obtém os subdomínios encontrados (com r_limit=100 e n_threads=100)
    output_file = "subd_up.txt"
    httpx(subdomains, output_file)

    # Gerar lista de URLs únicas
    wordlist_temp_file = "wlist_tmp.txt"
    with open(wordlist_temp_file, "w") as f:
        for subdomain in subdomains:
            domain = extract_domain(subdomain)
            if domain:
                f.write(domain + "\n")

    # Obter URLs do Wayback Machine
    waybackurls_output_file = "waybackurls.txt"
    gen_wayback(wordlist_temp_file, waybackurls_output_file)

    # Executar o ParamSpider usando a mesma lista de URLs gerada pelo Waybackurls
    paramspider_output_file = "paramspider_output.txt"
    paramspider(waybackurls_output_file, paramspider_output_file)

    # Remover duplicatas
    rem_duplicates(paramspider_output_file)

    # Executar o comando gf xss
    xss_output_file = "xss.txt"
    gf_xss(paramspider_output_file, xss_output_file)

    # Executar o LinkFinder
    linkfinder_output_file = "linkfinder_results.html"
    run_linkfinder(waybackurls_output_file, linkfinder_output_file)

    # Salvar a saída do LinkFinder em uma wordlist
    with open("wordlist_linkfinder.txt", "w") as f:
        with open(linkfinder_output_file, "r") as lf:
            f.write(lf.read())

if __name__ == "__main__":
    main()

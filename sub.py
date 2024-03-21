sys
import subprocess
import os
import re

def run_subfinder(domain, r_limit=100, n_threads=5):
    subfinder_cmd = [
        "subfinder",
        "-d", domain,
        "-rl", str(r_limit),
        "-t", str(n_threads),
        "--recursive",
        "-nW",
        "-silent",
        "-o", "subdomains.txt"  # Especificando o arquivo de saída do subfinder
    ]

    try:
        subprocess.run(subfinder_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Erro ao executar o subfinder: {e}")
        sys.exit(1)

def run_httpx(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Arquivo {input_file} não encontrado.")
        sys.exit(1)

    httpx_cmd = [
        "httpx",
        "-l", input_file,
        "-title", "-wc", "-sc", "-cl", "-location", "-web-server", "-asn",
        "-fc", "404",  
        "-o", output_file,
        "-silent"  
    ]

    try:
        subprocess.run(httpx_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Erro ao executar o httpx: {e}")
        sys.exit(1)

def extract_domain(url):
    url = url.strip().rstrip('/')
    
    match = re.match(r'https?://(?:www\.)?([^/]+\.[a-zA-Z0-9.]+)', url)
    if match:
        return match.group(1)
    else:
        return None

def scan_with_nmap(subdomain, folder_name):
    domain = extract_domain(subdomain)
    if domain is None:
        print(f'URL inválido: {subdomain}')
        return
    
    command = f'nmap -F -sV --script vulners {domain}'
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        folder_path = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        with open(os.path.join(folder_path, 'nmap.txt'), 'a') as f:
            f.write(f'=== Resultados para {domain} ===\n')
            f.write(result.stdout)
            f.write('\n\n')
    else:
        print(f'Erro ao escanear {domain}: {result.stderr}')

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "-d":
        print("Uso: python3 main.py -d <domínio>")
        sys.exit(1)

    domain = sys.argv[2]
    folder_name = domain.split('.')[0]  # Extrai o nome da pasta do domínio

    r_limit = input("Enter number of threads (default: 100):  ")
    n_threads = input("Enter number of threads (default: 5):  ")

    r_limit = int(r_limit) if r_limit.isdigit() else 100
    n_threads = int(n_threads) if n_threads.isdigit() else 5

    run_subfinder(domain, r_limit, n_threads)

    input_file = "subdomains.txt"  
    output_file = "subdomain_is_up.txt"  
    run_httpx(input_file, output_file)

    if os.path.exists(output_file):  
        with open(output_file, 'r') as f:
            subdomains = f.readlines()
        
        for subdomain in subdomains:
            subdomain = subdomain.strip()
            scan_with_nmap(subdomain, folder_name)
    else:
        print(f"Erro: O arquivo {output_file} não foi encontrado.")

if __name__ == "__main__":
    main()
" 

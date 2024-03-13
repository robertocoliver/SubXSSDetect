import sys
import subprocess
import os
import re

def run_sf(dom, rl=100, nt=5):
    sf_cmd = [
        "subfinder",
        "-d", dom,
        "-rl", str(rl),
        "-t", str(nt),
        "-o", "wlist.txt",
        "--recursive",
        "-nW",
        "-silent"
    ]

    try:
        subprocess.run(sf_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        sort_cmd = ["sort", "wlist.txt"]
        uniq_cmd = ["uniq"]
        sort_p = subprocess.Popen(sort_cmd, stdout=subprocess.PIPE)
        uniq_p = subprocess.run(uniq_cmd, stdin=sort_p.stdout, text=True, check=True)
        
    except Exception as e:
        pass

def run_hx(inp_file, out_file):
    hx_cmd = [
        "httpx",
        "-l", inp_file,
        "-title", "-wc", "-sc", "-cl", "-location", "-web-server", "-asn",
        "-fc", "404",  
        "-o", out_file,
        "-silent"  
    ]

    try:
        subprocess.run(hx_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        pass

def extr_dom(url):
    url = url.strip().rstrip('/')
    
    match = re.match(r'https?://(?:www\.)?([^/]+\.[a-zA-Z0-9.]+)', url)
    if match:
        return match.group(1)
    else:
        return None

def scan_with_nmap(subdom):
    dom = extr_dom(subdom)
    if dom is None:
        print(f'URL inválido: {subdom}')
        return
    
    command = f'nmap -F -sV --script vulners {dom}'
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        if not os.path.exists('vuln'):
            os.makedirs('vuln')
        
        with open(os.path.join('vuln', 'vuln.txt'), 'a') as f:
            f.write(f'=== Resultados para {dom} ===\n')
            f.write(result.stdout)
            f.write('\n\n')
    else:
        print(f'Erro ao escanear {dom}: {result.stderr}')

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "-d":
        sys.exit(1)

    domain = sys.argv[2]

    rl = input("Enter number of threads (default: 100):  ")
    nt = input("Enter number of threads (default: 5):  ")

    rl = int(rl) if rl.isdigit() else 100
    nt = int(nt) if nt.isdigit() else 5

    run_sf(domain, rl, nt)

    inp_file = "wlist.txt"
    out_file = "up-sd.txt"
    run_hx(inp_file, out_file)

    with open('up-sd.txt', 'r') as f:
        subdomains = f.readlines()
    
    for subdom in subdomains:
        subdom = subdom.strip()
        scan_with_nmap(subdom)

if __name__ == "__main__":
    main()


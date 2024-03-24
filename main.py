import subprocess
import os
import re
import sys
import shutil

def subfinder(dmn, r_lim=100, n_thrds=100):
    subs = []
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
        with open(temp_file, 'w') as f:
            subprocess.run(subf_cmd, check=True, stdout=f, stderr=subprocess.PIPE, text=True)

        subprocess.run(["sort", "-o", temp_file, temp_file])
        subprocess.run(["uniq", "-i", "-u", temp_file])
        with open(temp_file, 'r') as f:
            subs = f.read().split('\n')

    except:
        pass
    finally:
        os.remove(temp_file)

    return subs

def httpx(subs, output_file):
    if not subs:
        sys.exit(1)

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
        subprocess.run(httpx_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        pass
    finally:
        os.remove(temp_file)

def extract_domain(httpx_output_file, output_wordlist):
    domains = set()
    with open(httpx_output_file, 'r') as f:
        for line in f:
            match = re.search(r'https?://(?:www\.)?([^/\s]+\.[a-zA-Z0-9.-]+)', line)
            if match:
                domain = match.group(1)
                domains.add(domain)

    with open(output_wordlist, 'w') as f:
        for domain in domains:
            f.write(domain + '\n')

def run_paramspider(wordlist_file):
    paramspider_cmd = ["paramspider", "-l", wordlist_file]
    try:
        subprocess.run(paramspider_cmd, check=True)
    except:
        pass

def combine_wordlists_from_results_folder():
    results_dir = "results"
    output_wordlist = "combined_wordlist.txt"
    with open(output_wordlist, 'wb') as wfd:
        for subdir, _, files in os.walk(results_dir):
            for file in files:
                with open(os.path.join(subdir, file), 'rb') as fd:
                    shutil.copyfileobj(fd, wfd)

def gen_wayback(wordlist_file, output_file):
    wayback_cmd = ["cat", wordlist_file, "|", "waybackurls", ">", output_file]
    try:
        subprocess.run(" ".join(wayback_cmd), shell=True, check=True)
    except:
        pass

def main():
    if len(sys.argv) != 4 or sys.argv[1] != "-d":
        sys.exit(1)

    domain = sys.argv[2]
    output_wordlist = sys.argv[3]

    subdomains = subfinder(domain)
    output_file = "subd_up.txt"
    httpx(subdomains, output_file)

    extract_domain(output_file, output_wordlist)

    run_paramspider(output_wordlist)
    combine_wordlists_from_results_folder()

    gen_wayback(output_wordlist, "wayback_wordlist.txt")

if __name__ == "__main__":
    main()



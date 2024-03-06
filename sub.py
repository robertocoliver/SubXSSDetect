import sys
import subprocess

def run_sf(domain, rl=100, nt=5):
    sf_cmd = [
        "subfinder",
        "-d", domain,
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

def run_hx(input_file, output_file):
    hx_cmd = [
        "httpx",
        "-l", input_file,
        "-title", "-wc", "-sc", "-cl", "-location", "-web-server", "-asn",
        "-fc", "404",  
        "-o", output_file,
        "-silent"  
    ]

    try:
        subprocess.run(hx_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        pass

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "-d":
        sys.exit(1)

    domain = sys.argv[2]

    rl = input("Enter recursion limit (default: 100): ")
    nt = input("Enter number of threads (default: 5): ")

    rl = int(rl) if rl.isdigit() else 100
    nt = int(nt) if nt.isdigit() else 5

    run_sf(domain, rl, nt)

    input_file = "wlist.txt"
    output_file = "up-sd.txt"
    run_hx(input_file, output_file)

if __name__ == "__main__":
    main()

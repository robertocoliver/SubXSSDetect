# SubXSSDetect

I created this script to automate tasks involving the use of various tools for reconnaissance, asset verification, open ports, and vulnerability scanning. In a real penetration testing scenario, in certain contexts, it is necessary to automate certain tasks to avoid making them excessively exhaustive. Therefore, I developed this script that performs subdomain recognition, checks responsiveness, obtains information about open ports and services, acting as a vulnerability scanner. Additionally, it extracts endpoints to test potential injection vulnerabilities.

This script automates the process of subdomain recognition, integrating the Subfinder and HTTPX tools to identify active hosts. After the initial phase, nmap is employed to gather information about services, including versions and open ports. Lua automation is incorporated to optimize specific tasks. Subsequently, the script uses waybackurls for crawling, while GF by tomnomnom is employed to extract significant endpoints. The final phase involves the use of nuclei, including updated templates, to check for the presence of known vulnerabilities in web applications.

## How to Use?

Clone the repository
```bash
  git clone https://github.com/robertocoliver/SubXSSDetect
```
Enter the directory
```bash
  cd SubXSSDetect
```
Execute the tool
```bash
  python3 main.py -d google.com url.txt  
```

## Technology Used:
- **Python** 

## License
[MIT](https://choosealicense.com/licenses/mit/)

## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/robertocoliver/)
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://medium.com/@robertocoliver)

#### Legal Disclaimer
>  As this software automates enumeration, asset verification, and vulnerability scanning in an automated manner, caution must be exercised with the target host. The user may be held legally responsible through judicial means for any damages incurred;

>  It is the end user's responsibility to comply with all applicable local, state, and federal laws;

>  The author assumes no responsibility and is not liable for any misuse or damage caused by this tool.

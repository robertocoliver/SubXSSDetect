#!/bin/bash

# Instala httpx:
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/tomnomnom/waybackurls@latest

# Adicionar o diretório bin do Go ao PATH:
export PATH=$PATH:/root/go/bin


#Instale dependências:
pip install -r requirements.txt

"""
ASN Lookup Tool - Flask Web Application

Uma aplicação web para consulta de informações ASN (Autonomous System Number)
através de endereços IP ou nomes de domínio usando a API do IPinfo.

Copyright (c) 2025 Renylson Marques - Todos os direitos reservados
Este código é disponibilizado apenas para visualização e fins educacionais.
Qualquer uso comercial ou redistribuição requer autorização expressa.

Autor: Renylson Marques
Email: renylsonm@gmail.com
GitHub: github.com/renylson
LinkedIn: linkedin.com/in/renylsonmarques
"""

from flask import Flask, request, render_template, send_from_directory
import requests
import socket
import re
from urllib.parse import urlparse
import os


app = Flask(__name__)

# Configuração da API Key do IPinfo
# IMPORTANTE: Substitua 'XXXXXXXXXXXX' pela sua API key real
API_KEY = 'XXXXXXXXXXXX'

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve arquivos estáticos como CSS, imagens, etc."""
    return send_from_directory('.', filename)


def get_ip_info(ip):
    """
    Obtém informações detalhadas sobre um endereço IP usando a API do IPinfo.
    
    Args:
        ip (str): Endereço IP para consulta
        
    Returns:
        dict: Informações do IP incluindo ASN, ISP, localização, etc.
    """
    url = f'https://ipinfo.io/{ip}/json?token={API_KEY}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Erro na consulta da API: {str(e)}"}


def extract_ip_from_cidr(cidr):
    """
    Extrai o endereço IP de uma notação CIDR.
    
    Args:
        cidr (str): Endereço em notação CIDR (ex: 192.168.1.1/24)
        
    Returns:
        str: Endereço IP extraído
    """
    return cidr.split('/')[0]


def resolve_domain_to_ip(domain):
    """
    Resolve um nome de domínio para seu endereço IP correspondente.
    
    Args:
        domain (str): Nome do domínio para resolver
        
    Returns:
        str or None: Endereço IP resolvido ou None se houver erro
    """
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.error as e:
        print(f"Erro ao resolver domínio {domain}: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal da aplicação.
    
    GET: Exibe a página inicial com formulário
    POST: Processa as consultas de IP/domínio e exibe resultados
    """
    if request.method == 'POST':
        input_data = request.form.get('ips', '').strip()
        
        if not input_data:
            return render_template('index.html', error="Por favor, insira pelo menos um IP ou domínio.")
        

        items = [item.strip() for item in input_data.split(',') if item.strip()]
        results = []

        for item in items:
            parsed_url = urlparse(item)
            domain = parsed_url.netloc or parsed_url.path
            
            if re.match(r'^[a-zA-Z0-9.-]+$', domain) and '.' in domain:
    
                ip = resolve_domain_to_ip(domain)
                if ip:
                    print(f"Resolvendo domínio {domain} para IP {ip}")
                    item_info = {
                        'original_input': item,
                        'domain': domain,
                        'resolved_ip': ip
                    }
                else:
                    results.append({
                        "error": f"Não foi possível resolver o domínio: {domain}",
                        "original_input": item
                    })
                    continue
            else:

                ip = extract_ip_from_cidr(item)
                item_info = {
                    'original_input': item,
                    'ip': ip
                }


            try:
                ip_data = get_ip_info(ip)
                

                final_result = {**item_info, **ip_data}
                results.append(final_result)
                
            except Exception as e:
                results.append({
                    "error": f"Erro ao consultar IP {ip}: {str(e)}",
                    "original_input": item
                })

        return render_template('results.html', results=results)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

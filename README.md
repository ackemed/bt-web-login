# bt-web-login

bt-web-login
Este repositório contém uma ferramenta de brute force para formulário de login em aplicações web, desenvolvida em Python, com suporte para HTTP.

Funcionalidade
Brute force em formulários de login web.
Suporte para requisições HTTP.
Pré-requisitos
Python 3
Módulo requests
Módulo threading
Módulo argparse
Módulo pyfiglet
Instalação
Clone este repositório: git clone https://github.com/seu_usuario/bt-web-login.git
Navegue até o diretório do repositório: cd bt-web-login
Instale as dependências: pip install -r requirements.txt
Uso
css
Copy code
python bc_bruteforce-web-login.py -w WORDLIST -t NUM_THREADS -u USERNAME [-d DELAY]
Opções:
-w, --wordlist: Caminho para a wordlist contendo as senhas.
-t, --num_threads: Quantidade de threads para enviar as requisições em cada lote.
-u, --username: Nome de usuário para enviar as requisições.
-d, --delay: Atraso entre os lotes de requisições (em segundos).
Exemplo de Uso
Copy code
python bc_bruteforce-web-login.py -w passwords.txt -t 10 -u admin -d 0.5
Este comando envia requisições POST com uma lista de senhas do arquivo passwords.txt, utilizando 10 threads em cada lote, com o nome de usuário "admin" e um atraso de 0.5 segundos entre os lotes de requisições.

Contribuição
Contribuições são bem-vindas! Antes de enviar uma pull request, certifique-se de que sua contribuição esteja alinhada com o objetivo deste projeto. Por favor, discuta quaisquer mudanças importantes que você gostaria de fazer.

Licença
Este projeto é licenciado sob a [Inserir licença]. Veja o arquivo LICENSE para mais detalhes.

Aviso Legal
Este software é fornecido apenas para fins educacionais e de teste. O uso deste software para qualquer outra finalidade é de responsabilidade do usuário. O autor não se responsabiliza por qualquer uso indevido deste software.

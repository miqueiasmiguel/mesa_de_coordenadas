PROJETO PARA CONTROLE DA MESA DE COORDENADAS DO LAC

Desenvolvedores: - Bruno
                 - Elizabeth
                 - Miquéias



Configurações Iniciais:
====================================================================

- Instale o módulo para criação de ambiente virtual utilizando
  o comando 'pip3 install virtualenv'

- Em seguida, dentro da pasta destinada ao projeto, crie um ambiente
  virtual usando o comando 'virtualenv -p python3 venv'

- Utilizando o terminal, entre na pasta destinada ao projeto e
  execute o comando 'start venv\Scripts\activate' para ativar
  o ambiente virtual

- Instale as dependencias do projeto com o comando 
  'pip3 install -r requirements.txt'

- Instale o pre-commit com 'pre-commit install'

- Para criar um banco de dados, rode o script 'create_db.py', pois
  o bando de dados NÃO é compartilhado.
====================================================================


Algumas Informações:
====================================================================
- Os arquivos '.flake8', '.pre-commit-config.yaml' e ''.pylintrc'
  são arquivos de configuração de alguns módulos instalados.

- A pasta "flaskr" armazena todos os aqruivos relacionados ao flask.

- A pasta serial_modules refere-se aos aquivos relacionados à comu-
  nicação serial.
====================================================================

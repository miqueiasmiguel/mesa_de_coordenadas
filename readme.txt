PROJETO PARA CONTROLE DA MESA DE COORDENADAS DO LAC

Desenvolvedores: - Bruno
                 - Elizabeth
                 - Miquéias


Configurações Iniciais:
====================================================================================================
- Crie uma pasta chamada "Mesa de Coordenadas"

- Instale o módulo para criação de ambiente virtual utilizando
  o comando 'pip3 install virtualenv'

- Em seguida, dentro da pasta "Mesa de Coordenadas", crie um ambiente
  virtual usando o comando 'virtualenv -p python3 venv'

- Utilizando o terminal, entre na pasta "Mesa de Coordenadas" e
  execute o comando 'start venv\Scripts\activate' para ativar
  o ambiente virtual

- Instale as dependencias do projeto com o comando 
  'pip3 install -r requirements.txt'

- Instale o pre-commit com 'pre-commit install' (apenas se pretende alterar o repositório)

- Para criar um banco de dados, rode o script 'Mesa de Coordenadas/database/config/create_db.py'

- Rode o servidor executando o arquivo 'run.py'

- Como não há nenhum usuário cadastrado, você não terá acesso ao sistema. Vá para o arquivo
  'flaskr/routes.py'. Na linha 210 comente os decoradores '@login_required' e @required_roles.
  Isso possibilitará a criação de um primeiro usuário na url 'localhost:5000/register'. Em
  seguida, retire o comentário para que esta página só seja acessível por meio de login e
  que seja um usuário especial.
====================================================================================================


Algumas Informações:
====================================================================================================
- Os arquivos '.flake8', '.pre-commit-config.yaml' e ''.pylintrc'
  são arquivos de configuração de alguns módulos instalados.

- A pasta "database" refere-se aos arquivos de banco de dados

- A pasta "flaskr" armazena todos os aqruivos relacionados ao flask.

- A pasta serial_modules refere-se aos aquivos relacionados à comu-
  nicação serial.
====================================================================================================

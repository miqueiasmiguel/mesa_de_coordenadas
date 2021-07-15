PROJETO PARA CONTROLE DA MESA DE COORDENADAS DO LAC

Desenvolvedores: - Bruno
                 - Elizabeth
                 - Miquéias


Configurações Iniciais:
====================================================================================================
- Instale o módulo para criação de ambiente virtual utilizando
  o comando 'pip3 install virtualenv'

- Em seguida, dentro da pasta "mesa_de_coordenadas", crie um ambiente
  virtual usando o comando 'virtualenv -p python3 venv'

- Utilizando o terminal, entre na pasta "mesa_de_coordenadas" e
  execute o comando 'start venv\Scripts\activate' (caso seja um usuário
  de windows) para ativar o ambiente virtual. Caso seja Linux, o comando
  para ativar o ambiente virtual é diferente. Pesquise.

- Instale as dependencias do projeto com o comando 
  'pip3 install -r requirements.txt'

- Instale o pre-commit com 'pre-commit install' (apenas se pretende alterar o repositório).

- Para criar um banco de dados, rode o script 'src/database/config/create_db.py'

- Rode o servidor executando o arquivo 'run.py'

- Como não há nenhum usuário cadastrado, você não terá acesso ao sistema. Vá para o arquivo
  'flaskr/routes.py'. Na linha 210 comente os decoradores '@login_required' e @required_roles'.
  Isso possibilitará a criação de um primeiro usuário na url 'localhost:5000/register'. Em
  seguida, retire o comentário para que esta página só seja acessível apenas por meio de login e
  que seja necessário ser um usuário especial.
====================================================================================================


Algumas Informações:
====================================================================================================
- Os arquivos '.flake8', '.pre-commit-config.yaml' e ''.pylintrc'
  são arquivos de configuração de alguns módulos instalados.
====================================================================================================

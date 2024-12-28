Painel de Senhas

Este projeto é uma aplicação web simples para gerenciamento de senhas em um ambiente de atendimento. Ele foi desenvolvido como parte de um trabalho escolar e possui uma implementação básica, com algumas limitações e trechos de código repetido, visando a simplicidade e rapidez de desenvolvimento. O deploy foi realizado na plataforma Render.

Demonstração

Você pode acessar uma demonstração funcional do projeto clicando aqui. 

Funcionalidades

Recepção: Geração de senhas normais ou prioritárias.

Atendimento: Gerenciamento de clientes em fila, com opções de chamada, repetição, marcação como ausente ou finalização do atendimento.

Painel: Exibição da próxima senha a ser atendida.

Tecnologias Utilizadas

Frontend: HTML, CSS e JavaScript.

Backend: Python com Flask e Flask-SocketIO.

Banco de Dados: SQLite para armazenamento das senhas.

Deploy: Render.

Estrutura do Projeto

HTML Files:

recepcao.html: Página para geração de senhas.

atendimento.html: Página para gerenciar e atender clientes.

painel.html: Página para exibir a próxima senha a ser atendida.

Backend:

rotas.py: Configurações das rotas e comunicação com o banco de dados.

servicos.py: Implementação das operações no banco de dados SQLite.

Como Usar

Clone este repositório:

git clone https://github.com/seu-usuario/seu-repositorio.git

Instale as dependências:

pip install -r requirements.txt

Configure o caminho do banco de dados no arquivo rotas.py (variável caminho_banco).

Inicie a aplicação:

python rotas.py

Acesse o aplicativo no navegador através de http://localhost:5000.

Contribuição

Sinta-se à vontade para fazer um fork deste repositório e enviar pull requests com melhorias. Sugestões e feedbacks são bem-vindos!

Observações

Este projeto foi desenvolvido com fins educacionais e pode conter áreas para melhoria, como a remoção de códigos duplicados e otimizações de lógica.

O banco de dados SQLite é inicializado no diretório database/db.db. Certifique-se de criar o banco antes de executar a aplicação.

Licença

Você pode usar, modificar e distribuir este projeto conforme desejar.


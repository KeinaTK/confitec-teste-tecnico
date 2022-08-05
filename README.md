# Confitec Teste Técnico

Teste realizado em Agosto de 2022.

## Sobre a aplicação

Esta aplicação é completamente auto-contida e possui os seguintes contâineres:
- `api`: Baseado na imagem base de Python 3.10. Responsável por executar a aplicação principal;
- `db`: Baseado na imagem do [DynamoDB-Local](https://hub.docker.com/r/amazon/dynamodb-local). Responsável por hospedar o banco de dados;
- `redis`: Baseado na imagem base do Redis. Responsável por *cachear* os endpoints da aplicação;

---

## Como subir a aplicação

A aplicação é completamente *conteinerizada*, necessintando-se apenas de `docker` e da utilidade `docker-compose`. As informações e passo-a-passos de como instalá-los está disponível [neste documento oficial](https://docs.docker.com/engine/install/). Geralmente é possível obter ambas diretamente do gerenciador de pacotes da sua distro Linux.

Após instalar as dependências, certifique-se de copiar/renomear o arquivo `.env-example` para `.env`. Por exemplo, utilize o comando

```sh
cp .env-example .env
```

Então, basta subir os contâineres

```sh
docker-compose up
```

E a aplicação estará rodando na porta 5000, sendo acessível pelos endereços `127.0.0.1:5000` ou `localhost:50000`.

## Utilizando a aplicação

A aplicação conta com um endpoint acessível pelas rotas `/artists/<id>/` e `/artists/<id>/songs/`, que recebem o id de um artista a ser buscado no [Genius API](https://docs.genius.com/) e retornará um *payload* contendo seu nome e as 10 músicas mais populares, entre outros valores.

Como cliente de requisições, recomenda-se o uso da extensão [Thunderclient](https://www.thunderclient.com/) para o [VS Code](https://code.visualstudio.com/). Caso opte por usá-la, importe o endpoint contido [neste arquivo](thunder-collection_Confitec-Teste-Tecnico.json).

## Executando os testes

Como mencionado anteriormente, a aplicação é auto-contida no Docker, portanto a execução dos testes também ocorre dentro do contâiner. Para facilitar esta execução, o [Makefile](Makefile) conta com o comando `test` para rodar os testes com *coverage*, portanto garanta que sua distro possui o comando `make` instalado, ou obtenha-no pelo pacote `build-essential` do seu gerenciador de pacotes favorito.

Com o `make` instalado, execute

```sh
make test
```

E os arquivos de cobertura se encontrarão em `src/htmlcov`. É possível checar as coberturas facilmente abrindo o arquivo `index.html` e utilizando a extensão [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) também do VS Code.
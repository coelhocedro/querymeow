# Catabase — Sistema de Catálogo e Avaliação de Filmes

Aplicação web simples criada em **Python + SQLite**, sem bibliotecas externas. Ela atende aos casos de uso previstos no projeto da disciplina.

**Repositório do projeto:** https://github.com/coelhocedro/querymeow

## Funcionalidades implementadas

- UC01 — Cadastrar Usuário
- UC02 — Realizar Login
- UC03 — Cadastrar Filme
- UC04 — Consultar Catálogo de Filmes
- UC05 — Registrar Avaliação
- UC06 — Excluir Avaliação

## Dados de acesso para teste

A aplicação cria automaticamente uma conta de teste:

- **E-mail:** `teste@email.com`
- **Senha:** `123456`

Também são cadastrados alguns filmes iniciais para facilitar os testes.

## Como executar localmente

1. Abra o terminal na pasta do projeto.
2. Execute:

```bash
python app.py
```

3. Acesse no navegador:

```text
http://127.0.0.1:5000
```

## Banco de dados

O arquivo `catabase.db` será criado automaticamente na primeira execução.

Tabelas criadas:

- `Usuario`
- `Filme`
- `Avaliacao`

## Como usar na demonstração

1. Entrar com `teste@email.com` e senha `123456`.
2. Visualizar o catálogo de filmes.
3. Clicar em `+ Adicionar Filme`.
4. Cadastrar um filme novo.
5. Abrir o detalhe de um filme.
6. Registrar uma avaliação com nota e comentário.
7. Alterar a avaliação para demonstrar a sobrescrita.
8. Excluir a avaliação.

## Estrutura do projeto

```text
catabase_app/
├── app.py
├── README.md
├── docs/
│   └── PLANO_DE_TESTES_EXECUTADO.md
└── static/
    └── style.css
```

## Observação para entrega final

Para a entrega da disciplina, substitua a URL local pela URL pública, caso publique a aplicação em uma hospedagem.


## Publicação em hospedagem

Para publicar em plataformas como Render, use:

- **Build Command:** deixar em branco ou usar `pip install -r requirements.txt`
- **Start Command:** `python app.py`

A aplicação lê automaticamente a variável de ambiente `PORT`, exigida por plataformas de hospedagem, e escuta em `0.0.0.0`.

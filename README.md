# querymeow - Sistema de Catálogo e Avaliação de Filmes

Aplicação web simplificada para gerenciamento pessoal e colaborativo de filmes. O sistema permite o cadastro de usuários, autenticação, consulta de catálogo, cadastro de filmes, registro de avaliações, sobrescrita de avaliação existente e exclusão de avaliação.

## Integrantes

- Bárbara Coelho dos Santos Cedro
- Eduardo Castro Brito

## Repositório

https://github.com/coelhocedro/QueryMeow

## Quadro de acompanhamento

https://github.com/coelhocedro/QueryMeow/issues

## Tecnologias previstas

- Python
- Banco de dados SQL relacional
- Arquitetura MVC simplificada
- Navegador web como interface de acesso
- GitHub para versionamento e acompanhamento do projeto

## Funcionalidades implementadas/planejadas

- UC01 - Cadastrar Usuário
- UC02 - Realizar Login
- UC03 - Cadastrar Filme
- UC04 - Consultar Catálogo de Filmes
- UC05 - Registrar Avaliação
- UC06 - Excluir Avaliação

## Requisitos para executar localmente

- Python 3.10 ou superior
- Git
- Gerenciador `pip`
- Banco de dados SQL configurado conforme o projeto

## Como executar a aplicação

> Ajuste os comandos abaixo caso o arquivo principal do projeto tenha outro nome.

```bash
# 1. Clonar o repositório
git clone https://github.com/bcoelho21/QueryMeow.git
cd QueryMeow

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar ambiente virtual
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar a aplicação
python app.py
```

Depois de iniciar a aplicação, acesse no navegador:

```text
http://localhost:5000
```

## Configuração do banco de dados

O projeto utiliza persistência em banco SQL relacional. Antes de executar, confira se o arquivo de configuração do banco, scripts de criação das tabelas ou arquivo `.env` estão ajustados corretamente.

Estrutura conceitual prevista:

- `Usuario(id_usuario, nome, email, senha)`
- `Filme(id_filme, titulo, diretor, ano_lancamento, genero)`
- `Avaliacao(id_avaliacao, nota, comentario, data_registro, id_usuario, id_filme)`

## Dados de teste sugeridos

```text
E-mail: teste@email.com
Senha: 123456
```

Filmes sugeridos para teste:

- A Ilha do Medo - Martin Scorsese - 2010 - Suspense
- Clube da Luta - David Fincher - 1999 - Drama/Suspense
- Seven - David Fincher - 1995 - Suspense

## Plano de testes

O plano de testes cobre os casos de uso UC01 a UC06, incluindo fluxos principais e alternativos. A planilha `Plano_Execucao_Testes_QueryMeow.xlsx` contém:

- Casos TST-01 a TST-09
- Resultado esperado
- Campo para resultado obtido
- Status de execução
- Métricas automáticas de execução, aprovação, falha, bloqueio e cobertura

## Versionamento da Iteração 2

Para atender à atividade de versionamento, execute os comandos do arquivo:

```text
Comandos_Atividade_9_Git.txt
```

Resumo esperado:

- Criar tag `v1` referente à Iteração 1
- Criar branch `iteracao2` a partir do branch principal
- Alterar dois arquivos no branch `iteracao2`
- Fazer merge para `master` ou `main`
- Manter o branch `iteracao2`
- Criar tag `v2` referente à Iteração 2



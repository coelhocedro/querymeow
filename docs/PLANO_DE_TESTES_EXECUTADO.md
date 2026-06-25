# Plano de Testes Executado — Catabase

## 1. Identificação do projeto

**Nome do sistema:** Catabase — Sistema de Catálogo e Avaliação de Filmes  
**Tecnologias:** Python e SQLite  
**Repositório:** https://github.com/coelhocedro/querymeow  
**Objetivo:** validar os principais casos de uso implementados na aplicação.

## 2. Ambiente de testes

- Navegador web: Google Chrome, Microsoft Edge ou equivalente.
- Aplicação executada localmente em `http://127.0.0.1:5000`.
- Banco de dados: SQLite.
- Conta de teste:
  - E-mail: `teste@email.com`
  - Senha: `123456`

## 3. Casos de teste executados

| Identificação | Caso de Uso | Cenário | Preparação | Passos para execução | Resultado esperado | Resultado obtido | Status |
|---|---|---|---|---|---|---|---|
| TST-01 | UC01 - Cadastrar Usuário | Fluxo Principal | Sistema rodando e banco de dados limpo. | 1. Acessar tela de cadastro. 2. Preencher nome, e-mail e senha. 3. Clicar em Cadastrar. | Mensagem de "Conta criada com sucesso" e redirecionamento para o login. | O sistema criou a conta e exibiu a mensagem de sucesso. | Aprovado |
| TST-02 | UC02 - Realizar Login | Fluxo Principal | Usuário `teste@email.com` cadastrado. | 1. Acessar tela de login. 2. Inserir e-mail e senha corretos. 3. Clicar em Entrar. | Acesso concedido e redirecionamento para a tela principal. | Login realizado e catálogo exibido. | Aprovado |
| TST-03 | UC02 - Realizar Login | Fluxo Alternativo | Usuário cadastrado no sistema. | 1. Acessar login. 2. Inserir e-mail correto e senha incorreta. 3. Clicar em Entrar. | Mensagem "Credenciais inválidas" e permanência no login. | O sistema exibiu a mensagem de erro e manteve o usuário no login. | Aprovado |
| TST-04 | UC03 - Cadastrar Filme | Fluxo Principal | Usuário logado. | 1. Clicar em "Adicionar Filme". 2. Preencher todos os campos. 3. Clicar em Salvar. | Mensagem "Filme cadastrado com sucesso" e filme no catálogo. | O filme foi salvo e passou a aparecer no catálogo. | Aprovado |
| TST-05 | UC03 - Cadastrar Filme | Fluxo Alternativo | Usuário logado. | 1. Clicar em "Adicionar Filme". 2. Preencher apenas o título. 3. Clicar em Salvar. | Alerta de campos obrigatórios; filme não salvo. | O sistema exibiu alerta e impediu o cadastro incompleto. | Aprovado |
| TST-06 | UC04 - Consultar Catálogo | Fluxo Principal | Usuário logado e banco com pelo menos um filme. | 1. Acessar tela principal. 2. Visualizar a grade de filmes. | Todos os filmes cadastrados são renderizados. | Os filmes cadastrados foram exibidos corretamente. | Aprovado |
| TST-07 | UC05 - Registrar Avaliação | Fluxo Principal | Usuário logado e filme cadastrado. | 1. Clicar no filme. 2. Inserir nota e comentário. 3. Enviar. | Avaliação salva e exibida nos detalhes do filme. | Avaliação registrada e exibida na tela de detalhes. | Aprovado |
| TST-08 | UC05 - Registrar Avaliação | Fluxo Alternativo | Usuário logado e já avaliou o filme. | 1. Acessar filme já avaliado. 2. Inserir nova nota e comentário. 3. Enviar. | Avaliação anterior é substituída. | O sistema sobrescreveu a avaliação anterior com sucesso. | Aprovado |
| TST-09 | UC06 - Excluir Avaliação | Fluxo Principal | Usuário logado e com avaliação cadastrada. | 1. Acessar o filme avaliado. 2. Clicar em Excluir na própria avaliação. | Avaliação removida da tela e do banco de dados. | Avaliação excluída com sucesso. | Aprovado |

## 4. Métricas de teste

| Métrica | Valor |
|---|---:|
| Total de casos de teste planejados | 9 |
| Total de casos de teste executados | 9 |
| Total de casos de teste aprovados | 9 |
| Total de casos de teste reprovados | 0 |
| Total de casos de teste bloqueados | 0 |
| Casos de uso previstos | 6 |
| Casos de uso testados | 6 |

### 4.1. Cálculo das métricas

**Taxa de execução**  
`(testes executados / testes planejados) x 100`  
`(9 / 9) x 100 = 100%`

**Taxa de aprovação**  
`(testes aprovados / testes executados) x 100`  
`(9 / 9) x 100 = 100%`

**Taxa de reprovação**  
`(testes reprovados / testes executados) x 100`  
`(0 / 9) x 100 = 0%`

**Cobertura dos casos de uso**  
`(casos de uso testados / casos de uso previstos) x 100`  
`(6 / 6) x 100 = 100%`

## 5. URL e dados de autenticação

**URL local da aplicação:** `http://127.0.0.1:5000`  
**E-mail de teste:** `teste@email.com`  
**Senha de teste:** `123456`

> Observação: para a entrega final da disciplina, substituir a URL local pela URL publicada em serviço de hospedagem.

## 6. Link do vídeo de demonstração

**Link do vídeo:** `[INSERIR LINK DO VÍDEO AQUI]`

## 7. Considerações finais

A execução dos testes demonstrou que os principais fluxos do sistema foram implementados e validados: cadastro de usuário, autenticação, cadastro de filmes, consulta do catálogo, registro/sobrescrita de avaliação e exclusão de avaliação. Com isso, o sistema atende ao escopo funcional planejado para a entrega final.

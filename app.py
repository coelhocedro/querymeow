"""
Catabase — Sistema simples de Catálogo e Avaliação de Filmes.

Aplicação web feita apenas com bibliotecas padrão do Python:
- http.server para a camada web
- sqlite3 para banco SQL

Para executar:
    python app.py
Depois acesse:
    http://127.0.0.1:5000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, quote, unquote
from http.cookies import SimpleCookie
from html import escape
import hashlib
import os
import secrets
import sqlite3
from datetime import datetime

DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "catabase.db"))
SESSIONS = {}
GENEROS = [
    "Ação", "Aventura", "Comédia", "Drama", "Ficção Científica",
    "Suspense", "Terror", "Romance", "Animação", "Documentário"
]


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def init_db():
    conn = conectar()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS Usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Filme (
            id_filme INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            diretor TEXT NOT NULL,
            ano_lancamento INTEGER NOT NULL,
            genero TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Avaliacao (
            id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_filme INTEGER NOT NULL,
            nota INTEGER NOT NULL CHECK(nota BETWEEN 1 AND 5),
            comentario TEXT NOT NULL,
            data_registro TEXT NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
            FOREIGN KEY (id_filme) REFERENCES Filme(id_filme),
            UNIQUE(id_usuario, id_filme)
        );
        """
    )

    usuario = cur.execute("SELECT id_usuario FROM Usuario WHERE email = ?", ("teste@email.com",)).fetchone()
    if usuario is None:
        cur.execute(
            "INSERT INTO Usuario (nome, email, senha) VALUES (?, ?, ?)",
            ("Usuário Teste", "teste@email.com", hash_senha("123456")),
        )

    total_filmes = cur.execute("SELECT COUNT(*) AS total FROM Filme").fetchone()["total"]
    if total_filmes == 0:
        filmes = [
            ("A Ilha do Medo", "Martin Scorsese", 2010, "Suspense"),
            ("Clube da Luta", "David Fincher", 1999, "Drama"),
            ("Se7en", "David Fincher", 1995, "Suspense"),
            ("A Origem", "Christopher Nolan", 2010, "Ficção Científica"),
            ("O Sexto Sentido", "M. Night Shyamalan", 1999, "Suspense"),
            ("Os Suspeitos", "Bryan Singer", 1995, "Suspense"),
        ]
        cur.executemany(
            "INSERT INTO Filme (titulo, diretor, ano_lancamento, genero) VALUES (?, ?, ?, ?)",
            filmes,
        )

    conn.commit()
    conn.close()


def html_base(titulo, conteudo, usuario=None, msg=None, tipo="info"):
    nav = ""
    if usuario:
        nav = f"""
            <span class="user">Olá, {escape(usuario['nome'])}</span>
            <a href="/catalogo">Catálogo</a>
            <a class="button small" href="/filmes/novo">+ Adicionar Filme</a>
            <a href="/logout">Sair</a>
        """
    else:
        nav = '<a href="/login">Login</a><a href="/cadastro">Cadastro</a>'

    alerta = f'<div class="alert {escape(tipo)}">{escape(msg)}</div>' if msg else ""

    return f"""<!doctype html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(titulo)} | Catabase</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header class="topbar">
        <a class="brand" href="/catalogo">🐾 CAT<span>BASE</span></a>
        <nav>{nav}</nav>
    </header>
    <main class="container">
        {alerta}
        {conteudo}
    </main>
</body>
</html>"""


class CatabaseHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def usuario_atual(self):
        cookie_header = self.headers.get("Cookie", "")
        cookie = SimpleCookie(cookie_header)
        token = cookie.get("session_id")
        if not token:
            return None
        user_id = SESSIONS.get(token.value)
        if not user_id:
            return None
        conn = conectar()
        usuario = conn.execute("SELECT * FROM Usuario WHERE id_usuario = ?", (user_id,)).fetchone()
        conn.close()
        return usuario

    def ler_post(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        dados = self.rfile.read(tamanho).decode("utf-8")
        parsed = parse_qs(dados)
        return {k: v[0] for k, v in parsed.items()}

    def enviar_html(self, html, status=200, cookies=None):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        if cookies:
            for cookie in cookies:
                self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def redirect(self, caminho, msg=None, tipo="info", cookies=None):
        if msg:
            separador = "&" if "?" in caminho else "?"
            caminho = f"{caminho}{separador}msg={quote(msg)}&tipo={quote(tipo)}"
        self.send_response(303)
        self.send_header("Location", caminho)
        if cookies:
            for cookie in cookies:
                self.send_header("Set-Cookie", cookie)
        self.end_headers()

    def mensagem_query(self):
        params = parse_qs(urlparse(self.path).query)
        msg = unquote(params.get("msg", [""])[0])
        tipo = unquote(params.get("tipo", ["info"])[0])
        return msg or None, tipo

    def exigir_login(self):
        usuario = self.usuario_atual()
        if not usuario:
            self.redirect("/login", "Faça login para acessar esta funcionalidade.", "warning")
            return None
        return usuario

    def do_GET(self):
        rota = urlparse(self.path).path

        if rota == "/static/style.css":
            return self.servir_css()
        if rota == "/":
            return self.redirect("/catalogo" if self.usuario_atual() else "/login")
        if rota == "/login":
            return self.tela_login()
        if rota == "/cadastro":
            return self.tela_cadastro()
        if rota == "/logout":
            return self.logout()
        if rota == "/catalogo":
            return self.tela_catalogo()
        if rota == "/filmes/novo":
            return self.tela_novo_filme()
        if rota.startswith("/filmes/"):
            partes = rota.strip("/").split("/")
            if len(partes) == 2 and partes[1].isdigit():
                return self.tela_detalhes_filme(int(partes[1]))

        return self.erro_404()

    def do_POST(self):
        rota = urlparse(self.path).path
        if rota == "/login":
            return self.post_login()
        if rota == "/cadastro":
            return self.post_cadastro()
        if rota == "/filmes/novo":
            return self.post_novo_filme()
        if rota.startswith("/filmes/") and rota.endswith("/avaliar"):
            partes = rota.strip("/").split("/")
            if len(partes) == 3 and partes[1].isdigit():
                return self.post_avaliar_filme(int(partes[1]))
        if rota.startswith("/avaliacoes/") and rota.endswith("/excluir"):
            partes = rota.strip("/").split("/")
            if len(partes) == 3 and partes[1].isdigit():
                return self.post_excluir_avaliacao(int(partes[1]))
        return self.erro_404()

    def servir_css(self):
        caminho = os.path.join(os.path.dirname(__file__), "static", "style.css")
        with open(caminho, "rb") as f:
            css = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/css; charset=utf-8")
        self.end_headers()
        self.wfile.write(css)

    def tela_login(self):
        msg, tipo = self.mensagem_query()
        conteudo = """
        <section class="card auth-card">
            <h1>Entrar no Catabase</h1>
            <p class="muted">Use a conta de teste ou cadastre um novo usuário.</p>
            <form method="post" action="/login">
                <label>E-mail</label>
                <input type="email" name="email" placeholder="teste@email.com" required>
                <label>Senha</label>
                <input type="password" name="senha" placeholder="123456" required>
                <button type="submit">Entrar</button>
            </form>
            <p class="hint">Conta de teste: <strong>teste@email.com</strong> / <strong>123456</strong></p>
            <p>Não tem conta? <a href="/cadastro">Criar cadastro</a></p>
        </section>
        """
        self.enviar_html(html_base("Login", conteudo, msg=msg, tipo=tipo))

    def post_login(self):
        dados = self.ler_post()
        email = dados.get("email", "").strip().lower()
        senha = dados.get("senha", "").strip()

        conn = conectar()
        usuario = conn.execute("SELECT * FROM Usuario WHERE email = ?", (email,)).fetchone()
        conn.close()

        if not usuario or usuario["senha"] != hash_senha(senha):
            return self.redirect("/login", "Credenciais inválidas.", "danger")

        token = secrets.token_urlsafe(24)
        SESSIONS[token] = usuario["id_usuario"]
        cookie = f"session_id={token}; Path=/; HttpOnly; SameSite=Lax"
        self.redirect("/catalogo", "Login realizado com sucesso.", "success", cookies=[cookie])

    def logout(self):
        cookie_header = self.headers.get("Cookie", "")
        cookie = SimpleCookie(cookie_header)
        token = cookie.get("session_id")
        if token:
            SESSIONS.pop(token.value, None)
        self.redirect("/login", "Você saiu do sistema.", "info", cookies=["session_id=; Path=/; Max-Age=0"])

    def tela_cadastro(self):
        msg, tipo = self.mensagem_query()
        conteudo = """
        <section class="card auth-card">
            <h1>Cadastrar Usuário</h1>
            <p class="muted">Crie uma conta para cadastrar filmes e avaliações.</p>
            <form method="post" action="/cadastro">
                <label>Nome</label>
                <input type="text" name="nome" placeholder="Seu nome" required>
                <label>E-mail</label>
                <input type="email" name="email" placeholder="voce@email.com" required>
                <label>Senha</label>
                <input type="password" name="senha" placeholder="mínimo de 6 caracteres" required>
                <button type="submit">Cadastrar</button>
            </form>
            <p>Já tem conta? <a href="/login">Entrar</a></p>
        </section>
        """
        self.enviar_html(html_base("Cadastro", conteudo, msg=msg, tipo=tipo))

    def post_cadastro(self):
        dados = self.ler_post()
        nome = dados.get("nome", "").strip()
        email = dados.get("email", "").strip().lower()
        senha = dados.get("senha", "").strip()

        if not nome or not email or not senha:
            return self.redirect("/cadastro", "Preencha nome, e-mail e senha.", "danger")

        conn = conectar()
        try:
            conn.execute(
                "INSERT INTO Usuario (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, hash_senha(senha)),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return self.redirect("/cadastro", "Este e-mail já está cadastrado.", "danger")
        conn.close()
        self.redirect("/login", "Conta criada com sucesso. Faça login para continuar.", "success")

    def tela_catalogo(self):
        usuario = self.exigir_login()
        if not usuario:
            return
        msg, tipo = self.mensagem_query()

        conn = conectar()
        filmes = conn.execute(
            """
            SELECT f.*, ROUND(AVG(a.nota), 1) AS media, COUNT(a.id_avaliacao) AS total_avaliacoes
            FROM Filme f
            LEFT JOIN Avaliacao a ON a.id_filme = f.id_filme
            GROUP BY f.id_filme
            ORDER BY f.titulo ASC
            """
        ).fetchall()
        conn.close()

        cards = ""
        for filme in filmes:
            media = f"⭐ {filme['media']}/5 — {filme['total_avaliacoes']} avaliação(ões)" if filme["media"] else "Sem avaliações ainda"
            cards += f"""
            <a class="movie-card" href="/filmes/{filme['id_filme']}">
                <span class="movie-icon">🎬</span>
                <h2>{escape(filme['titulo'])}</h2>
                <p>{escape(filme['diretor'])} • {filme['ano_lancamento']}</p>
                <p class="genre">{escape(filme['genero'])}</p>
                <p class="rating">{media}</p>
            </a>
            """

        if not cards:
            cards = '<div class="card"><p>Nenhum filme cadastrado.</p></div>'

        conteudo = f"""
        <section class="page-title">
            <div>
                <h1>Catálogo de Filmes</h1>
                <p class="muted">Consulte os filmes cadastrados e registre suas avaliações.</p>
            </div>
            <a class="button" href="/filmes/novo">+ Adicionar Filme</a>
        </section>
        <section class="grid">{cards}</section>
        """
        self.enviar_html(html_base("Catálogo", conteudo, usuario=usuario, msg=msg, tipo=tipo))

    def tela_novo_filme(self):
        usuario = self.exigir_login()
        if not usuario:
            return
        msg, tipo = self.mensagem_query()
        opcoes = ''.join(f'<option value="{escape(g)}">{escape(g)}</option>' for g in GENEROS)
        conteudo = f"""
        <section class="card form-card">
            <a class="back" href="/catalogo">← Voltar ao catálogo</a>
            <h1>Cadastro de Novo Filme</h1>
            <form method="post" action="/filmes/novo">
                <label>Título</label>
                <input type="text" name="titulo" placeholder="Ex: Clube da Luta">
                <label>Diretor</label>
                <input type="text" name="diretor" placeholder="Ex: David Fincher">
                <div class="row">
                    <div>
                        <label>Ano</label>
                        <input type="number" name="ano_lancamento" placeholder="1999">
                    </div>
                    <div>
                        <label>Gênero</label>
                        <select name="genero">
                            <option value="">Selecione</option>
                            {opcoes}
                        </select>
                    </div>
                </div>
                <button type="submit">Salvar Filme</button>
            </form>
        </section>
        """
        self.enviar_html(html_base("Novo Filme", conteudo, usuario=usuario, msg=msg, tipo=tipo))

    def post_novo_filme(self):
        usuario = self.exigir_login()
        if not usuario:
            return
        dados = self.ler_post()
        titulo = dados.get("titulo", "").strip()
        diretor = dados.get("diretor", "").strip()
        ano = dados.get("ano_lancamento", "").strip()
        genero = dados.get("genero", "").strip()

        if not titulo or not diretor or not ano or not genero:
            return self.redirect("/filmes/novo", "Preencha todos os campos obrigatórios para cadastrar o filme.", "danger")

        try:
            ano_int = int(ano)
            if ano_int < 1888 or ano_int > datetime.now().year + 1:
                raise ValueError
        except ValueError:
            return self.redirect("/filmes/novo", "Informe um ano de lançamento válido.", "danger")

        conn = conectar()
        conn.execute(
            "INSERT INTO Filme (titulo, diretor, ano_lancamento, genero) VALUES (?, ?, ?, ?)",
            (titulo, diretor, ano_int, genero),
        )
        conn.commit()
        conn.close()
        self.redirect("/catalogo", "Filme cadastrado com sucesso.", "success")

    def tela_detalhes_filme(self, id_filme):
        usuario = self.exigir_login()
        if not usuario:
            return
        msg, tipo = self.mensagem_query()
        conn = conectar()
        filme = conn.execute("SELECT * FROM Filme WHERE id_filme = ?", (id_filme,)).fetchone()
        if not filme:
            conn.close()
            return self.redirect("/catalogo", "Filme não encontrado.", "danger")

        avaliacoes = conn.execute(
            """
            SELECT a.*, u.nome
            FROM Avaliacao a
            JOIN Usuario u ON u.id_usuario = a.id_usuario
            WHERE a.id_filme = ?
            ORDER BY a.id_avaliacao DESC
            """,
            (id_filme,),
        ).fetchall()
        minha = conn.execute(
            "SELECT * FROM Avaliacao WHERE id_filme = ? AND id_usuario = ?",
            (id_filme, usuario["id_usuario"]),
        ).fetchone()
        conn.close()

        opcoes_nota = ""
        for n in [1, 2, 3, 4, 5]:
            selected = "selected" if minha and minha["nota"] == n else ""
            opcoes_nota += f'<option value="{n}" {selected}>{n} estrela(s)</option>'

        texto_comentario = escape(minha["comentario"]) if minha else ""
        titulo_form = "Atualizar sua avaliação" if minha else "Avaliar este filme"

        lista = ""
        for av in avaliacoes:
            botao = ""
            if av["id_usuario"] == usuario["id_usuario"]:
                botao = f"""
                <form method="post" action="/avaliacoes/{av['id_avaliacao']}/excluir">
                    <button class="danger-button" type="submit">Excluir</button>
                </form>
                """
            lista += f"""
            <article class="review">
                <div>
                    <strong>{escape(av['nome'])}</strong>
                    <span>⭐ {av['nota']}/5</span>
                    <p>{escape(av['comentario'])}</p>
                    <small>{escape(av['data_registro'])}</small>
                </div>
                {botao}
            </article>
            """
        if not lista:
            lista = '<p class="muted">Este filme ainda não possui avaliações.</p>'

        conteudo = f"""
        <section class="card details-card">
            <a class="back" href="/catalogo">← Voltar ao catálogo</a>
            <h1>{escape(filme['titulo'])}</h1>
            <div class="movie-info">
                <p><strong>Diretor:</strong> {escape(filme['diretor'])}</p>
                <p><strong>Ano:</strong> {filme['ano_lancamento']}</p>
                <p><strong>Gênero:</strong> {escape(filme['genero'])}</p>
            </div>
            <section class="review-form">
                <h2>{titulo_form}</h2>
                <form method="post" action="/filmes/{id_filme}/avaliar">
                    <label>Nota</label>
                    <select name="nota" required>{opcoes_nota}</select>
                    <label>Comentário</label>
                    <textarea name="comentario" rows="4" placeholder="Escreva sua opinião" required>{texto_comentario}</textarea>
                    <button type="submit">Enviar Avaliação</button>
                </form>
            </section>
        </section>
        <section class="card">
            <h2>Avaliações</h2>
            {lista}
        </section>
        """
        self.enviar_html(html_base("Detalhes", conteudo, usuario=usuario, msg=msg, tipo=tipo))

    def post_avaliar_filme(self, id_filme):
        usuario = self.exigir_login()
        if not usuario:
            return
        dados = self.ler_post()
        comentario = dados.get("comentario", "").strip()
        try:
            nota = int(dados.get("nota", ""))
            if nota < 1 or nota > 5:
                raise ValueError
        except ValueError:
            return self.redirect(f"/filmes/{id_filme}", "Informe uma nota entre 1 e 5.", "danger")
        if not comentario:
            return self.redirect(f"/filmes/{id_filme}", "Digite um comentário para registrar a avaliação.", "danger")

        conn = conectar()
        filme = conn.execute("SELECT id_filme FROM Filme WHERE id_filme = ?", (id_filme,)).fetchone()
        if not filme:
            conn.close()
            return self.redirect("/catalogo", "Filme não encontrado.", "danger")

        existente = conn.execute(
            "SELECT id_avaliacao FROM Avaliacao WHERE id_usuario = ? AND id_filme = ?",
            (usuario["id_usuario"], id_filme),
        ).fetchone()
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        if existente:
            conn.execute(
                "UPDATE Avaliacao SET nota = ?, comentario = ?, data_registro = ? WHERE id_avaliacao = ?",
                (nota, comentario, data, existente["id_avaliacao"]),
            )
            msg = "Avaliação sobrescrita com sucesso."
        else:
            conn.execute(
                "INSERT INTO Avaliacao (id_usuario, id_filme, nota, comentario, data_registro) VALUES (?, ?, ?, ?, ?)",
                (usuario["id_usuario"], id_filme, nota, comentario, data),
            )
            msg = "Avaliação registrada com sucesso."
        conn.commit()
        conn.close()
        self.redirect(f"/filmes/{id_filme}", msg, "success")

    def post_excluir_avaliacao(self, id_avaliacao):
        usuario = self.exigir_login()
        if not usuario:
            return
        conn = conectar()
        avaliacao = conn.execute("SELECT * FROM Avaliacao WHERE id_avaliacao = ?", (id_avaliacao,)).fetchone()
        if not avaliacao:
            conn.close()
            return self.redirect("/catalogo", "Avaliação não encontrada.", "danger")
        if avaliacao["id_usuario"] != usuario["id_usuario"]:
            id_filme = avaliacao["id_filme"]
            conn.close()
            return self.redirect(f"/filmes/{id_filme}", "Você só pode excluir suas próprias avaliações.", "danger")
        id_filme = avaliacao["id_filme"]
        conn.execute("DELETE FROM Avaliacao WHERE id_avaliacao = ?", (id_avaliacao,))
        conn.commit()
        conn.close()
        self.redirect(f"/filmes/{id_filme}", "Avaliação excluída com sucesso.", "success")

    def erro_404(self):
        conteudo = '<section class="card"><h1>Página não encontrada</h1><p>A rota solicitada não existe.</p><a href="/catalogo">Voltar</a></section>'
        self.enviar_html(html_base("404", conteudo, usuario=self.usuario_atual()), status=404)


def run_server(host=None, port=None):
    init_db()
    host = host or os.environ.get("HOST", "0.0.0.0")
    port = int(port or os.environ.get("PORT", 5000))
    server = HTTPServer((host, port), CatabaseHandler)
    local_url = "http://127.0.0.1:%s" % port if host in ("0.0.0.0", "127.0.0.1", "localhost") else f"http://{host}:{port}"
    print(f"Catabase rodando. Acesse localmente: {local_url}")
    print("Conta de teste: teste@email.com / 123456")
    server.serve_forever()


if __name__ == "__main__":
    run_server()

import os
import tempfile
import unittest

import app


class TestBancoCatabase(unittest.TestCase):
    def setUp(self):
        self.fd, self.path = tempfile.mkstemp()
        self.old_db = app.DB_PATH
        app.DB_PATH = self.path
        app.init_db()

    def tearDown(self):
        app.DB_PATH = self.old_db
        os.close(self.fd)
        os.unlink(self.path)

    def test_usuario_teste_e_filmes_iniciais(self):
        conn = app.conectar()
        usuario = conn.execute("SELECT * FROM Usuario WHERE email = ?", ("teste@email.com",)).fetchone()
        filmes = conn.execute("SELECT COUNT(*) AS total FROM Filme").fetchone()["total"]
        conn.close()
        self.assertIsNotNone(usuario)
        self.assertGreaterEqual(filmes, 1)

    def test_hash_senha(self):
        self.assertEqual(app.hash_senha("123456"), app.hash_senha("123456"))
        self.assertNotEqual(app.hash_senha("123456"), app.hash_senha("senha_errada"))


if __name__ == "__main__":
    unittest.main()

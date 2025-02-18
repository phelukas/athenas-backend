from django.test import TestCase
from .models import Pessoa
from .tasks import PessoaTask


class PessoaTaskTestCase(TestCase):
    def setUp(self):
        self.pessoa_data = {
            "nome": "Teste",
            "data_nasc": "1990-01-01",
            "cpf": "111.222.333-44",
            "sexo": "M",
            "altura": 1.80,
            "peso": 80.0,
        }

    def test_create_pessoa(self):
        """Verifica se PessoaTask.create cria uma pessoa corretamente."""
        pessoa = PessoaTask.create(self.pessoa_data)
        self.assertIsNotNone(pessoa.id)
        self.assertEqual(pessoa.nome, "Teste")

    def test_update_pessoa(self):
        """Cria uma pessoa e testa se PessoaTask.update altera os dados."""
        pessoa = PessoaTask.create(self.pessoa_data)
        update_data = {"nome": "Teste Atualizado"}
        pessoa_atualizada = PessoaTask.update(pessoa.id, update_data)
        self.assertEqual(pessoa_atualizada.nome, "Teste Atualizado")

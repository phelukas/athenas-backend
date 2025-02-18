from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Pessoa


class PessoaAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.pessoa = Pessoa.objects.create(
            nome="João da Silva",
            data_nasc="1990-01-01",
            cpf="123.456.789-00",
            sexo="M",
            altura=1.75,
            peso=70.0,
        )
        self.valid_payload = {
            "nome": "Maria Souza",
            "data_nasc": "1995-05-15",
            "cpf": "987.654.321-00",
            "sexo": "F",
            "altura": 1.65,
            "peso": 60.0,
        }
        self.invalid_payload = {
            "nome": "",
            "data_nasc": "1995-05-15",
            "cpf": "987.654.321-00",
            "sexo": "F",
            "altura": 1.65,
            "peso": 60.0,
        }

    def test_listar_pessoas(self):
        """Teste para verificar se o endpoint de listagem funciona."""
        response = self.client.get(reverse("pessoa-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_incluir_pessoa_valida(self):
        """Teste para incluir uma nova pessoa com dados válidos."""
        response = self.client.post(
            reverse("pessoa-list-create"), data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome"], self.valid_payload["nome"])

    def test_incluir_pessoa_invalida(self):
        """Teste para incluir pessoa com dados inválidos (nome vazio)."""
        response = self.client.post(
            reverse("pessoa-list-create"), data=self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nome", response.data)

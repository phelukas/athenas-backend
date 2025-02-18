from .models import Pessoa
from django.shortcuts import get_object_or_404


class PessoaTask:
    @staticmethod
    def create(data):
        pessoa = Pessoa.objects.create(**data)
        return pessoa

    @staticmethod
    def update(pessoa_id, data):
        pessoa = get_object_or_404(Pessoa, pk=pessoa_id)
        for attr, value in data.items():
            setattr(pessoa, attr, value)
        pessoa.save()
        return pessoa

    @staticmethod
    def delete(pessoa_id):
        pessoa = get_object_or_404(Pessoa, pk=pessoa_id)
        pessoa.delete()
        return

    @staticmethod
    def retrieve(pessoa_id):
        pessoa = get_object_or_404(Pessoa, pk=pessoa_id)
        return pessoa

    @staticmethod
    def list_all():
        return Pessoa.objects.all()

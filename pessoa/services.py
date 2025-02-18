from .tasks import PessoaTask


class PessoaService:
    @staticmethod
    def incluir(data):
        return PessoaTask.create(data)

    @staticmethod
    def alterar(pessoa_id, data):
        return PessoaTask.update(pessoa_id, data)

    @staticmethod
    def excluir(pessoa_id):
        return PessoaTask.delete(pessoa_id)

    @staticmethod
    def pesquisar(pessoa_id):
        return PessoaTask.retrieve(pessoa_id)

    @staticmethod
    def listar():
        return PessoaTask.list_all()

    @staticmethod
    def calcular_peso_ideal(pessoa):
        if pessoa.sexo == "M":
            return (72.7 * float(pessoa.altura)) - 58
        elif pessoa.sexo == "F":
            return (62.1 * float(pessoa.altura)) - 44.7
        else:
            return None

    @staticmethod
    def pesquisarPorCpf(cpf):
        from .models import Pessoa
        from django.shortcuts import get_object_or_404

        return get_object_or_404(Pessoa, cpf=cpf)

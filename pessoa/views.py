from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PessoaSerializer
from .services import PessoaService


class PessoaListCreateView(APIView):
    def get(self, request):
        pessoas = PessoaService.listar()
        serializer = PessoaSerializer(pessoas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PessoaSerializer(data=request.data)
        if serializer.is_valid():
            pessoa = PessoaService.incluir(serializer.validated_data)
            return Response(
                PessoaSerializer(pessoa).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PessoaDetailView(APIView):
    def get(self, request, pk):
        pessoa = PessoaService.pesquisar(pk)
        serializer = PessoaSerializer(pessoa)
        return Response(serializer.data)

    def put(self, request, pk):
        pessoa = PessoaService.pesquisar(pk)
        serializer = PessoaSerializer(pessoa, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        PessoaService.excluir(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PessoaPesoIdealView(APIView):
    def get(self, request, pk):
        pessoa = PessoaService.pesquisar(pk)
        peso_ideal = PessoaService.calcular_peso_ideal(pessoa)
        return Response({"peso_ideal": peso_ideal})


class PessoaPorCpfView(APIView):
    def get(self, request, cpf):
        try:
            pessoa = PessoaService.pesquisarPorCpf(cpf)
        except Exception as e:
            return Response(
                {"detail": "Pessoa não encontrada."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = PessoaSerializer(pessoa)
        return Response(serializer.data)

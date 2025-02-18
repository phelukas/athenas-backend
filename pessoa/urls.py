from django.urls import path
from .views import (
    PessoaListCreateView,
    PessoaDetailView,
    PessoaPesoIdealView,
    PessoaPorCpfView,
)

urlpatterns = [
    path("pessoas/", PessoaListCreateView.as_view(), name="pessoa-list-create"),
    path("pessoas/<int:pk>/", PessoaDetailView.as_view(), name="pessoa-detail"),
    path(
        "pessoas/<int:pk>/peso-ideal/",
        PessoaPesoIdealView.as_view(),
        name="pessoa-peso-ideal",
    ),
    path("pessoas/cpf/<str:cpf>/", PessoaPorCpfView.as_view(), name="pessoa-por-cpf"),
]

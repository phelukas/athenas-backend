from django.db import models


class Pessoa(models.Model):
    SEXO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Feminino"),
    )

    nome = models.CharField(max_length=100)
    data_nasc = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    altura = models.DecimalField(max_digits=4, decimal_places=2)
    peso = models.DecimalField(max_digits=5, decimal_places=2)

    def calcular_peso_ideal(self):
        """
        Calcula o peso ideal de acordo com a altura e o sexo.
        """
        if self.sexo == "M":
            return round((72.7 * float(self.altura)) - 58, 2)
        elif self.sexo == "F":
            return round((62.1 * float(self.altura)) - 44.7, 2)
        return None

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

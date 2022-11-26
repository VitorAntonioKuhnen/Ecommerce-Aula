from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    tpCategoria = models.CharField(max_length=255)

    def __str__(self):
        return self.tpCategoria

class Marca(models.Model):
    nmMarca = models.CharField(max_length=255)

    def __str__(self):
        return self.nmMarca

class Hist_Produto(models.Model):
    valor_uni = models.FloatField()
    data_alt = models.DateField()
    hora_alt = models.TimeField()
    qtd = models.IntegerField()
    movimentacao = models.CharField(max_length=10)   

    def __str__(self):
        return self.movimentacao  

class Compra_Fornecedor(models.Model):
    qtd_entrada = models.IntegerField()
    valor = models.FloatField()
    dataEnt = models.DateField()
    horaEnt = models.TimeField()    
    

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    qtd = models.IntegerField()
    valor = models.FloatField()
    tamanho = models.CharField(max_length=2)
    endimg = models.ImageField(upload_to='Produto_img/%Y/%m/%d')
    compra_fornecedor = models.ForeignKey(Compra_Fornecedor, on_delete=models.DO_NOTHING)
    hist_produto = models.ForeignKey(Hist_Produto, on_delete=models.DO_NOTHING, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome


class Prod_Destaque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)           

    def __str__(self):
        return self.produto.nome

class Carrinho(models.Model):
    qtd_Prod = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.produto.nome

class Hist_Carrinho(models.Model):
    qtd_Prod = models.IntegerField()
    valor_tot = models.FloatField()
    valor_unit = models.FloatField()
    nmProduto = models.CharField(max_length=255)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nmProduto


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




class Tamanhos(models.Model):
    tamanhos = models.IntegerField()
    def __str__(self):
        return str(self.tamanhos)    

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    qtd = models.IntegerField()
    valor = models.FloatField()
    endimg = models.ImageField(upload_to='Produto_img/%Y/%m/%d')
    tamanho = models.ManyToManyField(Tamanhos)
    # tamanho = models.ForeignKey(Tamanhos, on_delete=models.DO_NOTHING)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome


class Hist_Produto(models.Model):
    valor_uni = models.FloatField()
    data_alt = models.DateField(auto_now_add=True)
    hora_alt = models.TimeField(auto_now_add=True)
    qtd = models.IntegerField()
    tamanho = models.CharField(max_length=2)
    movimentacao = models.CharField(max_length=1) # Saida ou Entrada
    carrinho = models.CharField(max_length=1)   # A para "Ativo" e F para "Finalizado"
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.movimentacao  

class Compra_Fornecedor(models.Model):
    nmFornece = models.CharField(max_length=255)
    qtd_entrada = models.IntegerField()
    valor = models.FloatField()
    dataEnt = models.DateField()
    horaEnt = models.TimeField()   
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)


class Prod_Destaque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)           

    def __str__(self):
        return self.produto.nome

class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    produto = models.ManyToManyField(Produto)
    status = models.CharField(max_length=1) # A para "Aberto" e F para "Finalizado"



class Hist_Carrinho(models.Model):
    qtd_Prod = models.IntegerField()
    valor_tot = models.FloatField()
    valor_unit = models.FloatField()
    nmProduto = models.CharField(max_length=255)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nmProduto

class Sac(models.Model):
      nome = models.CharField(max_length=255)
      email = models.CharField(max_length=255)
      comentario = models.TextField()    
      data = models.DateField()
      hora = models.TimeField()  
      status = models.CharField(max_length=1) # A para "Aberto" e F para "Finalizado"

      def __str__(self):
        return self.nome


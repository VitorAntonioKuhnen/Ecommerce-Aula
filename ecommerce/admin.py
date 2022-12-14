from re import search
from django.contrib import admin
from .models import *

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'valor']
    list_display_links = ['nome']
    search_fields = ['nome', 'descricao', 'valor']

admin.site.register(Produto, ProdutoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['tpCategoria']
    list_display_links = ['tpCategoria']
    search_fields = ['tpCategoria']

admin.site.register(Categoria, CategoriaAdmin)    

class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nmMarca']
    list_display_links = ['nmMarca']
    search_fields = ['nmMarca']

admin.site.register(Marca, MarcaAdmin)    

class SacAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'comentario', 'data', 'hora', 'status']
    list_display_links = ['nome']
    search_fields = ['nome', 'email', 'comentario', 'data', 'hora', 'status']

admin.site.register(Sac, SacAdmin)

admin.site.register(Hist_Carrinho)
admin.site.register(Hist_Produto)
admin.site.register(Compra_Fornecedor)
admin.site.register(Prod_Destaque)    
admin.site.register(Carrinho)
admin.site.register(Tamanhos)

# Administradora PAGSEGURO - Codevance

### Sistema que serve para o Fornecedor antecipar um valor que ele teria a receber numa data específica mediante um juros.

Para criar pagamento fictícios o user tem que ser um administrador do sistema após:

Entre no site: [PagSeguro](https://pagseguro-codevance.herokuapp.com/)

```
- Administrador: login: admin - senha: admin
```

Vamos "emular" um pagamento enviado ao Fornecedor

- PAGAMENTO -> Adicionar Pagamento
    - Escolha o provider(fornecedor)
    - Data de vencimento
    - Valor Original Confirme

## PARTE DO FORNECEDOR

```
- User: login: dininho - senha: @102030@
```

### Recebíveis -> Antecipar

## PARTE DO ADMINISTRADOR

O administrador loga-se novamente no sistema e vê quais os pagamentos a liberar

menu **HOME**

- Pedidos -> Fornecedor

E ao final escolha se aceita liberar(adiantar recebível) ou não

Após isso será gerado mais um log e enviado um e-mail para o fornecedor informando a decisão.

## PARTE DO FORNECEDOR

- Recebíveis

###Toda movimentação além do envio de e-mail para os fornecedores será gerado um log e salvo.

## Uso dos endpoints

###Endpoints:
 
- Fornecedor poder acessar um status em específico
 
````
/api/payments/<decision>/
````

- Fornecedor poder fazer a antecipação de um recebível

````
/api/request_advance/<id-do-payment>/
````

onde esse número será o id do recebível

___
Tabela de status:

- SEM_PEDIDO = 0
- ANTECIPADO = 1
- NEGADO = 2
- AGUARDANDO_CONFIRMACAO = 3
- INDISPONIVEL = 4

# Administradora PAGSEGURO - Codevance

### Sistema que serve para o Fornecedor antecipar um valor que ele teria a receber numa data específica mediante um juros.

Para criar pagamento fictícios o user tem que ser um administrador do sistema após:

Entre no site: [PagSeguro](https://pagseguro-codevance.herokuapp.com/)

Depois clicar em ENTRAR e digitar as informações para logar

```
- Administrador: login: admin - senha: admin
```

## PARTE DO ADMINISTRADOR

Vamos "emular" um pagamento enviado ao Fornecedor

Vá em:

- PAGAMENTO -> Adicionar Pagamento
    - Escolha o provider(fornecedor)
    - Data de vencimento
    - Valor Original Confirme

## PARTE DO FORNECEDOR

Depois deslogamos do sistema e entramos com as credenciais do fornecedor

```
- User: login: dininho - senha: @102030@
```

Após ir em **Recebíveis**

E o fornecedor verá uma tabela com seus recebimentos e as respectivas decisões da administradora podendo pedir a
antecipação e aguardar a resposta.

Será enviado um e-mail para o Fornecedor de toda mudança do campo decision

## PARTE DO ADMINISTRADOR

O administrador loga-se novamente no sistema e vê quais os pagamentos a liberar

Vai em pedidos e escolhe um Fornecedor

## Especificações

```
NOVO_VALOR = VALOR_ORIGINAL - (VALOR_ORIGINAL * ((3% / 30) * DIFERENCA_DE_DIAS))
```

```
DATA DE VENCIMENTO ORIGINAL = 01/10/2019
VALOR ORIGINAL = R$ 1.000,00
NOVA DATA DE VENCIMENTO = 15/09/2019

NOVO VALOR = 1000 - (1000 * ((3% / 30) * 16))
NOVO VALOR = 1000 - (1000 * 0,016)
NOVO VALOR = 1000 - 16

NOVO VALOR = R$ 984,00
```

- O sistema deve armazenar os pagamentos e suas informações básicas
    - id do pagamento, data de emissão, data de vencimento, valor original, a qual fornecedor pertence, dados cadastrais
      básicos deste fornecedor, como razão social e CNPJ.
- Para um pagamento ser adiantado, o fornecedor deve fazer uma solicitação, então o operador da empresa escolhe se
  libera a antecipação ou nega a antecipação. Toda essa movimentação deve ficar armazenada em um log.
    - Essa solicitação pode vir via sistema ou por outras vias. Quando vier por outras vias, o operador da empresa fará
      a solicitação no sistema.
- O fornecedor deve ter acesso a uma área, através de autenticação via email e senha, onde ele possa solicitar a
  antecipação de um pagamento. É necessário também que ele veja todos os pagamentos disponíveis para antecipação, todos
  os pagamentos aguardando liberação, todos os aprovados e todos os negados.
    - Importantíssimo que um fornecedor não veja os pagamentos de outro
- Para cada ação sobre um pagamento (solicitação, liberação, negação) o sistema deve enviar um email ao fornecedor.
    - Este envio de email deve ser feito de forma assíncrona (`celery` é seu amigo)
- Caso um pagamento chegue até sua data de vencimento sem ser antecipado, o mesmo deve ser indisponibilizado para
  operação, mas mantido no histórico.
    - Fornecedores não podem ver pagamentos indisponibilizados disponíveis para antecipação
- Deve haver uma API Rest básica com dois endpoints:
    - Um endpoint que liste as operações de um fornecedor, que estará autenticado via JWT. Este endpoint deve permitir
      filtro por estado do pagamento (indisponível, disponível, aguardando confirmação, antecipado, negado)
    - Outro endpoint que será responsável pela solicitação de antecipação de um pagamento. Este endpoint deve receber o
      identificador do pagamento e, obviamente, um usuário logado só pode solicitar antecipação dos pagamentos
      associados ao seu usuário.


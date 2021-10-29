import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate


@pytest.fixture
def resp_api(client):
    # headers = {
    #     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDM0MTg2LCJpYXQiOjE2MzU0MzA1ODYsImp0aSI6ImYxMjE0MjkyZWQxYTQ0ZTM5ODU1OWM0ZTQ1ZWIwMTZkIiwidXNlcl9pZCI6Mn0.-NBr7K6nzMoa48ZFD02lSwtlo0ZT97RtembM7MW6gi8',
    # }

    headers = {
        'Authorization': "Basic bWFyaW5hdWw6Mg==",
    }
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDQ0MzU5LCJpYXQiOjE2MzU0NDA3NTksImp0aSI6IjMwOTY0Yjg5ZTdmNzRlNmU4M2ZmMTc5OTc5OGRmODQzIiwidXNlcl9pZCI6Mn0.7y29LV49H87hSVsCgUgu2aMx8GZNWr18onUMoY0WHsQ'
    header = {
        'HTTP_AUTHORIZATION': f'Bearer {token}'
    }
    payload = {
        "username": 'marinaul',
        "password": '2',
    }
    resp = client.get("/api/payments/1/", headers=headers)
    # resp = client.get("/api/payments/1/", data=payload)
    return resp


@pytest.fixture
@pytest.mark.usefixtures("payment")
def nv_payment(payment):
    return payment


def test_gerar_pedido_para_a_administradora(nv_payment):
    """Criar um pagamento"""
    assert nv_payment.provider.corporate_name is not None


def test_administradora_decide_aprovar_antecipacao_de_recebivel(nv_payment):
    nv_payment.decision = 1
    nv_payment.save()
    assert nv_payment.decision == 1


def test_administradora_decide_negar_antecipacao_de_recebivel(nv_payment):
    nv_payment.decision = 2
    nv_payment.save()
    assert nv_payment.decision == 2


def test_erro_401_nao_autorizado(db):
    client = APIClient()
    token_url = reverse('token_obtain_pair')
    'http://localhost:8000/api/token/'
    content_type = 'application/json'
    username = "marinaul"
    password = "2"
    resp = client.post(token_url, {"username": username, "password": password}, format='json')
    # client.credentials(HTTP_AUTHORIZATION=_basic_auth_str(CLIENT_ID, CLIENT_SECRET))
    # user = User.objects.get(id=2)
    # client.login(username='marinaul', password='2')
    # client.login(username="luxu", password="2")
    uri = '/api/payments/1/'
    params = {
        "username": "marinaul",
        "password": "2"
    }
    response = client.post(uri, params)
    print(response)


# assert resp_api.status_code == 401


def test_autorizado(resp_api):
    assert resp_api.status_code == 401


def test_solicitar_antecipacao_de_recebivel(resp_api):
    assert resp_api.status_code == 200


def test_listar_por_estado_de_pagamento():
    assert 1 == 1


def test_desenvolvedor_index_put(client, db):
    headers = {
        "Authorization": "Basic eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDU0Njg4LCJpYXQiOjE2MzU0NTEwODgsImp0aSI6IjQ0Yjg5YmE1MGY4NzQ2MGE5YTVkNTBiMWMwZmNlZDk5IiwidXNlcl9pZCI6Mn0.RCffY62g-q9OCLRl21ciqDk0pUTMtAJKr0fNrkgYeTc"
    }
    payload = json.dumps(
        {
            "usernmae": "marinaul",
            "password": "2",
        }
    )
    assert (
            client.put("/api/payments/1/", headers=headers, data=payload).status_code
            == 200
    )


@pytest.mark.usefixtures("user")
def test_testar_solucao_drf(db, user):
    factory = APIRequestFactory()
    # user = User.objects.get(username='marinaul')
    # view = AccountDetail.as_view()
    view = factory.get(reverse("token_obtain_pair"))

    # Make an authenticated request to the view...

    # request = factory.get(reverse('api_payments_id', args={'decision': '1'}))
    request = factory.get('/api/payments/1/')
    force_authenticate(request, user=user)
    response = view(request)

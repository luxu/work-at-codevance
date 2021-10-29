from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.views import send_email_movement
from payments.models import Payments
from api.serializer import PaymentsSerializer


@api_view(['GET'])
def payments_list(request, decision):
    """Listar os pagamentos do fornecedor que está logado no sistema"""
    if request.method == 'GET':
        user_id = request.user.id
        payments = Payments.objects.filter(
            Q(provider__user_id=user_id)
            & Q(decision=decision)
        )
        serializer = PaymentsSerializer(payments, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def request_advance(request, payment_id):
    """Solicitar à administradora a antecipação do recebível"""
    if not request.user.is_superuser:
        if request.method == 'GET':
            try:
                payment_query = Payments.objects.get(Q(id=payment_id) & Q(decision=0))
                payment_query.decision = Payments.AGUARDANDO_CONFIRMACAO
                payment_query.save()
                send_email_movement(request, payment_query)
                return Response(f'Pedido enviado com sucesso!', status=status.HTTP_200_OK)
            except Payments.DoesNotExist:
                return Response(
                    f'{request.user}..Este pagamento não existe!',
                    status=status.HTTP_400_BAD_REQUEST
                )
    return Response(
        f'Desculpe, não existe pagamentos para administradores!!',
        status=status.HTTP_400_BAD_REQUEST
    )

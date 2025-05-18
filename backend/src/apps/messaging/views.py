from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.apps import apps  # Añadimos esto para obtener el modelo dinámicamente
from .models import Message

User = get_user_model()


@login_required
def inbox(request):
    # Filtrar mensajes recibidos (no eliminados por el destinatario)
    received_messages = Message.objects.filter(
        recipient=request.user, is_deleted_by_recipient=False
    )

    # Manejar búsqueda/filtrado
    search_query = request.GET.get("search", "")
    if search_query:
        received_messages = received_messages.filter(
            Q(sender__username__icontains=search_query)
            | Q(subject__icontains=search_query)
            | Q(body__icontains=search_query)
        )

    # Contar mensajes no leídos
    unread_count = received_messages.filter(is_read=False).count()

    return render(
        request,
        "messaging/inbox.html",
        {
            "received_messages": received_messages,
            "unread_count": unread_count,
            "search_query": search_query,
        },
    )


@login_required
def sent(request):
    # Filtrar mensajes enviados (no eliminados por el remitente)
    sent_messages = Message.objects.filter(
        sender=request.user, is_deleted_by_sender=False
    )

    # Manejar búsqueda/filtrado
    search_query = request.GET.get("search", "")
    if search_query:
        sent_messages = sent_messages.filter(
            Q(recipient__username__icontains=search_query)
            | Q(subject__icontains=search_query)
            | Q(body__icontains=search_query)
        )

    return render(
        request,
        "messaging/sent.html",
        {
            "sent_messages": sent_messages,
            "search_query": search_query,
        },
    )


@login_required
def compose(request):
    # Obtener contratos activos del usuario actual
    Contract = apps.get_model(
        "real_estate_auth", "Contract"
    )  # Obtenemos el modelo dinámicamente
    contracts = Contract.objects.filter(parties=request.user, status="active")
    allowed_users = set()
    for contract in contracts:
        allowed_users.update(contract.parties.all().exclude(id=request.user.id))

    if request.method == "POST":
        recipient_id = request.POST.get("recipient")
        subject = request.POST.get("subject")
        body = request.POST.get("body")
        contract_id = request.POST.get("contract")

        if recipient_id and subject and body and contract_id:
            recipient = get_object_or_404(User, id=recipient_id)
            contract = get_object_or_404(Contract, id=contract_id)
            # Verificar que el destinatario y el remitente estén en el mismo contrato
            if (
                request.user in contract.parties.all()
                and recipient in contract.parties.all()
            ):
                message = Message(
                    sender=request.user,
                    recipient=recipient,
                    contract=contract,
                    subject=subject,
                    body=body,
                )
                message.save()
                messages.success(request, "Correo enviado exitosamente.")
                return redirect("inbox")
        messages.error(
            request,
            "No tienes permiso para enviar un mensaje a este usuario o falta información.",
        )

    return render(
        request,
        "messaging/compose.html",
        {
            "allowed_users": allowed_users,
            "contracts": contracts,
        },
    )


@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    # Verificar permisos: solo el remitente o destinatario puede ver el mensaje
    if message.sender != request.user and message.recipient != request.user:
        messages.error(request, "No tienes permiso para ver este mensaje.")
        return redirect("inbox")
    # Marcar como leído si el usuario es el destinatario
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()
    return render(
        request,
        "messaging/view_message.html",
        {
            "message": message,
        },
    )


@login_required
def reply_message(request, message_id):
    original_message = get_object_or_404(
        Message, id=message_id, recipient=request.user, is_deleted_by_recipient=False
    )
    if request.method == "POST":
        subject = f"Re: {original_message.subject}"
        body = request.POST.get("body")
        if body:
            message = Message(
                sender=request.user,
                recipient=original_message.sender,
                contract=original_message.contract,
                subject=subject,
                body=body,
            )
            message.save()
            messages.success(request, "Respuesta enviada exitosamente.")
            return redirect("inbox")
        messages.error(request, "El cuerpo del mensaje es obligatorio.")
    return render(
        request,
        "messaging/reply.html",
        {
            "original_message": original_message,
        },
    )


@login_required
def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_read = True
    message.save()
    messages.success(request, "Mensaje marcado como leído.")
    return redirect("inbox")


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # Verificar si el usuario es el remitente o el destinatario
    if message.sender == request.user:
        message.is_deleted_by_sender = True
        message.save()
        messages.success(request, "Mensaje eliminado de tu bandeja de enviados.")
        return redirect("sent")
    elif message.recipient == request.user:
        message.is_deleted_by_recipient = True
        message.save()
        messages.success(request, "Mensaje eliminado de tu bandeja de entrada.")
        return redirect("inbox")

    messages.error(request, "No tienes permiso para eliminar este mensaje.")
    return redirect("inbox")

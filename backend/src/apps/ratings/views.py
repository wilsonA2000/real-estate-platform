from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .models import Rating, Relationship
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def ratings(request):
    ratings = Rating.objects.filter(to_user=request.user, approved=True)
    related_users = set()
    relationships = Relationship.objects.filter(
        user1=request.user
    ) | Relationship.objects.filter(user2=request.user)
    for rel in relationships:
        related_users.add(rel.user1.id if rel.user2 == request.user else rel.user2.id)

    users = User.objects.filter(id__in=related_users).exclude(id=request.user.id)

    if request.method == "POST":
        if request.user.profile_type in ["arrendatario", "prestador"]:
            to_user_id = request.POST.get("to_user")
            score = request.POST.get("score")
            comment = request.POST.get("comment")

            if to_user_id and score and comment and int(to_user_id) in related_users:
                to_user = User.objects.get(id=to_user_id)
                rating = Rating(
                    from_user=request.user,
                    to_user=to_user,
                    score=score,
                    comment=comment,
                )
                rating.save()
                messages.success(request, "Calificación enviada para revisión.")
                return redirect("ratings")
            messages.error(request, "Error: Debes seleccionar un usuario relacionado.")

    return render(
        request,
        "ratings.html",
        {
            "ratings": ratings,
            "users": users,
        },
    )


@login_required
def approve_ratings(request):
    if not request.user.is_superuser:
        messages.error(request, "Solo superusuarios pueden aprobar calificaciones.")
        return redirect("ratings")

    pending_ratings = Rating.objects.filter(approved=False)
    if request.method == "POST":
        rating_id = request.POST.get("rating_id")
        action = request.POST.get("action")
        if rating_id and action in ["approve", "reject"]:
            rating = Rating.objects.get(id=rating_id)
            if action == "approve":
                rating.approved = True
                rating.save()
                messages.success(request, "Calificación aprobada.")
            else:
                rating.delete()
                messages.success(request, "Calificación rechazada.")
        return redirect("approve_ratings")

    return render(
        request, "admin/approve_ratings.html", {"pending_ratings": pending_ratings}
    )

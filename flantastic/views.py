from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import Bakerie, Vote
from django.conf import settings
import json


def render_map(request: HttpRequest) -> HttpResponse:
    zoom_level: int
    if hasattr(settings, "FLANTASTIC_ZOOM_LEVEL_TO_GET_DATA"):
        zoom_level = settings.FLANTASTIC_ZOOM_LEVEL_TO_GET_DATA
    else:
        from .definitions import DEFAULT_FLANTASTIC_ZOOM_LEVEL_TO_GET_DATA

        zoom_level = DEFAULT_FLANTASTIC_ZOOM_LEVEL_TO_GET_DATA
    context = {"zoom_level": zoom_level}

    return render(request, "flantastic/maplayer.html", context)


def edit_bakerie(request: HttpRequest) -> JsonResponse:
    """
    Edition of existing bakerie.
    If no vote is exising, it is created.
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            data: dict = json.loads(request.body)

            bakery = Bakerie.objects.filter(pk=data["pk"]).first()
            # Update bakerie only if authorized
            # IMPROVE: Make groups instead of juste staff
            if request.user.is_staff:
                bakery.enseigne = data["enseigne"]
                bakery.save()

            # Update vote
            vote_q_set = Vote.objects.filter(bakerie__id=data["pk"]).filter(
                user=request.user
            )

            if vote_q_set.exists():
                vote = vote_q_set.first()
                vote.commentaire = data["commentaire"]
                vote.gout = data["gout"]
                vote.pate = data["pate"]
                vote.texture = data["texture"]
                vote.apparence = data["apparence"]
            else:
                vote = Vote(
                    commentaire=data["commentaire"],
                    gout=data["gout"],
                    pate=data["pate"],
                    texture=data["texture"],
                    apparence=data["apparence"],
                    user=request.user,
                    bakerie=bakery,
                )
            vote.save()
            bakery.refresh_from_db()
            data["global_note"] = bakery.global_note

            return JsonResponse(data)
        else:
            raise ConnectionRefusedError("Impossible to post if not logged")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("base")
    else:
        form = SignUpForm()
    return render(request, "flantastic/signup.html", {"form": form})

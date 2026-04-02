from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import date
import json
from django.utils import timezone
from .models import MealEntry, WeightEntry, Profile, FoodItem
from .forms import WeightForm, MealEntryForm, GoalsForm
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Si déjà connecté, hop, vers le dashboard
    return render(request, 'tracker/home.html')

@login_required
def dashboard(request):
    # Utilisation de timezone pour éviter les décalages horaires
    today = timezone.now().date()
    
    # 1. Récupération des repas du jour
    entries = MealEntry.objects.filter(user=request.user, date=today)
    
    # 2. Calcul des totaux (Correction de l'inversion c/f)
    totals = entries.aggregate(
        kcal=Sum('total_kcal'),
        p=Sum('total_proteins'),
        c=Sum('total_glucides'),  # c = carbs (glucides)
        f=Sum('total_lipides')    # f = fats (lipides)
    )

    # 3. Gestion de l'objectif (Target)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    target = profile.target_calories or 2000 # Valeur par défaut si 0
    
    current_kcal = totals.get('kcal') or 0
    remaining = target - current_kcal
    progress = min(int((current_kcal / target) * 100), 100) if target > 0 else 0

    # 4. Données pour le graphique (Correction du bug de Slicing)
    # On récupère le QuerySet complet d'abord
    all_weights = WeightEntry.objects.filter(user=request.user).order_by('date')
    
    # On slice pour le graphique (les 10 derniers)
    graph_weights = all_weights[:10]
    weight_labels = [w.date.strftime("%d/%m") for w in graph_weights]
    weight_values = [float(w.weight_kg) for w in graph_weights]

    context = {
        'entries': entries,
        'totals': totals,
        'target': target,
        'remaining': remaining,
        'progress': progress,
        'profile': profile,
        'weight_labels': json.dumps(weight_labels),
        'weight_values': json.dumps(weight_values),
        # On appelle .last() sur le QuerySet NON découpé
        'last_weight': all_weights.last() if all_weights.exists() else None
    }
    return render(request, 'tracker/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Connecte l'utilisateur après l'inscription
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def add_meal(request):
    if request.method == "POST":
        form = MealEntryForm(request.POST, request.FILES)
        action = request.POST.get('action')

        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            
            custom_name = form.cleaned_data.get('custom_name')
            food_image = form.cleaned_data.get('food_image')

            if custom_name:
                food, created = FoodItem.objects.get_or_create(
                    name=custom_name,
                    defaults={
                        'kcal_per_100g': 0,
                        'proteins': 0,
                        'lipides': 0,
                        'glucides': 0,
                        'image': food_image
                    }
                )
                meal.food_item = food

            # Si on clique sur "Enregistrer le repas"
            if action == "save_meal":
                meal.save()
                return redirect('dashboard')
            
            # Si on clique sur "Créer cet aliment uniquement"
            else:
                # On ne sauvegarde pas le meal, on veut juste créer le FoodItem (déjà fait au-dessus)
                return redirect('add_meal') 
    else:
        form = MealEntryForm(initial={'date': date.today()})
    
    return render(request, 'tracker/add_meal.html', {'form': form})

def add_weight(request):
    if request.method == "POST":
        form = WeightForm(request.POST)
        if form.is_valid():
            weight = form.save(commit=False)
            weight.user = request.user
            weight.save()
            return redirect('dashboard')
    else:
        form = WeightForm(initial={'date': date.today()})
    return render(request, 'tracker/add_weight.html', {'form': form})

def update_goals(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = GoalsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = GoalsForm(instance=profile)
    return render(request, 'tracker/update_goals.html', {'form': form})
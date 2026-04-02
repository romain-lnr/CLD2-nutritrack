from django import forms
from .models import WeightEntry, MealEntry, FoodItem, Profile

class WeightForm(forms.ModelForm):
    """
    Formulaire pour enregistrer le poids.
    Utilisé pour générer la courbe de poids du MVP.
    """
    class Meta:
        model = WeightEntry
        fields = ['weight_kg', 'date']
        widgets = {
            # Utilise le calendrier natif du navigateur (HTML5)
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'weight_kg': forms.NumberInput(attrs={'step': '0.1', 'placeholder': 'ex: 75.5', 'class': 'form-control'}),
        }

class MealEntryForm(forms.ModelForm):
    """
    Formulaire pour le journal alimentaire.
    Gère le Mode A (food_item) et le Mode B (custom_name).
    """
    food_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = MealEntry
        fields = ['date', 'meal_type', 'food_item', 'custom_name', 'quantity']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'food_item': forms.Select(attrs={'class': 'form-control'}),
            'custom_name': forms.TextInput(attrs={'placeholder': 'Nom de l\'aliment (si libre)', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Quantité en grammes', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On rend ces champs optionnels au niveau du formulaire pour permettre le choix A ou B
        self.fields['food_item'].required = False
        self.fields['custom_name'].required = False

    def clean(self):
        """
        Logique de validation personnalisée :
        Vérifie que l'utilisateur a soit choisi un aliment, soit écrit un nom.
        """
        cleaned_data = super().clean()
        food_item = cleaned_data.get('food_item')
        custom_name = cleaned_data.get('custom_name')

        if not food_item and not custom_name:
            raise forms.ValidationError(
                "Vous devez soit sélectionner un aliment (Mode A), soit saisir un nom (Mode B)."
            )
        
        return cleaned_data
    
class GoalsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['target_calories', 'target_proteins', 'target_lipides', 'target_glucides']

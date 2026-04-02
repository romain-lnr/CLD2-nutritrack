from django.db import models
from django.contrib.auth.models import User

# Extension du profil utilisateur
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height_cm = models.IntegerField(null=True, blank=True)
    target_calories = models.IntegerField(default=2000)
    target_proteins = models.IntegerField(null=True, blank=True)
    target_lipides = models.IntegerField(null=True, blank=True)
    target_glucides = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

# Table des Poids
class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight_kg = models.FloatField()
    date = models.DateField()

    class Meta:
        ordering = ['-date']

# Catalogue d'aliments (Mode A)
class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    kcal_per_100g = models.IntegerField()
    proteins = models.FloatField(default=0)
    lipides = models.FloatField(default=0)
    glucides = models.FloatField(default=0)
    image = models.ImageField(upload_to='food_items/', null=True, blank=True)

    def __str__(self):
        return self.name

# Journal Alimentaire
class MealEntry(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Petit-déjeuner'),
        ('lunch', 'Déjeuner'),
        ('dinner', 'Dîner'),
        ('snack', 'Collation'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)

    # Mode A / B
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True)
    custom_name = models.CharField(max_length=200, null=True, blank=True)

    quantity = models.FloatField(help_text="En grammes")

    # Champs calculés automatiquement
    total_kcal = models.IntegerField(default=0)
    total_proteins = models.FloatField(default=0)
    total_lipides = models.FloatField(default=0)
    total_glucides = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # Calcul automatique basé sur l'aliment choisi (Mode A)
        if self.food_item:
            ratio = self.quantity / 100
            self.total_kcal = int(self.food_item.kcal_per_100g * ratio)
            self.total_proteins = round(self.food_item.proteins * ratio, 1)
            self.total_carbs = round(self.food_item.glucides * ratio, 1)
            self.total_fat = round(self.food_item.lipides * ratio, 1)

        if not self.custom_name:
            self.custom_name = self.food_item.name
        super().save(*args, **kwargs)

from django import forms

class GrossesseForm(forms.Form):
    age = forms.IntegerField(label="Âge", min_value=15, max_value=50)
    mois_grossesse = forms.IntegerField(label="Mois de grossesse", min_value=1, max_value=9)
    poids_kg = forms.FloatField(label="Poids (kg)", min_value=40, max_value=150)
    taille_cm = forms.FloatField(label="Taille (cm)", min_value=140, max_value=200)
    
    ACTIVITE_CHOICES = [
        ('faible', 'Faible'),
        ('modérée', 'Modérée'),
        ('élevée', 'Élevée'),
    ]
    activité = forms.ChoiceField(label="Niveau d'activité physique", choices=ACTIVITE_CHOICES)
    
    REGIME_CHOICES = [
        ('omnivore', 'Omnivore'),
        ('végétarien', 'Végétarien'),
        ('végétalien', 'Végétalien'),
    ]
    régime = forms.ChoiceField(label="Régime alimentaire", choices=REGIME_CHOICES)
    
    ANTECEDENTS_CHOICES = [
        ('aucun', 'Aucun'),
        ('diabète', 'Diabète'),
        ('hypertension', 'Hypertension'),
        ('asthme', 'Asthme'),
        ('autre', 'Autre'),
    ]
    antécédents = forms.ChoiceField(label="Antécédents médicaux", choices=ANTECEDENTS_CHOICES)
    
    SYMPTOME_CHOICES = [
        ('aucun', 'Aucun'),
        ('nausée', 'Nausée'),
        ('fatigue', 'Fatigue'),
        ('douleur', 'Douleur'),
    ]
    symptôme = forms.ChoiceField(label="Symptôme principal", choices=SYMPTOME_CHOICES)
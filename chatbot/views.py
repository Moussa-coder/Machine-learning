from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import GrossesseForm
import joblib
import pandas as pd

def home_view(request):
    return render(request, 'chatbot/home.html')

def chatbot_view(request):
    if request.method == 'POST':
        form = GrossesseForm(request.POST)
        if form.is_valid():
            # Chargement du modèle et des encodeurs
            model = joblib.load('grossesse_model.joblib')
            le_target = joblib.load('label_encoder_target.joblib')
            
            # Création d'un DataFrame avec les données du formulaire
            data = {
                'age': [form.cleaned_data['age']],
                'mois_grossesse': [form.cleaned_data['mois_grossesse']],
                'poids_kg': [form.cleaned_data['poids_kg']],
                'taille_cm': [form.cleaned_data['taille_cm']],
                'activité': [form.cleaned_data['activité']],
                'régime': [form.cleaned_data['régime']],
                'antécédents': [form.cleaned_data['antécédents']],
                'symptôme': [form.cleaned_data['symptôme']],
            }
            df = pd.DataFrame(data)
            
            # Encodage des variables catégorielles
            categorical_cols = ['activité', 'régime', 'antécédents', 'symptôme']
            for col in categorical_cols:
                le = joblib.load(f'label_encoder_{col}.joblib')
                df[col] = le.transform(df[col])
            
            # Prédiction
            prediction = model.predict(df)
            profil_risque = le_target.inverse_transform(prediction)[0]
            
            # Conseils selon le profil de risque
            conseils = get_conseils(profil_risque, form.cleaned_data)
            
            return render(request, 'chatbot/resultat.html', {
                'profil_risque': profil_risque,
                'conseils': conseils,
                'form_data': form.cleaned_data
            })
    else:
        form = GrossesseForm()
    
    return render(request, 'chatbot/formulaire.html', {'form': form})

def get_conseils(profil_risque, form_data):
    conseils = []
    
    if profil_risque == 'normal':
        conseils.append("Votre grossesse présente un risque normal. Continuez à prendre soin de vous !")
        conseils.append("Conseils généraux :")
        conseils.append("- Maintenez une alimentation équilibrée et variée")
        conseils.append("- Buvez au moins 1,5 litre d'eau par jour")
        conseils.append("- Pratiquez une activité physique modérée régulièrement")
        
        if form_data['régime'] in ['végétarien', 'végétalien']:
            conseils.append("- En tant que végétarienne/végétalienne, veillez à vos apports en fer et vitamine B12")
    
    elif profil_risque == 'modéré':
        conseils.append("Votre grossesse présente un risque modéré. Une surveillance médicale renforcée est recommandée.")
        conseils.append("Conseils spécifiques :")
        conseils.append("- Consultez votre médecin deux fois par mois")
        conseils.append("- Évitez les situations stressantes")
        conseils.append("- Reposez-vous suffisamment")
        
        if form_data['antécédents'] == 'hypertension':
            conseils.append("- Surveillez régulièrement votre tension artérielle")
        elif form_data['antécédents'] == 'diabète':
            conseils.append("- Contrôlez régulièrement votre glycémie")
    
    else:  # élevé
        conseils.append("Votre grossesse présente un risque élevé. Un suivi médical strict est nécessaire.")
        conseils.append("Recommandations importantes :")
        conseils.append("- Consultez votre médecin chaque semaine")
        conseils.append("- Repos strict si recommandé par votre médecin")
        conseils.append("- Signalez immédiatement tout symptôme inhabituel")
        
        if form_data['age'] > 35:
            conseils.append("- En tant que femme de plus de 35 ans, des examens complémentaires peuvent être nécessaires")
        if form_data['antécédents'] in ['diabète', 'hypertension']:
            conseils.append(f"- Votre antécédent de {form_data['antécédents']} nécessite une attention particulière")
    
    return conseils

def about_view(request):
    return render(request, 'chatbot/about.html')
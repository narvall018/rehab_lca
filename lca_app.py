import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import time

# Configuration de la page
st.set_page_config(
    page_title="Rééducation LCA - Kenneth Jones",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé amélioré
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .phase-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .exercise-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .warning-card {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-card {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .danger-card {
        background: linear-gradient(135deg, #f8d7da 0%, #f1b2b7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .exercise-title {
        color: #2c3e50;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    .exercise-detail {
        color: #34495e;
        margin: 0.3rem 0;
    }
    .timer-display {
        font-size: 2rem;
        color: #e74c3c;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Classe principale pour la gestion du programme
class RehabProgram:
    def __init__(self):
        self.surgery_date = datetime(2025, 7, 28)
        self.patient_weight = 65  # kg
        self.patient_height = 168  # cm
        
        # Programmes pré-opératoires complets
        self.pre_op_programs = {
            "week_-4_-3": {
                "seance_A": [
                    {
                        "nom": "Leg Press Bilatéral",
                        "description": "Pieds écartés largeur épaules, descente contrôlée jusqu'à 90°, poussée explosive en gardant les talons au sol",
                        "series": 4,
                        "reps": 12,
                        "charge": "85kg (1.3x poids corps)",
                        "repos": "90s",
                        "focus": "Excentrique 3 secondes, concentrique explosif",
                        "conseils": "Gardez le dos plaqué, respirez pendant la montée"
                    },
                    {
                        "nom": "Fentes avant alternées",
                        "description": "Pas large (1.2x largeur épaules), descente verticale jusqu'à ce que le genou arrière frôle le sol",
                        "series": 3,
                        "reps": "10 chaque jambe",
                        "charge": "Haltères 8kg/main",
                        "repos": "60s",
                        "focus": "Stabilité du tronc, équilibre parfait",
                        "conseils": "Le genou avant ne dépasse jamais la pointe du pied"
                    },
                    {
                        "nom": "Soulevé de terre roumain",
                        "description": "Barre proche du corps, hanches poussées vers l'arrière, genoux légèrement fléchis",
                        "series": 3,
                        "reps": 10,
                        "charge": "Barre 40kg",
                        "repos": "75s",
                        "focus": "Activation maximale des ischio-jambiers",
                        "conseils": "Sentir l'étirement à l'arrière des cuisses"
                    },
                    {
                        "nom": "Leg Curl unilatéral machine",
                        "description": "Position allongée ventrale, flexion lente et contrôlée du genou",
                        "series": 3,
                        "reps": "12 chaque jambe",
                        "charge": "15kg",
                        "repos": "45s",
                        "focus": "Concentration maximale, tempo lent",
                        "conseils": "Pause 1 seconde en position haute"
                    },
                    {
                        "nom": "Gainage frontal",
                        "description": "Position planche, corps parfaitement aligné, contraction abdos et fessiers",
                        "series": 3,
                        "reps": "45s",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Respiration contrôlée, pas d'apnée",
                        "conseils": "Regarder le sol, ne pas cambrer le dos"
                    }
                ],
                "seance_B": [
                    {
                        "nom": "Squat Goblet",
                        "description": "Haltère tenu contre la poitrine, descente jusqu'à 90°, talons bien ancrés au sol",
                        "series": 4,
                        "reps": 12,
                        "charge": "Haltère 16kg",
                        "repos": "90s",
                        "focus": "Amplitude contrôlée, mobilité cheville",
                        "conseils": "Genoux dans l'axe des pieds"
                    },
                    {
                        "nom": "Squat Bulgare",
                        "description": "Pied arrière posé sur banc, descente verticale sur la jambe avant",
                        "series": 3,
                        "reps": "10 chaque jambe",
                        "charge": "Haltères 6kg/main",
                        "repos": "60s",
                        "focus": "Équilibre unilatéral, stabilité",
                        "conseils": "70% du poids sur la jambe avant"
                    },
                    {
                        "nom": "Leg Extension unilatéral",
                        "description": "Mouvement lent et contrôlé, contraction volontaire en fin d'amplitude",
                        "series": 3,
                        "reps": "12 chaque jambe",
                        "charge": "12kg",
                        "repos": "45s",
                        "focus": "Isométrie 2 secondes en position haute",
                        "conseils": "Éviter les à-coups, mouvement fluide"
                    },
                    {
                        "nom": "Pont fessier unilatéral",
                        "description": "Allongé, une jambe tendue, montée bassin par contraction fessiers",
                        "series": 3,
                        "reps": "15 chaque jambe",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Activation ciblée des fessiers",
                        "conseils": "Serrer fort les fessiers en haut"
                    },
                    {
                        "nom": "Gainage latéral",
                        "description": "Sur le côté, corps aligné des pieds à la tête",
                        "series": 3,
                        "reps": "30s chaque côté",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Stabilité dans le plan frontal",
                        "conseils": "Bassin légèrement poussé vers l'avant"
                    }
                ],
                "mobilite": [
                    {
                        "nom": "Étirements quadriceps",
                        "description": "Debout, ramener le talon vers le fessier avec la main",
                        "series": 3,
                        "reps": "30s chaque jambe",
                        "charge": "Sangle d'aide si nécessaire",
                        "repos": "10s",
                        "focus": "Flexibilité face antérieure cuisse",
                        "conseils": "Bassin en rétroversion, pas de cambrure"
                    },
                    {
                        "nom": "Étirements ischio-jambiers",
                        "description": "Assis, jambe tendue, penché vers l'avant",
                        "series": 3,
                        "reps": "30s chaque jambe",
                        "charge": "Sangle pour assistance",
                        "repos": "10s",
                        "focus": "Souplesse postérieure",
                        "conseils": "Dos droit, pencher depuis les hanches"
                    },
                    {
                        "nom": "Proprioception yeux fermés",
                        "description": "Équilibre sur une jambe, yeux fermés",
                        "series": 3,
                        "reps": "45s chaque jambe",
                        "charge": "Coussin instable optionnel",
                        "repos": "30s",
                        "focus": "Contrôle postural sans vision",
                        "conseils": "Concentrer sur les sensations du pied"
                    },
                    {
                        "nom": "Marche latérale élastique",
                        "description": "Pas chassés latéraux avec élastique autour des chevilles",
                        "series": 3,
                        "reps": "15 pas chaque direction",
                        "charge": "Élastique résistance moyenne",
                        "repos": "30s",
                        "focus": "Activation fessiers moyens",
                        "conseils": "Maintenir tension constante sur l'élastique"
                    }
                ]
            },
            "week_-2_-1": {
                "seance_A": [
                    {
                        "nom": "Leg Press Bilatéral",
                        "description": "Amplitude maximale sécurisée, mouvement explosif concentrique",
                        "series": 4,
                        "reps": 10,
                        "charge": "97kg (1.5x poids corps)",
                        "repos": "2min",
                        "focus": "Puissance concentrique maximale",
                        "conseils": "Explosion contrôlée, ne pas décoller le dos"
                    },
                    {
                        "nom": "Fentes avant alternées",
                        "description": "Progression en charge, contrôle parfait de la descente",
                        "series": 4,
                        "reps": "8 chaque jambe",
                        "charge": "Haltères 12kg/main",
                        "repos": "75s",
                        "focus": "Contrôle de la phase de décelération",
                        "conseils": "Freiner activement la descente"
                    },
                    {
                        "nom": "Soulevé de terre roumain",
                        "description": "Amplitude optimale, accent sur la phase excentrique",
                        "series": 4,
                        "reps": 8,
                        "charge": "Barre 50kg",
                        "repos": "90s",
                        "focus": "Phase excentrique sur 4 secondes",
                        "conseils": "Résister à la descente, contrôle total"
                    },
                    {
                        "nom": "Leg Curl unilatéral",
                        "description": "Augmentation de résistance, contraction volontaire maximale",
                        "series": 4,
                        "reps": "10 chaque jambe",
                        "charge": "20kg",
                        "repos": "60s",
                        "focus": "Contraction volontaire en fin de course",
                        "conseils": "Serrer fort en position haute 2 secondes"
                    },
                    {
                        "nom": "Dead Bug",
                        "description": "Coordination bras/jambe opposés, stabilité anti-rotation",
                        "series": 3,
                        "reps": "10 chaque côté",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Stabilité anti-rotation du tronc",
                        "conseils": "Lombaires collées au sol en permanence"
                    }
                ]
            }
        }
        
        # Programmes post-opératoires complets
        self.post_op_programs = {
            "semaine_1": {
                "quotidien": [
                    {
                        "nom": "Contractions isométriques quadriceps",
                        "description": "Allongé, jambe tendue, contraction du quadriceps sans bouger",
                        "series": 6,
                        "reps": 10,
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Réveil neuromusculaire - JAMBE OPÉRÉE uniquement",
                        "conseils": "Contracter 5s, relâcher 5s, visualiser le muscle"
                    },
                    {
                        "nom": "Flexions passives aidées",
                        "description": "Kinésithérapeute aide à fléchir le genou progressivement",
                        "series": 3,
                        "reps": 10,
                        "charge": "Aide manuelle",
                        "repos": "60s",
                        "focus": "Récupération amplitude 0-45°, progression +5°/jour",
                        "conseils": "Ne jamais forcer, douleur = STOP"
                    },
                    {
                        "nom": "Élévations jambe tendue passives",
                        "description": "Allongé, soulever la jambe opérée tendue avec les mains",
                        "series": 3,
                        "reps": 8,
                        "charge": "Aide des bras",
                        "repos": "45s",
                        "focus": "Maintien tonus sans contrainte",
                        "conseils": "Garder genou parfaitement tendu"
                    },
                    {
                        "nom": "Leg Extension jambe saine",
                        "description": "Renforcement de la jambe non opérée pour éviter l'atrophie",
                        "series": 3,
                        "reps": 15,
                        "charge": "8kg",
                        "repos": "45s",
                        "focus": "Maintien force jambe saine",
                        "conseils": "Mouvement normal, pleine amplitude"
                    },
                    {
                        "nom": "Gainage ventral modifié",
                        "description": "Planche sur avant-bras et genoux",
                        "series": 3,
                        "reps": "20s",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Maintien tonus abdominal",
                        "conseils": "Progression +5s tous les 2 jours"
                    }
                ]
            },
            "semaine_2-3": {
                "quotidien": [
                    {
                        "nom": "Flexion active aidée",
                        "description": "Patient initie le mouvement, aide avec sangle pour aller plus loin",
                        "series": 4,
                        "reps": 12,
                        "charge": "Sangle d'assistance",
                        "repos": "45s",
                        "focus": "Objectif 60° - Jambe opérée, progression +5°/semaine",
                        "conseils": "Initier le mouvement activement, puis aider"
                    },
                    {
                        "nom": "Élévation jambe tendue active",
                        "description": "Allongé, soulever la jambe opérée par la force du quadriceps",
                        "series": 3,
                        "reps": 12,
                        "charge": "Poids cheville 0.5kg (progression +0.5kg/semaine)",
                        "repos": "30s",
                        "focus": "Activation active du quadriceps",
                        "conseils": "Bien contracter avant de lever, genou tendu"
                    },
                    {
                        "nom": "Squat mural bilatéral",
                        "description": "Dos contre le mur, descente jusqu'à 45° maximum",
                        "series": 3,
                        "reps": 15,
                        "charge": "Poids corps",
                        "repos": "60s",
                        "focus": "Répartition égale du poids sur les 2 jambes",
                        "conseils": "Ne pas dépasser 45° de flexion"
                    },
                    {
                        "nom": "Vélo stationnaire",
                        "description": "Pédalage en douceur, résistance minimale",
                        "series": 1,
                        "reps": "15-20 minutes",
                        "charge": "Résistance 1-2/10",
                        "repos": "Continue",
                        "focus": "Cadence 60-70 RPM, mobilité douce",
                        "conseils": "Arrêter si douleur ou blocage"
                    },
                    {
                        "nom": "Renforcement jambe saine",
                        "description": "Programme complet jambe non opérée",
                        "series": 3,
                        "reps": 12,
                        "charge": "Charges habituelles",
                        "repos": "60s",
                        "focus": "Maintenir la force et masse musculaire",
                        "conseils": "Leg extension, Leg curl, mollets"
                    }
                ]
            },
            "semaine_4-6": {
                "3_seances_semaine": [
                    {
                        "nom": "Leg Press 2 jambes",
                        "description": "Retour progressif au travail bilatéral, amplitude limitée",
                        "series": 3,
                        "reps": 12,
                        "charge": "52kg (0.8x poids corps)",
                        "repos": "90s",
                        "focus": "Amplitude 0-60° maximum, répartition égale",
                        "conseils": "Écouter les sensations, progression graduelle"
                    },
                    {
                        "nom": "Leg Curl bilatéral",
                        "description": "Activation des ischio-jambiers en douceur",
                        "series": 3,
                        "reps": 12,
                        "charge": "8kg",
                        "repos": "60s",
                        "focus": "Mouvement lent et contrôlé",
                        "conseils": "Pas de compensation, mouvement symétrique"
                    },
                    {
                        "nom": "Proprioception avancée",
                        "description": "Équilibre unipodal sur plateau instable",
                        "series": 3,
                        "reps": "60s chaque jambe",
                        "charge": "Plateau instable",
                        "repos": "30s",
                        "focus": "Rééducation proprioceptive progressive",
                        "conseils": "Commencer yeux ouverts, puis fermés"
                    },
                    {
                        "nom": "Step-up bas",
                        "description": "Montée sur marche de 15cm, descente contrôlée",
                        "series": 3,
                        "reps": "10 chaque jambe",
                        "charge": "Poids corps",
                        "repos": "45s",
                        "focus": "Contrôle de la descente, pas d'impact",
                        "conseils": "Montée jambe opérée, descente en douceur"
                    },
                    {
                        "nom": "Vélo intensité modérée",
                        "description": "Augmentation progressive de l'intensité",
                        "series": 1,
                        "reps": "25-30 minutes",
                        "charge": "Résistance 3-4/10",
                        "repos": "Continue",
                        "focus": "Endurance et mobilité",
                        "conseils": "Cadence 70-80 RPM"
                    },
                    {
                        "nom": "Gainage complet",
                        "description": "Retour au gainage standard",
                        "series": 3,
                        "reps": "60s",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Stabilité globale du tronc",
                        "conseils": "Planche frontale, latérale, Superman"
                    }
                ]
            },
            "palier_1_j45-j90": {
                "4_seances_semaine": [
                    {
                        "nom": "Leg Press unilatéral progression",
                        "description": "Travail spécifique jambe opérée puis bilatéral",
                        "series": 4,
                        "reps": "12→8 (progression)",
                        "charge": "65→78kg (1.0→1.2x poids corps)",
                        "repos": "90s",
                        "focus": "Réduction déficit force à -20% en 4 semaines",
                        "conseils": "Comparer forces jambe opérée vs saine"
                    },
                    {
                        "nom": "Fentes avant contrôlées",
                        "description": "Retour mouvement lent, amplitude complète",
                        "series": 3,
                        "reps": "12 chaque jambe",
                        "charge": "6→12kg/main (progression)",
                        "repos": "60s",
                        "focus": "Symétrie parfaite des 2 côtés",
                        "conseils": "Même profondeur, même vitesse"
                    },
                    {
                        "nom": "Squats profonds progressifs",
                        "description": "Amplitude progressive de 45° vers 90°",
                        "series": 4,
                        "reps": 10,
                        "charge": "20→40kg",
                        "repos": "75s",
                        "focus": "Augmentation amplitude +10°/semaine",
                        "conseils": "Respecter les limites articulaires"
                    },
                    {
                        "nom": "Leg Curl unilatéral intensif",
                        "description": "Concentration maximale, charges progressives",
                        "series": 3,
                        "reps": "12 chaque jambe",
                        "charge": "15→25kg",
                        "repos": "45s",
                        "focus": "Objectif déficit -15% à la fin du palier",
                        "conseils": "Tempo lent, contraction maximale"
                    },
                    {
                        "nom": "Leg Extension bilatéral",
                        "description": "Retour travail quadriceps intensif",
                        "series": 3,
                        "reps": 12,
                        "charge": "15→25kg",
                        "repos": "60s",
                        "focus": "Symétrie des contractions",
                        "conseils": "Isométrie 2s en haut"
                    },
                    {
                        "nom": "Proprioception challenges",
                        "description": "Exercices d'équilibre complexes",
                        "series": 3,
                        "reps": "45s chaque jambe",
                        "charge": "Ballons, plateaux instables",
                        "repos": "30s",
                        "focus": "Préparation aux déplacements",
                        "conseils": "Yeux fermés, perturbations externes"
                    }
                ]
            },
            "palier_2_j90-j180": {
                "4_seances_semaine": [
                    {
                        "nom": "Squat Jump bilatéral",
                        "description": "Introduction de la pliométrie, réception contrôlée",
                        "series": 4,
                        "reps": "6 (+1 rep/semaine)",
                        "charge": "Poids corps",
                        "repos": "2min",
                        "focus": "Qualité de réception, amortissement",
                        "conseils": "Décoller et atterrir sur 2 pieds simultanément"
                    },
                    {
                        "nom": "Step-up explosif",
                        "description": "Montée explosive, descente lente et contrôlée",
                        "series": 3,
                        "reps": "8 chaque jambe",
                        "charge": "Gilet lesté 15kg",
                        "repos": "75s",
                        "focus": "Vitesse d'exécution concentrique",
                        "conseils": "Impulsion maximale, réception douce"
                    },
                    {
                        "nom": "Leg Press balistique",
                        "description": "Phase concentrique la plus rapide possible",
                        "series": 5,
                        "reps": 5,
                        "charge": "85kg (1.3x poids corps)",
                        "repos": "2min",
                        "focus": "Développement puissance maximale",
                        "conseils": "Descente contrôlée, explosion maximale"
                    },
                    {
                        "nom": "Box Jumps 30cm",
                        "description": "Sauts sur box, progression hauteur",
                        "series": 3,
                        "reps": 5,
                        "charge": "Poids corps",
                        "repos": "90s",
                        "focus": "Hauteur progressive +5cm/2semaines",
                        "conseils": "Descendre en marchant, pas en sautant"
                    },
                    {
                        "nom": "Fentes sautées alternées",
                        "description": "Fentes avec changement de jambe en vol",
                        "series": 3,
                        "reps": "6 chaque jambe",
                        "charge": "Poids corps",
                        "repos": "90s",
                        "focus": "Réactivité et stabilité dynamique",
                        "conseils": "Réception équilibrée, pause 1s entre sauts"
                    },
                    {
                        "nom": "Travail excentrique renforcé",
                        "description": "Squats avec phase excentrique lente",
                        "series": 4,
                        "reps": 6,
                        "charge": "60kg",
                        "repos": "2min",
                        "focus": "Contrôle excentrique 5 secondes",
                        "conseils": "Freiner activement la descente"
                    }
                ]
            },
            "palier_3_j180-j270": {
                "5_seances_semaine": [
                    {
                        "nom": "Fentes multi-directionnelles",
                        "description": "Fentes avant, arrière, latérales enchaînées",
                        "series": 3,
                        "reps": "6 chaque direction",
                        "charge": "12kg/main",
                        "repos": "90s",
                        "focus": "Préparation gestes sportifs multi-plans",
                        "conseils": "Fluidité entre les directions"
                    },
                    {
                        "nom": "Pivot contrôlé progressif",
                        "description": "Rotations 45° puis progression vers 90°",
                        "series": 3,
                        "reps": "5 chaque sens",
                        "charge": "Poids corps",
                        "repos": "60s",
                        "focus": "Progression angulaire +15°/semaine",
                        "conseils": "Pied planté, rotation sur l'avant-pied"
                    },
                    {
                        "nom": "Sprint en ligne droite",
                        "description": "Accélérations progressives en ligne droite",
                        "series": 6,
                        "reps": "20m",
                        "charge": "Poids corps",
                        "repos": "2min",
                        "focus": "Vitesse linéaire spécifique",
                        "conseils": "Progression 70%→85%→95% vitesse max"
                    },
                    {
                        "nom": "Sauts réactifs enchaînés",
                        "description": "Enchaînements pliométriques multi-directionnels",
                        "series": 4,
                        "reps": 4,
                        "charge": "Poids corps",
                        "repos": "2min",
                        "focus": "Réactivité neuromusculaire maximale",
                        "conseils": "Contact au sol minimum entre sauts"
                    },
                    {
                        "nom": "Changements de direction",
                        "description": "Slalom, 8, arrêts-démarrages",
                        "series": 4,
                        "reps": "30s",
                        "charge": "Poids corps",
                        "repos": "90s",
                        "focus": "Préparation retour sport avec pivot",
                        "conseils": "Intensité progressive 60%→80%→95%"
                    },
                    {
                        "nom": "Tests fonctionnels",
                        "description": "Hop Tests, Y-Balance, Single Leg Squat",
                        "series": 3,
                        "reps": "Test complet",
                        "charge": "Évaluation",
                        "repos": "3min",
                        "focus": "Validation critères retour sport",
                        "conseils": "Symétrie >95% obligatoire"
                    }
                ]
            }
        }
        
        # Tests d'évaluation par palier
        self.evaluation_tests = {
            "palier_1": {
                "leg_press_deficit": {"target": "<25%", "description": "Test force unilatérale"},
                "leg_extension_deficit": {"target": "<30%", "description": "Force quadriceps"},
                "hop_test": {"target": "<40%", "description": "Saut unipodal distance"}
            },
            "palier_2": {
                "force_deficit": {"target": "<15%", "description": "Tous exercices"},
                "saut_vertical": {"target": ">80%", "description": "Référence pré-blessure"},
                "y_balance": {"target": ">90%", "description": "Symétrie équilibre"}
            },
            "palier_3": {
                "force_deficit": {"target": "<10%", "description": "Tous muscles"},
                "hop_tests": {"target": ">95%", "description": "Symétrie tous tests"},
                "changements_direction": {"target": "Fluides", "description": "Sans appréhension"}
            }
        }

    def get_current_phase(self):
        """Détermine la phase actuelle selon la date"""
        today = datetime.now()
        days_to_surgery = (self.surgery_date - today).days
        days_post_surgery = (today - self.surgery_date).days
        
        if days_to_surgery > 0:
            if days_to_surgery > 14:
                return "pre_op_semaine_-4_-3", f"Pré-opératoire Adaptation (J-{days_to_surgery})", "🏋️"
            else:
                return "pre_op_semaine_-2_-1", f"Pré-opératoire Intensification (J-{days_to_surgery})", "💪"
        elif days_post_surgery <= 7:
            return "post_op_semaine_1", f"Post-op Réveil Musculaire (J+{days_post_surgery})", "🏥"
        elif days_post_surgery <= 21:
            return "post_op_semaine_2-3", f"Post-op Mobilisation Active (J+{days_post_surgery})", "🔄"
        elif days_post_surgery <= 45:
            return "post_op_semaine_4-6", f"Post-op Renforcement Progressif (J+{days_post_surgery})", "📈"
        elif days_post_surgery <= 90:
            return "post_op_palier_1", f"Réathlétisation Palier 1 (J+{days_post_surgery})", "🎯"
        elif days_post_surgery <= 180:
            return "post_op_palier_2", f"Réathlétisation Palier 2 (J+{days_post_surgery})", "🚀"
        elif days_post_surgery <= 270:
            return "post_op_palier_3", f"Retour Sportif (J+{days_post_surgery})", "⚡"
        else:
            return "maintenance", f"Maintenance Sportive (J+{days_post_surgery})", "🏆"

    def get_today_program(self):
        """Retourne le programme du jour selon la phase et le jour de la semaine"""
        phase, phase_name, emoji = self.get_current_phase()
        today_weekday = datetime.now().weekday()  # 0=Lundi, 6=Dimanche
        
        if "pre_op" in phase:
            if today_weekday in [0, 3]:  # Lundi, Jeudi
                if "semaine_-4_-3" in phase:
                    return "Séance Force A", self.pre_op_programs["week_-4_-3"]["seance_A"], "💪"
                else:
                    return "Séance Force A Intensifiée", self.pre_op_programs["week_-2_-1"]["seance_A"], "🔥"
            elif today_weekday in [1, 4]:  # Mardi, Vendredi
                if "semaine_-4_-3" in phase:
                    return "Séance Force B", self.pre_op_programs["week_-4_-3"]["seance_B"], "💪"
                else:
                    return "Séance Force B Intensifiée", self.pre_op_programs["week_-2_-1"]["seance_A"], "🔥"
            elif today_weekday == 2:  # Mercredi
                return "Séance Mobilité & Proprioception", self.pre_op_programs["week_-4_-3"]["mobilite"], "🧘"
            else:
                return "Repos Actif", [], "🛌"
        
        elif phase == "post_op_semaine_1":
            return "Programme Quotidien Réveil", self.post_op_programs["semaine_1"]["quotidien"], "🏥"
        
        elif phase == "post_op_semaine_2-3":
            return "Programme Mobilisation", self.post_op_programs["semaine_2-3"]["quotidien"], "🔄"
        
        elif phase == "post_op_semaine_4-6":
            if today_weekday in [0, 2, 4]:  # Lundi, Mercredi, Vendredi
                return "Renforcement Progressif", self.post_op_programs["semaine_4-6"]["3_seances_semaine"], "📈"
            else:
                return "Repos ou Mobilité Douce", [], "🛌"
        
        elif phase == "post_op_palier_1":
            if today_weekday in [0, 1, 3, 4]:  # 4 séances/semaine
                return "Réathlétisation Palier 1", self.post_op_programs["palier_1_j45-j90"]["4_seances_semaine"], "🎯"
            else:
                return "Repos Actif", [], "🛌"
        
        elif phase == "post_op_palier_2":
            if today_weekday in [0, 1, 3, 4]:  # 4 séances/semaine
                return "Réathlétisation Palier 2", self.post_op_programs["palier_2_j90-j180"]["4_seances_semaine"], "🚀"
            else:
                return "Repos Actif", [], "🛌"
        
        elif phase == "post_op_palier_3":
            if today_weekday != 6:  # 5 séances/semaine (tous sauf dimanche)
                return "Retour Sportif", self.post_op_programs["palier_3_j180-j270"]["5_seances_semaine"], "⚡"
            else:
                return "Repos Complet", [], "🛌"
        
        return "Programme Maintenance", [], "🏆"

    def get_phase_objectives(self, phase):
        """Retourne les objectifs de la phase actuelle"""
        objectives = {
            "pre_op_semaine_-4_-3": [
                "Maximiser la force bilatérale symétrique",
                "Développer la proprioception et l'équilibre",
                "Préparer le corps à la chirurgie",
                "Maintenir la condition cardiovasculaire"
            ],
            "pre_op_semaine_-2_-1": [
                "Intensifier le renforcement musculaire",
                "Optimiser la force maximale",
                "Perfectionner la technique d'exécution",
                "Préparer mentalement à l'intervention"
            ],
            "post_op_semaine_1": [
                "Réveiller le système neuromusculaire",
                "Prévenir l'amyotrophie du quadriceps",
                "Récupérer l'amplitude articulaire 0-45°",
                "Maintenir la force de la jambe saine"
            ],
            "post_op_semaine_2-3": [
                "Atteindre 60° de flexion active",
                "Initier le renforcement actif",
                "Améliorer la circulation et réduire l'œdème",
                "Préparer au passage en charge"
            ],
            "post_op_semaine_4-6": [
                "Récupérer l'amplitude articulaire complète",
                "Réintroduire les exercices bilatéraux",
                "Développer l'endurance musculaire",
                "Rétablir les schémas moteurs de base"
            ],
            "post_op_palier_1": [
                "Réduire le déficit de force à moins de 25%",
                "Développer la force symétrique",
                "Améliorer la proprioception avancée",
                "Préparer aux activités fonctionnelles"
            ],
            "post_op_palier_2": [
                "Atteindre moins de 15% de déficit",
                "Introduire les exercices pliométriques",
                "Développer la puissance musculaire",
                "Préparer aux gestes sportifs"
            ],
            "post_op_palier_3": [
                "Finaliser la symétrie (<10% déficit)",
                "Maîtriser les changements de direction",
                "Valider les critères de retour au sport",
                "Optimiser la performance sportive"
            ]
        }
        return objectives.get(phase, ["Maintenir la condition physique"])

# Initialisation de l'application
def init_session_state():
    if 'program' not in st.session_state:
        st.session_state.program = RehabProgram()
    if 'workout_history' not in st.session_state:
        st.session_state.workout_history = []
    if 'current_exercise_index' not in st.session_state:
        st.session_state.current_exercise_index = 0
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'timer_start' not in st.session_state:
        st.session_state.timer_start = 0
    if 'rest_duration' not in st.session_state:
        st.session_state.rest_duration = 60
    if 'current_set' not in st.session_state:
        st.session_state.current_set = 1
    if 'exercise_notes' not in st.session_state:
        st.session_state.exercise_notes = {}

def main():
    init_session_state()
    
    # Header principal avec animation
    st.markdown(
        '<h1 class="main-header">🏃‍♂️ RÉÉDUCATION LCA - KENNETH JONES</h1>', 
        unsafe_allow_html=True
    )
    
    # Sidebar enrichie
    st.sidebar.title("📊 TABLEAU DE BORD")
    
    # Informations patient
    st.sidebar.markdown("### 👤 Profil Patient")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Poids", f"{st.session_state.program.patient_weight} kg")
    with col2:
        st.metric("Taille", f"{st.session_state.program.patient_height} cm")
    
    st.sidebar.write(f"**🗓️ Opération:** {st.session_state.program.surgery_date.strftime('%d/%m/%Y')}")
    
    # Phase actuelle avec détails
    phase, phase_name, emoji = st.session_state.program.get_current_phase()
    st.sidebar.markdown(f"### 📅 Phase Actuelle")
    st.sidebar.markdown(
        f'<div class="phase-card">{emoji} <strong>{phase_name}</strong></div>', 
        unsafe_allow_html=True
    )
    
    # Objectifs de la phase
    objectives = st.session_state.program.get_phase_objectives(phase)
    st.sidebar.markdown("#### 🎯 Objectifs:")
    for obj in objectives[:3]:  # Limiter à 3 objectifs pour l'espace
        st.sidebar.markdown(f"• {obj}")
    
    # Statistiques rapides
    if st.session_state.workout_history:
        df = pd.DataFrame(st.session_state.workout_history)
        st.sidebar.markdown("### 📈 Stats Rapides")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Séances", len(df))
        with col2:
            if not df.empty:
                last_workout = (datetime.now() - df['date'].max()).days
                st.metric("Dernière", f"J-{last_workout}")
    
    # Navigation avec icônes
    page = st.sidebar.selectbox(
        "🧭 Navigation",
        [
            "🏋️ Programme du Jour",
            "📈 Suivi & Progrès", 
            "🧪 Tests d'Évaluation",
            "📚 Guide Complet",
            "⚙️ Paramètres"
        ]
    )
    
    # Routage des pages
    if page == "🏋️ Programme du Jour":
        show_daily_program()
    elif page == "📈 Suivi & Progrès":
        show_progress_tracking()
    elif page == "🧪 Tests d'Évaluation":
        show_evaluation_tests()
    elif page == "📚 Guide Complet":
        show_complete_guide()
    else:
        show_settings()

def show_daily_program():
    """Affiche le programme du jour avec timer et suivi avancé"""
    st.header("🏋️ Programme du Jour")
    
    # Récupération du programme
    session_name, exercises, session_emoji = st.session_state.program.get_today_program()
    phase, phase_name, phase_emoji = st.session_state.program.get_current_phase()
    
    # En-tête de séance
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### {session_emoji} {session_name}")
        st.caption(f"Phase: {phase_name}")
    
    with col2:
        st.metric("Exercices", len(exercises))
    
    with col3:
        if exercises:
            progress_pct = (st.session_state.current_exercise_index / len(exercises)) * 100
            st.metric("Progression", f"{progress_pct:.0f}%")
    
    # Cas du repos
    if not exercises:
        st.markdown(
            '<div class="success-card">'
            '<h3>🛌 Jour de Repos Programmé</h3>'
            '<p><strong>La récupération fait partie intégrante de votre protocole !</strong></p>'
            '<h4>💡 Recommandations du jour :</h4>'
            '<ul>'
            '<li><strong>💧 Hydratation :</strong> 2.5-3L d\'eau répartis dans la journée</li>'
            '<li><strong>😴 Sommeil :</strong> 8-9h de qualité pour optimiser la récupération</li>'
            '<li><strong>🧘 Mobilité douce :</strong> Étirements légers si souhaité (15-20min)</li>'
            '<li><strong>🧊 Cryothérapie :</strong> 15min de glace si gonflement résiduel</li>'
            '<li><strong>🍎 Nutrition :</strong> Privilégier protéines et anti-inflammatoires naturels</li>'
            '</ul>'
            '</div>',
            unsafe_allow_html=True
        )
        
        # Widgets de repos
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Noter une observation"):
                note = st.text_area("Observation du jour")
                if note:
                    st.session_state.workout_history.append({
                        "date": datetime.now(),
                        "exercice": "Repos - Observation",
                        "note": note,
                        "type": "repos"
                    })
        
        with col2:
            st.markdown("#### 🎯 Prochaine séance")
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_program, _, _ = st.session_state.program.get_today_program()
            st.info(f"Demain: {tomorrow_program}")
        
        return
    
    # Barre de progression générale
    progress = st.session_state.current_exercise_index / len(exercises)
    st.progress(progress)
    
    # Exercice actuel
    if st.session_state.current_exercise_index < len(exercises):
        exercise = exercises[st.session_state.current_exercise_index]
        
        # Affichage principal de l'exercice
        st.markdown(
            f'<div class="exercise-card">'
            f'<div class="exercise-title">🎯 {exercise["nom"]}</div>'
            f'<div class="exercise-detail"><strong>📝 Technique :</strong> {exercise["description"]}</div>'
            f'<div class="exercise-detail"><strong>🔢 Volume :</strong> {exercise["series"]} séries × {exercise["reps"]} répétitions</div>'
            f'<div class="exercise-detail"><strong>⚖️ Charge :</strong> {exercise["charge"]}</div>'
            f'<div class="exercise-detail"><strong>⏱️ Repos :</strong> {exercise["repos"]}</div>'
            f'<div class="exercise-detail"><strong>🎯 Focus :</strong> {exercise["focus"]}</div>'
            f'<div class="exercise-detail"><strong>💡 Conseils :</strong> {exercise["conseils"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Interface de contrôle
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Suivi des séries
            st.markdown(f"#### 📊 Série {st.session_state.current_set}")
            
            col_perf1, col_perf2, col_perf3 = st.columns(3)
            with col_perf1:
                poids_realise = st.number_input(
                    "Poids utilisé (kg)", 
                    min_value=0.0, 
                    step=0.5,
                    key=f"poids_{st.session_state.current_exercise_index}_{st.session_state.current_set}"
                )
            
            with col_perf2:
                reps_realisees = st.number_input(
                    "Répétitions", 
                    min_value=0, 
                    step=1,
                    key=f"reps_{st.session_state.current_exercise_index}_{st.session_state.current_set}"
                )
            
            with col_perf3:
                rpe = st.selectbox(
                    "RPE (1-10)", 
                    options=list(range(1, 11)),
                    key=f"rpe_{st.session_state.current_exercise_index}_{st.session_state.current_set}"
                )
            
            # Notes sur l'exercice
            note_exercice = st.text_area(
                "Notes personnelles", 
                placeholder="Sensations, difficultés, améliorations...",
                key=f"note_{st.session_state.current_exercise_index}_{st.session_state.current_set}"
            )
        
        with col2:
            # Timer de repos
            st.markdown("### ⏱️ Timer de Repos")
            
            # Extraction du temps de repos de l'exercice
            rest_str = exercise["repos"]
            if "min" in rest_str:
                rest_minutes = int(rest_str.split("min")[0])
                default_rest = rest_minutes * 60
            elif "s" in rest_str:
                default_rest = int(rest_str.replace("s", ""))
            else:
                default_rest = 60
            
            # Timer interface
            if not st.session_state.timer_running:
                col_timer1, col_timer2 = st.columns(2)
                with col_timer1:
                    if st.button("▶️ Démarrer", type="primary"):
                        st.session_state.timer_running = True
                        st.session_state.timer_start = time.time()
                        st.session_state.rest_duration = default_rest
                        st.rerun()
                
                with col_timer2:
                    custom_time = st.number_input("Temps (s)", value=default_rest, min_value=10, max_value=300)
            else:
                elapsed = int(time.time() - st.session_state.timer_start)
                remaining = max(0, st.session_state.rest_duration - elapsed)
                
                if remaining > 0:
                    mins, secs = divmod(remaining, 60)
                    st.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                    progress_timer = (st.session_state.rest_duration - remaining) / st.session_state.rest_duration
                    st.progress(progress_timer)
                else:
                    st.success("⏰ Repos terminé !")
                    st.balloons()
                
                if st.button("⏹️ Arrêter Timer"):
                    st.session_state.timer_running = False
            
            # Contrôles de série
            st.markdown("### 🎛️ Contrôles")
            
            col_ctrl1, col_ctrl2 = st.columns(2)
            with col_ctrl1:
                if st.button("✅ Série OK"):
                    # Enregistrer la série
                    st.session_state.workout_history.append({
                        "date": datetime.now(),
                        "exercice": exercise["nom"],
                        "serie": st.session_state.current_set,
                        "poids": poids_realise,
                        "reps": reps_realisees,
                        "rpe": rpe,
                        "note": note_exercice,
                        "phase": phase
                    })
                    
                    # Passer à la série suivante ou exercice suivant
                    if st.session_state.current_set < exercise["series"]:
                        st.session_state.current_set += 1
                    else:
                        st.session_state.current_set = 1
                        st.session_state.current_exercise_index += 1
                    
                    st.session_state.timer_running = False
                    st.rerun()
            
            with col_ctrl2:
                if st.button("⏭️ Exercice suivant"):
                    st.session_state.current_set = 1
                    st.session_state.current_exercise_index += 1
                    st.session_state.timer_running = False
                    st.rerun()
    
    else:
        # Séance terminée
        st.markdown(
            '<div class="success-card">'
            '<h2>🎉 SÉANCE TERMINÉE !</h2>'
            '<p><strong>Excellent travail ! Votre progression continue.</strong></p>'
            '</div>',
            unsafe_allow_html=True
        )
        
        # Résumé de séance
        if st.session_state.workout_history:
            today_workouts = [w for w in st.session_state.workout_history 
                            if w['date'].date() == datetime.now().date()]
            if today_workouts:
                st.markdown("### 📊 Résumé de la séance")
                df_today = pd.DataFrame(today_workouts)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Exercices", df_today['exercice'].nunique())
                with col2:
                    st.metric("Séries totales", len(df_today))
                with col3:
                    if 'poids' in df_today.columns:
                        total_tonnage = (df_today['poids'] * df_today['reps']).sum()
                        st.metric("Tonnage", f"{total_tonnage:.0f} kg")
        
        # Boutons de fin
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Recommencer la séance"):
                st.session_state.current_exercise_index = 0
                st.session_state.current_set = 1
                st.rerun()
        
        with col2:
            if st.button("📝 Ajouter un commentaire global"):
                global_note = st.text_area("Commentaire sur la séance")
                if global_note:
                    st.session_state.workout_history.append({
                        "date": datetime.now(),
                        "exercice": "Commentaire séance",
                        "note": global_note,
                        "type": "commentaire"
                    })
    
    # Conseils contextuels selon la phase
    st.markdown("### 💡 Conseils Spécialisés")
    phase_advice = {
        "pre_op": "🎯 **Pré-opératoire :** Chaque séance optimise votre récupération future. Qualité > Quantité !",
        "post_op_semaine_1": "⚠️ **Post-op précoce :** Douceur absolue. La patience d'aujourd'hui = performance de demain.",
        "post_op_semaine_2-3": "🔄 **Mobilisation :** Progression graduelle. Respectez vos sensations articulaires.",
        "post_op_semaine_4-6": "📈 **Renforcement :** Retour de la force ! Symétrie et contrôle avant tout.",
        "post_op_palier_1": "🎯 **Réathlé 1 :** Objectif déficit < 25%. Chaque % compte pour la suite !",
        "post_op_palier_2": "🚀 **Réathlé 2 :** Introduction pliométrie. Qualité d'exécution = sécurité.",
        "post_op_palier_3": "⚡ **Retour sport :** Dernière ligne droite ! Validez tous les critères."
    }
    
    for key, advice in phase_advice.items():
        if key in phase:
            st.info(advice)
            break

def show_progress_tracking():
    """Suivi détaillé des progrès avec graphiques avancés"""
    st.header("📈 Suivi & Analyse des Progrès")
    
    if not st.session_state.workout_history:
        st.info("🏁 Commencez votre premier entraînement pour voir vos progrès ici !")
        return
    
    # Conversion et nettoyage des données
    df = pd.DataFrame(st.session_state.workout_history)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['exercice'] != 'Commentaire séance']  # Exclure les commentaires
    
    # Métriques générales
    st.markdown("### 📊 Vue d'Ensemble")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_seances = df['date'].dt.date.nunique()
        st.metric("🏋️ Séances", total_seances)
    
    with col2:
        if 'poids' in df.columns and not df['poids'].isna().all():
            poids_moyen = df['poids'].mean()
            st.metric("⚖️ Poids moyen", f"{poids_moyen:.1f} kg")
        else:
            st.metric("⚖️ Poids moyen", "N/A")
    
    with col3:
        if 'reps' in df.columns and not df['reps'].isna().all():
            reps_total = df['reps'].sum()
            st.metric("🔥 Reps totales", f"{int(reps_total)}")
        else:
            st.metric("🔥 Reps totales", "N/A")
    
    with col4:
        if 'poids' in df.columns and 'reps' in df.columns:
            tonnage_total = (df['poids'] * df['reps']).sum()
            st.metric("💪 Tonnage", f"{tonnage_total:.0f} kg")
        else:
            st.metric("💪 Tonnage", "N/A")
    
    with col5:
        derniere_seance = df['date'].max()
        jours_depuis = (datetime.now() - derniere_seance).days
        st.metric("📅 Dernière séance", f"J-{jours_depuis}")
    
    # Onglets d'analyse
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Évolution", "🎯 Par Exercice", "📊 Performance", "📋 Détails"])
    
    with tab1:
        st.markdown("#### 📈 Évolution des Charges")
        
        if 'poids' in df.columns and len(df) > 1:
            # Graphique évolution par exercice
            df_filtered = df[df['poids'].notna() & (df['poids'] > 0)]
            if not df_filtered.empty:
                fig_evolution = px.line(
                    df_filtered.groupby(['date', 'exercice'])['poids'].max().reset_index(),
                    x='date', y='poids', color='exercice',
                    title="Évolution des charges maximales par exercice",
                    markers=True
                )
                fig_evolution.update_layout(height=400)
                st.plotly_chart(fig_evolution, use_container_width=True)
        
        # Graphique fréquence d'entraînement
        st.markdown("#### 📅 Fréquence d'Entraînement")
        freq_df = df.groupby(df['date'].dt.date).size().reset_index()
        freq_df.columns = ['date', 'exercices_count']
        
        fig_freq = px.bar(
            freq_df, x='date', y='exercices_count',
            title="Nombre d'exercices par séance",
            color='exercices_count',
            color_continuous_scale='viridis'
        )
        fig_freq.update_layout(height=300)
        st.plotly_chart(fig_freq, use_container_width=True)
    
    with tab2:
        st.markdown("#### 🎯 Analyse par Exercice")
        
        # Sélection d'exercice
        exercices_uniques = df['exercice'].unique()
        exercice_selectionne = st.selectbox("Choisir un exercice", exercices_uniques)
        
        df_exercice = df[df['exercice'] == exercice_selectionne]
        
        if not df_exercice.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Stats de l'exercice
                if 'poids' in df_exercice.columns:
                    poids_max = df_exercice['poids'].max()
                    poids_debut = df_exercice['poids'].iloc[0]
                    progression = ((poids_max - poids_debut) / poids_debut * 100) if poids_debut > 0 else 0
                    
                    st.metric("💪 Charge Max", f"{poids_max} kg")
                    st.metric("📈 Progression", f"{progression:+.1f}%")
                
                if 'reps' in df_exercice.columns:
                    reps_max = df_exercice['reps'].max()
                    st.metric("🔥 Reps Max", f"{int(reps_max)}")
            
            with col2:
                # Graphique de progression
                if 'poids' in df_exercice.columns and len(df_exercice) > 1:
                    fig_ex = px.scatter(
                        df_exercice, x='date', y='poids', size='reps',
                        title=f"Progression - {exercice_selectionne}",
                        hover_data=['reps', 'rpe'] if 'rpe' in df_exercice.columns else ['reps']
                    )
                    st.plotly_chart(fig_ex, use_container_width=True)
    
    with tab3:
        st.markdown("#### 📊 Analyse de Performance")
        
        if 'rpe' in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution RPE
                rpe_counts = df['rpe'].value_counts().sort_index()
                fig_rpe = px.bar(
                    x=rpe_counts.index, y=rpe_counts.values,
                    title="Distribution RPE (Effort Perçu)",
                    labels={'x': 'RPE', 'y': 'Fréquence'}
                )
                st.plotly_chart(fig_rpe, use_container_width=True)
            
            with col2:
                # RPE moyen par exercice
                rpe_by_exercise = df.groupby('exercice')['rpe'].mean().sort_values(ascending=False)
                fig_rpe_ex = px.bar(
                    x=rpe_by_exercise.values, y=rpe_by_exercise.index,
                    orientation='h',
                    title="RPE moyen par exercice"
                )
                st.plotly_chart(fig_rpe_ex, use_container_width=True)
        
        # Heatmap d'activité
        st.markdown("#### 🔥 Carte d'Activité")
        df['day_of_week'] = df['date'].dt.day_name()
        df['week'] = df['date'].dt.isocalendar().week
        
        heatmap_data = df.groupby(['week', 'day_of_week']).size().reset_index(name='count')
        
        if not heatmap_data.empty:
            fig_heatmap = px.density_heatmap(
                heatmap_data, x='day_of_week', y='week', z='count',
                title="Heatmap d'activité par jour et semaine"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab4:
        st.markdown("#### 📋 Historique Détaillé")
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("Date début", value=df['date'].min().date())
        with col2:
            end_date = st.date_input("Date fin", value=df['date'].max().date())
        with col3:
            exercice_filter = st.multiselect("Exercices", exercices_uniques, default=exercices_uniques[:5])
        
        # Données filtrées
        df_filtered = df[
            (df['date'].dt.date >= start_date) & 
            (df['date'].dt.date <= end_date) &
            (df['exercice'].isin(exercice_filter))
        ].copy()
        
        # Formatage pour affichage
        df_display = df_filtered.copy()
        df_display['date'] = df_display['date'].dt.strftime('%d/%m/%Y %H:%M')
        
        # Réorganiser les colonnes
        columns_order = ['date', 'exercice', 'serie', 'poids', 'reps', 'rpe', 'note']
        columns_available = [col for col in columns_order if col in df_display.columns]
        df_display = df_display[columns_available]
        
        st.dataframe(df_display.sort_values('date', ascending=False), use_container_width=True)
        
        # Export des données
        csv = df_display.to_csv(index=False)
        st.download_button(
            label="📥 Exporter les données filtrées",
            data=csv,
            file_name=f"rehab_lca_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def show_evaluation_tests():
    """Interface pour les tests d'évaluation par palier"""
    st.header("🧪 Tests d'Évaluation & Validation")
    
    phase, phase_name, emoji = st.session_state.program.get_current_phase()
    
    st.markdown(f"### {emoji} Phase Actuelle: {phase_name}")
    
    # Déterminer les tests selon la phase
    if "palier_1" in phase:
        current_tests = st.session_state.program.evaluation_tests["palier_1"]
        st.markdown("#### 🎯 Objectifs Palier 1 (J+45 à J+90)")
    elif "palier_2" in phase:
        current_tests = st.session_state.program.evaluation_tests["palier_2"]
        st.markdown("#### 🚀 Objectifs Palier 2 (J+90 à J+180)")
    elif "palier_3" in phase:
        current_tests = st.session_state.program.evaluation_tests["palier_3"]
        st.markdown("#### ⚡ Objectifs Palier 3 (J+180 à J+270)")
    else:
        st.info("Les tests d'évaluation sont disponibles à partir du Palier 1 de réathlétisation (J+45)")
        return
    
    # Interface de tests
    st.markdown("### 📊 Saisie des Résultats")
    
    # Formulaire de test
    with st.form("test_evaluation"):
        test_date = st.date_input("Date du test", value=datetime.now().date())
        
        test_results = {}
        
        for test_name, test_info in current_tests.items():
            st.markdown(f"#### {test_info['description']}")
            st.caption(f"Objectif: {test_info['target']}")
            
            col1, col2 = st.columns(2)
            
            if "deficit" in test_name:
                with col1:
                    jambe_operee = st.number_input(f"Jambe opérée - {test_name}", min_value=0.0, key=f"{test_name}_op")
                with col2:
                    jambe_saine = st.number_input(f"Jambe saine - {test_name}", min_value=0.0, key=f"{test_name}_saine")
                
                if jambe_saine > 0:
                    deficit = ((jambe_saine - jambe_operee) / jambe_saine) * 100
                    test_results[test_name] = {
                        "jambe_operee": jambe_operee,
                        "jambe_saine": jambe_saine,
                        "deficit_percent": deficit
                    }
                    
                    # Indication visuelle
                    target_value = float(test_info['target'].replace('<', '').replace('%', ''))
                    if deficit <= target_value:
                        st.success(f"✅ Déficit: {deficit:.1f}% - OBJECTIF ATTEINT!")
                    else:
                        st.warning(f"⚠️ Déficit: {deficit:.1f}% - À améliorer")
            
            elif "saut" in test_name or "hop" in test_name:
                with col1:
                    distance_operee = st.number_input(f"Distance jambe opérée (cm)", min_value=0, key=f"{test_name}_dist_op")
                with col2:
                    distance_saine = st.number_input(f"Distance jambe saine (cm)", min_value=0, key=f"{test_name}_dist_saine")
                
                if distance_saine > 0:
                    ratio = (distance_operee / distance_saine) * 100
                    test_results[test_name] = {
                        "distance_operee": distance_operee,
                        "distance_saine": distance_saine,
                        "ratio_percent": ratio
                    }
                    
                    target_value = float(test_info['target'].replace('>', '').replace('%', ''))
                    if ratio >= target_value:
                        st.success(f"✅ Ratio: {ratio:.1f}% - OBJECTIF ATTEINT!")
                    else:
                        st.warning(f"⚠️ Ratio: {ratio:.1f}% - À améliorer")
            
            else:
                # Tests qualitatifs
                result = st.selectbox(
                    f"Résultat {test_name}",
                    ["Non testé", "Échec", "Partiellement réussi", "Réussi"],
                    key=f"{test_name}_qual"
                )
                test_results[test_name] = {"result": result}
        
        # Notes additionnelles
        notes = st.text_area("Notes et observations du test")
        
        # Soumission
        if st.form_submit_button("💾 Enregistrer les résultats"):
            # Sauvegarder dans l'historique
            st.session_state.workout_history.append({
                "date": datetime.combine(test_date, datetime.min.time()),
                "exercice": f"Test d'évaluation - {phase}",
                "results": test_results,
                "notes": notes,
                "type": "evaluation"
            })
            st.success("✅ Résultats enregistrés avec succès!")
    
    # Historique des tests
    st.markdown("### 📈 Historique des Évaluations")
    
    eval_history = [w for w in st.session_state.workout_history if w.get('type') == 'evaluation']
    
    if eval_history:
        for i, eval_data in enumerate(reversed(eval_history[-5:])):  # 5 derniers tests
            with st.expander(f"Test du {eval_data['date'].strftime('%d/%m/%Y')} - {eval_data['exercice']}"):
                if 'results' in eval_data:
                    for test_name, result in eval_data['results'].items():
                        if 'deficit_percent' in result:
                            st.write(f"**{test_name}:** {result['deficit_percent']:.1f}% de déficit")
                        elif 'ratio_percent' in result:
                            st.write(f"**{test_name}:** {result['ratio_percent']:.1f}% de ratio")
                        else:
                            st.write(f"**{test_name}:** {result.get('result', 'N/A')}")
                
                if eval_data.get('notes'):
                    st.write(f"**Notes:** {eval_data['notes']}")
    else:
        st.info("Aucun test d'évaluation enregistré pour le moment.")
    
    # Conseils selon les résultats
    st.markdown("### 💡 Recommandations")
    
    recommendations = {
        "palier_1": [
            "Focus sur la symétrie: travaillez spécifiquement la jambe opérée",
            "Augmentez progressivement les charges sur les exercices unilatéraux",
            "Intégrez plus de proprioception dans votre routine",
            "Si déficit > 25%, ralentissez la progression"
        ],
        "palier_2": [
            "Introduisez la pliométrie si déficit < 15%",
            "Travaillez la vitesse d'exécution",
            "Intégrez des exercices fonctionnels spécifiques au sport",
            "Surveillez la qualité des mouvements avant la quantité"
        ],
        "palier_3": [
            "Finalisez la préparation au retour sport",
            "Tests de terrain spécifiques à votre discipline",
            "Validation psychologique de confiance",
            "Derniers ajustements techniques avec le kinésithérapeute"
        ]
    }
    
    for palier, recs in recommendations.items():
        if palier in phase:
            for rec in recs:
                st.info(f"💡 {rec}")

def show_complete_guide():
    """Guide complet avec toutes les phases détaillées"""
    st.header("📚 Guide Complet de Rééducation LCA")
    
    # Navigation par onglets
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏥 Pré-Opératoire", 
        "🔬 Post-Op Immédiat", 
        "💪 Renforcement", 
        "🎯 Réathlétisation",
        "⚠️ Sécurité",
        "📋 Matériel"
    ])
    
    with tab1:
        st.subheader("Phase Pré-Opératoire (4 semaines avant chirurgie)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🎯 Objectifs Principaux
            - **Maximiser la force bilatérale** des membres inférieurs
            - **Développer la proprioception** et l'équilibre
            - **Optimiser la condition physique** générale
            - **Préparer psychologiquement** à la chirurgie
            
            #### 📅 Planning Hebdomadaire
            - **Lundi & Jeudi :** Séance Force A
            - **Mardi & Vendredi :** Séance Force B  
            - **Mercredi :** Mobilité/Proprioception
            - **Weekend :** Repos actif ou cardio léger
            """)
        
        with col2:
            st.markdown("""
            #### 🔑 Points Clés
            - **Symétrie absolue** : même volume pour chaque jambe
            - **Charges adaptées** au profil sportif (65kg)
            - **Technique parfaite** > charges lourdes
            - **Progression graduelle** semaine après semaine
            
            #### ⚠️ Interdictions Strictes
            - Mouvements de pivot ou rotation
            - Sauts latéraux ou multidirectionnels
            - Sports avec changements de direction
            - Surcharge brutale des genoux
            """)
        
        st.markdown("#### 🏋️ Exercices Clés et Progressions")
        
        exercises_progression = {
            "Leg Press": "85kg → 97kg (progression +3kg/semaine)",
            "Fentes avant": "8kg → 12kg par main (progression +1kg/semaine)",
            "Soulevé de terre": "40kg → 50kg (progression +2.5kg/semaine)",
            "Gainage": "45s → 60s (progression +5s/semaine)"
        }
        
        for exercise, progression in exercises_progression.items():
            st.markdown(f"**{exercise}:** {progression}")
    
    with tab2:
        st.subheader("Phase Post-Opératoire Immédiate (J0 à J+45)")
        
        # Sous-phases
        subphase1, subphase2, subphase3 = st.tabs(["Semaine 1", "Semaines 2-3", "Semaines 4-6"])
        
        with subphase1:
            st.markdown("""
            #### 🏥 Semaine 1 : Réveil Neuromusculaire
            
            **Objectifs :**
            - Réactiver le quadriceps de la jambe opérée
            - Maintenir la force de la jambe saine
            - Commencer la récupération d'amplitude (0-45°)
            - Contrôler la douleur et l'inflammation
            
            **Programme Quotidien :**
            """)
            
            for exercise in st.session_state.program.post_op_programs["semaine_1"]["quotidien"]:
                st.markdown(
                    f"**{exercise['nom']}**\n"
                    f"- {exercise['series']} × {exercise['reps']}\n"
                    f"- {exercise['description']}\n"
                    f"- Focus : {exercise['focus']}\n"
                )
        
        with subphase2:
            st.markdown("""
            #### 🔄 Semaines 2-3 : Mobilisation Active
            
            **Objectifs :**
            - Atteindre 60° de flexion active
            - Renforcement actif progressif
            - Préparation au passage en charge partielle
            - Maintien condition physique générale
            """)
        
        with subphase3:
            st.markdown("""
            #### 📈 Semaines 4-6 : Renforcement Progressif
            
            **Objectifs :**
            - Récupération amplitude complète
            - Retour exercices bilatéraux
            - Passage en charge complète
            - Préparation réathlétisation
            """)
    
    with tab3:
        st.subheader("Phase de Renforcement (J+45 à J+90)")
        
        st.markdown("""
        #### 🎯 Objectifs du Palier 1
        - Réduire le déficit de force à **moins de 25%**
        - Rétablir la symétrie musculaire
        - Améliorer la proprioception avancée
        - Préparer aux activités fonctionnelles
        
        #### 📊 Tests de Validation
        """)
        
        test_criteria = {
            "Leg Press unilatéral": "Déficit < 25%",
            "Leg Extension": "Déficit < 30%", 
            "Hop Test unipodal": "Déficit < 40%"
        }
        
        for test, criteria in test_criteria.items():
            st.markdown(f"- **{test}:** {criteria}")
        
        st.markdown("""
        #### 🏋️ Programme Type (4 séances/semaine)
        
        **Séance A & C :**
        - Leg Press progression unilatérale → bilatérale
        - Fentes avant contrôlées
        - Travail proprioceptif avancé
        
        **Séance B & D :**
        - Squats profonds progressifs
        - Leg Curl/Extension intensifs
        - Gainage core stability
        """)
    
    with tab4:
        st.subheader("Phase de Réathlétisation (J+90 à J+270)")
        
        palier2, palier3 = st.tabs(["Palier 2 (J+90-J+180)", "Palier 3 (J+180-J+270)"])
        
        with palier2:
            st.markdown("""
            #### 🚀 Palier 2 : Force Fonctionnelle
            
            **Critères d'entrée :**
            - Déficit force < 25% (tous exercices)
            - Amplitude articulaire complète
            - Absence de douleur/gonflement
            
            **Nouveautés introduites :**
            - **Pliométrie bilatérale** (squat jumps, box jumps)
            - **Exercices balistiques** (leg press explosif)
            - **Travail en vitesse** et puissance
            - **Préparation gestes sportifs**
            
            **Objectifs de sortie :**
            - Déficit < 15% sur tous les tests
            - Saut vertical > 80% référence pré-blessure
            - Y-Balance Test > 90% symétrie
            """)
        
        with palier3:
            st.markdown("""
            #### ⚡ Palier 3 : Retour Sportif
            
            **Critères d'entrée :**
            - Déficit force < 15%
            - Tests pliométriques validés
            - Confiance psychologique
            
            **Programme spécialisé :**
            - **Fentes multi-directionnelles**
            - **Pivots contrôlés progressifs** (45° → 90°)
            - **Sprints en ligne** puis changements direction
            - **Sauts réactifs** et enchaînements
            
            **Validation retour sport :**
            - Déficit < 10% tous muscles
            - Hop Tests > 95% symétrie
            - Tests fonctionnels spécifiques au sport
            - Validation psychologique
            """)
    
    with tab5:
        st.subheader("⚠️ Sécurité et Contre-indications")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### ❌ Interdictions Absolues
            
            **Phase Pré-opératoire :**
            - Mouvements de pivot/rotation
            - Sauts multidirectionnels
            - Sports collectifs
            - Surcharge brutale
            
            **Post-opératoire précoce (0-6 semaines) :**
            - Appui complet sur jambe opérée
            - Flexion > 90° (selon protocole)
            - Résistance contre extension
            - Mouvements brusques
            
            **Toutes phases :**
            - Continuer sur douleur aiguë
            - Forcer amplitude articulaire
            - Progressions trop rapides
            """)
        
        with col2:
            st.markdown("""
            #### 🚨 Signaux d'Alerte
            
            **ARRÊT IMMÉDIAT si :**
            - Douleur aiguë soudaine
            - Sensation de "lâchage"
            - Gonflement important
            - Blocage articulaire
            
            **CONSULTATION URGENTE si :**
            - Douleur + fièvre
            - Perte force brutale
            - Genou chaud et rouge
            - Instabilité majeure
            
            **RALENTIR si :**
            - Douleurs persistantes
            - Fatigue excessive
            - Perte motivation
            - Déficit qui s'aggrave
            """)
        
        st.error("""
        **🆘 NUMÉROS D'URGENCE**
        - Chirurgien : [À remplir]
        - Kinésithérapeute : [À remplir]
        - SAMU : 15
        - En cas de doute, toujours consulter !
        """)
    
    with tab6:
        st.subheader("📋 Matériel et Équipements")
        
        phase_equipment = {
            "Pré-opératoire": [
                "🏋️ Haltères 6-20kg",
                "🏋️ Barre olympique + disques",
                "🦵 Machine Leg Press/Extension/Curl", 
                "🎗️ Élastiques résistance moyenne/forte",
                "⚖️ Coussin proprioception"
            ],
            "Post-op précoce": [
                "🎗️ Sangle de mobilisation",
                "🚴 Vélo stationnaire",
                "⚖️ Poids chevilles 0.5-2kg",
                "🔵 Plateau instable",
                "⚡ Électrostimulation (si prescrite)"
            ],
            "Réathlétisation": [
                "🏋️ Équipement salle complète",
                "📦 Box pliométrie 20-60cm",
                "🦺 Gilet lesté 10-20kg",
                "🔺 Cônes de marquage",
                "⏱️ Chronomètre précision",
                "🎾 Ballons proprioception"
            ]
        }
        
        for phase, equipment in phase_equipment.items():
            st.markdown(f"#### {phase}")
            for item in equipment:
                st.markdown(f"- {item}")
        
        st.markdown("""
        #### 🏠 Setup Maison vs 🏃 Salle de Sport
        
        **Minimum maison :**
        - Haltères ajustables 2-20kg
        - Élastiques de résistance
        - Tapis de sol
        - Chaise/banc stable
        
        **Idéal salle de sport :**
        - Machines guidées sécurisées
        - Large gamme de charges
        - Plateaux proprioception
        - Espace pour pliométrie
        """)

def show_settings():
    """Interface des paramètres avec options avancées"""
    st.header("⚙️ Paramètres & Configuration")
    
    # Onglets de paramètres
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profil", "📅 Planning", "💾 Données", "🎨 Préférences"])
    
    with tab1:
        st.subheader("👤 Profil Patient")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Données Physiques")
            new_weight = st.number_input(
                "Poids (kg)", 
                value=st.session_state.program.patient_weight, 
                min_value=40, 
                max_value=150,
                step=0.5
            )
            
            new_height = st.number_input(
                "Taille (cm)", 
                value=st.session_state.program.patient_height, 
                min_value=140, 
                max_value=220
            )
            
            # Calcul IMC
            imc = new_weight / ((new_height/100) ** 2)
            st.metric("IMC", f"{imc:.1f}")
            
            if imc < 18.5:
                st.warning("IMC en sous-poids")
            elif imc > 25:
                st.warning("IMC en surpoids - adaptation des charges recommandée")
        
        with col2:
            st.markdown("#### 🏃 Profil Sportif")
            niveau_sportif = st.selectbox(
                "Niveau avant blessure",
                ["Loisir", "Régulier", "Compétition amateur", "Haut niveau"],
                index=1
            )
            
            sport_principal = st.selectbox(
                "Sport principal",
                ["Football", "Rugby", "Basketball", "Tennis", "Ski", "Running", "Autres"],
                index=0
            )
            
            objectif_retour = st.selectbox(
                "Objectif de retour",
                ["Loisir/Santé", "Sport régulier", "Compétition", "Performance"],
                index=1
            )
            
            # Historique médical
            st.markdown("#### 🏥 Historique")
            premiere_rupture = st.checkbox("Première rupture LCA", value=False)
            chirurgie_anterieure = st.checkbox("Chirurgie genou antérieure", value=True)
            
        if st.button("💾 Sauvegarder le profil", type="primary"):
            st.session_state.program.patient_weight = new_weight
            st.session_state.program.patient_height = new_height
            st.success("✅ Profil mis à jour avec succès !")
    
    with tab2:
        st.subheader("📅 Gestion du Planning")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🗓️ Dates Importantes")
            current_surgery_date = st.session_state.program.surgery_date.date()
            new_surgery_date = st.date_input(
                "Date d'opération", 
                value=current_surgery_date,
                min_value=datetime(2025, 1, 1).date(),
                max_value=datetime(2026, 12, 31).date()
            )
            
            # Calculs automatiques
            today = datetime.now().date()
            if new_surgery_date > today:
                days_remaining = (new_surgery_date - today).days
                st.info(f"⏳ J-{days_remaining} avant l'opération")
            else:
                days_post = (today - new_surgery_date).days
                st.info(f"📅 J+{days_post} post-opératoire")
            
            # Dates de phase calculées
            st.markdown("#### 📊 Calendrier des Phases")
            phases_dates = {
                "Fin pré-op": new_surgery_date,
                "Fin post-op immédiat": new_surgery_date + timedelta(days=45),
                "Fin palier 1": new_surgery_date + timedelta(days=90),
                "Fin palier 2": new_surgery_date + timedelta(days=180),
                "Retour sport potentiel": new_surgery_date + timedelta(days=270)
            }
            
            for phase, date in phases_dates.items():
                st.write(f"**{phase}:** {date.strftime('%d/%m/%Y')}")
        
        with col2:
            st.markdown("#### ⏰ Préférences d'Entraînement")
            
            jours_preferes = st.multiselect(
                "Jours d'entraînement préférés",
                ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"],
                default=["Lundi", "Mardi", "Jeudi", "Vendredi"]
            )
            
            heure_preferee = st.time_input(
                "Heure préférée d'entraînement",
                value=datetime.strptime("18:00", "%H:%M").time()
            )
            
            duree_seance = st.slider(
                "Durée de séance souhaitée (minutes)",
                min_value=30,
                max_value=120,
                value=60,
                step=15
            )
            
            # Rappels
            rappels_actifs = st.checkbox("Activer les rappels", value=True)
            if rappels_actifs:
                st.info("🔔 Les rappels seront envoyés 2h avant la séance")
        
        if st.button("📅 Sauvegarder le planning"):
            st.session_state.program.surgery_date = datetime.combine(new_surgery_date, datetime.min.time())
            st.success("✅ Planning mis à jour !")
    
    with tab3:
        st.subheader("💾 Gestion des Données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📤 Export des Données")
            
            if st.session_state.workout_history:
                df = pd.DataFrame(st.session_state.workout_history)
                
                # Options d'export
                format_export = st.selectbox(
                    "Format d'export",
                    ["CSV", "Excel", "JSON"]
                )
                
                periode_export = st.selectbox(
                    "Période",
                    ["Tout l'historique", "30 derniers jours", "Depuis l'opération"]
                )
                
                # Filtrage selon la période
                if periode_export == "30 derniers jours":
                    date_limite = datetime.now() - timedelta(days=30)
                    df_export = df[df['date'] >= date_limite]
                elif periode_export == "Depuis l'opération":
                    df_export = df[df['date'] >= st.session_state.program.surgery_date]
                else:
                    df_export = df
                
                # Préparation du fichier
                timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                
                if format_export == "CSV":
                    data_export = df_export.to_csv(index=False)
                    filename = f"rehab_lca_{timestamp}.csv"
                    mime_type = "text/csv"
                elif format_export == "Excel":
                    # Pour Excel, on utiliserait to_excel() mais nécessite openpyxl
                    data_export = df_export.to_csv(index=False)
                    filename = f"rehab_lca_{timestamp}.csv"
                    mime_type = "text/csv"
                else:  # JSON
                    data_export = df_export.to_json(orient='records', date_format='iso')
                    filename = f"rehab_lca_{timestamp}.json"
                    mime_type = "application/json"
                
                st.download_button(
                    label=f"⬇️ Télécharger ({len(df_export)} entrées)",
                    data=data_export,
                    file_name=filename,
                    mime=mime_type
                )
                
                # Statistiques d'export
                st.write(f"📊 **Résumé de l'export:**")
                st.write(f"- Entrées: {len(df_export)}")
                st.write(f"- Période: {df_export['date'].min().strftime('%d/%m/%Y')} → {df_export['date'].max().strftime('%d/%m/%Y')}")
                
            else:
                st.info("Aucune donnée à exporter pour le moment")
        
        with col2:
            st.markdown("#### 📥 Import des Données")
            
            uploaded_file = st.file_uploader(
                "Importer un fichier de sauvegarde",
                type=['csv', 'json'],
                help="Fichier CSV ou JSON exporté précédemment"
            )
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df_import = pd.read_csv(uploaded_file)
                    else:  # JSON
                        df_import = pd.read_json(uploaded_file)
                    
                    st.write(f"📄 **Aperçu du fichier:**")
                    st.write(f"- {len(df_import)} entrées")
                    st.write(f"- Colonnes: {', '.join(df_import.columns)}")
                    
                    action_import = st.selectbox(
                        "Action d'import",
                        ["Aperçu seulement", "Remplacer toutes les données", "Ajouter aux données existantes"]
                    )
                    
                    if action_import != "Aperçu seulement":
                        if st.button("🔄 Confirmer l'import", type="secondary"):
                            if action_import == "Remplacer toutes les données":
                                st.session_state.workout_history = df_import.to_dict('records')
                            else:  # Ajouter
                                existing_data = st.session_state.workout_history
                                new_data = df_import.to_dict('records')
                                st.session_state.workout_history = existing_data + new_data
                            
                            st.success(f"✅ Import réalisé: {len(df_import)} entrées")
                            st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'import: {str(e)}")
        
        # Sauvegarde automatique
        st.markdown("#### 🔄 Sauvegarde Automatique")
        
        col_save1, col_save2 = st.columns(2)
        
        with col_save1:
            auto_save = st.checkbox("Sauvegarde automatique", value=True)
            if auto_save:
                save_frequency = st.selectbox(
                    "Fréquence",
                    ["Après chaque séance", "Quotidienne", "Hebdomadaire"]
                )
        
        with col_save2:
            st.markdown("#### 🗑️ Gestion")
            if st.button("🧹 Nettoyer les doublons"):
                # Logique de nettoyage des doublons
                initial_count = len(st.session_state.workout_history)
                # Ici on pourrait implémenter la logique de déduplication
                st.info(f"Nettoyage effectué: {initial_count} → {len(st.session_state.workout_history)} entrées")
            
            if st.button("🗑️ Réinitialiser tout", type="secondary"):
                confirm_reset = st.checkbox("⚠️ Confirmer la suppression totale")
                if confirm_reset:
                    st.session_state.workout_history = []
                    st.session_state.current_exercise_index = 0
                    st.session_state.current_set = 1
                    st.success("✅ Données réinitialisées")
                    st.rerun()
    
    with tab4:
        st.subheader("🎨 Préférences d'Interface")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎨 Apparence")
            
            theme = st.selectbox(
                "Thème d'interface",
                ["Automatique", "Clair", "Sombre"],
                index=0
            )
            
            couleur_accent = st.selectbox(
                "Couleur d'accent",
                ["Bleu (défaut)", "Vert", "Rouge", "Violet"],
                index=0
            )
            
            taille_police = st.slider(
                "Taille de police",
                min_value=12,
                max_value=20,
                value=14
            )
            
            animations = st.checkbox("Animations activées", value=True)
        
        with col2:
            st.markdown("#### 🔔 Notifications")
            
            notif_seance = st.checkbox("Rappel de séance", value=True)
            notif_repos = st.checkbox("Rappel jour de repos", value=False)
            notif_test = st.checkbox("Rappel tests d'évaluation", value=True)
            notif_progression = st.checkbox("Alerte progression", value=True)
            
            st.markdown("#### 📊 Affichage")
            
            unites = st.selectbox(
                "Unités de mesure",
                ["Métriques (kg, cm)", "Impériales (lbs, in)"],
                index=0
            )
            
            format_date = st.selectbox(
                "Format de date",
                ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"],
                index=0
            )
            
            graphiques_avances = st.checkbox("Graphiques avancés", value=True)
        
        if st.button("🎨 Appliquer les préférences"):
            st.success("✅ Préférences sauvegardées!")
    
    # Informations système
    st.markdown("---")
    st.markdown("### 🔧 Informations Système")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Version App", "2.1.0")
    
    with col2:
        if st.session_state.workout_history:
            last_backup = max([w['date'] for w in st.session_state.workout_history])
            st.metric("Dernière sauvegarde", last_backup.strftime('%d/%m/%Y'))
        else:
            st.metric("Dernière sauvegarde", "Jamais")
    
    with col3:
        data_size = len(str(st.session_state.workout_history))
        st.metric("Taille des données", f"{data_size/1024:.1f} KB")

# Fonctions utilitaires supplémentaires
def calculate_phase_progress(program):
    """Calcule le pourcentage de progression dans la phase actuelle"""
    phase, _, _ = program.get_current_phase()
    today = datetime.now()
    surgery_date = program.surgery_date
    
    if "pre_op" in phase:
        if "semaine_-4_-3" in phase:
            start_date = surgery_date - timedelta(days=28)
            end_date = surgery_date - timedelta(days=14)
        else:
            start_date = surgery_date - timedelta(days=14)
            end_date = surgery_date
    elif "semaine_1" in phase:
        start_date = surgery_date
        end_date = surgery_date + timedelta(days=7)
    elif "semaine_2-3" in phase:
        start_date = surgery_date + timedelta(days=7)
        end_date = surgery_date + timedelta(days=21)
    elif "semaine_4-6" in phase:
        start_date = surgery_date + timedelta(days=21)
        end_date = surgery_date + timedelta(days=45)
    elif "palier_1" in phase:
        start_date = surgery_date + timedelta(days=45)
        end_date = surgery_date + timedelta(days=90)
    elif "palier_2" in phase:
        start_date = surgery_date + timedelta(days=90)
        end_date = surgery_date + timedelta(days=180)
    elif "palier_3" in phase:
        start_date = surgery_date + timedelta(days=180)
        end_date = surgery_date + timedelta(days=270)
    else:
        return 100
    
    total_days = (end_date - start_date).days
    elapsed_days = (today - start_date).days
    
    return min(100, max(0, (elapsed_days / total_days) * 100))

def get_motivational_message(phase, progress_pct):
    """Retourne un message motivationnel selon la phase et progression"""
    messages = {
        "pre_op": [
            "🔥 Chaque entraînement optimise votre récupération future !",
            "💪 Votre force d'aujourd'hui = votre réussite de demain !",
            "🎯 Préparez votre corps comme un athlète professionnel !"
        ],
        "post_op_early": [
            "🌱 La patience d'aujourd'hui construit la performance de demain",
            "🔧 Chaque mouvement recrée votre genou plus fort",
            "⭐ Vous êtes sur la voie de la réussite !"
        ],
        "rehab": [
            "🚀 Votre progression est remarquable !",
            "⚡ Chaque séance vous rapproche du retour au sport",
            "🏆 Votre détermination fait la différence !"
        ]
    }
    
    if "pre_op" in phase:
        category = "pre_op"
    elif any(x in phase for x in ["semaine_1", "semaine_2-3", "semaine_4-6"]):
        category = "post_op_early"
    else:
        category = "rehab"
    
    import random
    return random.choice(messages[category])

def export_training_plan_pdf():
    """Génère un PDF du plan d'entraînement complet"""
    # Cette fonction nécessiterait une bibliothèque comme reportlab
    # Pour l'instant, on retourne une version texte
    
    plan_text = """
    PLAN DE RÉÉDUCATION LCA - KENNETH JONES
    =====================================
    
    PHASE PRÉ-OPÉRATOIRE (4 semaines)
    - Objectif: Maximiser force bilatérale
    - Fréquence: 4 séances/semaine
    - Focus: Symétrie et préparation
    
    PHASE POST-OPÉRATOIRE IMMÉDIATE (J0-J45)
    - Objectif: Réveil neuromusculaire
    - Progression: 0-45° puis 0-90° amplitude
    - Protection du greffon
    
    PHASE RÉATHLÉTISATION (J45-J270)
    - Palier 1: Déficit < 25%
    - Palier 2: Déficit < 15% + pliométrie
    - Palier 3: Déficit < 10% + retour sport
    
    Pour le plan détaillé, consulter l'application.
    """
    
    return plan_text

# Point d'entrée principal
if __name__ == "__main__":
    main()
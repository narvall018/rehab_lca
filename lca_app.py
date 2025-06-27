import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import base64
import time
from typing import Dict, List, Optional, Tuple
import numpy as np
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(
    page_title="Rééducation LCA - Kenneth Jones",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé moderne avec animations
st.markdown("""
<style>
    /* Variables CSS pour thème cohérent */
    :root {
        --primary-color: #3366ff;
        --secondary-color: #6c63ff;
        --success-color: #00d26a;
        --warning-color: #ffa000;
        --danger-color: #ff3b30;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        --hover-transform: translateY(-3px);
    }
    
    /* Animation d'entrée */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(51, 102, 255, 0.7);
        }
        70% {
            transform: scale(1.05);
            box-shadow: 0 0 0 10px rgba(51, 102, 255, 0);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(51, 102, 255, 0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Header principal amélioré */
    .main-header {
        font-size: 3.5rem;
        background: var(--bg-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Cards modernes avec glassmorphism */
    .modern-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .modern-card:hover {
        transform: var(--hover-transform);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25);
    }
    
    /* Phase cards avec gradients dynamiques */
    .phase-card {
        background: var(--bg-gradient);
        padding: 2rem;
        border-radius: 24px;
        color: white;
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .phase-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        transform: rotate(45deg);
        transition: all 0.5s ease;
    }
    
    .phase-card:hover::before {
        top: -60%;
        right: -60%;
    }
    
    /* Exercise cards améliorées */
    .exercise-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2rem;
        border-radius: 20px;
        border-left: 6px solid var(--primary-color);
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .exercise-card:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 30px rgba(0,0,0,0.12);
    }
    
    .exercise-card::after {
        content: '💪';
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 3rem;
        opacity: 0.1;
    }
    
    /* Success/Warning/Danger cards modernisées */
    .success-card {
        background: linear-gradient(135deg, #d4edda 0%, #a8e6cf 100%);
        border-left: 6px solid var(--success-color);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fff3cd 0%, #ffd93d 100%);
        border-left: 6px solid var(--warning-color);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .danger-card {
        background: linear-gradient(135deg, #f8d7da 0%, #ff6b6b 100%);
        border-left: 6px solid var(--danger-color);
        animation: slideInLeft 0.5s ease-out;
    }
    
    /* Metric cards avec effet néomorphisme */
    .metric-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 
            8px 8px 16px #d1d3d7,
            -8px -8px 16px #ffffff;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 
            4px 4px 8px #d1d3d7,
            -4px -4px 8px #ffffff;
    }
    
    /* Timer display amélioré */
    .timer-display {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff3b30 0%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 1rem 0;
        font-family: 'Monaco', monospace;
        animation: pulse 2s infinite;
    }
    
    /* Badges de progression */
    .progress-badge {
        display: inline-block;
        background: var(--bg-gradient);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Boutons modernes */
    .stButton > button {
        background: var(--bg-gradient);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Progress bars personnalisées */
    .stProgress > div > div > div > div {
        background: var(--bg-gradient);
        border-radius: 10px;
    }
    
    /* Tooltips modernes */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.875rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Animations de chargement */
    .loading-dots {
        display: inline-block;
        animation: loading 1.4s infinite;
    }
    
    @keyframes loading {
        0%, 60%, 100% {
            opacity: 0.3;
        }
        30% {
            opacity: 1;
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .modern-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .modern-card {
            background: rgba(30, 30, 30, 0.95);
            color: white;
        }
        
        .metric-card {
            background: #1a1a1a;
            box-shadow: 
                8px 8px 16px #0f0f0f,
                -8px -8px 16px #252525;
        }
    }
</style>
""", unsafe_allow_html=True)

def display_exercise_card(exercise, index, current_set):
    """Affiche une carte d'exercice en utilisant les composants natifs de Streamlit"""
    
    # En-tête avec nom et difficulté
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"### 🎯 {exercise['nom']}")
    with col2:
        difficulty_stars = "⭐" * exercise.get("difficulte", 3)
        st.markdown(f"**Difficulté:** {difficulty_stars}")
    
    # Description
    st.markdown(f"*{exercise['description']}*")
    
    # Informations d'exercice en colonnes
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**🔢 Volume:** {exercise['series']} séries × {exercise['reps']} reps")
        st.markdown(f"**⚖️ Charge:** {exercise['charge']}")
    with col2:
        st.markdown(f"**⏱️ Repos:** {exercise['repos']}")
        st.markdown(f"**🎯 Focus:** {exercise['focus']}")
    
    # Conseils dans un encadré
    st.info(f"💡 **Conseils:** {exercise['conseils']}")
    
    # Muscles ciblés
    st.markdown("**🏃 Muscles ciblés:**")
    muscles_text = ", ".join([f"_{muscle}_" for muscle in exercise.get("muscles", [])])
    st.markdown(muscles_text)
    
    # Série actuelle
    st.sidebar.markdown(f"### Série actuelle")
    st.sidebar.markdown(f"## {current_set}/{exercise['series']}")

# Classe GitHub Storage (identique mais avec améliorations)
class GitHubStorage:
    def __init__(self):
        try:
            self.token = st.secrets["github"]["token"]
            self.repo = st.secrets["github"]["repo"]
            self.branch = st.secrets["github"].get("branch", "main")
            self.base_url = f"https://api.github.com/repos/{self.repo}/contents"
            
            self.headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            self.connected = True
        except Exception as e:
            st.error(f"❌ Configuration GitHub manquante: {str(e)}")
            self.connected = False
    
    def read_file(self, filepath: str) -> Optional[Dict]:
        if not self.connected:
            return None
            
        # Utiliser le cache Streamlit pour éviter les appels répétés
        @st.cache_data(ttl=300)  # Cache de 5 minutes
        def _read_cached(url, headers_dict):
            try:
                response = requests.get(url, headers=headers_dict)
                
                if response.status_code == 200:
                    file_data = response.json()
                    content = base64.b64decode(file_data['content']).decode('utf-8')
                    return json.loads(content)
                elif response.status_code == 404:
                    return None
                else:
                    st.error(f"Erreur lecture GitHub: {response.status_code}")
                    return None
                    
            except Exception as e:
                st.error(f"Erreur GitHub: {str(e)}")
                return None
        
        url = f"{self.base_url}/{filepath}"
        # Passer les headers comme un dictionnaire, pas comme un tuple
        data = _read_cached(url, self.headers)
        
        if data is None:
            # Fichier n'existe pas - créer la structure par défaut
            return self.create_default_file(filepath)
        
        return data
            
        # Utiliser le cache Streamlit pour éviter les appels répétés
        @st.cache_data(ttl=300)  # Cache de 5 minutes
        def _read_cached(url, headers):
            try:
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    file_data = response.json()
                    content = base64.b64decode(file_data['content']).decode('utf-8')
                    return json.loads(content)
                elif response.status_code == 404:
                    return None
                else:
                    st.error(f"Erreur lecture GitHub: {response.status_code}")
                    return None
                    
            except Exception as e:
                st.error(f"Erreur GitHub: {str(e)}")
                return None
        
        url = f"{self.base_url}/{filepath}"
        data = _read_cached(url, tuple(self.headers.items()))
        
        if data is None:
            # Fichier n'existe pas - créer la structure par défaut
            return self.create_default_file(filepath)
        
        return data
    
    def create_default_file(self, filepath: str) -> Dict:
        """Crée un fichier avec structure par défaut"""
        default_data = {}
        
        if "workouts.json" in filepath:
            default_data = {"workouts": []}
        elif "user_profile.json" in filepath:
            default_data = {
                "patient_weight": 65.0,
                "patient_height": 168,
                "surgery_date": "2025-07-28",
                "created_at": datetime.now().isoformat(),
                "preferences": {
                    "notifications": True,
                    "theme": "auto",
                    "language": "fr"
                }
            }
        elif "evaluations.json" in filepath:
            default_data = {"evaluations": []}
        elif "achievements.json" in filepath:
            default_data = {"achievements": [], "badges": []}
        
        # Créer le fichier sur GitHub
        if self.write_file(filepath, default_data, f"Create {filepath}"):
            return default_data
        return {}
    
    def write_file(self, filepath: str, data: Dict, commit_message: str = None) -> bool:
        """Écrit un fichier JSON sur GitHub avec retry"""
        if not self.connected:
            return False
            
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if commit_message is None:
                    commit_message = f"Update {filepath} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                # Récupérer le SHA du fichier existant
                url = f"{self.base_url}/{filepath}"
                existing_response = requests.get(url, headers=self.headers)
                sha = None
                
                if existing_response.status_code == 200:
                    sha = existing_response.json()['sha']
                
                # Préparer le contenu
                content = json.dumps(data, indent=2, ensure_ascii=False)
                encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                
                # Payload pour l'API
                payload = {
                    "message": commit_message,
                    "content": encoded_content,
                    "branch": self.branch
                }
                
                if sha:
                    payload["sha"] = sha
                
                # Envoyer à GitHub
                response = requests.put(url, json=payload, headers=self.headers)
                
                if response.status_code in [200, 201]:
                    # Invalider le cache après écriture
                    st.cache_data.clear()
                    return True
                else:
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(1)  # Attendre avant de réessayer
                    else:
                        st.error(f"Erreur écriture GitHub après {max_retries} tentatives: {response.status_code}")
                        return False
                        
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    st.error(f"Erreur écriture GitHub: {str(e)}")
                    return False
    
    def append_workout(self, workout_data: Dict) -> bool:
        """Ajoute un workout à la liste existante"""
        existing_data = self.read_file("data/workouts.json")
        
        if existing_data is None:
            return False
        
        if "workouts" not in existing_data:
            existing_data["workouts"] = []
        
        # Ajouter le nouveau workout avec timestamp
        workout_data["id"] = len(existing_data["workouts"]) + 1
        workout_data["timestamp"] = datetime.now().isoformat()
        existing_data["workouts"].append(workout_data)
        
        # Sauvegarder
        commit_msg = f"Add workout: {workout_data.get('exercice', 'Unknown')} - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        return self.write_file("data/workouts.json", existing_data, commit_msg)
    
    def get_workouts(self) -> List[Dict]:
        """Récupère tous les workouts"""
        data = self.read_file("data/workouts.json")
        if data and "workouts" in data:
            return data["workouts"]
        return []
    
    def save_user_profile(self, profile_data: Dict) -> bool:
        """Sauvegarde le profil utilisateur"""
        profile_data["last_updated"] = datetime.now().isoformat()
        return self.write_file("data/user_profile.json", profile_data, "Update user profile")
    
    def get_user_profile(self) -> Dict:
        """Récupère le profil utilisateur"""
        return self.read_file("data/user_profile.json") or {}
    
    def save_evaluation(self, eval_data: Dict) -> bool:
        """Sauvegarde un test d'évaluation"""
        existing_data = self.read_file("data/evaluations.json") or {"evaluations": []}
        
        eval_data["id"] = len(existing_data["evaluations"]) + 1
        eval_data["timestamp"] = datetime.now().isoformat()
        existing_data["evaluations"].append(eval_data)
        
        commit_msg = f"Add evaluation: {eval_data.get('phase', 'Unknown')} - {datetime.now().strftime('%d/%m/%Y')}"
        return self.write_file("data/evaluations.json", existing_data, commit_msg)
    
    def get_evaluations(self) -> List[Dict]:
        """Récupère toutes les évaluations"""
        data = self.read_file("data/evaluations.json")
        if data and "evaluations" in data:
            return data["evaluations"]
        return []
    
    def save_achievement(self, achievement_data: Dict) -> bool:
        """Sauvegarde un achievement/badge"""
        existing_data = self.read_file("data/achievements.json") or {"achievements": [], "badges": []}
        
        achievement_data["timestamp"] = datetime.now().isoformat()
        existing_data["achievements"].append(achievement_data)
        
        return self.write_file("data/achievements.json", existing_data, f"New achievement: {achievement_data.get('name', 'Unknown')}")
    
    def get_achievements(self) -> Dict:
        """Récupère les achievements"""
        return self.read_file("data/achievements.json") or {"achievements": [], "badges": []}
    
    def save_progress_state(self, current_exercise_index: int, current_set: int) -> bool:
        """Sauvegarde l'état de progression actuel"""
        progress_data = {
            "current_exercise_index": current_exercise_index,
            "current_set": current_set,
            "last_updated": datetime.now().isoformat()
        }
        return self.write_file("data/progress_state.json", progress_data, "Update progression state")

    def get_progress_state(self) -> Dict:
        """Récupère l'état de progression sauvegardé"""
        data = self.read_file("data/progress_state.json")
        if data and "current_exercise_index" in data and "current_set" in data:
            return {
                "current_exercise_index": data["current_exercise_index"],
                "current_set": data["current_set"]
            }
        return {"current_exercise_index": 0, "current_set": 1}  # Valeurs par défaut

# Classe améliorée pour la gestion du programme
class RehabProgram:
    def __init__(self):
        self.surgery_date = datetime(2025, 7, 28)
        self.patient_weight = 65.0
        self.patient_height = 168
        
        # Ajout de vidéos d'exercices (liens YouTube)
        self.exercise_videos = {
            "Leg Press Bilatéral": "https://www.youtube.com/watch?v=IZxyjW7MPJQ",
            "Fentes avant alternées": "https://www.youtube.com/watch?v=QOVaHwm-Q6U",
            "Soulevé de terre roumain": "https://www.youtube.com/watch?v=JCXUYuzwNrM",
            "Squat Goblet": "https://www.youtube.com/watch?v=MeIiIdhvXT4",
            "Contractions isométriques quadriceps": "https://www.youtube.com/watch?v=4bWQGIm9raw",
            "Flexions passives aidées": "https://www.youtube.com/watch?v=_YLFwSaNEkk"
        }
        
        # Ajout de conseils nutritionnels par phase
        self.nutrition_tips = {
            "pre_op": {
                "calories": "Maintien ou léger surplus (+200-300 kcal)",
                "proteines": "1.6-2g/kg de poids corporel",
                "glucides": "4-5g/kg pour l'énergie",
                "lipides": "0.8-1g/kg (oméga-3 ++)",
                "hydratation": "35-40ml/kg + 500ml par heure d'exercice",
                "supplements": ["Vitamine D", "Omega-3", "Créatine", "Multivitamine"],
                "aliments_cles": ["Saumon", "Œufs", "Avoine", "Patate douce", "Épinards", "Baies"]
            },
            "post_op_early": {
                "calories": "Maintien pour cicatrisation",
                "proteines": "2-2.5g/kg (cicatrisation ++)",
                "glucides": "3-4g/kg",
                "lipides": "1g/kg",
                "hydratation": "40ml/kg minimum",
                "supplements": ["Vitamine C", "Zinc", "Collagène", "Vitamine D"],
                "aliments_cles": ["Poulet", "Quinoa", "Brocoli", "Agrumes", "Noix", "Yaourt grec"]
            },
            "rehab": {
                "calories": "Surplus progressif (+300-500 kcal)",
                "proteines": "2g/kg minimum",
                "glucides": "5-6g/kg selon intensité",
                "lipides": "1g/kg",
                "hydratation": "40ml/kg + compensation sudation",
                "supplements": ["Créatine", "BCAA", "Glucosamine", "Omega-3"],
                "aliments_cles": ["Bœuf maigre", "Riz complet", "Lentilles", "Avocat", "Banane", "Amandes"]
            }
        }
        
        # Programmes pré-opératoires (identiques à l'original)
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
                        "conseils": "Gardez le dos plaqué, respirez pendant la montée",
                        "muscles": ["Quadriceps", "Fessiers", "Ischio-jambiers"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Fentes avant alternées",
                        "description": "Pas large (1.2x largeur épaules), descente verticale jusqu'à ce que le genou arrière frôle le sol",
                        "series": 3,
                        "reps": "10 chaque jambe",
                        "charge": "Haltères 8kg/main",
                        "repos": "60s",
                        "focus": "Stabilité du tronc, équilibre parfait",
                        "conseils": "Le genou avant ne dépasse jamais la pointe du pied",
                        "muscles": ["Quadriceps", "Fessiers", "Core"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Soulevé de terre roumain",
                        "description": "Barre proche du corps, hanches poussées vers l'arrière, genoux légèrement fléchis",
                        "series": 3,
                        "reps": 10,
                        "charge": "Barre 40kg",
                        "repos": "75s",
                        "focus": "Activation maximale des ischio-jambiers",
                        "conseils": "Sentir l'étirement à l'arrière des cuisses",
                        "muscles": ["Ischio-jambiers", "Fessiers", "Érecteurs spinaux"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Leg Curl unilatéral machine",
                        "description": "Position allongée ventrale, flexion lente et contrôlée du genou",
                        "series": 3,
                        "reps": "12 chaque jambe",
                        "charge": "15kg",
                        "repos": "45s",
                        "focus": "Concentration maximale, tempo lent",
                        "conseils": "Pause 1 seconde en position haute",
                        "muscles": ["Ischio-jambiers"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Gainage frontal",
                        "description": "Position planche, corps parfaitement aligné, contraction abdos et fessiers",
                        "series": 3,
                        "reps": "45s",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Respiration contrôlée, pas d'apnée",
                        "conseils": "Regarder le sol, ne pas cambrer le dos",
                        "muscles": ["Core", "Épaules"],
                        "difficulte": 2
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
                        "conseils": "Genoux dans l'axe des pieds",
                        "muscles": ["Quadriceps", "Fessiers", "Core"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Squat Bulgare",
                        "description": "Pied arrière posé sur banc, descente verticale sur la jambe avant",
                        "series": 3,
                        "reps": "10 chaque jambe",
                        "charge": "Haltères 6kg/main",
                        "repos": "60s",
                        "focus": "Équilibre unilatéral, stabilité",
                        "conseils": "70% du poids sur la jambe avant",
                        "muscles": ["Quadriceps", "Fessiers", "Stabilisateurs"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Leg Extension unilatéral",
                        "description": "Mouvement lent et contrôlé, contraction volontaire en fin d'amplitude",
                        "series": 3,
                        "reps": "12 chaque jambe",
                        "charge": "12kg",
                        "repos": "45s",
                        "focus": "Isométrie 2 secondes en position haute",
                        "conseils": "Éviter les à-coups, mouvement fluide",
                        "muscles": ["Quadriceps"],
                        "difficulte": 1
                    },
                    {
                        "nom": "Pont fessier unilatéral",
                        "description": "Allongé, une jambe tendue, montée bassin par contraction fessiers",
                        "series": 3,
                        "reps": "15 chaque jambe",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Activation ciblée des fessiers",
                        "conseils": "Serrer fort les fessiers en haut",
                        "muscles": ["Fessiers", "Ischio-jambiers"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Gainage latéral",
                        "description": "Sur le côté, corps aligné des pieds à la tête",
                        "series": 3,
                        "reps": "30s chaque côté",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Stabilité dans le plan frontal",
                        "conseils": "Bassin légèrement poussé vers l'avant",
                        "muscles": ["Obliques", "Core"],
                        "difficulte": 2
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
                        "conseils": "Bassin en rétroversion, pas de cambrure",
                        "muscles": ["Quadriceps", "Psoas"],
                        "difficulte": 1
                    },
                    {
                        "nom": "Étirements ischio-jambiers",
                        "description": "Assis, jambe tendue, penché vers l'avant",
                        "series": 3,
                        "reps": "30s chaque jambe",
                        "charge": "Sangle pour assistance",
                        "repos": "10s",
                        "focus": "Souplesse postérieure",
                        "conseils": "Dos droit, pencher depuis les hanches",
                        "muscles": ["Ischio-jambiers"],
                        "difficulte": 1
                    },
                    {
                        "nom": "Proprioception yeux fermés",
                        "description": "Équilibre sur une jambe, yeux fermés",
                        "series": 3,
                        "reps": "45s chaque jambe",
                        "charge": "Coussin instable optionnel",
                        "repos": "30s",
                        "focus": "Contrôle postural sans vision",
                        "conseils": "Concentrer sur les sensations du pied",
                        "muscles": ["Stabilisateurs", "Core"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Marche latérale élastique",
                        "description": "Pas chassés latéraux avec élastique autour des chevilles",
                        "series": 3,
                        "reps": "15 pas chaque direction",
                        "charge": "Élastique résistance moyenne",
                        "repos": "30s",
                        "focus": "Activation fessiers moyens",
                        "conseils": "Maintenir tension constante sur l'élastique",
                        "muscles": ["Fessiers moyens", "TFL"],
                        "difficulte": 2
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
                        "conseils": "Explosion contrôlée, ne pas décoller le dos",
                        "muscles": ["Quadriceps", "Fessiers", "Ischio-jambiers"],
                        "difficulte": 4
                    },
                    {
                        "nom": "Fentes avant alternées",
                        "description": "Progression en charge, contrôle parfait de la descente",
                        "series": 4,
                        "reps": "8 chaque jambe",
                        "charge": "Haltères 12kg/main",
                        "repos": "75s",
                        "focus": "Contrôle de la phase de décelération",
                        "conseils": "Freiner activement la descente",
                        "muscles": ["Quadriceps", "Fessiers", "Core"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Soulevé de terre roumain",
                        "description": "Amplitude optimale, accent sur la phase excentrique",
                        "series": 4,
                        "reps": 8,
                        "charge": "Barre 50kg",
                        "repos": "90s",
                        "focus": "Phase excentrique sur 4 secondes",
                        "conseils": "Résister à la descente, contrôle total",
                        "muscles": ["Ischio-jambiers", "Fessiers", "Érecteurs spinaux"],
                        "difficulte": 4
                    },
                    {
                        "nom": "Leg Curl unilatéral",
                        "description": "Augmentation de résistance, contraction volontaire maximale",
                        "series": 4,
                        "reps": "10 chaque jambe",
                        "charge": "20kg",
                        "repos": "60s",
                        "focus": "Contraction volontaire en fin de course",
                        "conseils": "Serrer fort en position haute 2 secondes",
                        "muscles": ["Ischio-jambiers"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Dead Bug",
                        "description": "Coordination bras/jambe opposés, stabilité anti-rotation",
                        "series": 3,
                        "reps": "10 chaque côté",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Stabilité anti-rotation du tronc",
                        "conseils": "Lombaires collées au sol en permanence",
                        "muscles": ["Core", "Psoas"],
                        "difficulte": 2
                    }
                ]
            }
        }
        
        # Programmes post-opératoires (identiques à l'original)
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
                        "conseils": "Contracter 5s, relâcher 5s, visualiser le muscle",
                        "muscles": ["Quadriceps"],
                        "difficulte": 1
                    },
                    {
                        "nom": "Flexions passives aidées",
                        "description": "Kinésithérapeute aide à fléchir le genou progressivement",
                        "series": 3,
                        "reps": 10,
                        "charge": "Aide manuelle",
                        "repos": "60s",
                        "focus": "Récupération amplitude 0-45°, progression +5°/jour",
                        "conseils": "Ne jamais forcer, douleur = STOP",
                        "muscles": ["Articulation genou"],
                        "difficulte": 1
                    },
                    {
                        "nom": "Élévations jambe tendue passives",
                        "description": "Allongé, soulever la jambe opérée tendue avec les mains",
                        "series": 3,
                        "reps": 8,
                        "charge": "Aide des bras",
                        "repos": "45s",
                        "focus": "Maintien tonus sans contrainte",
                        "conseils": "Garder genou parfaitement tendu",
                        "muscles": ["Quadriceps", "Psoas"],
                        "difficulte": 1
                    },
                    {
                        "nom": "Leg Extension jambe saine",
                        "description": "Renforcement de la jambe non opérée pour éviter l'atrophie",
                        "series": 3,
                        "reps": 15,
                        "charge": "8kg",
                        "repos": "45s",
                        "focus": "Maintien force jambe saine",
                        "conseils": "Mouvement normal, pleine amplitude",
                        "muscles": ["Quadriceps"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Gainage ventral modifié",
                        "description": "Planche sur avant-bras et genoux",
                        "series": 3,
                        "reps": "20s",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Maintien tonus abdominal",
                        "conseils": "Progression +5s tous les 2 jours",
                        "muscles": ["Core"],
                        "difficulte": 1
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
                        "conseils": "Initier le mouvement activement, puis aider",
                        "muscles": ["Quadriceps", "Ischio-jambiers"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Élévation jambe tendue active",
                        "description": "Allongé, soulever la jambe opérée par la force du quadriceps",
                        "series": 3,
                        "reps": 12,
                        "charge": "Poids cheville 0.5kg (progression +0.5kg/semaine)",
                        "repos": "30s",
                        "focus": "Activation active du quadriceps",
                        "conseils": "Bien contracter avant de lever, genou tendu",
                        "muscles": ["Quadriceps", "Psoas"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Squat mural bilatéral",
                        "description": "Dos contre le mur, descente jusqu'à 45° maximum",
                        "series": 3,
                        "reps": 15,
                        "charge": "Poids corps",
                        "repos": "60s",
                        "focus": "Répartition égale du poids sur les 2 jambes",
                        "conseils": "Ne pas dépasser 45° de flexion",
                        "muscles": ["Quadriceps", "Fessiers"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Vélo stationnaire",
                        "description": "Pédalage en douceur, résistance minimale",
                        "series": 1,
                        "reps": "15-20 minutes",
                        "charge": "Résistance 1-2/10",
                        "repos": "Continue",
                        "focus": "Cadence 60-70 RPM, mobilité douce",
                        "conseils": "Arrêter si douleur ou blocage",
                        "muscles": ["Cardio", "Membres inférieurs"],
                        "difficulte": 1
                    },
                    {
                        "nom": "Renforcement jambe saine",
                        "description": "Programme complet jambe non opérée",
                        "series": 3,
                        "reps": 12,
                        "charge": "Charges habituelles",
                        "repos": "60s",
                        "focus": "Maintenir la force et masse musculaire",
                        "conseils": "Leg extension, Leg curl, mollets",
                        "muscles": ["Tous muscles jambe saine"],
                        "difficulte": 3
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
                        "conseils": "Écouter les sensations, progression graduelle",
                        "muscles": ["Quadriceps", "Fessiers", "Ischio-jambiers"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Leg Curl bilatéral",
                        "description": "Activation des ischio-jambiers en douceur",
                        "series": 3,
                        "reps": 12,
                        "charge": "8kg",
                        "repos": "60s",
                        "focus": "Mouvement lent et contrôlé",
                        "conseils": "Pas de compensation, mouvement symétrique",
                        "muscles": ["Ischio-jambiers"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Proprioception avancée",
                        "description": "Équilibre unipodal sur plateau instable",
                        "series": 3,
                        "reps": "60s chaque jambe",
                        "charge": "Plateau instable",
                        "repos": "30s",
                        "focus": "Rééducation proprioceptive progressive",
                        "conseils": "Commencer yeux ouverts, puis fermés",
                        "muscles": ["Stabilisateurs", "Core"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Step-up bas",
                        "description": "Montée sur marche de 15cm, descente contrôlée",
                        "series": 3,
                        "reps": "10 chaque jambe",
                        "charge": "Poids corps",
                        "repos": "45s",
                        "focus": "Contrôle de la descente, pas d'impact",
                        "conseils": "Montée jambe opérée, descente en douceur",
                        "muscles": ["Quadriceps", "Fessiers"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Vélo intensité modérée",
                        "description": "Augmentation progressive de l'intensité",
                        "series": 1,
                        "reps": "25-30 minutes",
                        "charge": "Résistance 3-4/10",
                        "repos": "Continue",
                        "focus": "Endurance et mobilité",
                        "conseils": "Cadence 70-80 RPM",
                        "muscles": ["Cardio", "Membres inférieurs"],
                        "difficulte": 2
                    },
                    {
                        "nom": "Gainage complet",
                        "description": "Retour au gainage standard",
                        "series": 3,
                        "reps": "60s",
                        "charge": "Poids corps",
                        "repos": "30s",
                        "focus": "Stabilité globale du tronc",
                        "conseils": "Planche frontale, latérale, Superman",
                        "muscles": ["Core complet"],
                        "difficulte": 3
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
                        "conseils": "Comparer forces jambe opérée vs saine",
                        "muscles": ["Quadriceps", "Fessiers", "Ischio-jambiers"],
                        "difficulte": 4
                    },
                    {
                        "nom": "Fentes avant contrôlées",
                        "description": "Retour mouvement lent, amplitude complète",
                        "series": 3,
                        "reps": "12 chaque jambe",
                        "charge": "6→12kg/main (progression)",
                        "repos": "60s",
                        "focus": "Symétrie parfaite des 2 côtés",
                        "conseils": "Même profondeur, même vitesse",
                        "muscles": ["Quadriceps", "Fessiers", "Core"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Squats profonds progressifs",
                        "description": "Amplitude progressive de 45° vers 90°",
                        "series": 4,
                        "reps": 10,
                        "charge": "20→40kg",
                        "repos": "75s",
                        "focus": "Augmentation amplitude +10°/semaine",
                        "conseils": "Respecter les limites articulaires",
                        "muscles": ["Quadriceps", "Fessiers"],
                        "difficulte": 4
                    },
                    {
                        "nom": "Leg Curl unilatéral intensif",
                        "description": "Concentration maximale, charges progressives",
                        "series": 3,
                        "reps": "12 chaque jambe",
                        "charge": "15→25kg",
                        "repos": "45s",
                        "focus": "Objectif déficit -15% à la fin du palier",
                        "conseils": "Tempo lent, contraction maximale",
                        "muscles": ["Ischio-jambiers"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Leg Extension bilatéral",
                        "description": "Retour travail quadriceps intensif",
                        "series": 3,
                        "reps": 12,
                        "charge": "15→25kg",
                        "repos": "60s",
                        "focus": "Symétrie des contractions",
                        "conseils": "Isométrie 2s en haut",
                        "muscles": ["Quadriceps"],
                        "difficulte": 3
                    },
                    {
                        "nom": "Proprioception challenges",
                        "description": "Exercices d'équilibre complexes",
                        "series": 3,
                        "reps": "45s chaque jambe",
                        "charge": "Ballons, plateaux instables",
                        "repos": "30s",
                        "focus": "Préparation aux déplacements",
                        "conseils": "Yeux fermés, perturbations externes",
                        "muscles": ["Stabilisateurs", "Core"],
                        "difficulte": 4
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
                        "conseils": "Décoller et atterrir sur 2 pieds simultanément",
                        "muscles": ["Quadriceps", "Fessiers", "Mollets"],
                        "difficulte": 4
                    },
                    {
                        "nom": "Step-up explosif",
                        "description": "Montée explosive, descente lente et contrôlée",
                        "series": 3,
                        "reps": "8 chaque jambe",
                        "charge": "Gilet lesté 15kg",
                        "repos": "75s",
                        "focus": "Vitesse d'exécution concentrique",
                        "conseils": "Impulsion maximale, réception douce",
                        "muscles": ["Quadriceps", "Fessiers", "Mollets"],
                        "difficulte": 4
                    },
                    {
                        "nom": "Leg Press balistique",
                        "description": "Phase concentrique la plus rapide possible",
                        "series": 5,
                        "reps": 5,
                        "charge": "85kg (1.3x poids corps)",
                        "repos": "2min",
                        "focus": "Développement puissance maximale",
                        "conseils": "Descente contrôlée, explosion maximale",
                        "muscles": ["Quadriceps", "Fessiers", "Ischio-jambiers"],
                        "difficulte": 5
                    },
                    {
                        "nom": "Box Jumps 30cm",
                        "description": "Sauts sur box, progression hauteur",
                        "series": 3,
                        "reps": 5,
                        "charge": "Poids corps",
                        "repos": "90s",
                        "focus": "Hauteur progressive +5cm/2semaines",
                        "conseils": "Descendre en marchant, pas en sautant",
                        "muscles": ["Quadriceps", "Fessiers", "Mollets"],
                        "difficulte": 4
                    },
                    {
                        "nom": "Fentes sautées alternées",
                        "description": "Fentes avec changement de jambe en vol",
                        "series": 3,
                        "reps": "6 chaque jambe",
                        "charge": "Poids corps",
                        "repos": "90s",
                        "focus": "Réactivité et stabilité dynamique",
                        "conseils": "Réception équilibrée, pause 1s entre sauts",
                        "muscles": ["Quadriceps", "Fessiers", "Core"],
                        "difficulte": 5
                    },
                    {
                        "nom": "Travail excentrique renforcé",
                        "description": "Squats avec phase excentrique lente",
                        "series": 4,
                        "reps": 6,
                        "charge": "60kg",
                        "repos": "2min",
                        "focus": "Contrôle excentrique 5 secondes",
                        "conseils": "Freiner activement la descente",
                        "muscles": ["Quadriceps", "Fessiers"],
                        "difficulte": 4
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
                        "conseils": "Fluidité entre les directions",
                        "muscles": ["Quadriceps", "Fessiers", "Stabilisateurs"],
                        "difficulte": 5
                    },
                    {
                        "nom": "Pivot contrôlé progressif",
                        "description": "Rotations 45° puis progression vers 90°",
                        "series": 3,
                        "reps": "5 chaque sens",
                        "charge": "Poids corps",
                        "repos": "60s",
                        "focus": "Progression angulaire +15°/semaine",
                        "conseils": "Pied planté, rotation sur l'avant-pied",
                        "muscles": ["Stabilisateurs genou", "Core"],
                        "difficulte": 5
                    },
                    {
                        "nom": "Sprint en ligne droite",
                        "description": "Accélérations progressives en ligne droite",
                        "series": 6,
                        "reps": "20m",
                        "charge": "Poids corps",
                        "repos": "2min",
                        "focus": "Vitesse linéaire spécifique",
                        "conseils": "Progression 70%→85%→95% vitesse max",
                        "muscles": ["Tout le corps"],
                        "difficulte": 5
                    },
                    {
                        "nom": "Sauts réactifs enchaînés",
                        "description": "Enchaînements pliométriques multi-directionnels",
                        "series": 4,
                        "reps": 4,
                        "charge": "Poids corps",
                        "repos": "2min",
                        "focus": "Réactivité neuromusculaire maximale",
                        "conseils": "Contact au sol minimum entre sauts",
                        "muscles": ["Quadriceps", "Fessiers", "Mollets"],
                        "difficulte": 5
                    },
                    {
                        "nom": "Changements de direction",
                        "description": "Slalom, 8, arrêts-démarrages",
                        "series": 4,
                        "reps": "30s",
                        "charge": "Poids corps",
                        "repos": "90s",
                        "focus": "Préparation retour sport avec pivot",
                        "conseils": "Intensité progressive 60%→80%→95%",
                        "muscles": ["Tout le corps", "Stabilisateurs"],
                        "difficulte": 5
                    },
                    {
                        "nom": "Tests fonctionnels",
                        "description": "Hop Tests, Y-Balance, Single Leg Squat",
                        "series": 3,
                        "reps": "Test complet",
                        "charge": "Évaluation",
                        "repos": "3min",
                        "focus": "Validation critères retour sport",
                        "conseils": "Symétrie >95% obligatoire",
                        "muscles": ["Évaluation globale"],
                        "difficulte": 5
                    }
                ]
            }
        }
        
        # Tests d'évaluation par palier
        self.evaluation_tests = {
            "palier_1": {
                "leg_press_deficit": {"target": "<25%", "description": "Test force unilatérale", "type": "force"},
                "leg_extension_deficit": {"target": "<30%", "description": "Force quadriceps", "type": "force"},
                "hop_test": {"target": "<40%", "description": "Saut unipodal distance", "type": "fonctionnel"}
            },
            "palier_2": {
                "force_deficit": {"target": "<15%", "description": "Tous exercices", "type": "force"},
                "saut_vertical": {"target": ">80%", "description": "Référence pré-blessure", "type": "fonctionnel"},
                "y_balance": {"target": ">90%", "description": "Symétrie équilibre", "type": "proprioception"}
            },
            "palier_3": {
                "force_deficit": {"target": "<10%", "description": "Tous muscles", "type": "force"},
                "hop_tests": {"target": ">95%", "description": "Symétrie tous tests", "type": "fonctionnel"},
                "changements_direction": {"target": "Fluides", "description": "Sans appréhension", "type": "sport_specifique"}
            }
        }
        
        # Système de badges et achievements
        self.achievements = {
            "first_workout": {"name": "🏁 Première Séance", "description": "Votre voyage commence!", "xp": 100},
            "week_complete": {"name": "📅 Semaine Complète", "description": "7 jours d'entraînement", "xp": 250},
            "month_warrior": {"name": "🗓️ Guerrier du Mois", "description": "30 jours de progression", "xp": 500},
            "force_milestone_10": {"name": "💪 Force +10%", "description": "10% de gain de force", "xp": 300},
            "force_milestone_25": {"name": "🔥 Force +25%", "description": "25% de gain de force", "xp": 500},
            "perfect_week": {"name": "⭐ Semaine Parfaite", "description": "Tous les entraînements complétés", "xp": 400},
            "early_bird": {"name": "🌅 Lève-tôt", "description": "5 séances avant 8h", "xp": 200},
            "night_owl": {"name": "🦉 Nocturne", "description": "5 séances après 20h", "xp": 200},
            "consistency_king": {"name": "👑 Roi de la Régularité", "description": "21 jours consécutifs", "xp": 750},
            "pre_op_complete": {"name": "✅ Pré-op Maîtrisé", "description": "Phase pré-opératoire terminée", "xp": 1000},
            "post_op_warrior": {"name": "🏥 Guerrier Post-op", "description": "6 semaines post-op complétées", "xp": 1500},
            "palier_1_champion": {"name": "🎯 Champion Palier 1", "description": "Palier 1 validé", "xp": 2000},
            "palier_2_hero": {"name": "🚀 Héros Palier 2", "description": "Palier 2 conquis", "xp": 2500},
            "return_to_sport": {"name": "🏆 Retour au Sport", "description": "Critères validés!", "xp": 5000}
        }

    def get_current_phase(self) -> Tuple[str, str, str]:
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

    def get_today_program(self) -> Tuple[str, List[Dict], str]:
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

    def get_phase_objectives(self, phase: str) -> List[str]:
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
    
    def get_nutrition_for_phase(self, phase: str) -> Dict:
        """Retourne les conseils nutritionnels pour la phase"""
        if "pre_op" in phase:
            return self.nutrition_tips["pre_op"]
        elif any(x in phase for x in ["semaine_1", "semaine_2-3", "semaine_4-6"]):
            return self.nutrition_tips["post_op_early"]
        else:
            return self.nutrition_tips["rehab"]
    
    def calculate_achievement_progress(self, workout_history: List[Dict]) -> Dict[str, bool]:
        """Calcule les achievements débloqués"""
        unlocked = {}
        
        if not workout_history:
            return unlocked
        
        # First workout
        if len(workout_history) >= 1:
            unlocked["first_workout"] = True
        
        # Week complete
        if len(set([w['date'].date() for w in workout_history])) >= 7:
            unlocked["week_complete"] = True
        
        # Month warrior
        if len(set([w['date'].date() for w in workout_history])) >= 30:
            unlocked["month_warrior"] = True
        
        # Perfect week - vérifier si toutes les séances d'une semaine sont faites
        # TODO: Implémenter la logique complète
        
        return unlocked

# Fonctions utilitaires améliorées
def load_lottie_url(url: str):
    """Charge une animation Lottie depuis une URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def create_circular_progress(progress: float, size: int = 200) -> str:
    """Crée un indicateur de progression circulaire en SVG"""
    # Calcul des paramètres du cercle
    radius = size // 2 - 10
    circumference = 2 * np.pi * radius
    stroke_dashoffset = circumference * (1 - progress)
    
    svg = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
        <circle
            cx="{size//2}"
            cy="{size//2}"
            r="{radius}"
            fill="none"
            stroke="#e0e0e0"
            stroke-width="8"
        />
        <circle
            cx="{size//2}"
            cy="{size//2}"
            r="{radius}"
            fill="none"
            stroke="url(#gradient)"
            stroke-width="8"
            stroke-dasharray="{circumference}"
            stroke-dashoffset="{stroke_dashoffset}"
            stroke-linecap="round"
            transform="rotate(-90 {size//2} {size//2})"
            style="transition: stroke-dashoffset 0.5s ease-in-out;"
        />
        <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
            </linearGradient>
        </defs>
        <text x="{size//2}" y="{size//2}" text-anchor="middle" dy=".3em" fill="#333" font-size="24" font-weight="bold">
            {int(progress * 100)}%
        </text>
    </svg>
    """
    return svg

def play_sound_effect(sound_type: str):
    """Joue un effet sonore (nécessite intégration audio)"""
    # Pour une vraie implémentation, utiliser st.audio ou JavaScript
    sound_urls = {
        "success": "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3",
        "timer_end": "https://www.soundjay.com/misc/sounds/bell-ringing-01.mp3",
        "achievement": "https://www.soundjay.com/misc/sounds/magic-chime-01.mp3"
    }
    
    # Implémentation basique avec JavaScript
    if sound_type in sound_urls:
        components.html(
            f"""
            <audio autoplay>
                <source src="{sound_urls[sound_type]}" type="audio/mpeg">
            </audio>
            """,
            height=0
        )

def generate_motivational_quote() -> str:
    """Génère une citation motivante"""
    quotes = [
        "La douleur d'aujourd'hui est la force de demain. 💪",
        "Chaque répétition vous rapproche de votre objectif. 🎯",
        "Le succès est la somme de petits efforts répétés jour après jour. ⭐",
        "Votre seule limite est vous-même. 🚀",
        "Les champions s'entraînent, les légendes persévèrent. 🏆",
        "La discipline est le pont entre les objectifs et l'accomplissement. 🌉",
        "Ne comptez pas les jours, faites que les jours comptent. 📅",
        "L'impossible d'aujourd'hui sera la routine de demain. ⚡",
        "Votre corps peut supporter presque tout. C'est votre esprit qu'il faut convaincre. 🧠",
        "Le progrès demande de la patience. La patience crée le progrès. 🌱"
    ]
    return np.random.choice(quotes)

def calculate_phase_progress(program: RehabProgram) -> float:
    """Calcule le pourcentage de progression dans la phase actuelle"""
    phase, _, _ = program.get_current_phase()
    today = datetime.now()
    surgery_date = program.surgery_date
    
    phase_durations = {
        "pre_op_semaine_-4_-3": (28, 14),
        "pre_op_semaine_-2_-1": (14, 0),
        "post_op_semaine_1": (0, 7),
        "post_op_semaine_2-3": (7, 21),
        "post_op_semaine_4-6": (21, 45),
        "post_op_palier_1": (45, 90),
        "post_op_palier_2": (90, 180),
        "post_op_palier_3": (180, 270)
    }
    
    if phase in phase_durations:
        start_days, end_days = phase_durations[phase]
        
        if "pre_op" in phase:
            start_date = surgery_date - timedelta(days=start_days)
            end_date = surgery_date - timedelta(days=end_days)
        else:
            start_date = surgery_date + timedelta(days=start_days)
            end_date = surgery_date + timedelta(days=end_days)
        
        total_days = (end_date - start_date).days
        elapsed_days = (today - start_date).days
        
        return min(1.0, max(0.0, elapsed_days / total_days))
    
    return 1.0

def create_exercise_card_html(exercise: Dict, index: int, current_set: int) -> str:
    """Crée une carte d'exercice HTML moderne"""
    difficulty_colors = {
        1: "#4CAF50",
        2: "#8BC34A", 
        3: "#FFC107",
        4: "#FF9800",
        5: "#F44336"
    }
    
    difficulty_stars = "⭐" * exercise.get("difficulte", 3)
    difficulty_color = difficulty_colors.get(exercise.get("difficulte", 3), "#FFC107")
    
    muscles_badges = "".join([f'<span class="progress-badge" style="font-size: 0.8rem; margin: 2px;">{m}</span>' 
                              for m in exercise.get("muscles", [])])
    
    html = f"""
    <div class="modern-card exercise-card" style="animation-delay: {index * 0.1}s;">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <h3 style="color: #3366ff; margin-bottom: 0.5rem;">
                    🎯 {exercise["nom"]}
                    <span style="color: {difficulty_color}; font-size: 0.9rem; margin-left: 10px;">
                        {difficulty_stars}
                    </span>
                </h3>
                
                <p style="color: #666; margin-bottom: 1rem; font-style: italic;">
                    {exercise["description"]}
                </p>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem;">
                    <div>
                        <strong style="color: #3366ff;">🔢 Volume:</strong> 
                        <span>{exercise["series"]} séries × {exercise["reps"]} reps</span>
                    </div>
                    <div>
                        <strong style="color: #3366ff;">⚖️ Charge:</strong> 
                        <span>{exercise["charge"]}</span>
                    </div>
                    <div>
                        <strong style="color: #3366ff;">⏱️ Repos:</strong> 
                        <span>{exercise["repos"]}</span>
                    </div>
                    <div>
                        <strong style="color: #3366ff;">🎯 Focus:</strong> 
                        <span>{exercise["focus"]}</span>
                    </div>
                </div>
                
                <div style="background: #f0f2f6; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                    <strong style="color: #ff6b6b;">💡 Conseils:</strong> 
                    <span>{exercise["conseils"]}</span>
                </div>
                
                <div style="margin-top: 1rem;">
                    <strong>🏃 Muscles ciblés:</strong>
                    <div style="margin-top: 0.5rem;">
                        {muscles_badges}
                    </div>
                </div>
            </div>
            
            <div style="text-align: center; margin-left: 2rem;">
                <div style="font-size: 3rem; color: #3366ff; font-weight: bold;">
                    {current_set}/{exercise["series"]}
                </div>
                <div style="color: #666; font-size: 0.9rem;">
                    Série actuelle
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def create_dashboard_metrics(program: RehabProgram, workout_history: List[Dict]) -> None:
    """Crée un tableau de bord avec métriques avancées"""
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculs des métriques
    total_workouts = len(set([w['date'].date() for w in workout_history])) if workout_history else 0
    current_streak = calculate_streak(workout_history) if workout_history else 0
    total_volume = sum([w.get('poids', 0) * w.get('reps', 0) for w in workout_history])
    phase_progress = calculate_phase_progress(program)
    
    with col1:
        st.metric("🏋️ Séances totales", total_workouts)
    
    with col2:
        st.metric("🔥 Jours consécutifs", current_streak)
    
    with col3:
        st.metric("💪 Volume total", f"{total_volume/1000:.1f}t")
    
    with col4:
        st.metric("📊 Progression phase", f"{int(phase_progress * 100)}%")

def calculate_streak(workout_history: List[Dict]) -> int:
    """Calcule la série de jours consécutifs d'entraînement"""
    if not workout_history:
        return 0
    
    dates = sorted(set([w['date'].date() for w in workout_history]), reverse=True)
    streak = 0
    today = datetime.now().date()
    
    for i, date in enumerate(dates):
        expected_date = today - timedelta(days=i)
        if date == expected_date:
            streak += 1
        else:
            break
    
    return streak

def show_achievement_notification(achievement_name: str, achievement_data: Dict):
    """Affiche une notification d'achievement débloqué"""
    st.success(f"""
    🎉 **NOUVEL ACHIEVEMENT DÉBLOQUÉ!**
    
    {achievement_data['name']}
    
    *{achievement_data['description']}*
    
    +{achievement_data['xp']} XP
    """)

def init_session_state():
    """Initialisation de l'état de session avec toutes les variables"""
    if 'program' not in st.session_state:
        st.session_state.program = RehabProgram()
    if 'github_storage' not in st.session_state:
        st.session_state.github_storage = GitHubStorage()
    
    # Charger les données depuis GitHub au démarrage
    if 'github_storage' in st.session_state and st.session_state.github_storage.connected:
        # Charger l'historique des workouts
        if 'workout_history' not in st.session_state:
            workouts = st.session_state.github_storage.get_workouts()
            # Convertir les timestamps string en datetime
            for workout in workouts:
                if 'timestamp' in workout:
                    workout['date'] = datetime.fromisoformat(workout['timestamp'])
            st.session_state.workout_history = workouts
        
        # Charger l'état de progression
        progress_state = st.session_state.github_storage.get_progress_state()
        if 'current_exercise_index' not in st.session_state:
            st.session_state.current_exercise_index = progress_state["current_exercise_index"]
        if 'current_set' not in st.session_state:
            st.session_state.current_set = progress_state["current_set"]
    else:
        if 'workout_history' not in st.session_state:
            st.session_state.workout_history = []
        if 'current_exercise_index' not in st.session_state:
            st.session_state.current_exercise_index = 0
        if 'current_set' not in st.session_state:
            st.session_state.current_set = 1
            
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'timer_start' not in st.session_state:
        st.session_state.timer_start = 0
    if 'rest_duration' not in st.session_state:
        st.session_state.rest_duration = 60
    if 'exercise_notes' not in st.session_state:
        st.session_state.exercise_notes = {}
    if 'unlocked_achievements' not in st.session_state:
        st.session_state.unlocked_achievements = set()
    if 'user_xp' not in st.session_state:
        st.session_state.user_xp = 0
    if 'user_level' not in st.session_state:
        st.session_state.user_level = 1
    if 'show_tutorial' not in st.session_state:
        st.session_state.show_tutorial = True

def save_workout_to_github(workout_data: Dict) -> bool:
    """Sauvegarde un workout sur GitHub avec gestion des achievements"""
    if not st.session_state.github_storage.connected:
        # Fallback en session seulement
        st.session_state.workout_history.append(workout_data)
        return True
    
    github_storage = st.session_state.github_storage
    
    # Préparer les données (enlever 'date' car on utilise 'timestamp')
    github_data = workout_data.copy()
    if 'date' in github_data:
        del github_data['date']  # Sera recréé avec timestamp
    
    # Sauvegarder sur GitHub
    if github_storage.append_workout(github_data):
        # Sauvegarder également l'état de progression actuel
        github_storage.save_progress_state(
            st.session_state.current_exercise_index,
            st.session_state.current_set
        )
        
        # Recharger les données dans la session
        updated_workouts = github_storage.get_workouts()
        for workout in updated_workouts:
            if 'timestamp' in workout:
                workout['date'] = datetime.fromisoformat(workout['timestamp'])
        st.session_state.workout_history = updated_workouts
        
        # Vérifier les achievements
        check_new_achievements()
        
        return True
    return False

def extract_weight(charge_str):
    """Extrait la valeur numérique du poids depuis différents formats"""
    try:
        if "kg" in charge_str:
            # Gère les cas comme "85kg"
            weight_part = charge_str.split("kg")[0].strip()
            # Prendre le dernier mot qui devrait être le nombre
            number_part = weight_part.split()[-1]
            return float(number_part)
        else:
            # Pour les cas comme "Haltère 16", extraire les nombres
            import re
            numbers = re.findall(r'\d+\.?\d*', charge_str)
            if numbers:
                return float(numbers[0])
            else:
                return 0.0
    except:
        # Si tout échoue, retourner la valeur par défaut
        return 0.0
    
def get_reps_value(reps_value):
    """Extrait le nombre de répétitions à partir de différents formats"""
    try:
        # Si c'est déjà un entier, on le retourne directement
        if isinstance(reps_value, int):
            return reps_value
        
        # Si c'est une chaîne qui peut être convertie en entier
        elif isinstance(reps_value, str):
            if reps_value.isdigit():
                return int(reps_value)
            else:
                # Pour les cas comme "10 chaque jambe", extraire le premier nombre
                import re
                numbers = re.findall(r'\d+', reps_value)
                if numbers:
                    return int(numbers[0])
        
        # Valeur par défaut
        return 10
    except:
        return 10

def check_new_achievements():
    """Vérifie et attribue les nouveaux achievements"""
    program = st.session_state.program
    workout_history = st.session_state.workout_history
    
    # Calculer les achievements débloqués
    unlocked = program.calculate_achievement_progress(workout_history)
    
    # Vérifier les nouveaux achievements
    for achievement_id, is_unlocked in unlocked.items():
        if is_unlocked and achievement_id not in st.session_state.unlocked_achievements:
            st.session_state.unlocked_achievements.add(achievement_id)
            achievement_data = program.achievements[achievement_id]
            st.session_state.user_xp += achievement_data['xp']
            
            # Calculer le niveau
            st.session_state.user_level = 1 + (st.session_state.user_xp // 1000)
            
            # Sauvegarder l'achievement
            if st.session_state.github_storage.connected:
                st.session_state.github_storage.save_achievement({
                    "achievement_id": achievement_id,
                    "name": achievement_data['name'],
                    "xp": achievement_data['xp']
                })
            
            # Afficher la notification
            show_achievement_notification(achievement_id, achievement_data)

def show_github_status():
    """Affiche le statut de la connexion GitHub avec design moderne"""
    st.sidebar.markdown("### 📁 Stockage Cloud")
    
    if not st.session_state.github_storage.connected:
        st.sidebar.error("❌ Non connecté")
        st.sidebar.caption("Vérifiez vos secrets GitHub")
        return
    
    github_storage = st.session_state.github_storage
    
    try:
        workouts = github_storage.get_workouts()
        
        # Métriques de synchronisation
        col1, col2 = st.sidebar.columns(2)
        with col1:
            status_emoji = "✅" if len(workouts) > 0 else "🔗"
            st.metric("Statut", status_emoji)
        with col2:
            st.metric("Workouts", len(workouts))
        
        # Dernière synchro avec style
        if workouts:
            last_workout = max([w.get('timestamp', '') for w in workouts])
            if last_workout:
                last_date = datetime.fromisoformat(last_workout)
                time_diff = datetime.now() - last_date
                
                if time_diff.days == 0:
                    if time_diff.seconds < 3600:
                        time_str = f"{time_diff.seconds // 60} min"
                    else:
                        time_str = f"{time_diff.seconds // 3600}h"
                else:
                    time_str = f"{time_diff.days}j"
                
                st.sidebar.caption(f"📅 Dernière synchro: il y a {time_str}")
        
        # Bouton de synchro avec animation
        if st.sidebar.button("🔄 Synchroniser", use_container_width=True):
            with st.spinner("🔄 Synchronisation en cours..."):
                updated_workouts = github_storage.get_workouts()
                for workout in updated_workouts:
                    if 'timestamp' in workout:
                        workout['date'] = datetime.fromisoformat(workout['timestamp'])
                st.session_state.workout_history = updated_workouts
                st.success("✅ Données synchronisées!")
                time.sleep(1)
                st.rerun()
                
    except Exception as e:
        st.sidebar.error("❌ Erreur GitHub")
        st.sidebar.caption(str(e)[:50] + "...")

def show_user_progress_bar():
    """Affiche la barre de progression XP de l'utilisateur"""
    xp = st.session_state.user_xp
    level = st.session_state.user_level
    xp_for_current_level = (level - 1) * 1000
    xp_for_next_level = level * 1000
    xp_progress = (xp - xp_for_current_level) / 1000
    
    st.sidebar.markdown("### 🌟 Progression")
    st.sidebar.markdown(
        f"""
        <div style="background: #f0f2f6; padding: 1rem; border-radius: 10px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: bold;">Niveau {level}</span>
                <span style="color: #666;">{xp} XP</span>
            </div>
            <div style="background: #ddd; height: 10px; border-radius: 5px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                           height: 100%; width: {xp_progress * 100}%; 
                           transition: width 0.5s ease;"></div>
            </div>
            <div style="text-align: center; margin-top: 0.5rem; font-size: 0.8rem; color: #666;">
                {int(xp_progress * 1000)}/1000 XP vers niveau {level + 1}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Badges débloqués
    if st.session_state.unlocked_achievements:
        st.sidebar.markdown("#### 🏅 Achievements")
        achievement_count = len(st.session_state.unlocked_achievements)
        total_achievements = len(st.session_state.program.achievements)
        st.sidebar.caption(f"{achievement_count}/{total_achievements} débloqués")

def main():
    init_session_state()
    
    # Header principal avec animation et citation
    st.markdown(
        '<h1 class="main-header">🏃‍♂️ RÉÉDUCATION LCA - KENNETH JONES</h1>', 
        unsafe_allow_html=True
    )
    
    # Citation motivante du jour
    quote = generate_motivational_quote()
    st.markdown(
        f'<div style="text-align: center; font-style: italic; color: #666; margin-bottom: 2rem;">"{quote}"</div>',
        unsafe_allow_html=True
    )
    
    # Tutorial pour nouveaux utilisateurs
    if st.session_state.show_tutorial and not st.session_state.workout_history:
        with st.info("💡 **Bienvenue dans votre programme de rééducation!**"):
            st.write("""
            Voici comment utiliser l'application:
            1. **Programme du Jour** : Suivez vos exercices quotidiens
            2. **Suivi & Progrès** : Visualisez votre évolution
            3. **Tests d'Évaluation** : Validez vos paliers de progression
            4. **Guide Complet** : Consultez toutes les phases du programme
            
            Prêt à commencer? C'est parti! 🚀
            """)
            if st.button("J'ai compris! 👍"):
                st.session_state.show_tutorial = False
                st.rerun()
    
    # Sidebar enrichie
    st.sidebar.title("📊 TABLEAU DE BORD")
    
    # Profil utilisateur avec avatar
    st.sidebar.markdown("### 👤 Profil Athlète")
    col1, col2 = st.sidebar.columns([1, 2])
    with col1:
        # Avatar avec niveau
        st.markdown(
            f"""
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; border-radius: 50%; 
                           background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                           display: flex; align-items: center; justify-content: center;
                           color: white; font-size: 1.5rem; font-weight: bold;">
                    {st.session_state.user_level}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.metric("Poids", f"{st.session_state.program.patient_weight:.1f} kg")
        st.metric("Taille", f"{st.session_state.program.patient_height} cm")
    
    st.sidebar.write(f"**🗓️ Opération:** {st.session_state.program.surgery_date.strftime('%d/%m/%Y')}")
    
    # Barre de progression XP
    show_user_progress_bar()
    
    # Phase actuelle avec animation
    phase, phase_name, emoji = st.session_state.program.get_current_phase()
    st.sidebar.markdown(f"### 📅 Phase Actuelle")

    # Utiliser une méthode plus simple pour afficher la phase
    st.sidebar.info(f"{emoji} **{phase_name}**")

    # Progress bar simple pour la progression de phase
    phase_progress = calculate_phase_progress(st.session_state.program)
    st.sidebar.progress(phase_progress)
    st.sidebar.caption(f"Progression: {int(phase_progress * 100)}%")
    
    # Objectifs de la phase
    objectives = st.session_state.program.get_phase_objectives(phase)
    with st.sidebar.expander("🎯 Objectifs de phase", expanded=False):
        for obj in objectives:
            st.write(f"• {obj}")
    
    # Statut GitHub
    show_github_status()
    
    # Statistiques rapides avec graphiques sparkline
    if st.session_state.workout_history:
        st.sidebar.markdown("### 📈 Stats Rapides")
        
        # Créer un mini graphique des 7 derniers jours
        df = pd.DataFrame(st.session_state.workout_history)
        df['date'] = pd.to_datetime(df['date'])
        last_7_days = datetime.now() - timedelta(days=7)
        df_recent = df[df['date'] >= last_7_days]
        
        if not df_recent.empty:
            daily_counts = df_recent.groupby(df_recent['date'].dt.date).size()
            
            # Utiliser un graphique plus simple
            if len(daily_counts) > 0:
                # Créer un petit graphique ligne
                dates = daily_counts.index.tolist()
                values = daily_counts.values.tolist()
                
                # Afficher les stats sans graphique complexe
                st.sidebar.metric("📊 Cette semaine", f"{sum(values)} exercices")
                st.sidebar.metric("📅 Moyenne/jour", f"{sum(values)/7:.1f}")
    
    # Navigation avec icônes et badges
    st.sidebar.markdown("### 🧭 Navigation")
    
    # Compter les exercices non complétés
    session_name, exercises, _ = st.session_state.program.get_today_program()
    exercises_remaining = len(exercises) - st.session_state.current_exercise_index if exercises else 0
    
    pages = {
        "🏋️ Programme du Jour": exercises_remaining if exercises_remaining > 0 else None,
        "📈 Suivi & Progrès": None,
        "🧪 Tests d'Évaluation": None,
        "🍎 Nutrition": None,
        "📚 Guide Complet": None,
        "🏅 Achievements": len(st.session_state.unlocked_achievements),
        "⚙️ Paramètres": None
    }
    
    # Créer le menu avec badges
    page_options = []
    for page, badge in pages.items():
        if badge:
            page_options.append(f"{page} ({badge})")
        else:
            page_options.append(page)
    
    selected_page_with_badge = st.sidebar.selectbox("Choisissez une page", page_options)
    
    # Extraire le nom de la page sans le badge
    page = selected_page_with_badge.split(" (")[0]
    
    # Routage des pages
    if page == "🏋️ Programme du Jour":
        show_daily_program()
    elif page == "📈 Suivi & Progrès":
        show_progress_tracking()
    elif page == "🧪 Tests d'Évaluation":
        show_evaluation_tests()
    elif page == "🍎 Nutrition":
        show_nutrition_guide()
    elif page == "📚 Guide Complet":
        show_complete_guide()
    elif page == "🏅 Achievements":
        show_achievements_page()
    else:
        show_settings()

def show_daily_program():
    """Affiche le programme du jour avec timer et suivi avancé"""
    st.header("🏋️ Programme du Jour")
    
    # Dashboard de métriques
    create_dashboard_metrics(st.session_state.program, st.session_state.workout_history)
    
    # Récupération du programme
    session_name, exercises, session_emoji = st.session_state.program.get_today_program()
    phase, phase_name, phase_emoji = st.session_state.program.get_current_phase()
    
    # En-tête de séance avec style
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(
            f"""
            <div class="modern-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <h2 style="margin: 0;">{session_emoji} {session_name}</h2>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Phase: {phase_name}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        if exercises:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">{len(exercises)}</div>
                    <div style="color: #666;">Exercices</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with col3:
        if exercises:
            progress_pct = (st.session_state.current_exercise_index / len(exercises)) * 100
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">{progress_pct:.0f}%</div>
                    <div style="color: #666;">Complété</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Cas du repos avec design moderne
    if not exercises:
        # Animation Lottie pour le repos
        lottie_rest = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_xd9ypluc.json")
        if lottie_rest:
            st_lottie(lottie_rest, height=200, key="rest_animation")
        
        st.markdown(
            '<div class="modern-card success-card">'
            '<h3>🛌 Jour de Repos Programmé</h3>'
            '<p><strong>La récupération fait partie intégrante de votre protocole !</strong></p>'
            '</div>',
            unsafe_allow_html=True
        )
        
        # Recommandations en colonnes avec icônes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                <div class="modern-card">
                    <h4>💧 Hydratation</h4>
                    <p>2.5-3L d'eau répartis dans la journée</p>
                    <div style="background: #e3f2fd; padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;">
                        💡 Ajoutez une pincée de sel et du citron pour l'électrolyte
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(
                """
                <div class="modern-card">
                    <h4>😴 Sommeil</h4>
                    <p>8-9h de qualité pour optimiser la récupération</p>
                    <div style="background: #e8f5e9; padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;">
                        💡 Température chambre: 18-20°C
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                """
                <div class="modern-card">
                    <h4>🧘 Mobilité douce</h4>
                    <p>Étirements légers si souhaité (15-20min)</p>
                    <div style="background: #fce4ec; padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;">
                        💡 Focus sur les zones tendues
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(
                """
                <div class="modern-card">
                    <h4>🍎 Nutrition</h4>
                    <p>Privilégier protéines et anti-inflammatoires</p>
                    <div style="background: #fff3e0; padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;">
                        💡 Saumon, baies, curcuma
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Section d'observation avec design moderne
        with st.expander("📝 Ajouter une observation", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                douleur = st.slider("Niveau de douleur (0-10)", 0, 10, 0)
                gonflement = st.selectbox("Gonflement", ["Aucun", "Léger", "Modéré", "Important"])
                mobilite = st.slider("Mobilité du genou (%)", 0, 100, 50)
            with col2:
                humeur = st.selectbox("Humeur", ["😊 Excellent", "🙂 Bien", "😐 Moyen", "😕 Difficile"])
                sommeil = st.number_input("Heures de sommeil", 0.0, 12.0, 8.0, 0.5)
            
            note = st.text_area("Observations supplémentaires", placeholder="Comment vous sentez-vous aujourd'hui?")
            
            if st.button("💾 Sauvegarder l'observation", type="primary"):
                observation_data = {
                    "date": datetime.now(),
                    "exercice": "Repos - Observation",
                    "douleur": douleur,
                    "gonflement": gonflement,
                    "mobilite": mobilite,
                    "humeur": humeur,
                    "sommeil": sommeil,
                    "note": note,
                    "type": "repos"
                }
                if save_workout_to_github(observation_data):
                    st.success("✅ Observation sauvegardée!")
        
        return
    
    # Barre de progression visuelle améliorée
    progress = st.session_state.current_exercise_index / len(exercises)
    st.markdown(
        f"""
        <div style="background: #f0f2f6; border-radius: 20px; padding: 4px; margin: 1rem 0;">
            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 {progress*100}%, #e0e0e0 {progress*100}%);
                        height: 20px; border-radius: 16px; transition: all 0.5s ease;">
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    

    # Affichage des exercices avec navigation
    if st.session_state.current_exercise_index < len(exercises):
        exercise = exercises[st.session_state.current_exercise_index]
        
        # Navigation entre exercices
        col_prev, col_title, col_next = st.columns([1, 6, 1])
        
        with col_prev:
            if st.session_state.current_exercise_index > 0:
                if st.button("◀️", help="Exercice précédent"):
                    st.session_state.current_exercise_index -= 1
                    st.session_state.current_set = 1
                    # Sauvegarder l'état de progression
                    if st.session_state.github_storage.connected:
                        st.session_state.github_storage.save_progress_state(
                            st.session_state.current_exercise_index,
                            st.session_state.current_set
                        )
                    st.rerun()
        
        with col_title:
            st.markdown(
                f"<h3 style='text-align: center; color: #3366ff;'>Exercice {st.session_state.current_exercise_index + 1}/{len(exercises)}</h3>",
                unsafe_allow_html=True
            )
        
        with col_next:
            if st.session_state.current_exercise_index < len(exercises) - 1:
                if st.button("▶️", help="Exercice suivant"):
                    st.session_state.current_exercise_index += 1
                    st.session_state.current_set = 1
                    # Sauvegarder l'état de progression
                    if st.session_state.github_storage.connected:
                        st.session_state.github_storage.save_progress_state(
                            st.session_state.current_exercise_index,
                            st.session_state.current_set
                        )
                    st.rerun()
                        

        
        # Affichage de l'exercice avec carte moderne
        # components.html(
        #     create_exercise_card_html(exercise, st.session_state.current_exercise_index, st.session_state.current_set),
        #     height=400
        # )
        
        display_exercise_card(exercise, st.session_state.current_exercise_index, st.session_state.current_set)

        # Vidéo de démonstration si disponible
        if exercise["nom"] in st.session_state.program.exercise_videos:
            with st.expander("🎥 Voir la démonstration vidéo", expanded=False):
                st.video(st.session_state.program.exercise_videos[exercise["nom"]])
        
        # Interface de suivi améliorée
        st.markdown("### 📊 Enregistrement de la Série")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Formulaire de performance avec style
            col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
            
            
            
            
            with col_perf1:
                poids_realise = st.number_input(
                "⚖️ Poids (kg)", 
                min_value=0.0, 
                step=0.5,
                value=extract_weight(exercise["charge"]),
                key=f"poids_{st.session_state.current_exercise_index}_{st.session_state.current_set}"
            )
            
            with col_perf2:                
                reps_realisees = st.number_input(
                "🔢 Répétitions", 
                min_value=0, 
                step=1,
                value=get_reps_value(exercise["reps"]),
                key=f"reps_{st.session_state.current_exercise_index}_{st.session_state.current_set}"
            )
                        
            with col_perf3:
                # RPE avec émojis
                rpe_options = {
                    1: "1 - 😴 Très facile",
                    2: "2 - 😌 Facile",
                    3: "3 - 🙂 Léger",
                    4: "4 - 😊 Modéré",
                    5: "5 - 😐 Moyen",
                    6: "6 - 😤 Difficile",
                    7: "7 - 😓 Très difficile",
                    8: "8 - 😰 Intense",
                    9: "9 - 😵 Très intense",
                    10: "10 - 💀 Maximum"
                }
                rpe = st.selectbox(
                    "💪 RPE", 
                    options=list(rpe_options.keys()),
                    format_func=lambda x: rpe_options[x],
                    index=4,
                    key=f"rpe_{st.session_state.current_exercise_index}_{st.session_state.current_set}"
                )
            
            with col_perf4:
                # Technique rating
                technique = st.select_slider(
                    "🎯 Technique",
                    options=["❌ Mauvaise", "⚠️ Moyenne", "✅ Bonne", "⭐ Excellente"],
                    value="✅ Bonne",
                    key=f"tech_{st.session_state.current_exercise_index}_{st.session_state.current_set}"
                )
            
            # Zone de notes avec placeholder contextuel
            placeholders = [
                "Ex: Légère gêne au début, disparue après échauffement",
                "Ex: Bonne sensation, amplitude complète atteinte",
                "Ex: Fatigue en fin de série, forme maintenue",
                "Ex: Progression par rapport à la dernière fois"
            ]
            
            note_exercice = st.text_area(
                "📝 Notes sur la série", 
                placeholder=np.random.choice(placeholders),
                key=f"note_{st.session_state.current_exercise_index}_{st.session_state.current_set}",
                height=80
            )
        
        with col2:
            # Timer amélioré avec design moderne
            st.markdown("### ⏱️ Chronomètre de Repos")
            
            # Extraction intelligente du temps de repos
            rest_str = exercise["repos"]
            if "min" in rest_str:
                rest_minutes = float(rest_str.replace("min", "").strip())
                default_rest = int(rest_minutes * 60)
            elif "s" in rest_str:
                default_rest = int(rest_str.replace("s", "").strip())
            else:
                default_rest = 60
            
            # Timer circulaire
            if not st.session_state.timer_running:
                # Personnalisation du temps
                custom_time = st.number_input(
                    "⏱️ Temps personnalisé (s)", 
                    value=default_rest, 
                    min_value=10, 
                    max_value=300,
                    step=10
                )
                
                col_timer1, col_timer2 = st.columns(2)
                with col_timer1:
                    if st.button("▶️ GO!", type="primary", use_container_width=True):
                        st.session_state.timer_running = True
                        st.session_state.timer_start = time.time()
                        st.session_state.rest_duration = custom_time
                        st.rerun()
                
                with col_timer2:
                    # Presets de temps
                    if st.button(f"⚡ {default_rest}s", use_container_width=True):
                        st.session_state.timer_running = True
                        st.session_state.timer_start = time.time()
                        st.session_state.rest_duration = default_rest
                        st.rerun()
            else:
                # Timer en cours
                elapsed = int(time.time() - st.session_state.timer_start)
                remaining = max(0, st.session_state.rest_duration - elapsed)
                
                if remaining > 0:
                    mins, secs = divmod(remaining, 60)
                    
                    # Affichage du timer avec cercle de progression
                    progress_timer = 1 - (remaining / st.session_state.rest_duration)
                    timer_svg = f"""
                    <svg width="200" height="200" viewBox="0 0 200 200">
                        <circle cx="100" cy="100" r="90" fill="none" stroke="#e0e0e0" stroke-width="10"/>
                        <circle cx="100" cy="100" r="90" fill="none" stroke="#ff3b30" stroke-width="10"
                                stroke-dasharray="{2 * np.pi * 90}"
                                stroke-dashoffset="{2 * np.pi * 90 * (1 - progress_timer)}"
                                stroke-linecap="round"
                                transform="rotate(-90 100 100)"
                                style="transition: stroke-dashoffset 0.5s linear;"/>
                        <text x="100" y="100" text-anchor="middle" dy=".3em" 
                              fill="#ff3b30" font-size="48" font-weight="bold">
                            {mins:02d}:{secs:02d}
                        </text>
                    </svg>
                    """
                    
                    components.html(
                        f"""
                        <div style="display: flex; justify-content: center; margin: 1rem 0;">
                            {timer_svg}
                        </div>
                        """,
                        height=220
                    )
                    
                    # Auto-refresh pour le timer
                    time.sleep(0.1)
                    st.rerun()
                else:
                    # Timer terminé
                    st.success("⏰ Repos terminé !")
                    st.session_state.timer_running = False
                
                if st.button("⏹️ Stop", type="secondary", use_container_width=True):
                    st.session_state.timer_running = False
                    st.rerun()
            
            # Boutons d'action avec style
            st.markdown("### 🎮 Actions")
            
            if st.button("✅ Valider la Série", type="primary", use_container_width=True):
                # Enregistrer la série
                workout_data = {
                    "date": datetime.now(),
                    "exercice": exercise["nom"],
                    "serie": st.session_state.current_set,
                    "poids": poids_realise,
                    "reps": reps_realisees,
                    "rpe": rpe,
                    "technique": technique,
                    "note": note_exercice,
                    "phase": phase,
                    "muscles": exercise.get("muscles", [])
                }
                
                # Animation de sauvegarde
                with st.spinner("💾 Sauvegarde..."):
                    if save_workout_to_github(workout_data):
                        st.success("✅ Série enregistrée!")
                        
                        # Passer à la série suivante ou exercice suivant
                        if st.session_state.current_set < exercise["series"]:
                            st.session_state.current_set += 1
                            st.info(f"🔄 Série {st.session_state.current_set}/{exercise['series']}")
                        else:
                            st.session_state.current_set = 1
                            st.session_state.current_exercise_index += 1
                            if st.session_state.current_exercise_index < len(exercises):
                                st.info("➡️ Exercice suivant!")
                        
                        st.session_state.timer_running = False
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Erreur sauvegarde")
            
            if st.button("⏭️ Passer", use_container_width=True):
                st.session_state.current_set = 1
                st.session_state.current_exercise_index += 1
                st.session_state.timer_running = False
                st.rerun()
    
    else:
        # Séance terminée - écran de félicitations
        st.markdown(
            """
            <div class="modern-card success-card" style="text-align: center; padding: 3rem;">
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">🎉 BRAVO!</h1>
                <h2>Séance Terminée avec Succès!</h2>
                <p style="font-size: 1.2rem; margin-top: 1rem;">
                    Excellent travail! Votre détermination paie. 💪
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
                
        # Résumé détaillé de la séance
        if st.session_state.workout_history:
            today_workouts = [w for w in st.session_state.workout_history 
                            if w['date'].date() == datetime.now().date()]
            
            if today_workouts:
                st.markdown("### 📊 Résumé de Performance")
                
                # Métriques en colonnes
                col1, col2, col3, col4 = st.columns(4)
                
                df_today = pd.DataFrame(today_workouts)
                
                with col1:
                    total_exercises = df_today['exercice'].nunique()
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div style="font-size: 2rem;">🎯</div>
                            <div style="font-size: 2rem; font-weight: bold;">{total_exercises}</div>
                            <div style="color: #666;">Exercices</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with col2:
                    total_series = len(df_today)
                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div style="font-size: 2rem;">📈</div>
                            <div style="font-size: 2rem; font-weight: bold;">{total_series}</div>
                            <div style="color: #666;">Séries</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with col3:
                    if 'poids' in df_today.columns and 'reps' in df_today.columns:
                        total_tonnage = (df_today['poids'] * df_today['reps']).sum()
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div style="font-size: 2rem;">💪</div>
                                <div style="font-size: 2rem; font-weight: bold;">{total_tonnage/1000:.1f}t</div>
                                <div style="color: #666;">Tonnage</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                with col4:
                    if 'rpe' in df_today.columns:
                        avg_rpe = df_today['rpe'].mean()
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div style="font-size: 2rem;">🔥</div>
                                <div style="font-size: 2rem; font-weight: bold;">{avg_rpe:.1f}</div>
                                <div style="color: #666;">RPE moyen</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                # Graphique de performance de la séance
                if len(df_today) > 1:
                    fig_session = go.Figure()
                    
                    # RPE par exercice
                    rpe_by_exercise = df_today.groupby('exercice')['rpe'].mean()
                    
                    fig_session.add_trace(go.Bar(
                        x=rpe_by_exercise.index,
                        y=rpe_by_exercise.values,
                        name='RPE moyen',
                        marker=dict(
                            color=rpe_by_exercise.values,
                            colorscale='RdYlGn_r',
                            showscale=True,
                            colorbar=dict(title="RPE")
                        )
                    ))
                    
                    fig_session.update_layout(
                        title="Intensité par Exercice",
                        xaxis_title="Exercice",
                        yaxis_title="RPE",
                        height=300,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_session, use_container_width=True)
        
        # Actions post-séance
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Refaire la séance", use_container_width=True):
                st.session_state.current_exercise_index = 0
                st.session_state.current_set = 1
                st.rerun()

        with col2:
            if st.button("📊 Voir mes progrès", use_container_width=True):
                # Au lieu de switch_page, changer la sélection dans la sidebar
                st.session_state.selected_page = "📈 Suivi & Progrès"
                st.rerun()

        with col3:
            with st.expander("📝 Commentaire global"):
                global_note = st.text_area(
                    "Comment s'est passée la séance?",
                    placeholder="Sensations générales, points à améliorer..."
                )
                
                feeling = st.select_slider(
                    "Ressenti global",
                    options=["😵 Épuisé", "😓 Fatigué", "😊 Bien", "💪 En forme", "🚀 Excellent"],
                    value="😊 Bien"
                )
                
                if st.button("💾 Sauvegarder", type="primary"):
                    comment_data = {
                        "date": datetime.now(),
                        "exercice": "Commentaire séance",
                        "note": global_note,
                        "feeling": feeling,
                        "type": "commentaire"
                    }
                    if save_workout_to_github(comment_data):
                        st.success("✅ Commentaire sauvegardé!")
    
    # Section conseils contextuels avec cards modernes
    st.markdown("---")
    phase_tips = st.session_state.program.get_nutrition_for_phase(phase)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class="modern-card">
                <h3>🍎 Nutrition du Jour</h3>
                <p><strong>Calories:</strong> {phase_tips['calories']}</p>
                <p><strong>Protéines:</strong> {phase_tips['proteines']}</p>
                <p><strong>Glucides:</strong> {phase_tips['glucides']}</p>
                <p><strong>Hydratation:</strong> {phase_tips['hydratation']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="modern-card">
                <h3>💊 Suppléments Recommandés</h3>
                <ul style="list-style: none; padding: 0;">
                    {''.join([f'<li>✓ {supp}</li>' for supp in phase_tips['supplements']])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

def show_progress_tracking():
    """Suivi détaillé des progrès avec graphiques interactifs avancés"""
    st.header("📈 Suivi & Analyse des Progrès")
    
    if not st.session_state.workout_history:
        # État vide avec call-to-action
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                """
                <div class="modern-card" style="text-align: center; padding: 3rem;">
                    <h2>🏁 Commencez votre voyage!</h2>
                    <p style="font-size: 1.2rem; margin: 2rem 0;">
                        Aucune donnée pour le moment.<br>
                        Complétez votre première séance pour voir vos progrès ici!
                    </p>
                    <div style="font-size: 5rem; margin: 2rem 0;">📊</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        return
    
    # Préparation des données
    df = pd.DataFrame(st.session_state.workout_history)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['exercice'] != 'Commentaire séance']
    
    # Vue d'ensemble avec KPIs visuels
    st.markdown("### 🎯 Vue d'Ensemble")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    # Calcul des métriques avancées
    total_seances = df['date'].dt.date.nunique()
    total_volume = (df['poids'] * df['reps']).sum() if 'poids' in df.columns and 'reps' in df.columns else 0
    avg_rpe = df['rpe'].mean() if 'rpe' in df.columns else 0
    current_streak = calculate_streak(st.session_state.workout_history)
    consistency = (total_seances / ((datetime.now() - df['date'].min()).days + 1) * 100) if not df.empty else 0
    
    # Dernière performance vs première
    if len(df) > 10:
        recent_avg_rpe = df.tail(10)['rpe'].mean() if 'rpe' in df.columns else 0
        old_avg_rpe = df.head(10)['rpe'].mean() if 'rpe' in df.columns else 0
        rpe_evolution = ((recent_avg_rpe - old_avg_rpe) / old_avg_rpe * 100) if old_avg_rpe > 0 else 0
    else:
        rpe_evolution = 0
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color: #667eea;">🏋️</div>
                <div style="font-size: 1.8rem; font-weight: bold;">{total_seances}</div>
                <div style="font-size: 0.8rem; color: #666;">Séances</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color: #ff6b6b;">🔥</div>
                <div style="font-size: 1.8rem; font-weight: bold;">{current_streak}</div>
                <div style="font-size: 0.8rem; color: #666;">Série actuelle</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color: #4CAF50;">💪</div>
                <div style="font-size: 1.8rem; font-weight: bold;">{total_volume/1000:.1f}t</div>
                <div style="font-size: 0.8rem; color: #666;">Volume total</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color: #FFC107;">⚡</div>
                <div style="font-size: 1.8rem; font-weight: bold;">{avg_rpe:.1f}</div>
                <div style="font-size: 0.8rem; color: #666;">RPE moyen</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col5:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color: #9C27B0;">📅</div>
                <div style="font-size: 1.8rem; font-weight: bold;">{consistency:.0f}%</div>
                <div style="font-size: 0.8rem; color: #666;">Régularité</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col6:
        evolution_color = "#4CAF50" if rpe_evolution > 0 else "#ff6b6b"
        evolution_icon = "📈" if rpe_evolution > 0 else "📉"
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color: {evolution_color};">{evolution_icon}</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: {evolution_color};">
                    {rpe_evolution:+.0f}%
                </div>
                <div style="font-size: 0.8rem; color: #666;">Évolution RPE</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Graphique principal interactif
    st.markdown("### 📊 Analyse Temporelle")
    
    # Sélecteur de métrique
    metric_choice = st.selectbox(
        "Choisir la métrique à analyser",
        ["Volume par séance", "Charge maximale", "RPE moyen", "Nombre d'exercices"],
        label_visibility="collapsed"
    )
    
    # Préparation des données selon la métrique
    if metric_choice == "Volume par séance":
        daily_data = df.groupby(df['date'].dt.date).apply(
            lambda x: (x['poids'] * x['reps']).sum() if 'poids' in x.columns and 'reps' in x.columns else 0
        ).reset_index()
        daily_data.columns = ['date', 'value']
        y_title = "Volume (kg)"
        color = "#667eea"
    elif metric_choice == "Charge maximale":
        daily_data = df.groupby(df['date'].dt.date)['poids'].max().reset_index()
        daily_data.columns = ['date', 'value']
        y_title = "Charge max (kg)"
        color = "#ff6b6b"
    elif metric_choice == "RPE moyen":
        daily_data = df.groupby(df['date'].dt.date)['rpe'].mean().reset_index()
        daily_data.columns = ['date', 'value']
        y_title = "RPE moyen"
        color = "#FFC107"
    else:
        daily_data = df.groupby(df['date'].dt.date).size().reset_index()
        daily_data.columns = ['date', 'value']
        y_title = "Nombre d'exercices"
        color = "#4CAF50"
    
    # Graphique principal avec tendance
    fig_main = go.Figure()
    
    # Données principales
    fig_main.add_trace(go.Scatter(
        x=daily_data['date'],
        y=daily_data['value'],
        mode='lines+markers',
        name=metric_choice,
        line=dict(color=color, width=3),
        marker=dict(size=8, color=color),
        hovertemplate='<b>Date:</b> %{x}<br><b>Valeur:</b> %{y:.1f}<extra></extra>'
    ))
    
    # Ajout de la tendance (moyenne mobile)
    if len(daily_data) > 7:
        daily_data['trend'] = daily_data['value'].rolling(window=7, center=True).mean()
        fig_main.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['trend'],
            mode='lines',
            name='Tendance (7j)',
            line=dict(color='rgba(0,0,0,0.3)', width=2, dash='dash'),
            hovertemplate='<b>Tendance:</b> %{y:.1f}<extra></extra>'
        ))
    
    # Mise en forme du graphique
    fig_main.update_layout(
        title={
            'text': f"<b>{metric_choice}</b> - Évolution Temporelle",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Date",
        yaxis_title=y_title,
        hovermode='x unified',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            rangeslider=dict(visible=True)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            zeroline=False
        )
    )
    
    st.plotly_chart(fig_main, use_container_width=True)
    
    # Tabs d'analyse détaillée
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Par Exercice", 
        "📊 Comparaisons", 
        "🔥 Heatmap", 
        "💪 Records",
        "📈 Prédictions"
    ])
    
    with tab1:
        st.markdown("#### 🎯 Analyse Détaillée par Exercice")
        
        # Sélection d'exercice avec preview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            exercices_uniques = df['exercice'].unique()
            exercice_selectionne = st.selectbox(
                "Sélectionner un exercice",
                exercices_uniques,
                format_func=lambda x: f"💪 {x}"
            )
        
        with col2:
            # Mini stats de l'exercice
            df_ex = df[df['exercice'] == exercice_selectionne]
            if not df_ex.empty and 'poids' in df_ex.columns:
                max_weight = df_ex['poids'].max()
                total_sets = len(df_ex)
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div style="font-size: 1.2rem;">🏋️ Max: {max_weight}kg</div>
                        <div style="font-size: 0.9rem; color: #666;">📊 {total_sets} séries</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        if not df_ex.empty:
            # Graphique évolution de l'exercice
            fig_ex = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Évolution de la Charge', 'Distribution RPE', 
                              'Volume par Séance', 'Progression Relative'),
                specs=[[{"type": "scatter"}, {"type": "bar"}],
                      [{"type": "scatter"}, {"type": "scatter"}]]
            )
            
            # 1. Évolution charge
            if 'poids' in df_ex.columns:
                charge_evolution = df_ex.groupby('date')['poids'].max().reset_index()
                fig_ex.add_trace(
                    go.Scatter(
                        x=charge_evolution['date'],
                        y=charge_evolution['poids'],
                        mode='lines+markers',
                        name='Charge Max',
                        line=dict(color='#667eea', width=2),
                        marker=dict(size=8)
                    ),
                    row=1, col=1
                )
            
            # 2. Distribution RPE
            if 'rpe' in df_ex.columns:
                rpe_dist = df_ex['rpe'].value_counts().sort_index()
                fig_ex.add_trace(
                    go.Bar(
                        x=rpe_dist.index,
                        y=rpe_dist.values,
                        name='Fréquence RPE',
                        marker=dict(
                            color=rpe_dist.index,
                            colorscale='RdYlGn_r',
                            showscale=False
                        )
                    ),
                    row=1, col=2
                )
            
            # 3. Volume par séance
            if 'poids' in df_ex.columns and 'reps' in df_ex.columns:
                volume_seance = df_ex.groupby('date').apply(
                    lambda x: (x['poids'] * x['reps']).sum()
                ).reset_index()
                volume_seance.columns = ['date', 'volume']
                
                fig_ex.add_trace(
                    go.Scatter(
                        x=volume_seance['date'],
                        y=volume_seance['volume'],
                        mode='lines+markers',
                        name='Volume',
                        line=dict(color='#4CAF50', width=2),
                        fill='tozeroy',
                        fillcolor='rgba(76, 175, 80, 0.2)'
                    ),
                    row=2, col=1
                )
            
            # 4. Progression relative
            if 'poids' in df_ex.columns and len(df_ex) > 1:
                first_weight = df_ex.iloc[0]['poids']
                df_ex['progression'] = ((df_ex['poids'] - first_weight) / first_weight * 100)
                
                fig_ex.add_trace(
                    go.Scatter(
                        x=df_ex['date'],
                        y=df_ex['progression'],
                        mode='lines+markers',
                        name='Progression %',
                        line=dict(color='#ff6b6b', width=2),
                        marker=dict(size=6)
                    ),
                    row=2, col=2
                )
            
            # Mise en forme
            fig_ex.update_layout(height=600, showlegend=False)
            fig_ex.update_xaxes(showgrid=False)
            fig_ex.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.1)')
            
            st.plotly_chart(fig_ex, use_container_width=True)
            
            # Statistiques détaillées
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'poids' in df_ex.columns:
                    poids_debut = df_ex.iloc[0]['poids']
                    poids_actuel = df_ex.iloc[-1]['poids']
                    progression_totale = ((poids_actuel - poids_debut) / poids_debut * 100) if poids_debut > 0 else 0
                    
                    st.markdown(
                        f"""
                        <div class="modern-card">
                            <h4>📈 Progression Totale</h4>
                            <p style="font-size: 2rem; font-weight: bold; color: {'#4CAF50' if progression_totale > 0 else '#ff6b6b'};">
                                {progression_totale:+.1f}%
                            </p>
                            <p style="color: #666;">De {poids_debut}kg à {poids_actuel}kg</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with col2:
                if 'rpe' in df_ex.columns:
                    rpe_moyen = df_ex['rpe'].mean()
                    rpe_recent = df_ex.tail(5)['rpe'].mean() if len(df_ex) > 5 else rpe_moyen
                    
                    st.markdown(
                        f"""
                        <div class="modern-card">
                            <h4>💪 Intensité Moyenne</h4>
                            <p style="font-size: 2rem; font-weight: bold; color: #FFC107;">
                                {rpe_moyen:.1f}/10
                            </p>
                            <p style="color: #666;">Récent: {rpe_recent:.1f}/10</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with col3:
                frequence = len(df_ex) / ((df_ex['date'].max() - df_ex['date'].min()).days + 1) * 7
                
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <h4>📅 Fréquence</h4>
                        <p style="font-size: 2rem; font-weight: bold; color: #9C27B0;">
                            {frequence:.1f}
                        </p>
                        <p style="color: #666;">fois/semaine</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with tab2:
        st.markdown("#### 📊 Comparaisons entre Exercices")
        
        # Sélection multiple d'exercices
        exercices_comparer = st.multiselect(
            "Sélectionner les exercices à comparer",
            df['exercice'].unique(),
            default=df['exercice'].value_counts().head(3).index.tolist()
        )
        
        if len(exercices_comparer) >= 2:
            # Graphique de comparaison
            fig_comp = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Charge Maximale', 'Volume Total'),
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Données pour comparaison
            comparison_data = []
            for ex in exercices_comparer:
                df_comp = df[df['exercice'] == ex]
                if 'poids' in df_comp.columns:
                    max_charge = df_comp['poids'].max()
                    total_volume = (df_comp['poids'] * df_comp['reps']).sum() if 'reps' in df_comp.columns else 0
                    comparison_data.append({
                        'exercice': ex,
                        'charge_max': max_charge,
                        'volume_total': total_volume
                    })
            
            df_comparison = pd.DataFrame(comparison_data)
            
            # Graphique charges max
            fig_comp.add_trace(
                go.Bar(
                    x=df_comparison['exercice'],
                    y=df_comparison['charge_max'],
                    name='Charge Max',
                    marker=dict(color='#667eea')
                ),
                row=1, col=1
            )
            
            # Graphique volume total
            fig_comp.add_trace(
                go.Bar(
                    x=df_comparison['exercice'],
                    y=df_comparison['volume_total'],
                    name='Volume Total',
                    marker=dict(color='#4CAF50')
                ),
                row=1, col=2
            )
            
            fig_comp.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Radar chart de comparaison
            if 'rpe' in df.columns:
                st.markdown("##### 🎯 Profil de Performance")
                
                categories = ['Charge Max (%)', 'Volume (%)', 'RPE Moyen', 'Fréquence', 'Progression']
                
                fig_radar = go.Figure()
                
                for ex in exercices_comparer[:3]:  # Limiter à 3 pour la lisibilité
                    df_ex = df[df['exercice'] == ex]
                    
                    # Normalisation des valeurs (0-100)
                    charge_norm = (df_ex['poids'].max() / df['poids'].max() * 100) if 'poids' in df.columns else 0
                    volume_norm = ((df_ex['poids'] * df_ex['reps']).sum() / (df['poids'] * df['reps']).sum() * 100) if all(col in df.columns for col in ['poids', 'reps']) else 0
                    rpe_norm = (df_ex['rpe'].mean() / 10 * 100) if 'rpe' in df_ex.columns else 0
                    freq_norm = (len(df_ex) / len(df) * 100)
                    
                    if len(df_ex) > 1 and 'poids' in df_ex.columns:
                        prog = ((df_ex.iloc[-1]['poids'] - df_ex.iloc[0]['poids']) / df_ex.iloc[0]['poids'] * 100)
                        prog_norm = min(100, max(0, prog + 50))  # Centrer autour de 50
                    else:
                        prog_norm = 50
                    
                    values = [charge_norm, volume_norm, rpe_norm, freq_norm, prog_norm]
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name=ex[:20] + '...' if len(ex) > 20 else ex
                    ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True,
                    height=400
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab3:
        st.markdown("#### 🔥 Carte d'Activité")
        
        # Préparer les données pour la heatmap
        df['day_of_week'] = df['date'].dt.day_name()
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['year'] = df['date'].dt.year
        
        # Grouper par jour et semaine
        activity_data = df.groupby(['year', 'week_of_year', 'day_of_week']).size().reset_index(name='count')
        
        # Ordonner les jours
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        activity_data['day_order'] = activity_data['day_of_week'].map({day: i for i, day in enumerate(days_order)})
        activity_data = activity_data.sort_values(['year', 'week_of_year', 'day_order'])
        
        # Créer la heatmap style GitHub
        if not activity_data.empty:
            # Pivot pour créer la matrice
            pivot_data = activity_data.pivot_table(
                index='day_of_week',
                columns=['year', 'week_of_year'],
                values='count',
                fill_value=0
            )
            
            # Réordonner les lignes
            pivot_data = pivot_data.reindex(days_order)
            
            # Créer la heatmap
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=pivot_data.values,
                x=[f"S{week}" for year, week in pivot_data.columns],
                y=pivot_data.index,
                colorscale=[
                    [0, '#ebedf0'],
                    [0.25, '#c6e48b'],
                    [0.5, '#7bc96f'],
                    [0.75, '#239a3b'],
                    [1, '#196127']
                ],
                showscale=True,
                colorbar=dict(
                    title="Exercices",
                    titleside="right"
                )
            ))
            
            fig_heatmap.update_layout(
                title="Calendrier d'Activité",
                xaxis_title="Semaines",
                yaxis_title="Jours",
                height=400,
                xaxis=dict(
                    tickmode='linear',
                    tick0=0,
                    dtick=4  # Afficher une semaine sur 4
                )
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Statistiques d'activité
            col1, col2, col3 = st.columns(3)
            
            with col1:
                most_active_day = df['day_of_week'].value_counts().index[0]
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div>📅 Jour le plus actif</div>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">
                            {most_active_day}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                avg_per_week = df.groupby(['year', 'week_of_year']).size().mean()
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div>📊 Moyenne/semaine</div>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #4CAF50;">
                            {avg_per_week:.1f} séances
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col3:
                longest_streak = calculate_longest_streak(st.session_state.workout_history)
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div>🔥 Plus longue série</div>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #ff6b6b;">
                            {longest_streak} jours
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with tab4:
        st.markdown("#### 💪 Records Personnels")
        
        # Identifier les records
        records = []
        
        for exercice in df['exercice'].unique():
            df_ex = df[df['exercice'] == exercice]
            
            if 'poids' in df_ex.columns and not df_ex['poids'].isna().all():
                # Record de charge
                max_idx = df_ex['poids'].idxmax()
                max_record = df_ex.loc[max_idx]
                
                records.append({
                    'type': '🏋️ Charge Max',
                    'exercice': exercice,
                    'valeur': f"{max_record['poids']}kg",
                    'date': max_record['date'].strftime('%d/%m/%Y'),
                    'note': max_record.get('note', ''),
                    'category': 'charge'
                })
            
            if all(col in df_ex.columns for col in ['poids', 'reps']):
                # Record de volume
                df_ex['volume'] = df_ex['poids'] * df_ex['reps']
                max_vol_idx = df_ex['volume'].idxmax()
                max_vol_record = df_ex.loc[max_vol_idx]
                
                records.append({
                    'type': '📊 Volume Max',
                    'exercice': exercice,
                    'valeur': f"{max_vol_record['volume']:.0f}kg",
                    'date': max_vol_record['date'].strftime('%d/%m/%Y'),
                    'note': f"{max_vol_record['poids']}kg × {max_vol_record['reps']} reps",
                    'category': 'volume'
                })
        
        # Afficher les records par catégorie
        if records:
            # Trier par catégorie et valeur
            df_records = pd.DataFrame(records)
            
            # Records de charge
            st.markdown("##### 🏋️ Records de Charge")
            charge_records = df_records[df_records['category'] == 'charge'].sort_values('valeur', ascending=False)
            
            for _, record in charge_records.head(5).iterrows():
                st.markdown(
                    f"""
                    <div class="modern-card" style="margin: 0.5rem 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>{record['exercice']}</strong><br>
                                <span style="font-size: 1.5rem; color: #667eea; font-weight: bold;">
                                    {record['valeur']}
                                </span>
                            </div>
                            <div style="text-align: right; color: #666;">
                                <small>{record['date']}</small><br>
                                <small>{record['note']}</small>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Records de volume
            st.markdown("##### 📊 Records de Volume")
            volume_records = df_records[df_records['category'] == 'volume'].sort_values('valeur', ascending=False)
            
            for _, record in volume_records.head(5).iterrows():
                st.markdown(
                    f"""
                    <div class="modern-card" style="margin: 0.5rem 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>{record['exercice']}</strong><br>
                                <span style="font-size: 1.5rem; color: #4CAF50; font-weight: bold;">
                                    {record['valeur']}
                                </span>
                            </div>
                            <div style="text-align: right; color: #666;">
                                <small>{record['date']}</small><br>
                                <small>{record['note']}</small>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Timeline des records
            st.markdown("##### 📈 Timeline des Records")
            
            # Préparer les données pour la timeline
            timeline_data = []
            for _, record in df_records.iterrows():
                timeline_data.append({
                    'date': pd.to_datetime(record['date'], format='%d/%m/%Y'),
                    'event': f"{record['type']} - {record['exercice']}: {record['valeur']}",
                    'category': record['category']
                })
            
            df_timeline = pd.DataFrame(timeline_data).sort_values('date')
            
            # Graphique timeline
            fig_timeline = go.Figure()
            
            colors = {'charge': '#667eea', 'volume': '#4CAF50'}
            
            for category in df_timeline['category'].unique():
                df_cat = df_timeline[df_timeline['category'] == category]
                
                fig_timeline.add_trace(go.Scatter(
                    x=df_cat['date'],
                    y=[category] * len(df_cat),
                    mode='markers+text',
                    name=category,
                    marker=dict(
                        size=12,
                        color=colors.get(category, '#666'),
                        symbol='star'
                    ),
                    text=df_cat['event'],
                    textposition='top center',
                    textfont=dict(size=10),
                    hovertemplate='<b>%{text}</b><br>Date: %{x}<extra></extra>'
                ))
            
            fig_timeline.update_layout(
                title="Chronologie des Records",
                xaxis_title="Date",
                yaxis=dict(
                    ticktext=['Charge', 'Volume'],
                    tickvals=['charge', 'volume']
                ),
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    with tab5:
        st.markdown("#### 📈 Prédictions et Objectifs")
        
        # Sélection de l'exercice pour prédiction
        exercice_prediction = st.selectbox(
            "Exercice pour prédiction",
            df['exercice'].unique(),
            key="pred_exercise"
        )
        
        df_pred = df[df['exercice'] == exercice_prediction]
        
        if len(df_pred) >= 3 and 'poids' in df_pred.columns:
            # Préparer les données
            charge_evolution = df_pred.groupby('date')['poids'].max().reset_index()
            charge_evolution['days_since_start'] = (charge_evolution['date'] - charge_evolution['date'].min()).dt.days
            
            # Régression linéaire simple
            from sklearn.linear_model import LinearRegression
            
            X = charge_evolution['days_since_start'].values.reshape(-1, 1)
            y = charge_evolution['poids'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Prédictions futures
            future_days = np.array([30, 60, 90]) + charge_evolution['days_since_start'].max()
            future_dates = [charge_evolution['date'].max() + timedelta(days=int(d)) for d in [30, 60, 90]]
            future_predictions = model.predict(future_days.reshape(-1, 1))
            
            # Graphique avec prédictions
            fig_pred = go.Figure()
            
            # Données historiques
            fig_pred.add_trace(go.Scatter(
                x=charge_evolution['date'],
                y=charge_evolution['poids'],
                mode='lines+markers',
                name='Historique',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            # Ligne de tendance
            trend_line = model.predict(X)
            fig_pred.add_trace(go.Scatter(
                x=charge_evolution['date'],
                y=trend_line,
                mode='lines',
                name='Tendance',
                line=dict(color='rgba(0,0,0,0.3)', width=2, dash='dash')
            ))
            
            # Prédictions
            fig_pred.add_trace(go.Scatter(
                x=future_dates,
                y=future_predictions,
                mode='markers+text',
                name='Prédictions',
                marker=dict(size=12, color='#ff6b6b', symbol='star'),
                text=[f"{pred:.1f}kg" for pred in future_predictions],
                textposition='top center'
            ))
            
            # Zone de confiance (simplifiée)
            confidence = 0.1  # 10% d'incertitude
            upper_bound = future_predictions * (1 + confidence)
            lower_bound = future_predictions * (1 - confidence)
            
            fig_pred.add_trace(go.Scatter(
                x=future_dates + future_dates[::-1],
                y=list(upper_bound) + list(lower_bound[::-1]),
                fill='toself',
                fillcolor='rgba(255, 107, 107, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False,
                name='Zone de confiance'
            ))
            
            fig_pred.update_layout(
                title=f"Prédiction de Progression - {exercice_prediction}",
                xaxis_title="Date",
                yaxis_title="Charge (kg)",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_pred, use_container_width=True)
            
            # Objectifs SMART
            st.markdown("##### 🎯 Objectifs SMART Suggérés")
            
            current_max = charge_evolution['poids'].max()
            progression_rate = (future_predictions[0] - current_max) / 30  # kg par jour
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <h4>🎯 Court terme (30j)</h4>
                        <p style="font-size: 1.5rem; font-weight: bold; color: #4CAF50;">
                            {future_predictions[0]:.1f}kg
                        </p>
                        <p style="color: #666;">
                            +{future_predictions[0] - current_max:.1f}kg<br>
                            ({(future_predictions[0] - current_max) / current_max * 100:.1f}%)
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <h4>🎯 Moyen terme (60j)</h4>
                        <p style="font-size: 1.5rem; font-weight: bold; color: #FFC107;">
                            {future_predictions[1]:.1f}kg
                        </p>
                        <p style="color: #666;">
                            +{future_predictions[1] - current_max:.1f}kg<br>
                            ({(future_predictions[1] - current_max) / current_max * 100:.1f}%)
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <h4>🎯 Long terme (90j)</h4>
                        <p style="font-size: 1.5rem; font-weight: bold; color: #ff6b6b;">
                            {future_predictions[2]:.1f}kg
                        </p>
                        <p style="color: #666;">
                            +{future_predictions[2] - current_max:.1f}kg<br>
                            ({(future_predictions[2] - current_max) / current_max * 100:.1f}%)
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Plan d'action
            st.markdown("##### 📋 Plan d'Action Recommandé")
            
            if progression_rate > 0:
                weekly_increase = progression_rate * 7
                st.info(f"""
                **Pour atteindre vos objectifs :**
                - 📈 Augmentation hebdomadaire cible : +{weekly_increase:.1f}kg
                - 🏋️ Maintenir une fréquence de 2-3x/semaine minimum
                - 💪 RPE cible : 7-8/10 sur les séries principales
                - 🍎 Assurer un surplus calorique de 300-500 kcal/jour
                - 😴 Prioriser 8h de sommeil pour la récupération
                """)
            else:
                st.warning("""
                **Attention:** La tendance actuelle est négative ou stagnante.
                Recommandations:
                - Vérifier la récupération et la nutrition
                - Considérer une phase de deload
                - Ajuster le volume ou l'intensité
                """)
        else:
            st.info("Pas assez de données pour établir des prédictions fiables. Continuez à vous entraîner!")
    
    # Export des données avec options avancées
    st.markdown("---")
    with st.expander("📥 Export Avancé des Données"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            format_export = st.selectbox(
                "Format d'export",
                ["CSV détaillé", "JSON complet", "Excel avec graphiques", "PDF rapport"]
            )
        
        with col2:
            periode_export = st.selectbox(
                "Période",
                ["Tout", "30 derniers jours", "Phase actuelle", "Personnalisé"]
            )
        
        with col3:
            if periode_export == "Personnalisé":
                date_debut = st.date_input("Du", value=df['date'].min().date())
                date_fin = st.date_input("Au", value=df['date'].max().date())
        
        # Bouton d'export avec style
        if st.button("📥 Générer l'Export", type="primary", use_container_width=True):
            # Logique d'export selon le format
            # (Implémentation simplifiée pour l'exemple)
            
            if format_export == "CSV détaillé":
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Télécharger CSV",
                    data=csv,
                    file_name=f"rehab_lca_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            st.success("✅ Export généré avec succès!")

def calculate_longest_streak(workout_history: List[Dict]) -> int:
    """Calcule la plus longue série de jours consécutifs"""
    if not workout_history:
        return 0
    
    dates = sorted(set([w['date'].date() for w in workout_history]))
    
    max_streak = 1
    current_streak = 1
    
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    
    return max_streak

def show_nutrition_guide():
    """Guide nutritionnel personnalisé selon la phase"""
    st.header("🍎 Guide Nutritionnel Personnalisé")
    
    # Phase actuelle
    phase, phase_name, emoji = st.session_state.program.get_current_phase()
    nutrition_tips = st.session_state.program.get_nutrition_for_phase(phase)
    
    # En-tête avec phase
    st.markdown(
        f"""
        <div class="phase-card">
            <h3>{emoji} Recommandations pour: {phase_name}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Calculateur de besoins
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🧮 Vos Besoins")
        
        # Calculs personnalisés
        poids = st.session_state.program.patient_weight
        taille = st.session_state.program.patient_height
        
        # Métabolisme de base (Mifflin-St Jeor)
        bmr = 10 * poids + 6.25 * taille - 5 * 25 + 5  # Homme, 25 ans estimé
        
        # Facteur d'activité selon la phase
        activity_factors = {
            "pre_op": 1.6,
            "post_op_early": 1.3,
            "rehab": 1.5
        }
        
        factor = activity_factors.get(
            "pre_op" if "pre_op" in phase else "post_op_early" if any(x in phase for x in ["semaine_1", "semaine_2-3", "semaine_4-6"]) else "rehab",
            1.4
        )
        
        tdee = bmr * factor
        
        st.markdown(
            f"""
            <div class="metric-card">
                <div>⚡ Métabolisme</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{bmr:.0f} kcal</div>
                <div style="font-size: 0.8rem; color: #666;">BMR</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div class="metric-card">
                <div>🔥 Dépense totale</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{tdee:.0f} kcal</div>
                <div style="font-size: 0.8rem; color: #666;">TDEE</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Recommandation calorique
        calorie_rec = nutrition_tips['calories']
        if "surplus" in calorie_rec:
            target_calories = tdee + 300
        else:
            target_calories = tdee
        
        st.markdown(
            f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #d4edda 0%, #a8e6cf 100%);">
                <div>🎯 Objectif</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{target_calories:.0f} kcal</div>
                <div style="font-size: 0.8rem; color: #666;">{calorie_rec}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("### 📊 Répartition Macronutriments")
        
        # Calcul des macros
        proteines_g = poids * 2  # 2g/kg
        lipides_g = poids * 1    # 1g/kg
        glucides_g = (target_calories - (proteines_g * 4 + lipides_g * 9)) / 4
        
        # Graphique donut des macros
        fig_macros = go.Figure(data=[go.Pie(
            labels=['Protéines', 'Glucides', 'Lipides'],
            values=[proteines_g * 4, glucides_g * 4, lipides_g * 9],
            hole=.4,
            marker=dict(colors=['#ff6b6b', '#4CAF50', '#FFC107'])
        )])
        
        fig_macros.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>%{value:.0f} kcal<br>%{percent}<extra></extra>'
        )
        
        fig_macros.update_layout(
            height=300,
            showlegend=False,
            annotations=[dict(text=f'{target_calories:.0f}<br>kcal', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        st.plotly_chart(fig_macros, use_container_width=True)
        
        # Détails des macros
        col_p, col_g, col_l = st.columns(3)
        
        with col_p:
            st.markdown(
                f"""
                <div class="modern-card" style="border-left: 4px solid #ff6b6b;">
                    <h4>🥩 Protéines</h4>
                    <p style="font-size: 1.5rem; font-weight: bold;">{proteines_g:.0f}g</p>
                    <p style="color: #666; font-size: 0.9rem;">{nutrition_tips['proteines']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col_g:
            st.markdown(
                f"""
                <div class="modern-card" style="border-left: 4px solid #4CAF50;">
                    <h4>🌾 Glucides</h4>
                    <p style="font-size: 1.5rem; font-weight: bold;">{glucides_g:.0f}g</p>
                    <p style="color: #666; font-size: 0.9rem;">{nutrition_tips['glucides']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col_l:
            st.markdown(
                f"""
                <div class="modern-card" style="border-left: 4px solid #FFC107;">
                    <h4>🥑 Lipides</h4>
                    <p style="font-size: 1.5rem; font-weight: bold;">{lipides_g:.0f}g</p>
                    <p style="color: #666; font-size: 0.9rem;">{nutrition_tips['lipides']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Timing nutritionnel
    st.markdown("### ⏰ Timing Nutritionnel Optimal")
    
    timing_tabs = st.tabs(["🌅 Jour d'entraînement", "😴 Jour de repos", "💊 Supplémentation"])
    
    with timing_tabs[0]:
        st.markdown(
            """
            <div class="modern-card">
                <h4>🕐 Pré-entraînement (1-2h avant)</h4>
                <ul>
                    <li>Glucides complexes: 40-60g (avoine, riz, patate douce)</li>
                    <li>Protéines maigres: 20-30g (poulet, poisson, whey)</li>
                    <li>Lipides: minimal (5-10g max)</li>
                    <li>Hydratation: 500-750ml d'eau</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="modern-card">
                <h4>🏋️ Post-entraînement (0-30min)</h4>
                <ul>
                    <li>Protéines rapides: 30-40g (whey, isolat)</li>
                    <li>Glucides simples: 40-80g selon intensité</li>
                    <li>Créatine: 5g (si utilisée)</li>
                    <li>Hydratation: 750-1000ml</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="modern-card">
                <h4>🍽️ Repas post-entraînement (1-2h après)</h4>
                <ul>
                    <li>Repas complet équilibré</li>
                    <li>Protéines: 30-40g</li>
                    <li>Glucides complexes: 60-100g</li>
                    <li>Légumes variés: 200-300g</li>
                    <li>Lipides sains: 15-20g</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with timing_tabs[1]:
        st.markdown(
            """
            <div class="modern-card">
                <h4>🌄 Petit-déjeuner</h4>
                <ul>
                    <li>Protéines: 25-35g (œufs, yaourt grec, fromage blanc)</li>
                    <li>Glucides modérés: 40-60g</li>
                    <li>Lipides: 15-20g (avocat, noix, huile d'olive)</li>
                    <li>Fibres: fruits et/ou légumes</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="modern-card">
                <h4>🥗 Déjeuner & Dîner</h4>
                <ul>
                    <li>Répartition équilibrée des macros</li>
                    <li>Focus sur aliments complets non transformés</li>
                    <li>Légumes = 50% de l'assiette</li>
                    <li>Hydratation continue</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with timing_tabs[2]:
        st.markdown("#### 💊 Suppléments Recommandés par Phase")
        
        # Suppléments avec dosages
        supplements_detail = {
            "Vitamine D": {"dose": "2000-4000 UI/jour", "timing": "Avec repas gras", "benefices": "Fonction musculaire, immunité"},
            "Omega-3": {"dose": "2-3g EPA/DHA", "timing": "Avec repas", "benefices": "Anti-inflammatoire, récupération"},
            "Créatine": {"dose": "5g/jour", "timing": "Post-entraînement", "benefices": "Force, puissance, récupération"},
            "Collagène": {"dose": "10-20g/jour", "timing": "À jeun ou soir", "benefices": "Tissus conjonctifs, tendons"},
            "Vitamine C": {"dose": "1000mg/jour", "timing": "Matin", "benefices": "Synthèse collagène, antioxydant"},
            "Zinc": {"dose": "15-30mg/jour", "timing": "À jeun", "benefices": "Cicatrisation, immunité"},
            "Magnésium": {"dose": "300-400mg/jour", "timing": "Soir", "benefices": "Relaxation musculaire, sommeil"},
            "Glucosamine": {"dose": "1500mg/jour", "timing": "Avec repas", "benefices": "Santé articulaire"},
            "BCAA": {"dose": "10-15g/jour", "timing": "Pendant entraînement", "benefices": "Préservation masse musculaire"}
        }
        
        for supp in nutrition_tips['supplements']:
            if supp in supplements_detail:
                detail = supplements_detail[supp]
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <h5>💊 {supp}</h5>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div>
                                <strong>Dosage:</strong> {detail['dose']}<br>
                                <strong>Timing:</strong> {detail['timing']}
                            </div>
                            <div>
                                <strong>Bénéfices:</strong><br>
                                <small>{detail['benefices']}</small>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Aliments clés avec visualisation
    st.markdown("### 🥗 Aliments Clés pour votre Phase")
    
    cols = st.columns(3)
    for i, aliment in enumerate(nutrition_tips['aliments_cles']):
        with cols[i % 3]:
            # Émojis pour chaque aliment
            food_emojis = {
                "Saumon": "🐟", "Œufs": "🥚", "Avoine": "🌾", "Patate douce": "🍠",
                "Épinards": "🥬", "Baies": "🫐", "Poulet": "🍗", "Quinoa": "🌾",
                "Brocoli": "🥦", "Agrumes": "🍊", "Noix": "🥜", "Yaourt grec": "🥛",
                "Bœuf maigre": "🥩", "Riz complet": "🍚", "Lentilles": "🫘",
                "Avocat": "🥑", "Banane": "🍌", "Amandes": "🌰"
            }
            
            emoji = food_emojis.get(aliment, "🍽️")
            
            st.markdown(
                f"""
                <div class="modern-card" style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem;">{emoji}</div>
                    <div style="font-weight: bold; margin-top: 0.5rem;">{aliment}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Plan de repas exemple
    st.markdown("### 📅 Exemple de Journée Type")
    
    meal_plan = {
        "Petit-déjeuner (7h)": {
            "plat": "Bowl protéiné",
            "composition": ["3 œufs brouillés", "100g flocons d'avoine", "1 banane", "30g amandes"],
            "macros": {"calories": 650, "proteines": 35, "glucides": 75, "lipides": 20}
        },
        "Collation (10h)": {
            "plat": "Shake post-entraînement",
            "composition": ["30g whey", "1 pomme", "200ml lait d'amande"],
            "macros": {"calories": 250, "proteines": 30, "glucides": 25, "lipides": 3}
        },
        "Déjeuner (13h)": {
            "plat": "Assiette équilibrée",
            "composition": ["150g poulet grillé", "200g riz basmati", "Salade verte", "1 cs huile d'olive"],
            "macros": {"calories": 600, "proteines": 40, "glucides": 70, "lipides": 15}
        },
        "Collation (16h)": {
            "plat": "Snack protéiné",
            "composition": ["200g fromage blanc 0%", "30g fruits secs", "Cannelle"],
            "macros": {"calories": 200, "proteines": 20, "glucides": 20, "lipides": 5}
        },
        "Dîner (19h)": {
            "plat": "Repas récupération",
            "composition": ["200g saumon", "300g patate douce", "Brocolis vapeur", "Salade"],
            "macros": {"calories": 550, "proteines": 45, "glucides": 60, "lipides": 15}
        },
        "Soir (22h)": {
            "plat": "Collation nuit",
            "composition": ["30g caséine", "20g beurre d'amande"],
            "macros": {"calories": 250, "proteines": 25, "glucides": 10, "lipides": 12}
        }
    }
    
    total_macros = {
        "calories": sum(meal['macros']['calories'] for meal in meal_plan.values()),
        "proteines": sum(meal['macros']['proteines'] for meal in meal_plan.values()),
        "glucides": sum(meal['macros']['glucides'] for meal in meal_plan.values()),
        "lipides": sum(meal['macros']['lipides'] for meal in meal_plan.values())
    }
    
    # Timeline des repas
    fig_timeline = go.Figure()
    
    times = list(meal_plan.keys())
    calories = [meal['macros']['calories'] for meal in meal_plan.values()]
    
    fig_timeline.add_trace(go.Bar(
        x=times,
        y=calories,
        marker=dict(
            color=calories,
            colorscale='Viridis',
            showscale=False
        ),
        text=[f"{cal} kcal" for cal in calories],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Calories: %{y} kcal<extra></extra>'
    ))
    
    fig_timeline.update_layout(
        title="Répartition Calorique Journalière",
        xaxis_title="Repas",
        yaxis_title="Calories",
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Détails des repas en accordéon
    for meal_time, meal_data in meal_plan.items():
        with st.expander(f"🍽️ {meal_time} - {meal_data['plat']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**Composition:**")
                for item in meal_data['composition']:
                    st.write(f"• {item}")
            
            with col2:
                st.markdown("**Macros:**")
                st.write(f"🔥 {meal_data['macros']['calories']} kcal")
                st.write(f"🥩 {meal_data['macros']['proteines']}g protéines")
                st.write(f"🌾 {meal_data['macros']['glucides']}g glucides")
                st.write(f"🥑 {meal_data['macros']['lipides']}g lipides")
    
    # Résumé total
    st.markdown(
        f"""
        <div class="modern-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h3 style="margin: 0;">📊 Total Journalier</h3>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold;">{total_macros['calories']}</div>
                    <div>Calories</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold;">{total_macros['proteines']}g</div>
                    <div>Protéines</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold;">{total_macros['glucides']}g</div>
                    <div>Glucides</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold;">{total_macros['lipides']}g</div>
                    <div>Lipides</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Conseils d'hydratation
    st.markdown("### 💧 Hydratation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class="modern-card">
                <h4>💧 Besoins Quotidiens</h4>
                <p style="font-size: 1.5rem; font-weight: bold; color: #2196F3;">
                    {nutrition_tips['hydratation']}
                </p>
                <ul>
                    <li>Au réveil: 500ml</li>
                    <li>Avant repas: 250ml</li>
                    <li>Pendant entraînement: 750ml/h</li>
                    <li>Soirée: limiter pour sommeil</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="modern-card">
                <h4>🥤 Boissons Recommandées</h4>
                <ul>
                    <li>✅ Eau plate/gazeuse</li>
                    <li>✅ Thé vert (antioxydants)</li>
                    <li>✅ Café noir (1-2/jour)</li>
                    <li>✅ Eau de coco (post-effort)</li>
                    <li>⚠️ Jus de fruits (limiter)</li>
                    <li>❌ Sodas/boissons sucrées</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

def show_achievements_page():
    """Page dédiée aux achievements et gamification"""
    st.header("🏅 Achievements & Progression")
    
    # Barre de progression niveau
    xp = st.session_state.user_xp
    level = st.session_state.user_level
    xp_for_current_level = (level - 1) * 1000
    xp_for_next_level = level * 1000
    xp_progress = (xp - xp_for_current_level) / 1000
    
    # Header avec niveau et XP
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card" style="text-align: center;">
                <div style="font-size: 3rem; font-weight: bold; color: #667eea;">
                    {level}
                </div>
                <div>Niveau actuel</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Barre de progression XP
        st.markdown(
            f"""
            <div class="modern-card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Niveau {level}</span>
                    <span>{xp} / {xp_for_next_level} XP</span>
                    <span>Niveau {level + 1}</span>
                </div>
                <div style="background: #e0e0e0; height: 30px; border-radius: 15px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                               height: 100%; width: {xp_progress * 100}%; 
                               transition: width 0.5s ease;
                               display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                        {int(xp_progress * 100)}%
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card" style="text-align: center;">
                <div style="font-size: 3rem; font-weight: bold; color: #4CAF50;">
                    {xp}
                </div>
                <div>XP Total</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Tabs pour différentes sections
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Achievements", "🎯 En Cours", "📊 Statistiques", "🏅 Classement"])
    
    with tab1:
        st.markdown("### 🏆 Achievements Débloqués")
        
        # Catégories d'achievements
        achievement_categories = {
            "Débuts": ["first_workout", "week_complete"],
            "Régularité": ["month_warrior", "perfect_week", "consistency_king"],
            "Force": ["force_milestone_10", "force_milestone_25"],
            "Phases": ["pre_op_complete", "post_op_warrior", "palier_1_champion", "palier_2_hero", "return_to_sport"],
            "Spéciaux": ["early_bird", "night_owl"]
        }
        
        for category, achievement_ids in achievement_categories.items():
            st.markdown(f"#### {category}")
            
            cols = st.columns(4)
            col_idx = 0
            
            for achievement_id in achievement_ids:
                if achievement_id in st.session_state.program.achievements:
                    achievement = st.session_state.program.achievements[achievement_id]
                    is_unlocked = achievement_id in st.session_state.unlocked_achievements
                    
                    with cols[col_idx % 4]:
                        if is_unlocked:
                            st.markdown(
                                f"""
                                <div class="modern-card" style="text-align: center; background: linear-gradient(135deg, #d4edda 0%, #a8e6cf 100%);">
                                    <div style="font-size: 3rem;">{achievement['name'].split()[0]}</div>
                                    <h5>{achievement['name']}</h5>
                                    <p style="font-size: 0.9rem; color: #666;">{achievement['description']}</p>
                                    <div style="color: #4CAF50; font-weight: bold;">+{achievement['xp']} XP</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f"""
                                <div class="modern-card" style="text-align: center; opacity: 0.5; filter: grayscale(100%);">
                                    <div style="font-size: 3rem;">🔒</div>
                                    <h5>???</h5>
                                    <p style="font-size: 0.9rem; color: #666;">Non débloqué</p>
                                    <div style="color: #666;">+{achievement['xp']} XP</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    
                    col_idx += 1
    
    with tab2:
        st.markdown("### 🎯 Achievements en Cours")
        
        # Calculer la progression vers les prochains achievements
        workout_count = len(st.session_state.workout_history)
        unique_days = len(set([w['date'].date() for w in st.session_state.workout_history])) if workout_count > 0 else 0
        current_streak = calculate_streak(st.session_state.workout_history)
        
        # Achievements proches
        upcoming_achievements = []
        
        if "week_complete" not in st.session_state.unlocked_achievements:
            progress = min(100, (unique_days / 7) * 100)
            upcoming_achievements.append({
                "name": "📅 Semaine Complète",
                "description": "Complétez 7 jours d'entraînement",
                "progress": progress,
                "current": unique_days,
                "target": 7,
                "xp": 250
            })
        
        if "month_warrior" not in st.session_state.unlocked_achievements:
            progress = min(100, (unique_days / 30) * 100)
            upcoming_achievements.append({
                "name": "🗓️ Guerrier du Mois",
                "description": "30 jours de progression",
                "progress": progress,
                "current": unique_days,
                "target": 30,
                "xp": 500
            })
        
        if "consistency_king" not in st.session_state.unlocked_achievements:
            progress = min(100, (current_streak / 21) * 100)
            upcoming_achievements.append({
                "name": "👑 Roi de la Régularité",
                "description": "21 jours consécutifs",
                "progress": progress,
                "current": current_streak,
                "target": 21,
                "xp": 750
            })
        
        # Afficher les achievements en cours
        for achievement in upcoming_achievements[:3]:  # Top 3
            st.markdown(
                f"""
                <div class="modern-card">
                    <h4>{achievement['name']} <span style="color: #667eea;">+{achievement['xp']} XP</span></h4>
                    <p>{achievement['description']}</p>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span>Progression: {achievement['current']}/{achievement['target']}</span>
                        <span>{achievement['progress']:.0f}%</span>
                    </div>
                    <div style="background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                                   height: 100%; width: {achievement['progress']}%; 
                                   transition: width 0.5s ease;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with tab3:
        st.markdown("### 📊 Statistiques de Progression")
        
        # Graphique XP dans le temps
        if st.session_state.workout_history:
            # Simuler l'historique XP (dans une vraie app, ce serait stocké)
            xp_history = []
            cumulative_xp = 0
            
            for i, workout in enumerate(st.session_state.workout_history):
                # Attribuer des XP pour chaque workout
                base_xp = 10
                if i == 0:  # First workout
                    cumulative_xp += 100
                if i % 7 == 6:  # Chaque semaine
                    cumulative_xp += 50
                cumulative_xp += base_xp
                
                xp_history.append({
                    'date': workout['date'],
                    'xp': cumulative_xp
                })
            
            df_xp = pd.DataFrame(xp_history)
            
            # Graphique progression XP
            fig_xp = go.Figure()
            
            fig_xp.add_trace(go.Scatter(
                x=df_xp['date'],
                y=df_xp['xp'],
                mode='lines+markers',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.2)',
                name='XP'
            ))
            
            # Ajouter les niveaux
            max_xp = df_xp['xp'].max()
            for level in range(1, int(max_xp / 1000) + 2):
                fig_xp.add_hline(
                    y=level * 1000,
                    line_dash="dash",
                    line_color="gray",
                    annotation_text=f"Niveau {level + 1}",
                    annotation_position="right"
                )
            
            fig_xp.update_layout(
                title="Progression XP dans le Temps",
                xaxis_title="Date",
                yaxis_title="XP Total",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_xp, use_container_width=True)
        
        # Stats achievements
        col1, col2, col3, col4 = st.columns(4)
        
        total_achievements = len(st.session_state.program.achievements)
        unlocked_count = len(st.session_state.unlocked_achievements)
        completion_rate = (unlocked_count / total_achievements * 100) if total_achievements > 0 else 0
        
        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem; font-weight: bold;">{unlocked_count}</div>
                    <div>Achievements débloqués</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem; font-weight: bold;">{total_achievements - unlocked_count}</div>
                    <div>Restants</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem; font-weight: bold;">{completion_rate:.0f}%</div>
                    <div>Complété</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            avg_xp_per_achievement = xp / unlocked_count if unlocked_count > 0 else 0
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem; font-weight: bold;">{avg_xp_per_achievement:.0f}</div>
                    <div>XP moyen/achievement</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with tab4:
        st.markdown("### 🏅 Classement Global")
        
        # Simuler un classement
        st.info("🔜 Fonctionnalité bientôt disponible! Comparez vos progrès avec d'autres athlètes en rééducation.")
        
        # Aperçu du futur classement
        leaderboard_preview = pd.DataFrame({
            'Rang': ['🥇', '🥈', '🥉', '4', '5'],
            'Athlète': ['Vous', 'Alex M.', 'Sarah L.', 'Tom B.', 'Emma R.'],
            'Niveau': [level, level + 2, level + 1, level, level - 1],
            'XP': [xp, xp + 2500, xp + 1200, xp - 300, xp - 800],
            'Achievements': [unlocked_count, unlocked_count + 5, unlocked_count + 3, unlocked_count - 1, unlocked_count - 2]
        })
        
        st.dataframe(
            leaderboard_preview,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rang": st.column_config.TextColumn("Rang", width="small"),
                "Niveau": st.column_config.NumberColumn("Niveau", format="%d"),
                "XP": st.column_config.NumberColumn("XP", format="%d"),
                "Achievements": st.column_config.NumberColumn("🏅", format="%d")
            }
        )

def show_evaluation_tests():
    """Interface améliorée pour les tests d'évaluation"""
    st.header("🧪 Tests d'Évaluation & Validation")
    
    phase, phase_name, emoji = st.session_state.program.get_current_phase()
    
    # Header avec progression
    st.markdown(
        f"""
        <div class="phase-card">
            <h2 style="margin: 0;">{emoji} {phase_name}</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Validez vos critères de progression</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Vérifier la phase pour les tests
    if not any(palier in phase for palier in ["palier_1", "palier_2", "palier_3"]):
        st.info("📋 Les tests d'évaluation sont disponibles à partir du Palier 1 de réathlétisation (J+45)")
        
        # Timeline des futures évaluations
        st.markdown("### 📅 Calendrier des Évaluations")
        
        surgery_date = st.session_state.program.surgery_date
        evaluation_dates = {
            "Palier 1": surgery_date + timedelta(days=45),
            "Palier 2": surgery_date + timedelta(days=90),
            "Palier 3": surgery_date + timedelta(days=180),
            "Retour Sport": surgery_date + timedelta(days=270)
        }
        
        for eval_name, eval_date in evaluation_dates.items():
            days_until = (eval_date - datetime.now()).days
            if days_until > 0:
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>{eval_name}</strong><br>
                                <small>{eval_date.strftime('%d/%m/%Y')}</small>
                            </div>
                            <div style="text-align: right;">
                                <span style="font-size: 1.5rem; font-weight: bold; color: #667eea;">
                                    J-{days_until}
                                </span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        return
    
    # Déterminer les tests selon la phase
    if "palier_1" in phase:
        current_tests = st.session_state.program.evaluation_tests["palier_1"]
        palier_name = "Palier 1"
        palier_desc = "Objectif: Réduire le déficit de force à moins de 25%"
    elif "palier_2" in phase:
        current_tests = st.session_state.program.evaluation_tests["palier_2"]
        palier_name = "Palier 2"
        palier_desc = "Objectif: Développer la puissance et réduire le déficit à moins de 15%"
    else:  # palier_3
        current_tests = st.session_state.program.evaluation_tests["palier_3"]
        palier_name = "Palier 3"
        palier_desc = "Objectif: Valider les critères de retour au sport"
    
    # Vue d'ensemble des tests
    st.markdown(f"### 🎯 Tests {palier_name}")
    st.info(palier_desc)
    
    # Tabs pour organisation
    tab1, tab2, tab3 = st.tabs(["📝 Nouveau Test", "📊 Historique", "📈 Analyse"])
    
    with tab1:
        st.markdown("#### 📝 Enregistrer un Nouveau Test")
        
        # Date et conditions
        col1, col2 = st.columns(2)
        with col1:
            test_date = st.date_input("Date du test", value=datetime.now().date())
        with col2:
            test_conditions = st.selectbox(
                "Conditions",
                ["Optimal", "Fatigué", "Douleur légère", "Après entraînement"]
            )
        
        # Formulaire de test avec design moderne
        test_results = {}
        all_tests_valid = True
        
        for test_name, test_info in current_tests.items():
            st.markdown(f"##### {test_info['description']}")
            
            # Badge du type de test
            test_type_badges = {
                "force": "💪 Force",
                "fonctionnel": "🏃 Fonctionnel",
                "proprioception": "⚖️ Équilibre",
                "sport_specifique": "⚽ Sport"
            }
            
            badge = test_type_badges.get(test_info['type'], "📊 Test")
            st.markdown(
                f'<span class="progress-badge">{badge}</span> Objectif: **{test_info["target"]}**',
                unsafe_allow_html=True
            )
            
            if "deficit" in test_name:
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    jambe_operee = st.number_input(
                        f"Jambe opérée",
                        min_value=0.0,
                        step=0.5,
                        key=f"{test_name}_op",
                        help="Valeur mesurée pour la jambe opérée"
                    )
                
                with col2:
                    jambe_saine = st.number_input(
                        f"Jambe saine",
                        min_value=0.0,
                        step=0.5,
                        key=f"{test_name}_saine",
                        help="Valeur mesurée pour la jambe saine"
                    )
                
                with col3:
                    if jambe_saine > 0:
                        deficit = ((jambe_saine - jambe_operee) / jambe_saine) * 100
                        test_results[test_name] = {
                            "jambe_operee": jambe_operee,
                            "jambe_saine": jambe_saine,
                            "deficit_percent": deficit
                        }
                        
                        # Visualisation du déficit
                        target_value = float(test_info['target'].replace('<', '').replace('%', ''))
                        
                        if deficit <= target_value:
                            st.markdown(
                                f"""
                                <div class="success-card" style="text-align: center; padding: 1rem;">
                                    <div style="font-size: 1.5rem; font-weight: bold;">
                                        ✅ {deficit:.1f}%
                                    </div>
                                    <div style="font-size: 0.9rem;">VALIDÉ</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f"""
                                <div class="warning-card" style="text-align: center; padding: 1rem;">
                                    <div style="font-size: 1.5rem; font-weight: bold;">
                                        ⚠️ {deficit:.1f}%
                                    </div>
                                    <div style="font-size: 0.9rem;">À améliorer</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            all_tests_valid = False
            
            elif any(keyword in test_name for keyword in ["saut", "hop", "balance"]):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    valeur_operee = st.number_input(
                        f"Jambe opérée (cm/pts)",
                        min_value=0.0,
                        step=1.0,
                        key=f"{test_name}_val_op"
                    )
                
                with col2:
                    valeur_saine = st.number_input(
                        f"Jambe saine (cm/pts)",
                        min_value=0.0,
                        step=1.0,
                        key=f"{test_name}_val_saine"
                    )
                
                with col3:
                    if valeur_saine > 0:
                        ratio = (valeur_operee / valeur_saine) * 100
                        test_results[test_name] = {
                            "valeur_operee": valeur_operee,
                            "valeur_saine": valeur_saine,
                            "ratio_percent": ratio
                        }
                        
                        target_value = float(test_info['target'].replace('>', '').replace('%', ''))
                        
                        if ratio >= target_value:
                            st.markdown(
                                f"""
                                <div class="success-card" style="text-align: center; padding: 1rem;">
                                    <div style="font-size: 1.5rem; font-weight: bold;">
                                        ✅ {ratio:.1f}%
                                    </div>
                                    <div style="font-size: 0.9rem;">VALIDÉ</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f"""
                                <div class="warning-card" style="text-align: center; padding: 1rem;">
                                    <div style="font-size: 1.5rem; font-weight: bold;">
                                        ⚠️ {ratio:.1f}%
                                    </div>
                                    <div style="font-size: 0.9rem;">À améliorer</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            all_tests_valid = False
            
            else:
                # Tests qualitatifs
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    result = st.select_slider(
                        f"Résultat",
                        options=["❌ Échec", "⚠️ Partiel", "✅ Réussi", "⭐ Excellent"],
                        value="✅ Réussi",
                        key=f"{test_name}_qual"
                    )
                    test_results[test_name] = {"result": result}
                
                with col2:
                    if "✅" in result or "⭐" in result:
                        st.markdown(
                            '<div style="text-align: center; font-size: 3rem;">✅</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<div style="text-align: center; font-size: 3rem;">⚠️</div>',
                            unsafe_allow_html=True
                        )
                        all_tests_valid = False
            
            st.markdown("---")
        
        # Notes et vidéo
        col1, col2 = st.columns(2)
        
        with col1:
            notes = st.text_area(
                "📝 Notes et observations",
                placeholder="Sensations, douleurs, conditions particulières...",
                height=100
            )
        
        with col2:
            video_upload = st.file_uploader(
                "🎥 Vidéo du test (optionnel)",
                type=['mp4', 'mov', 'avi'],
                help="Enregistrez vos tests pour analyse ultérieure"
            )
        
        # Résumé et validation
        if test_results:
            if all_tests_valid:
                st.markdown(
                    """
                    <div class="success-card" style="text-align: center; padding: 2rem;">
                        <h2 style="margin: 0;">🎉 TOUS LES TESTS VALIDÉS!</h2>
                        <p>Félicitations! Vous êtes prêt pour la phase suivante.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="warning-card" style="text-align: center; padding: 2rem;">
                        <h3 style="margin: 0;">⚠️ Tests à améliorer</h3>
                        <p>Continuez votre progression avant de passer au palier suivant.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Bouton de sauvegarde
        if st.button("💾 Enregistrer les Résultats", type="primary", use_container_width=True):
            eval_data = {
                "date": datetime.combine(test_date, datetime.min.time()),
                "phase": phase,
                "palier": palier_name,
                "conditions": test_conditions,
                "results": test_results,
                "all_valid": all_tests_valid,
                "notes": notes,
                "type": "evaluation"
            }
            
            if st.session_state.github_storage.connected:
                if st.session_state.github_storage.save_evaluation(eval_data):
                    st.success("✅ Résultats sauvegardés!")
                    
                    # Check achievement
                    if all_tests_valid:
                        achievement_map = {
                            "Palier 1": "palier_1_champion",
                            "Palier 2": "palier_2_hero",
                            "Palier 3": "return_to_sport"
                        }
                        
                        achievement_id = achievement_map.get(palier_name)
                        if achievement_id and achievement_id not in st.session_state.unlocked_achievements:
                            st.session_state.unlocked_achievements.add(achievement_id)
                            achievement_data = st.session_state.program.achievements[achievement_id]
                            st.session_state.user_xp += achievement_data['xp']
                            st.session_state.user_level = 1 + (st.session_state.user_xp // 1000)
                            show_achievement_notification(achievement_id, achievement_data)
                else:
                    st.error("❌ Erreur sauvegarde")
            else:
                st.session_state.workout_history.append(eval_data)
                st.success("✅ Résultats enregistrés localement!")
    
    with tab2:
        st.markdown("#### 📊 Historique des Tests")
        
        # Récupérer l'historique
        if st.session_state.github_storage.connected:
            eval_history = st.session_state.github_storage.get_evaluations()
        else:
            eval_history = [w for w in st.session_state.workout_history if w.get('type') == 'evaluation']
        
        if eval_history:
            # Trier par date décroissante
            eval_history.sort(key=lambda x: x.get('timestamp', x.get('date', '')), reverse=True)
            
            # Afficher les tests récents
            for eval_data in eval_history[:10]:
                eval_date = eval_data.get('timestamp', eval_data.get('date', 'Date inconnue'))
                if isinstance(eval_date, str):
                    try:
                        eval_date_obj = datetime.fromisoformat(eval_date)
                        eval_date_str = eval_date_obj.strftime('%d/%m/%Y')
                    except:
                        eval_date_str = str(eval_date)[:10]
                else:
                    eval_date_str = eval_date.strftime('%d/%m/%Y')
                
                palier = eval_data.get('palier', 'Non spécifié')
                all_valid = eval_data.get('all_valid', False)
                
                # Card pour chaque test
                card_class = "success-card" if all_valid else "warning-card"
                status_icon = "✅" if all_valid else "⚠️"
                
                with st.expander(f"{status_icon} Test du {eval_date_str} - {palier}"):
                    if 'results' in eval_data:
                        # Afficher les résultats en colonnes
                        results_cols = st.columns(len(eval_data['results']))
                        
                        for idx, (test_name, result) in enumerate(eval_data['results'].items()):
                            with results_cols[idx]:
                                st.markdown(f"**{test_name}**")
                                
                                if 'deficit_percent' in result:
                                    deficit = result['deficit_percent']
                                    color = "#4CAF50" if deficit < 25 else "#ff6b6b"
                                    st.markdown(
                                        f'<div style="font-size: 1.5rem; color: {color}; font-weight: bold;">'
                                        f'{deficit:.1f}% déficit</div>',
                                        unsafe_allow_html=True
                                    )
                                elif 'ratio_percent' in result:
                                    ratio = result['ratio_percent']
                                    color = "#4CAF50" if ratio > 80 else "#ff6b6b"
                                    st.markdown(
                                        f'<div style="font-size: 1.5rem; color: {color}; font-weight: bold;">'
                                        f'{ratio:.1f}% ratio</div>',
                                        unsafe_allow_html=True
                                    )
                                else:
                                    st.write(result.get('result', 'N/A'))
                    
                    if eval_data.get('notes'):
                        st.markdown("**Notes:**")
                        st.write(eval_data['notes'])
        else:
            st.info("Aucun test enregistré pour le moment.")
    
    with tab3:
        st.markdown("#### 📈 Analyse de Progression")
        
        if eval_history and len(eval_history) >= 2:
            # Préparer les données pour analyse
            analysis_data = []
            
            for eval_data in eval_history:
                if 'results' in eval_data:
                    eval_date = eval_data.get('timestamp', eval_data.get('date'))
                    if isinstance(eval_date, str):
                        eval_date = datetime.fromisoformat(eval_date)
                    
                    # Extraire les métriques clés
                    for test_name, result in eval_data['results'].items():
                        if 'deficit_percent' in result:
                            analysis_data.append({
                                'date': eval_date,
                                'test': test_name,
                                'value': result['deficit_percent'],
                                'type': 'deficit'
                            })
                        elif 'ratio_percent' in result:
                            analysis_data.append({
                                'date': eval_date,
                                'test': test_name,
                                'value': result['ratio_percent'],
                                'type': 'ratio'
                            })
            
            if analysis_data:
                df_analysis = pd.DataFrame(analysis_data)
                
                # Graphique d'évolution
                fig_evolution = go.Figure()
                
                # Grouper par test
                for test_name in df_analysis['test'].unique():
                    df_test = df_analysis[df_analysis['test'] == test_name].sort_values('date')
                    
                    fig_evolution.add_trace(go.Scatter(
                        x=df_test['date'],
                        y=df_test['value'],
                        mode='lines+markers',
                        name=test_name,
                        line=dict(width=3),
                        marker=dict(size=10)
                    ))
                
                # Ajouter les zones cibles
                fig_evolution.add_hline(
                    y=25, line_dash="dash", line_color="green",
                    annotation_text="Cible Palier 1 (<25%)"
                )
                fig_evolution.add_hline(
                    y=15, line_dash="dash", line_color="orange",
                    annotation_text="Cible Palier 2 (<15%)"
                )
                fig_evolution.add_hline(
                    y=10, line_dash="dash", line_color="red",
                    annotation_text="Cible Palier 3 (<10%)"
                )
                
                fig_evolution.update_layout(
                    title="Évolution des Tests dans le Temps",
                    xaxis_title="Date",
                    yaxis_title="Valeur (%)",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_evolution, use_container_width=True)
                
                # Statistiques de progression
                st.markdown("##### 📊 Analyse Statistique")
                
                col1, col2, col3 = st.columns(3)
                
                # Calculer les améliorations
                improvements = []
                for test_name in df_analysis['test'].unique():
                    df_test = df_analysis[df_analysis['test'] == test_name].sort_values('date')
                    if len(df_test) >= 2:
                        first_value = df_test.iloc[0]['value']
                        last_value = df_test.iloc[-1]['value']
                        
                        if df_test.iloc[0]['type'] == 'deficit':
                            improvement = first_value - last_value
                        else:  # ratio
                            improvement = last_value - first_value
                        
                        improvements.append({
                            'test': test_name,
                            'improvement': improvement,
                            'first': first_value,
                            'last': last_value
                        })
                
                # Afficher les améliorations
                for idx, imp in enumerate(improvements[:3]):
                    with [col1, col2, col3][idx % 3]:
                        color = "#4CAF50" if imp['improvement'] > 0 else "#ff6b6b"
                        st.markdown(
                            f"""
                            <div class="modern-card">
                                <h5>{imp['test']}</h5>
                                <div style="font-size: 1.5rem; font-weight: bold; color: {color};">
                                    {imp['improvement']:+.1f}%
                                </div>
                                <div style="font-size: 0.9rem; color: #666;">
                                    {imp['first']:.1f}% → {imp['last']:.1f}%
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        else:
            st.info("Effectuez au moins 2 tests pour voir l'analyse de progression.")
    
    # Recommandations personnalisées
    st.markdown("### 💡 Recommandations Personnalisées")
    
    if eval_history and 'results' in eval_history[0]:
        latest_results = eval_history[0]['results']
        recommendations = []
        
        # Analyser les résultats et donner des recommandations
        for test_name, result in latest_results.items():
            if 'deficit_percent' in result and result['deficit_percent'] > 25:
                recommendations.append({
                    "type": "force",
                    "message": f"Déficit de {result['deficit_percent']:.1f}% sur {test_name}",
                    "action": "Augmentez le travail unilatéral sur la jambe opérée"
                })
            elif 'ratio_percent' in result and result['ratio_percent'] < 80:
                recommendations.append({
                    "type": "fonctionnel",
                    "message": f"Ratio de {result['ratio_percent']:.1f}% sur {test_name}",
                    "action": "Intégrez plus d'exercices pliométriques progressifs"
                })
        
        if recommendations:
            for rec in recommendations:
                icon = "💪" if rec['type'] == "force" else "🏃"
                st.warning(f"{icon} **{rec['message']}**\n\n➡️ {rec['action']}")
        else:
            st.success("🎯 Excellents résultats! Continuez votre progression actuelle.")
    else:
        st.info("Effectuez votre premier test pour recevoir des recommandations personnalisées.")

def show_complete_guide():
    """Guide complet avec toutes les phases détaillées version améliorée"""
    st.header("📚 Guide Complet de Rééducation LCA")
    
    # Header interactif avec progression
    phase_actuelle, _, _ = st.session_state.program.get_current_phase()
    
    # Timeline visuelle des phases
    st.markdown("### 🗺️ Parcours de Rééducation")
    
    phases_timeline = [
        {"name": "Pré-op", "duration": "4 sem", "icon": "🏋️", "color": "#667eea"},
        {"name": "Post-op", "duration": "6 sem", "icon": "🏥", "color": "#764ba2"},
        {"name": "Palier 1", "duration": "6 sem", "icon": "🎯", "color": "#ff6b6b"},
        {"name": "Palier 2", "duration": "12 sem", "icon": "🚀", "color": "#4CAF50"},
        {"name": "Palier 3", "duration": "12 sem", "icon": "⚡", "color": "#FFC107"},
        {"name": "Sport", "duration": "∞", "icon": "🏆", "color": "#9C27B0"}
    ]
    
    # Créer la timeline HTML
    timeline_html = '<div style="display: flex; align-items: center; margin: 2rem 0;">'
    for i, phase in enumerate(phases_timeline):
        is_current = phase["name"].lower() in phase_actuelle.lower()
        opacity = "1" if is_current else "0.6"
        scale = "1.2" if is_current else "1"
        
        timeline_html += f'''
        <div style="flex: 1; text-align: center; transform: scale({scale}); opacity: {opacity};">
            <div style="background: {phase["color"]}; color: white; padding: 1rem; 
                        border-radius: 10px; margin: 0 0.5rem;">
                <div style="font-size: 2rem;">{phase["icon"]}</div>
                <div style="font-weight: bold;">{phase["name"]}</div>
                <div style="font-size: 0.8rem;">{phase["duration"]}</div>
            </div>
        </div>
        '''
        
        if i < len(phases_timeline) - 1:
            timeline_html += '<div style="font-size: 2rem; color: #ccc;">→</div>'
    
    timeline_html += '</div>'
    st.markdown(timeline_html, unsafe_allow_html=True)
    
    # Navigation par onglets améliorée
    tabs = st.tabs([
        "🏋️ Pré-Opératoire",
        "🏥 Post-Op Immédiat",
        "💪 Renforcement",
        "🎯 Réathlétisation",
        "⚡ Sport Spécifique",
        "⚠️ Sécurité",
        "📋 Protocoles",
        "🎥 Vidéothèque"
    ])
    
    with tabs[0]:  # Pré-Opératoire
        st.subheader("Phase Pré-Opératoire (4 semaines avant chirurgie)")
        
        # Objectifs avec cards visuelles
        st.markdown("#### 🎯 Objectifs Principaux")
        
        objectives_cards = [
            {
                "icon": "💪",
                "title": "Force Maximale",
                "desc": "Développer la force bilatérale symétrique",
                "target": "1.5x poids corps en leg press"
            },
            {
                "icon": "⚖️",
                "title": "Proprioception",
                "desc": "Optimiser le contrôle neuromusculaire",
                "target": "45s équilibre unipodal yeux fermés"
            },
            {
                "icon": "🏃",
                "title": "Condition Physique",
                "desc": "Maintenir l'endurance cardiovasculaire",
                "target": "30min cardio modéré 3x/semaine"
            },
            {
                "icon": "🧠",
                "title": "Mental",
                "desc": "Préparer psychologiquement à la chirurgie",
                "target": "Visualisation positive quotidienne"
            }
        ]
        
        cols = st.columns(2)
        for i, obj in enumerate(objectives_cards):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <div style="font-size: 2rem; text-align: center;">{obj['icon']}</div>
                        <h4 style="text-align: center;">{obj['title']}</h4>
                        <p>{obj['desc']}</p>
                        <div style="background: #f0f2f6; padding: 0.5rem; border-radius: 8px;">
                            <strong>Cible:</strong> {obj['target']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Programme détaillé avec progression
        st.markdown("#### 📅 Programmation Progressive")
        
        week_tabs = st.tabs(["Semaine -4 à -3", "Semaine -2 à -1"])
        
        with week_tabs[0]:
            st.markdown("##### 🏋️ Phase d'Adaptation")
            
            # Exemple de séance avec détails visuels
            seance_exemple = st.session_state.program.pre_op_programs["week_-4_-3"]["seance_A"]
            
            for ex in seance_exemple[:3]:  # Premiers exercices
                with st.expander(f"💪 {ex['nom']}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {ex['description']}")
                        st.markdown(f"**Focus:** {ex['focus']}")
                        st.markdown(f"**Conseils:** {ex['conseils']}")
                    
                    with col2:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div>📊 {ex['series']} × {ex['reps']}</div>
                                <div>⚖️ {ex['charge']}</div>
                                <div>⏱️ {ex['repos']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    # Muscles ciblés avec badges
                    muscles_html = " ".join([f'<span class="progress-badge">{m}</span>' 
                                           for m in ex.get('muscles', [])])
                    st.markdown(f"**Muscles:** {muscles_html}", unsafe_allow_html=True)
        
        with week_tabs[1]:
            st.markdown("##### 🔥 Phase d'Intensification")
            st.info("Augmentation des charges de 10-15% par rapport aux semaines précédentes")
            
            # Tableau de progression
            progression_data = {
                "Exercice": ["Leg Press", "Fentes", "SDT Roumain"],
                "Sem -4/-3": ["85kg", "8kg/main", "40kg"],
                "Sem -2/-1": ["97kg", "12kg/main", "50kg"],
                "Progression": ["+14%", "+50%", "+25%"]
            }
            
            df_prog = pd.DataFrame(progression_data)
            st.dataframe(
                df_prog,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Progression": st.column_config.TextColumn(
                        "Progression",
                        help="Augmentation entre les phases"
                    )
                }
            )
    
    with tabs[1]:  # Post-Op Immédiat
        st.subheader("Phase Post-Opératoire Immédiate (J0 à J+45)")
        
        # Timeline post-op
        post_op_phases = [
            {
                "period": "J0-J7",
                "name": "Réveil Musculaire",
                "focus": "Protection maximale du greffon",
                "color": "#ff6b6b"
            },
            {
                "period": "J8-J21",
                "name": "Mobilisation Active",
                "focus": "Récupération amplitude 0-60°",
                "color": "#FFC107"
            },
            {
                "period": "J22-J45",
                "name": "Renforcement Progressif",
                "focus": "Retour charge complète",
                "color": "#4CAF50"
            }
        ]
        
        for phase in post_op_phases:
            st.markdown(
                f"""
                <div class="modern-card" style="border-left: 6px solid {phase['color']};">
                    <h4>{phase['period']} - {phase['name']}</h4>
                    <p style="color: #666; margin: 0;">{phase['focus']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Protocole RICE amélioré
        st.markdown("#### ❄️ Protocole RICE+ Moderne")
        
        rice_protocol = {
            "R - Rest": {
                "icon": "🛌",
                "desc": "Repos relatif, pas immobilisation totale",
                "tips": ["Contractions isométriques", "Mobilisation passive douce"]
            },
            "I - Ice": {
                "icon": "🧊",
                "desc": "Cryothérapie 15-20min toutes les 2-3h",
                "tips": ["Jamais directement sur la peau", "Machine de cryothérapie si disponible"]
            },
            "C - Compression": {
                "icon": "🩹",
                "desc": "Bandage compressif ou bas de contention",
                "tips": ["Pas trop serré", "Retirer la nuit si gênant"]
            },
            "E - Elevation": {
                "icon": "⬆️",
                "desc": "Surélever la jambe au-dessus du cœur",
                "tips": ["30min plusieurs fois/jour", "Pendant le sommeil si possible"]
            }
        }
        
        cols = st.columns(4)
        for i, (key, value) in enumerate(rice_protocol.items()):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="modern-card" style="text-align: center;">
                        <div style="font-size: 3rem;">{value['icon']}</div>
                        <h5>{key}</h5>
                        <p style="font-size: 0.9rem;">{value['desc']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                with st.expander("Conseils"):
                    for tip in value['tips']:
                        st.write(f"• {tip}")
        
        # Exercices par semaine avec vidéos
        st.markdown("#### 🏃 Programme Progressif")
        
        week_selector = st.selectbox(
            "Sélectionnez la semaine",
            ["Semaine 1 (J0-J7)", "Semaines 2-3 (J8-J21)", "Semaines 4-6 (J22-J45)"]
        )
        
        if "Semaine 1" in week_selector:
            exercises = st.session_state.program.post_op_programs["semaine_1"]["quotidien"]
        elif "2-3" in week_selector:
            exercises = st.session_state.program.post_op_programs["semaine_2-3"]["quotidien"]
        else:
            exercises = st.session_state.program.post_op_programs["semaine_4-6"]["3_seances_semaine"]
        
        # Afficher les exercices avec indicateur de difficulté
        for ex in exercises[:3]:
            difficulty_color = {1: "#4CAF50", 2: "#8BC34A", 3: "#FFC107", 4: "#FF9800", 5: "#F44336"}
            diff_level = ex.get('difficulte', 2)
            
            st.markdown(
                f"""
                <div class="exercise-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h4>{ex['nom']}</h4>
                            <p style="color: #666;">{ex['description']}</p>
                        </div>
                        <div style="text-align: right;">
                            <div style="color: {difficulty_color[diff_level]};">
                                {'⭐' * diff_level}
                            </div>
                            <div style="font-size: 0.8rem; color: #666;">Difficulté</div>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
                        <div style="background: #f0f2f6; padding: 0.5rem; border-radius: 8px;">
                            <strong>Volume:</strong> {ex['series']} × {ex['reps']}
                        </div>
                        <div style="background: #f0f2f6; padding: 0.5rem; border-radius: 8px;">
                            <strong>Charge:</strong> {ex['charge']}
                        </div>
                        <div style="background: #f0f2f6; padding: 0.5rem; border-radius: 8px;">
                            <strong>Repos:</strong> {ex['repos']}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with tabs[2]:  # Renforcement
        st.subheader("Phase de Renforcement (J+45 à J+90)")
        
        # Critères de passage
        st.markdown("#### ✅ Critères de Passage en Phase Renforcement")
        
        criteria = [
            {"name": "Amplitude", "target": "0-120° minimum", "icon": "📐"},
            {"name": "Douleur", "target": "< 3/10 au repos", "icon": "😌"},
            {"name": "Œdème", "target": "Minimal ou absent", "icon": "💧"},
            {"name": "Marche", "target": "Sans boiterie", "icon": "🚶"},
            {"name": "Force", "target": "Contraction quadriceps active", "icon": "💪"}
        ]
        
        cols = st.columns(5)
        for i, crit in enumerate(criteria):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div style="font-size: 2rem;">{crit['icon']}</div>
                        <div style="font-weight: bold;">{crit['name']}</div>
                        <div style="font-size: 0.8rem; color: #666;">{crit['target']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Progression des charges
        st.markdown("#### 📈 Stratégie de Progression")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                <div class="modern-card">
                    <h4>🎯 Méthode 2RM Progressive</h4>
                    <ol>
                        <li>Tester la force jambe saine</li>
                        <li>Commencer à 50% sur jambe opérée</li>
                        <li>Progression +10% par semaine si:</li>
                        <ul>
                            <li>Aucune douleur pendant/après</li>
                            <li>Pas de gonflement +24h</li>
                            <li>Technique parfaite maintenue</li>
                        </ul>
                        <li>Objectif: déficit < 25% à J+90</li>
                    </ol>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            # Graphique de progression théorique
            weeks = list(range(1, 7))
            deficit_target = [50, 45, 38, 32, 27, 22]
            
            fig_prog = go.Figure()
            fig_prog.add_trace(go.Scatter(
                x=weeks,
                y=deficit_target,
                mode='lines+markers',
                name='Progression idéale',
                line=dict(color='#667eea', width=3),
                marker=dict(size=10)
            ))
            
            fig_prog.add_hline(y=25, line_dash="dash", line_color="green",
                              annotation_text="Objectif Palier 1")
            
            fig_prog.update_layout(
                title="Réduction du Déficit de Force",
                xaxis_title="Semaines",
                yaxis_title="Déficit (%)",
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig_prog, use_container_width=True)
        
        # Programme type semaine
        st.markdown("#### 📅 Semaine Type Palier 1")
        
        weekly_schedule = {
            "Lundi": {"type": "Force", "focus": "Membres inférieurs complet", "icon": "💪"},
            "Mardi": {"type": "Proprioception", "focus": "Équilibre et contrôle", "icon": "⚖️"},
            "Mercredi": {"type": "Repos actif", "focus": "Mobilité et récupération", "icon": "🧘"},
            "Jeudi": {"type": "Force", "focus": "Chaînes postérieures", "icon": "💪"},
            "Vendredi": {"type": "Fonctionnel", "focus": "Patterns de mouvement", "icon": "🏃"},
            "Weekend": {"type": "Récupération", "focus": "Repos ou activité légère", "icon": "😴"}
        }
        
        for day, content in weekly_schedule.items():
            st.markdown(
                f"""
                <div class="modern-card" style="margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{day}</strong> - {content['type']}
                            <div style="font-size: 0.9rem; color: #666;">{content['focus']}</div>
                        </div>
                        <div style="font-size: 2rem;">{content['icon']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with tabs[3]:  # Réathlétisation
        st.subheader("Phases de Réathlétisation")
        
        # Vue d'ensemble des paliers
        st.markdown("#### 🎯 Les 3 Paliers de Réathlétisation")
        
        paliers_overview = [
            {
                "name": "Palier 1",
                "period": "J+45 à J+90",
                "goal": "Force & Symétrie",
                "criteria": "Déficit < 25%",
                "color": "#667eea",
                "exercises": ["Leg Press uni/bi", "Squats progressifs", "Proprioception avancée"]
            },
            {
                "name": "Palier 2",
                "period": "J+90 à J+180",
                "goal": "Puissance & Pliométrie",
                "criteria": "Déficit < 15%",
                "color": "#4CAF50",
                "exercises": ["Squat jumps", "Box jumps", "Leg press explosif"]
            },
            {
                "name": "Palier 3",
                "period": "J+180 à J+270",
                "goal": "Sport Spécifique",
                "criteria": "Déficit < 10%",
                "color": "#FFC107",
                "exercises": ["Pivots contrôlés", "Sprints", "Changements direction"]
            }
        ]
        
        # Cards interactives pour chaque palier
        palier_tabs = st.tabs([p["name"] for p in paliers_overview])
        
        for i, (tab, palier) in enumerate(zip(palier_tabs, paliers_overview)):
            with tab:
                # Header du palier
                st.markdown(
                    f"""
                    <div class="phase-card" style="background: {palier['color']};">
                        <h3 style="margin: 0; color: white;">{palier['name']} - {palier['goal']}</h3>
                        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; color: white;">
                            {palier['period']} | Critère: {palier['criteria']}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Exercices clés avec progression
                st.markdown("##### 🏋️ Exercices Clés")
                
                for exercise in palier['exercises']:
                    st.markdown(f"• **{exercise}**")
                
                # Exemple de progression
                if i == 0:  # Palier 1
                    st.markdown("##### 📊 Exemple de Progression - Leg Press")
                    
                    progression_example = pd.DataFrame({
                        'Semaine': [1, 2, 3, 4, 5, 6],
                        'Jambe Opérée (kg)': [40, 45, 52, 58, 65, 70],
                        'Jambe Saine (kg)': [80, 82, 85, 87, 90, 92],
                        'Déficit (%)': [50, 45, 39, 33, 28, 24]
                    })
                    
                    fig_ex_prog = go.Figure()
                    
                    fig_ex_prog.add_trace(go.Bar(
                        name='Jambe Opérée',
                        x=progression_example['Semaine'],
                        y=progression_example['Jambe Opérée (kg)'],
                        marker_color='#ff6b6b'
                    ))
                    
                    fig_ex_prog.add_trace(go.Bar(
                        name='Jambe Saine',
                        x=progression_example['Semaine'],
                        y=progression_example['Jambe Saine (kg)'],
                        marker_color='#4CAF50'
                    ))
                    
                    fig_ex_prog.update_layout(
                        title="Progression Type sur 6 Semaines",
                        xaxis_title="Semaine",
                        yaxis_title="Charge (kg)",
                        height=300,
                        barmode='group'
                    )
                    
                    st.plotly_chart(fig_ex_prog, use_container_width=True)
                
                elif i == 1:  # Palier 2
                    st.markdown("##### 🚀 Introduction de la Pliométrie")
                    
                    st.warning("""
                    **⚠️ Prérequis Pliométrie:**
                    - Déficit force < 25% sur tous les tests
                    - Amplitude articulaire complète
                    - Aucune douleur lors des activités quotidiennes
                    - Validation par le kinésithérapeute
                    """)
                    
                    # Progression pliométrique
                    plio_progression = {
                        "Semaine 1-2": ["Sauts sur place 2 pieds", "Step-ups dynamiques", "Corde à sauter légère"],
                        "Semaine 3-4": ["Squat jumps", "Box jumps 20cm", "Fentes sautées statiques"],
                        "Semaine 5-8": ["Box jumps 30-40cm", "Broad jumps", "Lateral bounds"],
                        "Semaine 9-12": ["Depth jumps", "Single leg hops", "Multi-directional jumps"]
                    }
                    
                    for week, exercises in plio_progression.items():
                        with st.expander(f"🗓️ {week}"):
                            for ex in exercises:
                                st.write(f"• {ex}")
                
                else:  # Palier 3
                    st.markdown("##### ⚡ Préparation Retour Sport")
                    
                    # Checklist retour sport
                    st.markdown("**✅ Checklist Retour au Sport**")
                    
                    checklist = [
                        "Déficit force < 10% tous muscles",
                        "Hop tests > 95% symétrie",
                        "Pas d'appréhension dans les mouvements",
                        "Validation tests fonctionnels sport-spécifiques",
                        "Clearance médicale complète",
                        "Préparation psychologique validée"
                    ]
                    
                    for item in checklist:
                        st.checkbox(item, key=f"checklist_{item}")
    
    with tabs[4]:  # Sport Spécifique
        st.subheader("Entraînement Sport-Spécifique")
        
        # Sélection du sport
        sport = st.selectbox(
            "Sélectionnez votre sport",
            ["Football", "Basketball", "Rugby", "Tennis", "Ski", "Course à pied", "Autre"]
        )
        
        # Programmes spécifiques par sport
        sport_programs = {
            "Football": {
                "icon": "⚽",
                "focus": ["Changements de direction", "Pivots", "Frappe de balle"],
                "exercises": [
                    "Slalom avec ballon",
                    "Tirs progressifs",
                    "Duels contrôlés",
                    "Jeu réduit progressif"
                ],
                "timeline": "4-6 semaines de préparation spécifique"
            },
            "Basketball": {
                "icon": "🏀",
                "focus": ["Sauts répétés", "Pivots rapides", "Changements de rythme"],
                "exercises": [
                    "Lay-ups progressifs",
                    "Rebonds contrôlés",
                    "1v1 sans contact",
                    "Scrimmage progressif"
                ],
                "timeline": "3-5 semaines de réintégration"
            },
            "Tennis": {
                "icon": "🎾",
                "focus": ["Déplacements latéraux", "Rotation tronc", "Décélérations"],
                "exercises": [
                    "Shadow tennis",
                    "Volées progression",
                    "Service modifié",
                    "Points contrôlés"
                ],
                "timeline": "3-4 semaines avant compétition"
            },
                        "Ski": {
                "icon": "⛷️",
                "focus": ["Proprioception", "Force excentrique", "Équilibre dynamique"],
                "exercises": [
                    "Squats excentriques",
                    "Sauts latéraux",
                    "Équilibre sur Bosu",
                    "Simulation virages"
                ],
                "timeline": "6-8 semaines pré-saison"
            },
            "Course à pied": {
                "icon": "🏃",
                "focus": ["Endurance progressive", "Économie de course", "Cadence"],
                "exercises": [
                    "Marche/course alternée",
                    "Foulée progressive",
                    "Côtes douces",
                    "Tempo runs"
                ],
                "timeline": "4-6 semaines progression"
            }
        }
        
        if sport in sport_programs:
            program = sport_programs[sport]
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(
                    f"""
                    <div class="metric-card" style="text-align: center;">
                        <div style="font-size: 5rem;">{program['icon']}</div>
                        <div style="font-weight: bold;">{sport}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.info(f"⏱️ {program['timeline']}")
            
            with col2:
                st.markdown("#### 🎯 Focus Spécifiques")
                for focus in program['focus']:
                    st.write(f"• {focus}")
                
                st.markdown("#### 🏃 Progression")
                for i, ex in enumerate(program['exercises'], 1):
                    st.write(f"{i}. {ex}")
        
        # Protocole de retour progressif
        st.markdown("### 📈 Protocole de Retour Progressif")

        return_protocol = [
            {
                "Semaine": "Semaine 1",
                "Volume": "25%",
                "Intensité": "50-60%",
                "Contact": "Aucun",
                "Description": "Réintégration technique individuelle"
            },
            {
                "Semaine": "Semaine 2",
                "Volume": "50%",
                "Intensité": "70-80%",
                "Contact": "Limité",
                "Description": "Exercices collectifs sans opposition"
            },
            {
                "Semaine": "Semaine 3",
                "Volume": "75%",
                "Intensité": "85-90%",
                "Contact": "Contrôlé",
                "Description": "Opposition progressive"
            },
            {
                "Semaine": "Semaine 4+",
                "Volume": "100%",
                "Intensité": "95-100%",
                "Contact": "Complet",
                "Description": "Retour compétition"
            }
        ]

        # Afficher sous forme de tableau simple
        df_protocol = pd.DataFrame(return_protocol)
        st.dataframe(
            df_protocol,
            use_container_width=True,
            hide_index=True
        )

        # Ou afficher avec des métriques visuelles
        st.markdown("#### 📊 Détails par Semaine")
        for row in return_protocol:
            with st.expander(f"📅 {row['Semaine']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Volume", row['Volume'])
                with col2:
                    st.metric("Intensité", row['Intensité'])
                with col3:
                    st.metric("Contact", row['Contact'])
                st.info(f"**Description:** {row['Description']}")

    
    with tabs[5]:  # Sécurité
        st.subheader("⚠️ Sécurité et Prévention")
        
        # Signaux d'alerte principaux
        st.markdown("### 🚨 Signaux d'Alerte Majeurs")
        
        alert_levels = {
            "URGENCE IMMÉDIATE": {
                "color": "#dc3545",
                "icon": "🚨",
                "signs": [
                    "Sensation de 'claquement' ou rupture",
                    "Blocage articulaire complet",
                    "Gonflement massif et soudain",
                    "Douleur aiguë insupportable",
                    "Fièvre + genou chaud et rouge"
                ],
                "action": "ARRÊT IMMÉDIAT + URGENCES"
            },
            "CONSULTATION RAPIDE": {
                "color": "#ffc107",
                "icon": "⚠️",
                "signs": [
                    "Augmentation progressive du gonflement",
                    "Douleur qui persiste au repos",
                    "Sensation d'instabilité nouvelle",
                    "Perte de mobilité progressive",
                    "Échauffement articulaire inhabituel"
                ],
                "action": "Consultation sous 24-48h"
            },
            "SURVEILLANCE": {
                "color": "#28a745",
                "icon": "👁️",
                "signs": [
                    "Fatigue musculaire normale",
                    "Courbatures post-exercice",
                    "Gêne légère en fin de séance",
                    "Raideur matinale < 30min"
                ],
                "action": "Adapter charge/volume si besoin"
            }
        }
        
        for level, data in alert_levels.items():
            st.markdown(
                f"""
                <div class="modern-card" style="border-left: 6px solid {data['color']};">
                    <h4>{data['icon']} {level}</h4>
                    <ul style="margin: 0.5rem 0;">
                        {''.join([f'<li>{sign}</li>' for sign in data['signs']])}
                    </ul>
                    <div style="background: {data['color']}20; padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;">
                        <strong>Action:</strong> {data['action']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Prévention des complications
        st.markdown("### 🛡️ Prévention des Complications")
        
        prevention_tabs = st.tabs(["Arthrofibrose", "Syndrome Rotulien", "Re-rupture", "Complications Générales"])
        
        with prevention_tabs[0]:
            st.markdown("""
            **🦴 Arthrofibrose (Raideur excessive)**
            
            **Facteurs de risque:**
            - Immobilisation prolongée
            - Inflammation non contrôlée
            - Non-respect du protocole de mobilisation
            
            **Prévention:**
            - ✅ Mobilisation précoce et régulière
            - ✅ Contrôle de l'inflammation (glace, AINS si prescrit)
            - ✅ Étirements doux quotidiens
            - ✅ Massage cicatriciel après J+15
            
            **Signes d'alerte:**
            - Perte progressive d'amplitude
            - Douleur croissante en flexion/extension
            - Sensation de "blocage" mécanique
            """)
        
        with prevention_tabs[1]:
            st.markdown("""
            **🦵 Syndrome Fémoro-Patellaire**
            
            **Facteurs de risque:**
            - Faiblesse du vaste médial
            - Déséquilibre musculaire
            - Surcharge trop rapide
            
            **Prévention:**
            - ✅ Renforcement spécifique VMO
            - ✅ Étirements chaîne latérale
            - ✅ Progression très graduelle des charges
            - ✅ Taping rotulien si besoin
            
            **Exercices préventifs:**
            - Terminal knee extension
            - Squats avec bande élastique
            - Step-downs contrôlés
            """)
        
        with prevention_tabs[2]:
            st.markdown("""
            **💔 Prévention Re-rupture**
            
            **Facteurs de risque majeurs:**
            - Retour au sport trop précoce
            - Déficit de force > 15%
            - Mauvaise proprioception
            - Fatigue neuromusculaire
            
            **Protocole préventif:**
            1. **Respect strict des délais** (minimum 9 mois)
            2. **Tests de validation obligatoires**
            3. **Programme préventif à vie:**
               - 2x/semaine renforcement
               - Échauffement spécifique 20min
               - Proprioception continue
            4. **Gestion de la fatigue**
            
            **Taux de re-rupture selon retour:**
            - < 6 mois: 25-30%
            - 6-9 mois: 15-20%
            - > 9 mois avec tests validés: < 10%
            """)
        
        with prevention_tabs[3]:
            st.markdown("""
            **⚕️ Complications Générales**
            
            **Thrombose veineuse:**
            - Mobilisation précoce
            - Bas de contention si prescrit
            - Hydratation ++
            
            **Infection:**
            - Surveillance cicatrice
            - Hygiène stricte
            - Consultation si rougeur/chaleur
            
            **Algodystrophie:**
            - Mobilisation douce continue
            - Gestion douleur optimale
            - Soutien psychologique
            """)
    
    with tabs[6]:  # Protocoles
        st.subheader("📋 Protocoles et Guidelines")
        
        # Téléchargements de protocoles
        st.markdown("### 📥 Documents Téléchargeables")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                """
                <div class="modern-card" style="text-align: center;">
                    <div style="font-size: 3rem;">📄</div>
                    <h5>Protocole Complet</h5>
                    <p style="font-size: 0.9rem;">Guide détaillé 40 pages</p>
                    <button style="width: 100%;">Télécharger PDF</button>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                """
                <div class="modern-card" style="text-align: center;">
                    <div style="font-size: 3rem;">📊</div>
                    <h5>Fiches Exercices</h5>
                    <p style="font-size: 0.9rem;">Illustrations détaillées</p>
                    <button style="width: 100%;">Télécharger PDF</button>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                """
                <div class="modern-card" style="text-align: center;">
                    <div style="font-size: 3rem;">📱</div>
                    <h5>Carnet de Suivi</h5>
                    <p style="font-size: 0.9rem;">Version imprimable</p>
                    <button style="width: 100%;">Télécharger PDF</button>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Guidelines internationales
        st.markdown("### 🌍 Guidelines Internationales")
        
        guidelines = {
            "AOSSM (American Orthopedic Society)": {
                "focus": "Critères retour au sport",
                "points": [
                    "Minimum 9 mois post-op",
                    "Déficit force < 10%",
                    "Hop tests > 90%",
                    "Tests psychologiques validés"
                ]
            },
            "ESSKA (European Society)": {
                "focus": "Protocole de rééducation",
                "points": [
                    "Mobilisation précoce J+1",
                    "Charge progressive individualisée",
                    "Pliométrie après 3 mois si critères OK",
                    "Sport spécifique après 6 mois"
                ]
            },
            "FIFA 11+ Prevention": {
                "focus": "Prévention des blessures",
                "points": [
                    "Échauffement standardisé 20min",
                    "Exercices neuromusculaires",
                    "Proprioception dynamique",
                    "Réduction risque de 30-50%"
                ]
            }
        }
        
        for org, content in guidelines.items():
            with st.expander(f"📚 {org}"):
                st.markdown(f"**Focus:** {content['focus']}")
                for point in content['points']:
                    st.write(f"• {point}")
    
    with tabs[7]:  # Vidéothèque
        st.subheader("🎥 Vidéothèque d'Exercices")
        
        st.info("🎬 Section vidéo interactive - Visualisez la technique parfaite pour chaque exercice")
        
        # Catégories de vidéos
        video_categories = {
            "Renforcement": ["Leg Press", "Squats", "Fentes", "Leg Curl"],
            "Proprioception": ["Équilibre unipodal", "Plateau instable", "Yeux fermés"],
            "Pliométrie": ["Squat jumps", "Box jumps", "Lateral bounds"],
            "Sport-Spécifique": ["Pivots", "Changements direction", "Décélérations"]
        }
        
        selected_category = st.selectbox("Catégorie", list(video_categories.keys()))
        
        cols = st.columns(2)
        for i, exercise in enumerate(video_categories[selected_category]):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div class="modern-card">
                        <h5>🎥 {exercise}</h5>
                        <div style="background: #000; height: 200px; display: flex; 
                                    align-items: center; justify-content: center; 
                                    border-radius: 8px; margin: 1rem 0;">
                            <span style="color: white;">Vidéo disponible</span>
                        </div>
                        <p style="font-size: 0.9rem;">
                            Points clés technique à respecter pour cet exercice.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

def show_settings():
    """Interface des paramètres avec options avancées et design moderne"""
    st.header("⚙️ Paramètres & Configuration")
    
    # Tabs de paramètres
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Profil", 
        "📅 Planning", 
        "💾 Données", 
        "🎨 Préférences",
        "🔔 Notifications"
    ])
    
    with tab1:
        st.subheader("👤 Profil Patient")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Données Physiques")
            
            # Card pour les données actuelles
            st.markdown(
                f"""
                <div class="modern-card">
                    <h5>Données actuelles</h5>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <div style="font-size: 2rem; font-weight: bold; color: #667eea;">
                                {st.session_state.program.patient_weight:.1f}kg
                            </div>
                            <div style="color: #666;">Poids</div>
                        </div>
                        <div>
                            <div style="font-size: 2rem; font-weight: bold; color: #667eea;">
                                {st.session_state.program.patient_height}cm
                            </div>
                            <div style="color: #666;">Taille</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Modification des données
            with st.expander("Modifier les données"):
                new_weight = st.number_input(
                    "Nouveau poids (kg)", 
                    value=float(st.session_state.program.patient_weight), 
                    min_value=40.0, 
                    max_value=150.0,
                    step=0.5
                )
                
                new_height = st.number_input(
                    "Nouvelle taille (cm)", 
                    value=st.session_state.program.patient_height, 
                    min_value=140, 
                    max_value=220,
                    step=1
                )
                
                # Calcul IMC en temps réel
                imc = new_weight / ((new_height/100) ** 2)
                imc_color = "#4CAF50" if 18.5 <= imc <= 25 else "#FFC107" if 25 < imc <= 30 else "#ff6b6b"
                
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div>IMC Calculé</div>
                        <div style="font-size: 1.5rem; font-weight: bold; color: {imc_color};">
                            {imc:.1f}
                        </div>
                        <div style="font-size: 0.8rem; color: #666;">
                            {
                                "Normal" if 18.5 <= imc <= 25 else 
                                "Surpoids" if 25 < imc <= 30 else 
                                "Obésité" if imc > 30 else "Sous-poids"
                            }
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        with col2:
            st.markdown("#### 🏃 Profil Sportif")
            
            # Sélections avec emojis
            niveau_sportif = st.selectbox(
                "Niveau avant blessure",
                ["🟢 Loisir", "🔵 Régulier", "🟡 Compétition amateur", "🔴 Haut niveau"],
                index=1
            )
            
            sport_principal = st.selectbox(
                "Sport principal",
                ["⚽ Football", "🏉 Rugby", "🏀 Basketball", "🎾 Tennis", "⛷️ Ski", "🏃 Running", "🎯 Autres"],
                index=0
            )
            
            objectif_retour = st.selectbox(
                "Objectif de retour",
                ["😌 Loisir/Santé", "💪 Sport régulier", "🏆 Compétition", "🚀 Performance"],
                index=1
            )
            
            # Historique médical avec toggles modernes
            st.markdown("#### 🏥 Historique Médical")
            
            col_hist1, col_hist2 = st.columns(2)
            
            with col_hist1:
                premiere_rupture = st.checkbox("Première rupture LCA", value=True)
                chirurgie_anterieure = st.checkbox("Chirurgie genou antérieure", value=False)
            
            with col_hist2:
                lesions_associees = st.checkbox("Lésions associées", value=False)
                antecedents_autres = st.checkbox("Autres antécédents", value=False)
            
            if lesions_associees:
                lesions_type = st.multiselect(
                    "Type de lésions",
                    ["Ménisque", "Cartilage", "LLI", "LLE", "Autre"]
                )
        
        # Section additionnelle
        st.markdown("#### 📋 Informations Complémentaires")
        
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            profession = st.text_input("Profession", placeholder="Ex: Enseignant, Ingénieur...")
            lateralite = st.radio("Latéralité", ["Droitier", "Gaucher"], horizontal=True)
        
        with col_info2:
            genou_opere = st.radio("Genou opéré", ["Droit", "Gauche"], horizontal=True)
            type_greffe = st.selectbox(
                "Type de greffe",
                ["DIDT", "DT4", "Kenneth Jones", "DIDT+DT4", "Allogreffe", "Autre"]
            )
        
        # Bouton de sauvegarde stylé
        if st.button("💾 Sauvegarder le profil", type="primary", use_container_width=True):
            st.session_state.program.patient_weight = new_weight
            st.session_state.program.patient_height = new_height
            
            # Sauvegarder sur GitHub
            profile_data = {
                "patient_weight": new_weight,
                "patient_height": new_height,
                "niveau_sportif": niveau_sportif,
                "sport_principal": sport_principal,
                "objectif_retour": objectif_retour,
                "premiere_rupture": premiere_rupture,
                "chirurgie_anterieure": chirurgie_anterieure,
                "lesions_associees": lesions_associees,
                "profession": profession,
                "lateralite": lateralite,
                "genou_opere": genou_opere,
                "type_greffe": type_greffe
            }
            
            if st.session_state.github_storage.connected:
                with st.spinner("💾 Sauvegarde en cours..."):
                    if st.session_state.github_storage.save_user_profile(profile_data):
                        st.success("✅ Profil sauvegardé avec succès!")
                    else:
                        st.error("❌ Erreur lors de la sauvegarde")
            else:
                st.success("✅ Profil mis à jour localement!")
    
    with tab2:
        st.subheader("📅 Gestion du Planning")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 🗓️ Configuration des Dates")
            
            # Date de chirurgie avec visualisation
            current_surgery_date = st.session_state.program.surgery_date.date()
            new_surgery_date = st.date_input(
                "Date d'opération", 
                value=current_surgery_date,
                min_value=datetime(2025, 1, 1).date(),
                max_value=datetime(2026, 12, 31).date()
            )
            
            # Timeline visuelle
            today = datetime.now().date()
            if new_surgery_date > today:
                days_remaining = (new_surgery_date - today).days
                st.markdown(
                    f"""
                    <div class="modern-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                        <h3 style="margin: 0;">⏳ J-{days_remaining}</h3>
                        <p style="margin: 0.5rem 0 0 0;">avant l'opération</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                days_post = (today - new_surgery_date).days
                weeks_post = days_post // 7
                st.markdown(
                    f"""
                    <div class="modern-card" style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white;">
                        <h3 style="margin: 0;">📅 J+{days_post}</h3>
                        <p style="margin: 0.5rem 0 0 0;">post-opératoire (Semaine {weeks_post + 1})</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Jalons importants calculés
            st.markdown("#### 🎯 Jalons du Parcours")
            
            milestones = {
                "Mobilisation active": new_surgery_date + timedelta(days=7),
                "Charge complète": new_surgery_date + timedelta(days=21),
                "Début réathlétisation": new_surgery_date + timedelta(days=45),
                "Introduction pliométrie": new_surgery_date + timedelta(days=90),
                "Tests retour sport": new_surgery_date + timedelta(days=180),
                "Retour sport potentiel": new_surgery_date + timedelta(days=270)
            }
            
            for milestone, date in milestones.items():
                status = "✅" if date <= today else "⏳"
                days_diff = (date - today).days
                
                st.markdown(
                    f"""
                    <div class="modern-card" style="margin: 0.5rem 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>{status} {milestone}</strong>
                                <div style="font-size: 0.9rem; color: #666;">
                                    {date.strftime('%d/%m/%Y')}
                                </div>
                            </div>
                            <div style="text-align: right;">
                                {f"Dans {days_diff}j" if days_diff > 0 else "Complété" if days_diff < 0 else "Aujourd'hui"}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        with col2:
            st.markdown("#### ⏰ Préférences Horaires")
            
            # Jours d'entraînement avec interface moderne
            jours_semaine = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
            jours_preferes = st.multiselect(
                "Jours d'entraînement",
                jours_semaine,
                default=["Lun", "Mar", "Jeu", "Ven"]
            )
            
            # Visualisation des jours sélectionnés
            jours_html = ""
            for jour in jours_semaine:
                if jour in jours_preferes:
                    jours_html += f'<span class="progress-badge" style="margin: 2px;">{jour}</span>'
                else:
                    jours_html += f'<span style="display: inline-block; background: #e0e0e0; color: #999; padding: 0.3rem 0.6rem; border-radius: 15px; margin: 2px; font-size: 0.8rem;">{jour}</span>'
            
            st.markdown(
                f'<div style="text-align: center; margin: 1rem 0;">{jours_html}</div>',
                unsafe_allow_html=True
            )
            
            # Heure préférée avec slider
            heure_preferee = st.time_input(
                "Heure habituelle",
                value=datetime.strptime("18:00", "%H:%M").time()
            )
            
            # Durée de séance
            duree_seance = st.slider(
                "Durée moyenne (min)",
                min_value=30,
                max_value=120,
                value=60,
                step=15,
                format="%d min"
            )
            
            # Rappels avec toggles
            st.markdown("#### 🔔 Rappels")
            
            rappels_actifs = st.toggle("Activer les rappels", value=True)
            
            if rappels_actifs:
                rappel_avant = st.select_slider(
                    "Rappel avant séance",
                    options=[15, 30, 60, 120],
                    value=60,
                    format_func=lambda x: f"{x} min" if x < 60 else f"{x//60}h"
                )
        
        # Calendrier visuel du mois
        st.markdown("#### 📆 Vue Mensuelle")
        
        # Créer un calendrier simple pour le mois en cours
        import calendar
        
        cal = calendar.monthcalendar(today.year, today.month)
        month_name = calendar.month_name[today.month]
        
        calendar_html = f"""
        <div class="modern-card">
            <h4 style="text-align: center;">{month_name} {today.year}</h4>
            <table style="width: 100%; text-align: center;">
                <tr>
                    {''.join([f'<th style="padding: 0.5rem; color: #666;">{day}</th>' for day in ['L', 'M', 'M', 'J', 'V', 'S', 'D']])}
                </tr>
        """
        
        for week in cal:
            calendar_html += "<tr>"
            for day in week:
                if day == 0:
                    calendar_html += '<td style="padding: 0.5rem;"></td>'
                elif day == today.day:
                    calendar_html += f'<td style="padding: 0.5rem;"><div style="background: #667eea; color: white; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; margin: auto;">{day}</div></td>'
                else:
                    calendar_html += f'<td style="padding: 0.5rem;">{day}</td>'
            calendar_html += "</tr>"
        
        calendar_html += """
            </table>
        </div>
        """
        
        st.markdown(calendar_html, unsafe_allow_html=True)
        
        if st.button("📅 Sauvegarder le planning", type="primary", use_container_width=True):
            st.session_state.program.surgery_date = datetime.combine(new_surgery_date, datetime.min.time())
            st.success("✅ Planning mis à jour avec succès!")
    
    with tab3:
        st.subheader("💾 Gestion des Données")
        
        # Statistiques de stockage
        st.markdown("### 📊 Statistiques de Stockage")
        
        col1, col2, col3, col4 = st.columns(4)
        
        workout_count = len(st.session_state.workout_history)
        data_size = len(str(st.session_state.workout_history))
        
        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">💾</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{workout_count}</div>
                    <div style="color: #666;">Enregistrements</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">📦</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">{data_size/1024:.1f}KB</div>
                    <div style="color: #666;">Taille données</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            if st.session_state.github_storage.connected:
                sync_status = "✅ Synchronisé"
                sync_color = "#4CAF50"
            else:
                sync_status = "❌ Local"
                sync_color = "#ff6b6b"
            
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">☁️</div>
                    <div style="font-size: 1rem; font-weight: bold; color: {sync_color};">
                        {sync_status}
                    </div>
                    <div style="color: #666;">Statut Cloud</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            if workout_count > 0:
                last_backup = max([w['date'] for w in st.session_state.workout_history])
                days_since = (datetime.now() - last_backup).days
                backup_text = f"Il y a {days_since}j" if days_since > 0 else "Aujourd'hui"
            else:
                backup_text = "Jamais"
            
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size: 2rem;">🔄</div>
                    <div style="font-size: 1rem; font-weight: bold;">{backup_text}</div>
                    <div style="color: #666;">Dernière activité</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Export des données
        st.markdown("### 📤 Export des Données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Export Personnalisé")
            
            # Options d'export
            export_format = st.selectbox(
                "Format d'export",
                ["📄 CSV (Excel)", "📊 JSON (Données)", "📑 PDF (Rapport)", "📦 Archive complète"]
            )
            
            periode_export = st.selectbox(
                "Période",
                ["Tout l'historique", "30 derniers jours", "Phase actuelle", "Personnalisé"]
            )
            
            if periode_export == "Personnalisé":
                date_debut = st.date_input("Du", value=datetime.now().date() - timedelta(days=30))
                date_fin = st.date_input("Au", value=datetime.now().date())
            
            # Options supplémentaires
            include_options = st.multiselect(
                "Inclure",
                ["Exercices", "Évaluations", "Commentaires", "Graphiques"],
                default=["Exercices", "Évaluations"]
            )
            
            # Bouton d'export avec animation
            if st.button("📥 Générer l'Export", type="primary", use_container_width=True):
                with st.spinner("🔄 Préparation de l'export..."):
                    # Préparation des données
                    if st.session_state.workout_history:
                        df = pd.DataFrame(st.session_state.workout_history)
                        
                        # Filtrage selon la période
                        if periode_export == "30 derniers jours":
                            date_limite = datetime.now() - timedelta(days=30)
                            df_export = df[df['date'] >= date_limite]
                        elif periode_export == "Phase actuelle":
                            # Logique pour filtrer par phase
                            df_export = df
                        elif periode_export == "Personnalisé":
                            df_export = df[
                                (df['date'].dt.date >= date_debut) & 
                                (df['date'].dt.date <= date_fin)
                            ]
                        else:
                            df_export = df
                        
                        # Export selon le format
                        if "CSV" in export_format:
                            csv = df_export.to_csv(index=False)
                            st.download_button(
                                label="💾 Télécharger CSV",
                                data=csv,
                                file_name=f"rehab_lca_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                        
                        st.success(f"✅ Export généré: {len(df_export)} entrées")
                    else:
                        st.warning("Aucune donnée à exporter")
        
        with col2:
            st.markdown("#### 📥 Import & Restauration")
            
            uploaded_file = st.file_uploader(
                "Importer un fichier",
                type=['csv', 'json'],
                help="Restaurez vos données depuis une sauvegarde"
            )
            
            if uploaded_file is not None:
                # Aperçu du fichier
                st.markdown("##### 👁️ Aperçu du fichier")
                
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df_import = pd.read_csv(uploaded_file)
                    else:  # JSON
                        df_import = pd.read_json(uploaded_file)
                    
                    st.markdown(
                        f"""
                        <div class="modern-card">
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                                <div>
                                    <strong>📊 Entrées:</strong> {len(df_import)}
                                </div>
                                <div>
                                    <strong>📅 Période:</strong> {df_import['date'].min()} à {df_import['date'].max()}
                                </div>
                                <div>
                                    <strong>📋 Type:</strong> {uploaded_file.name.split('.')[-1].upper()}
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Options d'import
                    import_mode = st.radio(
                        "Mode d'import",
                        ["🔄 Remplacer toutes les données", "➕ Ajouter aux données existantes", "🔍 Aperçu seulement"],
                        index=2
                    )
                    
                    if import_mode != "🔍 Aperçu seulement":
                        if st.button("✅ Confirmer l'import", type="secondary"):
                            if "Remplacer" in import_mode:
                                st.session_state.workout_history = df_import.to_dict('records')
                                st.success(f"✅ Données remplacées: {len(df_import)} entrées")
                            else:  # Ajouter
                                existing_count = len(st.session_state.workout_history)
                                st.session_state.workout_history.extend(df_import.to_dict('records'))
                                st.success(f"✅ Données ajoutées: {len(df_import)} nouvelles entrées")
                            
                            st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'import: {str(e)}")
        
        # Maintenance des données
        st.markdown("### 🧹 Maintenance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Analyser les doublons", use_container_width=True):
                if st.session_state.workout_history:
                    # Logique simple de détection de doublons
                    df = pd.DataFrame(st.session_state.workout_history)
                    duplicates = df.duplicated(subset=['date', 'exercice', 'serie']).sum()
                    
                    if duplicates > 0:
                        st.warning(f"⚠️ {duplicates} doublons potentiels détectés")
                        if st.button("🧹 Nettoyer les doublons"):
                            df_clean = df.drop_duplicates(subset=['date', 'exercice', 'serie'])
                            st.session_state.workout_history = df_clean.to_dict('records')
                            st.success(f"✅ {duplicates} doublons supprimés")
                            st.rerun()
                    else:
                        st.success("✅ Aucun doublon détecté")
                else:
                    st.info("Aucune donnée à analyser")
        
        with col2:
            if st.button("🗑️ Réinitialiser tout", use_container_width=True):
                st.warning("⚠️ Cette action supprimera TOUTES vos données!")
                
                col_confirm1, col_confirm2 = st.columns(2)
                with col_confirm1:
                    if st.button("❌ Annuler", use_container_width=True):
                        st.info("Réinitialisation annulée")
                
                with col_confirm2:
                    if st.button("✅ Confirmer suppression", type="secondary", use_container_width=True):
                        st.session_state.workout_history = []
                        st.session_state.current_exercise_index = 0
                        st.session_state.current_set = 1
                        st.session_state.unlocked_achievements = set()
                        st.session_state.user_xp = 0
                        st.session_state.user_level = 1
                        st.success("✅ Toutes les données ont été réinitialisées")
                        time.sleep(1)
                        st.rerun()
        
        # Sauvegarde automatique
        st.markdown("### 🔄 Sauvegarde Automatique")
        
        auto_save = st.toggle("Activer la sauvegarde automatique", value=True)
        
        if auto_save:
            save_options = st.selectbox(
                "Fréquence de sauvegarde",
                ["Après chaque exercice", "Après chaque séance", "Quotidienne", "Hebdomadaire"]
            )
            
            st.info(f"💾 Les données seront sauvegardées automatiquement: {save_options}")
    
    with tab4:
        st.subheader("🎨 Préférences d'Interface")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎨 Apparence")
            
            # Thème avec preview
            theme = st.selectbox(
                "Thème d'interface",
                ["🌞 Clair", "🌙 Sombre", "🎨 Automatique"],
                index=2
            )
            
            # Preview du thème
            theme_colors = {
                "🌞 Clair": {"bg": "#ffffff", "text": "#000000", "accent": "#667eea"},
                "🌙 Sombre": {"bg": "#1a1a1a", "text": "#ffffff", "accent": "#9b88ff"},
                "🎨 Automatique": {"bg": "#f0f2f6", "text": "#333333", "accent": "#667eea"}
            }
            
            colors = theme_colors[theme]
            st.markdown(
                f"""
                <div class="modern-card" style="background: {colors['bg']}; border: 2px solid {colors['accent']};">
                    <h5 style="color: {colors['text']};">Aperçu du thème</h5>
                    <p style="color: {colors['text']};">Voici à quoi ressemblera l'interface</p>
                    <button style="background: {colors['accent']}; color: white; border: none; 
                                   padding: 0.5rem 1rem; border-radius: 8px;">
                        Bouton exemple
                    </button>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Taille de police
            taille_police = st.select_slider(
                "Taille du texte",
                options=["Très petit", "Petit", "Normal", "Grand", "Très grand"],
                value="Normal"
            )
            
            # Animations
            animations = st.toggle("Animations activées", value=True)
            if animations:
                animation_speed = st.select_slider(
                    "Vitesse des animations",
                    options=["Lente", "Normale", "Rapide"],
                    value="Normale"
                )
            
            # Mode compact
            mode_compact = st.toggle("Mode compact", value=False)
            if mode_compact:
                st.info("💡 L'interface sera plus condensée pour afficher plus d'informations")
        
        with col2:
            st.markdown("#### 📊 Affichage des Données")
            
            # Unités de mesure
            unites = st.radio(
                "Système d'unités",
                ["🇫🇷 Métrique (kg, cm)", "🇺🇸 Impérial (lbs, in)"],
                index=0
            )
            
            # Format de date
            format_date = st.selectbox(
                "Format de date",
                ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD", "DD Month YYYY"],
                index=0
            )
            
            # Exemple de date
            example_date = datetime.now()
            date_formats = {
                "DD/MM/YYYY": example_date.strftime("%d/%m/%Y"),
                "MM/DD/YYYY": example_date.strftime("%m/%d/%Y"),
                "YYYY-MM-DD": example_date.strftime("%Y-%m-%d"),
                "DD Month YYYY": example_date.strftime("%d %B %Y")
            }
            
            st.caption(f"Exemple: {date_formats[format_date]}")
            
            # Graphiques
            st.markdown("#### 📈 Graphiques")
            
            graphiques_3d = st.checkbox("Graphiques 3D", value=False)
            couleurs_daltonien = st.checkbox("Palette adaptée daltoniens", value=False)
            
            # Densité d'information
            densite_info = st.select_slider(
                "Densité d'information",
                options=["Minimale", "Normale", "Détaillée", "Complète"],
                value="Normale"
            )
        
        # Langue et localisation
        st.markdown("### 🌍 Langue et Localisation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            langue = st.selectbox(
                "Langue de l'interface",
                ["🇫🇷 Français", "🇬🇧 English", "🇪🇸 Español", "🇩🇪 Deutsch"],
                index=0
            )
            
            timezone = st.selectbox(
                "Fuseau horaire",
                ["Europe/Paris", "Europe/London", "America/New_York", "Asia/Tokyo"],
                index=0
            )
        
        with col2:
            # Sons
            st.markdown("#### 🔊 Sons")
            
            sons_actifs = st.toggle("Sons activés", value=True)
            
            if sons_actifs:
                volume = st.slider("Volume", 0, 100, 50, format="%d%%")
                
                sons_options = {
                    "Fin de timer": True,
                    "Achievement débloqué": True,
                    "Nouveau record": True,
                    "Erreur": False
                }
                
                for son, default in sons_options.items():
                    st.checkbox(son, value=default, key=f"son_{son}")
        
        # Bouton de sauvegarde des préférences
        if st.button("🎨 Appliquer les préférences", type="primary", use_container_width=True):
            # Ici on sauvegarderait les préférences
            st.success("✅ Préférences sauvegardées et appliquées!")
    
    with tab5:
        st.subheader("🔔 Paramètres de Notifications")
        
        # État global des notifications
        notifications_actives = st.toggle("Activer toutes les notifications", value=True)
        
        if notifications_actives:
            # Types de notifications
            st.markdown("### 📱 Types de Notifications")
            
            notification_types = {
                "Rappels de séance": {
                    "icon": "🏋️",
                    "desc": "Notification avant chaque séance programmée",
                    "default": True,
                    "options": ["15 min avant", "30 min avant", "1h avant", "2h avant"]
                },
                "Jours de repos": {
                    "icon": "😴",
                    "desc": "Rappel les jours sans entraînement",
                    "default": False,
                    "options": ["Matin (9h)", "Midi (12h)", "Soir (18h)"]
                },
                "Tests d'évaluation": {
                    "icon": "🧪",
                    "desc": "Rappel pour les tests de progression",
                    "default": True,
                    "options": ["1 jour avant", "3 jours avant", "1 semaine avant"]
                },
                "Milestones": {
                    "icon": "🎯",
                    "desc": "Célébration des étapes importantes",
                    "default": True,
                    "options": ["Instantané", "Résumé quotidien", "Résumé hebdomadaire"]
                },
                "Achievements": {
                    "icon": "🏅",
                    "desc": "Nouveaux achievements débloqués",
                    "default": True,
                    "options": ["Instantané", "Groupé par session"]
                }
            }
            
            for notif_type, config in notification_types.items():
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    enabled = st.checkbox(
                        f"{config['icon']} {notif_type}",
                        value=config['default'],
                        help=config['desc']
                    )
                
                with col2:
                    if enabled:
                        st.selectbox(
                            "Timing",
                            config['options'],
                            key=f"notif_timing_{notif_type}",
                            label_visibility="collapsed"
                        )
            
            # Canaux de notification
            st.markdown("### 📬 Canaux de Notification")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📱 Push Mobile")
                push_enabled = st.toggle("Notifications push", value=True)
                
                if push_enabled:
                    st.info("📲 Scannez le QR code dans l'app mobile pour activer")
                    # Ici on afficherait un QR code
                
                st.markdown("#### 📧 Email")
                email_enabled = st.toggle("Notifications email", value=False)
                
                if email_enabled:
                    email = st.text_input("Adresse email", placeholder="votre@email.com")
                    email_frequency = st.selectbox(
                        "Fréquence",
                        ["Instantané", "Résumé quotidien", "Résumé hebdomadaire"]
                    )
            
            with col2:
                st.markdown("#### 💬 SMS")
                sms_enabled = st.toggle("Notifications SMS", value=False)
                
                if sms_enabled:
                    phone = st.text_input("Numéro de téléphone", placeholder="+33 6 XX XX XX XX")
                    st.warning("💰 Des frais peuvent s'appliquer")
                
                st.markdown("#### 🔔 Navigateur")
                browser_enabled = st.toggle("Notifications navigateur", value=True)
                
                if browser_enabled:
                    if st.button("Autoriser les notifications"):
                        st.info("✅ Autorisez les notifications dans votre navigateur")
            
            # Horaires de notification
            st.markdown("### ⏰ Horaires de Notification")
            
            col1, col2 = st.columns(2)
            
            with col1:
                heure_debut = st.time_input(
                    "Ne pas déranger avant",
                    value=datetime.strptime("08:00", "%H:%M").time()
                )
            
            with col2:
                heure_fin = st.time_input(
                    "Ne pas déranger après",
                    value=datetime.strptime("22:00", "%H:%M").time()
                )
            
            # Mode ne pas déranger
            st.markdown("### 🌙 Mode Ne Pas Déranger")
            
            dnd_enabled = st.toggle("Activer le mode Ne Pas Déranger", value=False)
            
            if dnd_enabled:
                dnd_options = st.multiselect(
                    "Activer automatiquement",
                    ["La nuit (22h-8h)", "Pendant les séances", "Weekend", "Jours fériés"],
                    default=["La nuit (22h-8h)"]
                )
        
        # Test de notification
        st.markdown("### 🧪 Test de Notification")
        
        if st.button("📤 Envoyer une notification test", use_container_width=True):
            st.success("✅ Notification test envoyée!")
            st.toast("🔔 Ceci est une notification test!", icon='🎉')
    
    # Informations système
    st.markdown("---")
    st.markdown("### 🔧 Informations Système")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div>📱 Version</div>
                <div style="font-size: 1.2rem; font-weight: bold;">2.5.0</div>
                <div style="font-size: 0.8rem; color: #666;">Dernière màj: 01/2025</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div>🔌 API</div>
                <div style="font-size: 1.2rem; font-weight: bold; color: #4CAF50;">En ligne</div>
                <div style="font-size: 0.8rem; color: #666;">Latence: 45ms</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div>💾 Cache</div>
                <div style="font-size: 1.2rem; font-weight: bold;">12.3 MB</div>
                <div style="font-size: 0.8rem; color: #666;">
                    <a href="#" style="color: #667eea;">Vider le cache</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <div>🌐 Navigateur</div>
                <div style="font-size: 1.2rem; font-weight: bold;">Chrome</div>
                <div style="font-size: 0.8rem; color: #666;">v120.0.0</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Footer avec liens utiles
    st.markdown(
        """
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: #f0f2f6; border-radius: 10px;">
            <p style="margin: 0;">
                <a href="#" style="margin: 0 1rem;">📖 Documentation</a>
                <a href="#" style="margin: 0 1rem;">💬 Support</a>
                <a href="#" style="margin: 0 1rem;">🐛 Signaler un bug</a>
                <a href="#" style="margin: 0 1rem;">💡 Suggestions</a>
            </p>
            <p style="margin-top: 1rem; color: #666; font-size: 0.9rem;">
                Développé avec ❤️ pour optimiser votre rééducation
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Point d'entrée principal
if __name__ == "__main__":
    main()                    
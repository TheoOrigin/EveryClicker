import json
import os
import threading
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

# Virtual Keycodes mapping
VK_MAP = {
    0x01: "Clic Gauche",
    0x02: "Clic Droit",
    0x04: "Clic Milieu",
    0x08: "Retour arrière",
    0x09: "Tab",
    0x0D: "Entrée",
    0x10: "Shift",
    0x11: "Ctrl",
    0x12: "Alt",
    0x13: "Pause",
    0x14: "Verr Maj",
    0x1B: "Échap",
    0x20: "Espace",
    0x21: "Page Haut",
    0x22: "Page Bas",
    0x23: "Fin",
    0x24: "Origine",
    0x25: "Flèche Gauche",
    0x26: "Flèche Haut",
    0x27: "Flèche Droite",
    0x28: "Flèche Bas",
    0x2D: "Inser",
    0x2E: "Suppr",
    # F1 - F12
    0x70: "F1", 0x71: "F2", 0x72: "F3", 0x73: "F4", 0x74: "F5", 0x75: "F6",
    0x76: "F7", 0x77: "F8", 0x78: "F9", 0x79: "F10", 0x7A: "F11", 0x7B: "F12",
    # Numpad
    0x60: "Num 0", 0x61: "Num 1", 0x62: "Num 2", 0x63: "Num 3", 0x64: "Num 4",
    0x65: "Num 5", 0x66: "Num 6", 0x67: "Num 7", 0x68: "Num 8", 0x69: "Num 9",
    0x6A: "Num *", 0x6B: "Num +", 0x6D: "Num -", 0x6E: "Num .", 0x6F: "Num /",
}

def get_key_name(vk_code):
    if not vk_code:
        return "Aucune"
    if vk_code in VK_MAP:
        return VK_MAP[vk_code]
    
    # Query OS for localized key name
    scancode = user32.MapVirtualKeyW(vk_code, 0)
    lParam = scancode << 16
    if vk_code in [0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2D, 0x2E]:
        lParam |= (1 << 24)
        
    buf = ctypes.create_unicode_buffer(128)
    res = user32.GetKeyNameTextW(lParam, buf, 128)
    if res > 0:
        return buf.value.capitalize()
    
    if 32 < vk_code < 127:
        return chr(vk_code).upper()
        
    return f"Touche {vk_code}"

# Complete localization dictionary for FR, EN, ES
TRANSLATIONS = {
    "fr": {
        "title": "EveryClicker",
        "subtitle": "Mouse & Keyboard clicker",
        "tab_clicker": "Clicker",
        "tab_macro": "Macros",
        "sec_action": "1. ACTION À SIMULER",
        "sec_interval": "2. INTERVALLE ENTRE LES ENTRÉES",
        "sec_stop": "3. CONDITION D'ARRÊT",
        "sec_hotkey": "4. CONTRÔLE GLOBAL D'ACTIVATION",
        "button": "Bouton :",
        "click_type": "Type :",
        "key": "Touche :",
        "left": "Gauche",
        "right": "Droit",
        "middle": "Milieu",
        "single": "Simple",
        "double": "Double",
        "mouse": "Souris",
        "keyboard": "Clavier",
        "change_key": "Modifier la touche",
        "press_key": "Pressez une touche...",
        "examples_ms": "Exemples : 1.0 ms = 1000 clics/s | 100.0 ms = 10 clics/s",
        "stop_infinite": "Infini",
        "stop_cycles": "Cycles",
        "stop_timer": "Minuteur",
        "lbl_cycles": "Répéter le clic :",
        "lbl_cycles_unit": "fois (cycles)",
        "lbl_timer": "Durée :",
        "lbl_hotkey": "Raccourci Global :",
        "btn_change_hotkey": "Changer le raccourci",
        "status_inactive": "Statut : INACTIF",
        "status_active_timer": "Statut : ACTIF ({time} restants)",
        "status_active_cycles": "Statut : ACTIF ({cycles} cycles restants)",
        "status_active_inf": "Statut : ACTIF (Indéfini)",
        "btn_start": "DÉMARRER",
        "btn_stop": "ARRÊTER",
        "btn_raccourci": "Raccourci :",
        "err_same_key": "Erreur : La touche '{key}' ne peut pas être à la fois le raccourci et la touche simulée !",
        "err_interval": "Erreur : L'intervalle doit être supérieur à 0 !",
        "err_cycles": "Erreur : Le nombre de cycles doit être un entier supérieur à 0 !",
        "err_timer": "Erreur : La durée doit être supérieure à 0 seconde !",
        
        # Presets section
        "sec_presets": "PRESETS DE CONFIGURATION",
        "lbl_preset": "Preset :",
        "btn_save_preset": "Enregistrer",
        "btn_del_preset": "Supprimer",
        "new_item": "+ Nouveau...",
        "btn_cancel": "Annuler",
        
        # Macro section
        "macro_sec_controls": "1. ENREGISTREMENT ET LECTURE",
        "macro_btn_record": "Enregistrer la Macro",
        "macro_btn_stop_record": "Arrêter l'enregistrement",
        "macro_btn_clear": "Effacer",
        "macro_btn_save_macro": "Enregistrer",
        "macro_btn_del_macro": "Supprimer",
        "macro_sec_timing": "2. GESTION DES DÉLAIS",
        "macro_radio_real": "Délai enregistré (temps réel)",
        "macro_radio_fixed": "Délai fixe entre chaque touche (ms)",
        "macro_sec_stop": "3. CONDITION D'ARRÊT LECTURE",
        "macro_lbl_actions": "Actions enregistrées : {count}",
        "macro_sec_save": "MACROS ENREGISTRÉES",
        "macro_lbl_macro_name": "Macro :",
        "macro_err_no_actions": "Erreur : Aucune touche n'a été enregistrée !",
        "macro_err_name_empty": "Erreur : Veuillez entrer un nom pour la macro !",
        "macro_err_fixed_delay": "Erreur : Le délai fixe doit être supérieur à 0 !",
        "macro_lbl_status_recording": "Enregistrement en cours... Pressez '{hotkey}' pour arrêter.",
        "macro_lbl_status_active_cycles": "Lecture macro en cours... ({cycles} cycles restants)",
        "macro_lbl_status_active_inf": "Lecture macro en cours... (Infini)",
        
        # Silent section
        "tab_silent": "Silencieux",
        "sec_interval_min": "2. INTERVALLE MINIMUM (A)",
        "sec_interval_max": "3. INTERVALLE MAXIMUM (B)",
        "sec_random_dist": "4. DISTRIBUTION DE L'ALÉATOIRE",
        "lbl_rand_type": "Type de Random :",
        "rand_uniform": "Totalement Aléatoire",
        "rand_biased": "Biaisé (Triché)",
        "lbl_bias_split": "Seuil de coupure (C) :",
        "lbl_bias_percent": "Pourcentage (P) :",
        "lbl_bias_direction": "Zone ciblée :",
        "bias_above": "Au-dessus du seuil",
        "bias_below": "En-dessous du seuil",
        "status_active_silent": "Statut : ACTIF (Silencieux)",
        "sec_stop_silent": "5. CONDITION D'ARRÊT"
    },
    "en": {
        "title": "EveryClicker",
        "subtitle": "Mouse & Keyboard clicker",
        "tab_clicker": "Clicker",
        "tab_macro": "Macros",
        "sec_action": "1. ACTION TO SIMULATE",
        "sec_interval": "2. INTERVAL BETWEEN INPUTS",
        "sec_stop": "3. STOP CONDITION",
        "sec_hotkey": "4. GLOBAL ACTIVATION HOTKEY",
        "button": "Button:",
        "click_type": "Type:",
        "key": "Key:",
        "left": "Left",
        "right": "Right",
        "middle": "Middle",
        "single": "Single",
        "double": "Double",
        "mouse": "Mouse",
        "keyboard": "Keyboard",
        "change_key": "Change Key",
        "press_key": "Press a key...",
        "examples_ms": "Examples: 1.0 ms = 1000 clicks/s | 100.0 ms = 10 clicks/s",
        "stop_infinite": "Infinite",
        "stop_cycles": "Cycles",
        "stop_timer": "Timer",
        "lbl_cycles": "Repeat click:",
        "lbl_cycles_unit": "times (cycles)",
        "lbl_timer": "Duration:",
        "lbl_hotkey": "Global Hotkey:",
        "btn_change_hotkey": "Change Hotkey",
        "status_inactive": "Status: INACTIVE",
        "status_active_timer": "Status: ACTIVE ({time} remaining)",
        "status_active_cycles": "Status: ACTIVE ({cycles} cycles remaining)",
        "status_active_inf": "Status: ACTIVE (Infinite)",
        "btn_start": "START",
        "btn_stop": "STOP",
        "btn_raccourci": "Shortcut:",
        "err_same_key": "Error: Key '{key}' cannot be both the shortcut and the simulated key!",
        "err_interval": "Error: Interval must be greater than 0!",
        "err_cycles": "Error: Cycles count must be an integer greater than 0!",
        "err_timer": "Error: Duration must be greater than 0 seconds!",
        
        # Presets section
        "sec_presets": "CONFIGURATION PRESETS",
        "lbl_preset": "Preset:",
        "btn_save_preset": "Save",
        "btn_del_preset": "Delete",
        "new_item": "+ New...",
        "btn_cancel": "Cancel",
        
        # Macro section
        "macro_sec_controls": "1. RECORDING & PLAYBACK",
        "macro_btn_record": "Record Macro",
        "macro_btn_stop_record": "Stop Recording",
        "macro_btn_clear": "Clear",
        "macro_btn_save_macro": "Save",
        "macro_btn_del_macro": "Delete",
        "macro_sec_timing": "2. TIMING SETTINGS",
        "macro_radio_real": "Recorded delay (real-time)",
        "macro_radio_fixed": "Fixed delay between keys (ms)",
        "macro_sec_stop": "3. PLAYBACK STOP CONDITION",
        "macro_lbl_actions": "Recorded actions: {count}",
        "macro_sec_save": "SAVED MACROS",
        "macro_lbl_macro_name": "Macro:",
        "macro_err_no_actions": "Error: No keys have been recorded!",
        "macro_err_name_empty": "Error: Please enter a name for the macro!",
        "macro_err_fixed_delay": "Error: Fixed delay must be greater than 0!",
        "macro_lbl_status_recording": "Recording... Press '{hotkey}' to stop.",
        "macro_lbl_status_active_cycles": "Playing macro... ({cycles} cycles remaining)",
        "macro_lbl_status_active_inf": "Playing macro... (Infinite)",
        
        # Silent section
        "tab_silent": "Silent",
        "sec_interval_min": "2. MINIMUM INTERVAL (A)",
        "sec_interval_max": "3. MAXIMUM INTERVAL (B)",
        "sec_random_dist": "4. RANDOM DISTRIBUTION",
        "lbl_rand_type": "Random Type:",
        "rand_uniform": "Fully Random",
        "rand_biased": "Biased (Cheated)",
        "lbl_bias_split": "Split threshold (C):",
        "lbl_bias_percent": "Percentage (P):",
        "lbl_bias_direction": "Targeted area:",
        "bias_above": "Above threshold",
        "bias_below": "Below threshold",
        "status_active_silent": "Status: ACTIVE (Silent)",
        "sec_stop_silent": "5. STOP CONDITION"
    },
    "es": {
        "title": "EveryClicker",
        "subtitle": "Mouse & Keyboard clicker",
        "tab_clicker": "Clicker",
        "tab_macro": "Macros",
        "sec_action": "1. ACCIÓN A SIMULAR",
        "sec_interval": "2. INTERVALO ENTRE ENTRADAS",
        "sec_stop": "3. CONDICIÓN DE PARADA",
        "sec_hotkey": "4. ATRAJO DE ACTIVACIÓN GLOBAL",
        "button": "Botón:",
        "click_type": "Tipo:",
        "key": "Tecla:",
        "left": "Izquierda",
        "right": "Derecha",
        "middle": "Centro",
        "single": "Simple",
        "double": "Doble",
        "mouse": "Ratón",
        "keyboard": "Teclado",
        "change_key": "Cambiar tecla",
        "press_key": "Presione una tecla...",
        "examples_ms": "Ejemplos: 1.0 ms = 1000 clics/s | 100.0 ms = 10 clics/s",
        "stop_infinite": "Infinito",
        "stop_cycles": "Ciclos",
        "stop_timer": "Temporizador",
        "lbl_cycles": "Repetir clic:",
        "lbl_cycles_unit": "veces (ciclos)",
        "lbl_timer": "Duración:",
        "lbl_hotkey": "Atajo Global:",
        "btn_change_hotkey": "Cambiar atajo",
        "status_inactive": "Estado: INACTIVO",
        "status_active_timer": "Estado: ACTIVO ({time} restantes)",
        "status_active_cycles": "Estado: ACTIVO ({cycles} ciclos restantes)",
        "status_active_inf": "Estado: ACTIVO (Infinito)",
        "btn_start": "INICIAR",
        "btn_stop": "DETENER",
        "btn_raccourci": "Atajo:",
        "err_same_key": "Error: ¡La tecla '{key}' no puede ser tanto el atajo como la tecla simulada!",
        "err_interval": "Error: ¡El intervalo debe ser mayor que 0!",
        "err_cycles": "Error: ¡El número de ciclos debe ser un entero mayor que 0!",
        "err_timer": "Error: ¡La duración debe ser mayor que 0 segundos!",
        
        # Presets section
        "sec_presets": "PRESETS DE CONFIGURACIÓN",
        "lbl_preset": "Preset:",
        "btn_save_preset": "Guardar",
        "btn_del_preset": "Eliminar",
        "new_item": "+ Nuevo...",
        "btn_cancel": "Cancelar",
        
        # Macro section
        "macro_sec_controls": "1. GRABACIÓN Y REPRODUCCIÓN",
        "macro_btn_record": "Grabar Macro",
        "macro_btn_stop_record": "Detener Grabación",
        "macro_btn_clear": "Limpiar",
        "macro_btn_save_macro": "Guardar",
        "macro_btn_del_macro": "Eliminar",
        "macro_sec_timing": "2. GESTIÓN DE TIEMPOS",
        "macro_radio_real": "Retraso grabado (tiempo real)",
        "macro_radio_fixed": "Retraso fijo entre teclas (ms)",
        "macro_sec_stop": "3. CONDICIÓN DE PARADA DE LECTURA",
        "macro_lbl_actions": "Acciones grabadas: {count}",
        "macro_sec_save": "MACROS GUARDADAS",
        "macro_lbl_macro_name": "Macro:",
        "macro_err_no_actions": "Error: ¡No se ha grabado ninguna tecla!",
        "macro_err_name_empty": "Error: ¡Por favor ingrese un nombre para la macro!",
        "macro_err_fixed_delay": "Error: ¡El retraso fijo debe ser mayor que 0!",
        "macro_lbl_status_recording": "Grabando... Presione '{hotkey}' para detener.",
        "macro_lbl_status_active_cycles": "Reproduciendo macro... ({cycles} ciclos restantes)",
        "macro_lbl_status_active_inf": "Reproduciendo macro... (Infinito)",
        
        # Silent section
        "tab_silent": "Silencioso",
        "sec_interval_min": "2. INTERVALO MÍNIMO (A)",
        "sec_interval_max": "3. INTERVALO MÁXIMO (B)",
        "sec_random_dist": "4. DISTRIBUCIÓN DEL RANDOM",
        "lbl_rand_type": "Tipo de Random:",
        "rand_uniform": "Totalmente Aleatorio",
        "rand_biased": "Sesgado (Con trampa)",
        "lbl_bias_split": "Límite de corte (C):",
        "lbl_bias_percent": "Porcentaje (P):",
        "lbl_bias_direction": "Zona orientada:",
        "bias_above": "Por encima del límite",
        "bias_below": "Por debajo del límite",
        "status_active_silent": "Estado: ACTIVO (Silencioso)",
        "sec_stop_silent": "5. CONDICIÓN DE PARADA"
    }
}

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.lock = threading.Lock()
        
        # Default settings
        self.data = {
            "language": "fr",
            "hotkey": 0x75,  # F6
            "clicker": {
                "mode": "mouse",
                "button": "left",
                "double": False,
                "keyboard_vk": 0x20,  # Space
                "interval_ms": 100.0,
                "stop_mode": "Infini",
                "cycles": 100,
                "duration_h": 0,
                "duration_m": 10,
                "duration_s": 0
            },
            "presets": [
                {
                    "name": "Minecraft Clicker (12 CPS)",
                    "interval_ms": 83.3,
                    "stop_mode": "Infini"
                },
                {
                    "name": "Rapid Fire (100 CPS)",
                    "interval_ms": 10.0,
                    "stop_mode": "Infini"
                },
                {
                    "name": "AFK Timer (5 min)",
                    "interval_ms": 1000.0,
                    "stop_mode": "Minuteur",
                    "duration_h": 0,
                    "duration_m": 5,
                    "duration_s": 0
                }
            ],
            "macros": {},
            "silent": {
                "mode": "mouse",
                "button": "left",
                "double": False,
                "keyboard_vk": 0x20,
                "min_interval_ms": 10.0,
                "max_interval_ms": 100.0,
                "bias_mode": "uniform",
                "bias_split_ms": 70.0,
                "bias_percent": 70,
                "bias_direction": "above",
                "stop_mode": "Infini",
                "cycles": 100,
                "duration_h": 0,
                "duration_m": 10,
                "duration_s": 0
            }
        }
        self.load()

    def load(self):
        with self.lock:
            if os.path.exists(self.filename):
                try:
                    with open(self.filename, "r", encoding="utf-8") as f:
                        loaded_data = json.load(f)
                        # Merge dictionary to keep defaults in case of missing keys
                        self._merge_dicts(self.data, loaded_data)
                except Exception as e:
                    print(f"Error loading settings: {e}")

    def save(self):
        with self.lock:
            try:
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Error saving settings: {e}")

    def _merge_dicts(self, target, source):
        for k, v in source.items():
            if k in target and isinstance(target[k], dict) and isinstance(v, dict):
                self._merge_dicts(target[k], v)
            else:
                target[k] = v

    def get_text(self, key, **kwargs):
        lang = self.data.get("language", "fr")
        if lang not in TRANSLATIONS:
            lang = "fr"
        text = TRANSLATIONS[lang].get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass
        return text

    def set_language(self, lang):
        if lang in ["fr", "en", "es"]:
            self.data["language"] = lang
            self.save()

    def get_language(self):
        return self.data.get("language", "fr")

    def get_hotkey(self):
        return self.data.get("hotkey", 0x75)

    def set_hotkey(self, vk):
        self.data["hotkey"] = vk
        self.save()

    # Presets management
    def get_presets(self):
        return self.data.get("presets", [])

    def add_preset(self, preset_dict):
        # Remove if name exists already to overwrite
        self.data["presets"] = [p for p in self.data["presets"] if p["name"] != preset_dict["name"]]
        self.data["presets"].append(preset_dict)
        self.save()

    def delete_preset(self, name):
        self.data["presets"] = [p for p in self.data["presets"] if p["name"] != name]
        self.save()

    # Macros management
    def get_macros(self):
        return self.data.get("macros", {})

    def add_macro(self, name, actions):
        self.data["macros"][name] = actions
        self.save()

    def delete_macro(self, name):
        if name in self.data["macros"]:
            del self.data["macros"][name]
            self.save()

import tkinter as tk
import customtkinter as ctk
from settings import get_key_name

class SilentClickerFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.engine = app.engine
        
        self.recording_target_key = False
        
        self.create_widgets()
        self.refresh_texts()
        self.load_settings()

    def create_widgets(self):
        # -----------------------------------------
        # Card 1: Configuration de la Cible
        # -----------------------------------------
        self.card_target = ctk.CTkFrame(self)
        self.card_target.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_action = ctk.CTkLabel(self.card_target, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_action.grid(row=0, column=0, columnspan=2, padx=15, pady=(5, 2), sticky="w")
        
        self.btn_segmented_mode = ctk.CTkSegmentedButton(self.card_target, values=["Souris", "Clavier"], command=self.on_mode_changed)
        self.btn_segmented_mode.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="ew")
        
        # Mouse sub-frame
        self.frame_mouse = ctk.CTkFrame(self.card_target, fg_color="transparent")
        self.frame_mouse.grid(row=2, column=0, columnspan=2, padx=15, pady=(2, 5), sticky="ew")
        
        self.lbl_btn = ctk.CTkLabel(self.frame_mouse, text="Bouton:")
        self.lbl_btn.grid(row=0, column=0, padx=(0, 8), pady=3, sticky="w")
        self.combo_button = ctk.CTkComboBox(self.frame_mouse, values=["Gauche", "Droit", "Milieu"], width=100, command=self.on_mouse_config_changed)
        self.combo_button.grid(row=0, column=1, padx=8, pady=3, sticky="w")
        
        self.lbl_click_type = ctk.CTkLabel(self.frame_mouse, text="Type:")
        self.lbl_click_type.grid(row=0, column=2, padx=(15, 8), pady=3, sticky="w")
        self.combo_click_type = ctk.CTkComboBox(self.frame_mouse, values=["Simple", "Double"], width=100, command=self.on_mouse_config_changed)
        self.combo_click_type.grid(row=0, column=3, padx=8, pady=3, sticky="w")
        
        # Keyboard sub-frame (hidden by default)
        self.frame_keyboard = ctk.CTkFrame(self.card_target, fg_color="transparent")
        
        self.lbl_target_k = ctk.CTkLabel(self.frame_keyboard, text="Touche :")
        self.lbl_target_k.grid(row=0, column=0, padx=(0, 8), pady=3, sticky="w")
        self.lbl_target_key_display = ctk.CTkLabel(self.frame_keyboard, text="Espace", font=ctk.CTkFont(weight="bold"), text_color="#2ecc71")
        self.lbl_target_key_display.grid(row=0, column=1, padx=8, pady=3, sticky="w")
        
        self.btn_record_target_key = ctk.CTkButton(self.frame_keyboard, text="Modifier", command=self.start_recording_target_key, width=120)
        self.btn_record_target_key.grid(row=0, column=2, padx=15, pady=3, sticky="w")

        # -----------------------------------------
        # Card 2: Intervalle Minimum (A)
        # -----------------------------------------
        self.card_speed_min = ctk.CTkFrame(self)
        self.card_speed_min.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_interval_min = ctk.CTkLabel(self.card_speed_min, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_interval_min.grid(row=0, column=0, columnspan=5, padx=15, pady=(5, 2), sticky="w")
        
        self.slider_ms_min = ctk.CTkSlider(self.card_speed_min, from_=1.0, to=2000.0, number_of_steps=1999, width=220, command=self.on_slider_min_changed)
        self.slider_ms_min.grid(row=1, column=0, padx=(15, 10), pady=5, sticky="w")
        
        self.entry_ms_min = ctk.CTkEntry(self.card_speed_min, width=70, placeholder_text="10")
        self.entry_ms_min.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_ms_min.bind("<KeyRelease>", self.on_entry_min_changed)
        
        self.lbl_ms_unit_min = ctk.CTkLabel(self.card_speed_min, text="ms", text_color="gray")
        self.lbl_ms_unit_min.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        self.entry_cps_min = ctk.CTkEntry(self.card_speed_min, width=70, placeholder_text="CPS", text_color="#2ecc71", font=ctk.CTkFont(weight="bold"))
        self.entry_cps_min.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.entry_cps_min.bind("<KeyRelease>", self.on_entry_cps_min_changed)
        
        self.lbl_cps_unit_min = ctk.CTkLabel(self.card_speed_min, text="cps", text_color="gray")
        self.lbl_cps_unit_min.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        # -----------------------------------------
        # Card 3: Intervalle Maximum (B)
        # -----------------------------------------
        self.card_speed_max = ctk.CTkFrame(self)
        self.card_speed_max.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_interval_max = ctk.CTkLabel(self.card_speed_max, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_interval_max.grid(row=0, column=0, columnspan=5, padx=15, pady=(5, 2), sticky="w")
        
        self.slider_ms_max = ctk.CTkSlider(self.card_speed_max, from_=1.0, to=2000.0, number_of_steps=1999, width=220, command=self.on_slider_max_changed)
        self.slider_ms_max.grid(row=1, column=0, padx=(15, 10), pady=5, sticky="w")
        
        self.entry_ms_max = ctk.CTkEntry(self.card_speed_max, width=70, placeholder_text="100")
        self.entry_ms_max.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_ms_max.bind("<KeyRelease>", self.on_entry_max_changed)
        
        self.lbl_ms_unit_max = ctk.CTkLabel(self.card_speed_max, text="ms", text_color="gray")
        self.lbl_ms_unit_max.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        self.entry_cps_max = ctk.CTkEntry(self.card_speed_max, width=70, placeholder_text="CPS", text_color="#2ecc71", font=ctk.CTkFont(weight="bold"))
        self.entry_cps_max.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.entry_cps_max.bind("<KeyRelease>", self.on_entry_cps_max_changed)
        
        self.lbl_cps_unit_max = ctk.CTkLabel(self.card_speed_max, text="cps", text_color="gray")
        self.lbl_cps_unit_max.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        # -----------------------------------------
        # Card 4: Distribution de l'Aléatoire (Random Biaisé / Triché)
        # -----------------------------------------
        self.card_rand_dist = ctk.CTkFrame(self)
        self.card_rand_dist.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_random_dist = ctk.CTkLabel(self.card_rand_dist, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_random_dist.grid(row=0, column=0, columnspan=5, padx=15, pady=(5, 2), sticky="w")
        
        self.lbl_rand_type = ctk.CTkLabel(self.card_rand_dist, text="Type de Random:")
        self.lbl_rand_type.grid(row=1, column=0, padx=(15, 5), pady=4, sticky="w")
        self.btn_segmented_rand = ctk.CTkSegmentedButton(self.card_rand_dist, values=["Totalement Aléatoire", "Pondéré"], command=self.on_bias_mode_changed)
        self.btn_segmented_rand.grid(row=1, column=1, columnspan=4, padx=5, pady=4, sticky="ew")
        
        # Sub-frame for biased inputs
        self.frame_biased_settings = ctk.CTkFrame(self.card_rand_dist, fg_color="transparent")
        
        # Row 1 of sub-frame: split point C
        self.lbl_bias_split = ctk.CTkLabel(self.frame_biased_settings, text="Seuil (C):")
        self.lbl_bias_split.grid(row=0, column=0, padx=(0, 5), pady=4, sticky="w")
        
        self.slider_bias_split = ctk.CTkSlider(self.frame_biased_settings, from_=1.0, to=2000.0, number_of_steps=1999, width=170, command=self.on_slider_split_changed)
        self.slider_bias_split.grid(row=0, column=1, padx=5, pady=4, sticky="w")
        
        self.entry_bias_split = ctk.CTkEntry(self.frame_biased_settings, width=60, placeholder_text="70")
        self.entry_bias_split.grid(row=0, column=2, padx=5, pady=4, sticky="w")
        self.entry_bias_split.bind("<KeyRelease>", self.on_entry_split_changed)
        
        self.lbl_ms_unit_split = ctk.CTkLabel(self.frame_biased_settings, text="ms", text_color="gray")
        self.lbl_ms_unit_split.grid(row=0, column=3, padx=2, pady=4, sticky="w")
        
        self.entry_cps_split = ctk.CTkEntry(self.frame_biased_settings, width=60, placeholder_text="CPS", text_color="#2ecc71", font=ctk.CTkFont(weight="bold"))
        self.entry_cps_split.grid(row=0, column=4, padx=5, pady=4, sticky="w")
        self.entry_cps_split.bind("<KeyRelease>", self.on_entry_cps_split_changed)
        
        self.lbl_cps_unit_split = ctk.CTkLabel(self.frame_biased_settings, text="cps", text_color="gray")
        self.lbl_cps_unit_split.grid(row=0, column=5, padx=2, pady=4, sticky="w")
        
        # Row 2 of sub-frame: percentage P
        self.lbl_bias_percent = ctk.CTkLabel(self.frame_biased_settings, text="Pourcentage (P):")
        self.lbl_bias_percent.grid(row=1, column=0, padx=(0, 5), pady=4, sticky="w")
        
        self.slider_bias_percent = ctk.CTkSlider(self.frame_biased_settings, from_=0, to=100, number_of_steps=100, width=170, command=self.on_slider_percent_changed)
        self.slider_bias_percent.grid(row=1, column=1, padx=5, pady=4, sticky="w")
        
        self.entry_bias_percent = ctk.CTkEntry(self.frame_biased_settings, width=60, placeholder_text="70")
        self.entry_bias_percent.grid(row=1, column=2, padx=5, pady=4, sticky="w")
        self.entry_bias_percent.bind("<KeyRelease>", self.on_entry_percent_changed)
        
        self.lbl_percent_unit = ctk.CTkLabel(self.frame_biased_settings, text="%", text_color="gray")
        self.lbl_percent_unit.grid(row=1, column=3, padx=2, pady=4, sticky="w")
        
        # Row 3: Direction
        self.lbl_bias_direction = ctk.CTkLabel(self.frame_biased_settings, text="Zone Ciblée:")
        self.lbl_bias_direction.grid(row=2, column=0, padx=(0, 5), pady=4, sticky="w")
        self.btn_segmented_dir = ctk.CTkSegmentedButton(self.frame_biased_settings, values=["Au-dessus", "En-dessous"], width=200)
        self.btn_segmented_dir.grid(row=2, column=1, columnspan=4, padx=5, pady=4, sticky="w")

        # -----------------------------------------
        # Card 5: Conditions d'Arrêt (Infini / Cycles / Minuteur)
        # -----------------------------------------
        self.card_duration = ctk.CTkFrame(self)
        self.card_duration.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_stop = ctk.CTkLabel(self.card_duration, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_stop.grid(row=0, column=0, columnspan=3, padx=15, pady=(5, 2), sticky="w")
        
        self.btn_segmented_stop = ctk.CTkSegmentedButton(self.card_duration, values=["Infini", "Cycles", "Minuteur"], command=self.on_stop_mode_changed)
        self.btn_segmented_stop.grid(row=1, column=0, columnspan=3, padx=15, pady=5, sticky="ew")
        
        # Sub-frame 1: Cycles Frame
        self.frame_stop_cycles = ctk.CTkFrame(self.card_duration, fg_color="transparent")
        self.lbl_cycles_title = ctk.CTkLabel(self.frame_stop_cycles, text="Répéter :")
        self.lbl_cycles_title.grid(row=0, column=0, padx=(0, 10), pady=3, sticky="w")
        self.entry_cycles = ctk.CTkEntry(self.frame_stop_cycles, width=90, placeholder_text="100")
        self.entry_cycles.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.lbl_cycles_unit = ctk.CTkLabel(self.frame_stop_cycles, text="fois", text_color="gray")
        self.lbl_cycles_unit.grid(row=0, column=2, padx=5, pady=3, sticky="w")
        
        # Sub-frame 2: Minuteur Frame
        self.frame_stop_timer = ctk.CTkFrame(self.card_duration, fg_color="transparent")
        self.lbl_timer_dur = ctk.CTkLabel(self.frame_stop_timer, text="Durée :")
        self.lbl_timer_dur.grid(row=0, column=0, padx=(0, 5), pady=3, sticky="w")
        
        self.entry_hours = ctk.CTkEntry(self.frame_stop_timer, width=40)
        self.entry_hours.grid(row=0, column=1, padx=2, pady=3)
        self.lbl_h = ctk.CTkLabel(self.frame_stop_timer, text="h", text_color="gray")
        self.lbl_h.grid(row=0, column=2, padx=(1, 8), pady=3)
        
        self.entry_minutes = ctk.CTkEntry(self.frame_stop_timer, width=40)
        self.entry_minutes.grid(row=0, column=3, padx=2, pady=3)
        self.lbl_m = ctk.CTkLabel(self.frame_stop_timer, text="m", text_color="gray")
        self.lbl_m.grid(row=0, column=4, padx=(1, 8), pady=3)
        
        self.entry_seconds = ctk.CTkEntry(self.frame_stop_timer, width=40)
        self.entry_seconds.grid(row=0, column=5, padx=2, pady=3)
        self.lbl_s = ctk.CTkLabel(self.frame_stop_timer, text="s", text_color="gray")
        self.lbl_s.grid(row=0, column=6, padx=(1, 8), pady=3)

    def refresh_texts(self):
        t = self.app.settings_manager.get_text
        
        self.lbl_sec_action.configure(text=t("sec_action"))
        
        current_mode = self.btn_segmented_mode.get()
        self.btn_segmented_mode.configure(values=[t("mouse"), t("keyboard")])
        self.btn_segmented_mode.set(t("mouse") if current_mode in ["Souris", "Mouse", "Ratón"] else t("keyboard"))
        
        self.lbl_btn.configure(text=t("button"))
        self.lbl_click_type.configure(text=t("click_type"))
        self.lbl_target_k.configure(text=t("key"))
        self.btn_record_target_key.configure(text=t("change_key"))
        
        self.combo_button.configure(values=[t("left"), t("right"), t("middle")])
        self.combo_button.set(t(self.engine.mouse_button))
        
        self.combo_click_type.configure(values=[t("single"), t("double")])
        self.combo_click_type.set(t("double") if self.engine.mouse_double else t("single"))
        
        self.lbl_target_key_display.configure(text=get_key_name(self.engine.keyboard_vk))
        
        self.lbl_sec_interval_min.configure(text=t("sec_interval_min"))
        self.lbl_sec_interval_max.configure(text=t("sec_interval_max"))
        
        self.lbl_sec_random_dist.configure(text=t("sec_random_dist"))
        self.lbl_rand_type.configure(text=t("lbl_rand_type"))
        
        current_rand_type = self.btn_segmented_rand.get()
        self.btn_segmented_rand.configure(values=[t("rand_uniform"), t("rand_biased")])
        self.btn_segmented_rand.set(t("rand_uniform") if current_rand_type in ["Totalement Aléatoire", "Fully Random", "Totalmente Aleatorio"] else t("rand_biased"))
        
        self.lbl_bias_split.configure(text=t("lbl_bias_split"))
        self.lbl_bias_percent.configure(text=t("lbl_bias_percent"))
        self.lbl_bias_direction.configure(text=t("lbl_bias_direction"))
        
        current_dir = self.btn_segmented_dir.get()
        self.btn_segmented_dir.configure(values=[t("bias_above"), t("bias_below")])
        self.btn_segmented_dir.set(t("bias_above") if current_dir in ["Au-dessus", "Above", "Por encima del límite", "Au-dessus du seuil"] else t("bias_below"))
        
        self.lbl_sec_stop.configure(text=t("sec_stop_silent"))
        
        current_stop = self.btn_segmented_stop.get()
        self.btn_segmented_stop.configure(values=[t("stop_infinite"), t("stop_cycles"), t("stop_timer")])
        if current_stop in ["Infini", "Infinite", "Infinito"]:
            self.btn_segmented_stop.set(t("stop_infinite"))
        elif current_stop in ["Cycles", "Cycles", "Ciclos"]:
            self.btn_segmented_stop.set(t("stop_cycles"))
        else:
            self.btn_segmented_stop.set(t("stop_timer"))
            
        self.lbl_cycles_title.configure(text=t("lbl_cycles"))
        self.lbl_cycles_unit.configure(text=t("lbl_cycles_unit"))
        self.lbl_timer_dur.configure(text=t("lbl_timer"))

    def load_settings(self):
        cfg = self.app.settings_manager.data.get("silent", {})
        
        # Load targets
        mode = cfg.get("mode", "mouse")
        t = self.app.settings_manager.get_text
        self.btn_segmented_mode.set(t("mouse") if mode == "mouse" else t("keyboard"))
        self.on_mode_changed(self.btn_segmented_mode.get())
        
        button = cfg.get("button", "left")
        self.combo_button.set(t(button))
        
        double = cfg.get("double", False)
        self.combo_click_type.set(t("double") if double else t("single"))
        
        self.engine.keyboard_vk = cfg.get("keyboard_vk", 0x20)
        self.lbl_target_key_display.configure(text=get_key_name(self.engine.keyboard_vk))
        
        # Load intervals
        min_ms = cfg.get("min_interval_ms", 10.0)
        self.slider_ms_min.set(min_ms)
        self.entry_ms_min.delete(0, "end")
        self.entry_ms_min.insert(0, f"{min_ms:.1f}")
        self.update_cps_display("min")
        
        max_ms = cfg.get("max_interval_ms", 100.0)
        self.slider_ms_max.set(max_ms)
        self.entry_ms_max.delete(0, "end")
        self.entry_ms_max.insert(0, f"{max_ms:.1f}")
        self.update_cps_display("max")
        
        # Load random settings
        bias_mode = cfg.get("bias_mode", "uniform")
        self.btn_segmented_rand.set(t("rand_uniform") if bias_mode == "uniform" else t("rand_biased"))
        self.on_bias_mode_changed(self.btn_segmented_rand.get())
        
        split_ms = cfg.get("bias_split_ms", 70.0)
        self.slider_bias_split.set(split_ms)
        self.entry_bias_split.delete(0, "end")
        self.entry_bias_split.insert(0, f"{split_ms:.1f}")
        self.update_cps_display("split")
        
        percent = cfg.get("bias_percent", 70)
        self.slider_bias_percent.set(percent)
        self.entry_bias_percent.delete(0, "end")
        self.entry_bias_percent.insert(0, str(percent))
        
        direction = cfg.get("bias_direction", "above")
        self.btn_segmented_dir.set(t("bias_above") if direction == "above" else t("bias_below"))
        
        # Load stops
        stop_mode = cfg.get("stop_mode", "Infini")
        if stop_mode == "Infini":
            self.btn_segmented_stop.set(t("stop_infinite"))
        elif stop_mode == "Cycles":
            self.btn_segmented_stop.set(t("stop_cycles"))
            self.entry_cycles.delete(0, "end")
            self.entry_cycles.insert(0, str(cfg.get("cycles", 100)))
        else:
            self.btn_segmented_stop.set(t("stop_timer"))
            self.entry_hours.delete(0, "end")
            self.entry_hours.insert(0, str(cfg.get("duration_h", 0)))
            self.entry_minutes.delete(0, "end")
            self.entry_minutes.insert(0, str(cfg.get("duration_m", 10)))
            self.entry_seconds.delete(0, "end")
            self.entry_seconds.insert(0, str(cfg.get("duration_s", 0)))
            
        self.on_stop_mode_changed(self.btn_segmented_stop.get())
        self.update_split_slider_bounds()

    def save_settings(self):
        t = self.app.settings_manager.get_text
        
        cfg = {}
        # Mode & targets
        cfg["mode"] = "mouse" if self.btn_segmented_mode.get() in [t("mouse"), "Souris", "Mouse", "Ratón"] else "keyboard"
        
        btn = self.combo_button.get()
        if btn in [t("left"), "Gauche", "Left", "Izquierda"]:
            cfg["button"] = "left"
        elif btn in [t("right"), "Droit", "Right", "Derecha"]:
            cfg["button"] = "right"
        else:
            cfg["button"] = "middle"
            
        cfg["double"] = (self.combo_click_type.get() in [t("double"), "Double"])
        cfg["keyboard_vk"] = self.engine.keyboard_vk
        
        # Speeds
        try:
            cfg["min_interval_ms"] = float(self.entry_ms_min.get())
        except:
            cfg["min_interval_ms"] = 10.0
            
        try:
            cfg["max_interval_ms"] = float(self.entry_ms_max.get())
        except:
            cfg["max_interval_ms"] = 100.0
            
        # Random distribution
        cfg["bias_mode"] = "uniform" if self.btn_segmented_rand.get() in [t("rand_uniform"), "Totalement Aléatoire", "Fully Random", "Totalmente Aleatorio"] else "biased"
        
        try:
            split_ms = float(self.entry_bias_split.get())
        except:
            split_ms = 70.0
            
        min_ms = cfg["min_interval_ms"]
        max_ms = cfg["max_interval_ms"]
        if min_ms > max_ms:
            min_ms, max_ms = max_ms, min_ms
            
        split_ms = min(max_ms, max(min_ms, split_ms))
        cfg["bias_split_ms"] = split_ms
        
        self.entry_bias_split.delete(0, "end")
        self.entry_bias_split.insert(0, f"{split_ms:.1f}")
        self.update_cps_display("split")
            
        try:
            cfg["bias_percent"] = int(self.entry_bias_percent.get())
        except:
            cfg["bias_percent"] = 70
            
        cfg["bias_direction"] = "above" if self.btn_segmented_dir.get() in [t("bias_above"), "Au-dessus", "Above", "Por encima del límite", "Au-dessus du seuil"] else "below"
        
        # Stop modes
        stop_val = self.btn_segmented_stop.get()
        if stop_val in [t("stop_infinite"), "Infini", "Infinite", "Infinito"]:
            cfg["stop_mode"] = "Infini"
        elif stop_val in [t("stop_cycles"), "Cycles", "Ciclos"]:
            cfg["stop_mode"] = "Cycles"
            try:
                cfg["cycles"] = int(self.entry_cycles.get())
            except:
                cfg["cycles"] = 100
        else:
            cfg["stop_mode"] = "Minuteur"
            try:
                cfg["duration_h"] = int(self.entry_hours.get())
                cfg["duration_m"] = int(self.entry_minutes.get())
                cfg["duration_s"] = int(self.entry_seconds.get())
            except:
                cfg["duration_h"] = 0
                cfg["duration_m"] = 10
                cfg["duration_s"] = 0
                
        self.app.settings_manager.data["silent"] = cfg
        self.app.settings_manager.save()

    # Inputs Handlers
    def on_mode_changed(self, mode_text):
        t = self.app.settings_manager.get_text
        if mode_text in [t("mouse"), "Souris", "Mouse", "Ratón"]:
            self.frame_keyboard.grid_forget()
            self.frame_mouse.grid(row=2, column=0, columnspan=2, padx=15, pady=(3, 8), sticky="ew")
            self.engine.mode = "mouse"
            self.app.clear_warning()
        else:
            self.frame_mouse.grid_forget()
            self.frame_keyboard.grid(row=2, column=0, columnspan=2, padx=15, pady=(3, 8), sticky="ew")
            self.engine.mode = "keyboard"
            self.app.check_key_conflicts(self.engine.keyboard_vk, self.app.hotkey_manager.vk)

    def on_mouse_config_changed(self, val=None):
        t = self.app.settings_manager.get_text
        btn = self.combo_button.get()
        if btn in [t("left"), "Gauche", "Left", "Izquierda"]:
            self.engine.mouse_button = "left"
        elif btn in [t("right"), "Droit", "Right", "Derecha"]:
            self.engine.mouse_button = "right"
        else:
            self.engine.mouse_button = "middle"
            
        t_click = self.combo_click_type.get()
        self.engine.mouse_double = (t_click in [t("double"), "Double"])

    # Double Speed Conversion Helpers (Min)
    def on_slider_min_changed(self, value):
        self.entry_ms_min.delete(0, "end")
        self.entry_ms_min.insert(0, f"{value:.1f}")
        self.update_cps_display("min")
        self.update_split_slider_bounds()

    def on_entry_min_changed(self, event):
        val_str = self.entry_ms_min.get()
        try:
            val = float(val_str)
            if val > 0:
                self.slider_ms_min.set(min(2000.0, max(1.0, val)))
                self.update_cps_display("min")
                self.update_split_slider_bounds()
        except ValueError:
            pass

    def on_entry_cps_min_changed(self, event):
        val_str = self.entry_cps_min.get().strip().replace(",", ".")
        try:
            cps = float(val_str)
            if cps > 0:
                ms = 1000.0 / cps
                self.slider_ms_min.set(min(2000.0, max(1.0, ms)))
                self.entry_ms_min.delete(0, "end")
                self.entry_ms_min.insert(0, f"{ms:.1f}")
                self.app.clear_warning()
                self.update_split_slider_bounds()
        except ValueError:
            pass

    # Double Speed Conversion Helpers (Max)
    def on_slider_max_changed(self, value):
        self.entry_ms_max.delete(0, "end")
        self.entry_ms_max.insert(0, f"{value:.1f}")
        self.update_cps_display("max")
        self.update_split_slider_bounds()

    def on_entry_max_changed(self, event):
        val_str = self.entry_ms_max.get()
        try:
            val = float(val_str)
            if val > 0:
                self.slider_ms_max.set(min(2000.0, max(1.0, val)))
                self.update_cps_display("max")
                self.update_split_slider_bounds()
        except ValueError:
            pass

    def on_entry_cps_max_changed(self, event):
        val_str = self.entry_cps_max.get().strip().replace(",", ".")
        try:
            cps = float(val_str)
            if cps > 0:
                ms = 1000.0 / cps
                self.slider_ms_max.set(min(2000.0, max(1.0, ms)))
                self.entry_ms_max.delete(0, "end")
                self.entry_ms_max.insert(0, f"{ms:.1f}")
                self.app.clear_warning()
                self.update_split_slider_bounds()
        except ValueError:
            pass

    # Double Speed Conversion Helpers (Split point C)
    def on_slider_split_changed(self, value):
        self.entry_bias_split.delete(0, "end")
        self.entry_bias_split.insert(0, f"{value:.1f}")
        self.update_cps_display("split")

    def on_entry_split_changed(self, event):
        val_str = self.entry_bias_split.get()
        try:
            val = float(val_str)
            if val > 0:
                self.slider_bias_split.set(min(2000.0, max(1.0, val)))
                self.update_cps_display("split")
        except ValueError:
            pass

    def on_entry_cps_split_changed(self, event):
        val_str = self.entry_cps_split.get().strip().replace(",", ".")
        try:
            cps = float(val_str)
            if cps > 0:
                ms = 1000.0 / cps
                self.slider_bias_split.set(min(2000.0, max(1.0, ms)))
                self.entry_bias_split.delete(0, "end")
                self.entry_bias_split.insert(0, f"{ms:.1f}")
                self.app.clear_warning()
        except ValueError:
            pass

    # Percentage synchronization helpers
    def on_slider_percent_changed(self, value):
        self.entry_bias_percent.delete(0, "end")
        self.entry_bias_percent.insert(0, str(int(value)))

    def on_entry_percent_changed(self, event):
        val_str = self.entry_bias_percent.get().strip()
        try:
            val = int(val_str)
            if 0 <= val <= 100:
                self.slider_bias_percent.set(val)
        except ValueError:
            pass

    def update_cps_display(self, field_type):
        try:
            if field_type == "min":
                val = float(self.entry_ms_min.get())
                entry = self.entry_cps_min
            elif field_type == "max":
                val = float(self.entry_ms_max.get())
                entry = self.entry_cps_max
            else:
                val = float(self.entry_bias_split.get())
                entry = self.entry_cps_split
                
            if val > 0:
                cps = 1000.0 / val
                entry.delete(0, "end")
                if cps >= 100:
                    entry.insert(0, f"{cps:.1f}")
                else:
                    entry.insert(0, f"{cps:.2f}")
            else:
                entry.delete(0, "end")
        except:
            pass

    def on_bias_mode_changed(self, mode):
        t = self.app.settings_manager.get_text
        if mode in [t("rand_biased"), "Pondéré", "Weighted", "Ponderado", "Biaisé (Triché)", "Biased (Cheated)", "Sesgado (Con trampa)"]:
            self.frame_biased_settings.grid(row=2, column=0, columnspan=5, padx=15, pady=4, sticky="ew")
        else:
            self.frame_biased_settings.grid_forget()

    def update_split_slider_bounds(self):
        try:
            try:
                min_val = float(self.entry_ms_min.get())
            except ValueError:
                min_val = 1.0
            try:
                max_val = float(self.entry_ms_max.get())
            except ValueError:
                max_val = 2000.0
                
            if min_val > max_val:
                min_val, max_val = max_val, min_val
                
            # Update bounds of split slider
            self.slider_bias_split.configure(from_=min_val, to=max_val)
            
            # Read current split value
            try:
                c_val = float(self.entry_bias_split.get())
            except ValueError:
                c_val = min_val + (max_val - min_val) / 2.0
                
            # Clamp current split point if it falls outside the new range
            if c_val < min_val or c_val > max_val:
                c_val = min_val + (max_val - min_val) / 2.0
                self.slider_bias_split.set(c_val)
                self.entry_bias_split.delete(0, "end")
                self.entry_bias_split.insert(0, f"{c_val:.1f}")
                self.update_cps_display("split")
            else:
                self.slider_bias_split.set(c_val)
        except Exception as e:
            print(f"Error updating split bounds: {e}")

    def on_stop_mode_changed(self, stop_text):
        t = self.app.settings_manager.get_text
        self.frame_stop_cycles.grid_forget()
        self.frame_stop_timer.grid_forget()
        
        if stop_text in [t("stop_cycles"), "Cycles", "Ciclos"]:
            self.frame_stop_cycles.grid(row=2, column=0, columnspan=3, padx=15, pady=(2, 5), sticky="ew")
        elif stop_text in [t("stop_timer"), "Minuteur", "Timer", "Temporizador"]:
            self.frame_stop_timer.grid(row=2, column=0, columnspan=3, padx=15, pady=(2, 5), sticky="ew")

    # Keyboard Capture route
    def start_recording_target_key(self):
        if self.engine.active:
            return
        self.recording_target_key = True
        self.btn_record_target_key.configure(text=self.app.settings_manager.get_text("press_key"), fg_color="#2ecc71")
        self.app.clear_warning()

    def handle_key_press(self, vk):
        if self.recording_target_key:
            if self.app.check_key_conflicts(vk, self.app.hotkey_manager.vk):
                self.btn_record_target_key.configure(text=self.app.settings_manager.get_text("change_key"), fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
                self.recording_target_key = False
                return True
                
            self.engine.keyboard_vk = vk
            self.lbl_target_key_display.configure(text=get_key_name(vk))
            self.btn_record_target_key.configure(text=self.app.settings_manager.get_text("change_key"), fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            self.recording_target_key = False
            self.app.clear_warning()
            return True
        return False

    def start_clicker(self):
        t = self.app.settings_manager.get_text
        stop_val = self.btn_segmented_stop.get()
        
        # Parse stops
        if stop_val in [t("stop_infinite"), "Infini", "Infinite", "Infinito"]:
            self.engine.max_clicks = None
            self.engine.duration_sec = None
        elif stop_val in [t("stop_cycles"), "Cycles", "Ciclos"]:
            try:
                cycles = int(self.entry_cycles.get().strip())
                if cycles <= 0:
                    raise ValueError()
                self.engine.max_clicks = cycles
                self.engine.duration_sec = None
            except ValueError:
                self.app.lbl_warning.configure(text=t("err_cycles"))
                return
        else:
            try:
                h = int(self.entry_hours.get().strip() or "0")
                m = int(self.entry_minutes.get().strip() or "0")
                s = int(self.entry_seconds.get().strip() or "0")
                if h < 0 or m < 0 or s < 0:
                    raise ValueError()
                total = h * 3600 + m * 60 + s
                if total <= 0:
                    raise ValueError()
                self.engine.duration_sec = total
                self.engine.max_clicks = None
            except ValueError:
                self.app.lbl_warning.configure(text=t("err_timer"))
                return
                
        # Load clicker configurations into engine
        self.engine.random_mode = True
        
        # Parse Min and Max speeds
        try:
            min_val = float(self.entry_ms_min.get().strip())
            max_val = float(self.entry_ms_max.get().strip())
            if min_val <= 0 or max_val <= 0:
                raise ValueError()
            self.engine.min_interval_ms = min_val
            self.engine.max_interval_ms = max_val
        except ValueError:
            self.app.lbl_warning.configure(text=t("err_interval"))
            return
            
        # Parse Random distribution configs
        bias_val = self.btn_segmented_rand.get()
        if bias_val in [t("rand_biased"), "Pondéré", "Weighted", "Ponderado", "Biaisé (Triché)", "Biased (Cheated)", "Sesgado (Con trampa)"]:
            self.engine.bias_mode = "biased"
            try:
                split_val = float(self.entry_bias_split.get().strip())
                percent_val = int(self.entry_bias_percent.get().strip())
                
                # Clamp split_val between min and max
                min_val = self.engine.min_interval_ms
                max_val = self.engine.max_interval_ms
                if min_val > max_val:
                    min_val, max_val = max_val, min_val
                split_val = min(max_val, max(min_val, split_val))
                
                if split_val <= 0 or not (0 <= percent_val <= 100):
                    raise ValueError()
                self.engine.bias_split_ms = split_val
                self.engine.bias_percent = percent_val
                
                # Update UI to reflect clamped value
                self.entry_bias_split.delete(0, "end")
                self.entry_bias_split.insert(0, f"{split_val:.1f}")
                self.slider_bias_split.set(split_val)
                self.update_cps_display("split")
            except ValueError:
                self.app.lbl_warning.configure(text=t("err_interval"))
                return
                
            dir_val = self.btn_segmented_dir.get()
            self.engine.bias_direction = "above" if dir_val in [t("bias_above"), "Au-dessus", "Above", "Por encima del límite", "Au-dessus du seuil"] else "below"
        else:
            self.engine.bias_mode = "uniform"
            
        # Target action configuration
        cfg_mode = self.btn_segmented_mode.get()
        if cfg_mode in [t("mouse"), "Souris", "Mouse", "Ratón"]:
            self.engine.mode = "mouse"
            btn = self.combo_button.get()
            if btn in [t("left"), "Gauche", "Left", "Izquierda"]:
                self.engine.mouse_button = "left"
            elif btn in [t("right"), "Droit", "Right", "Derecha"]:
                self.engine.mouse_button = "right"
            else:
                self.engine.mouse_button = "middle"
            t_click = self.combo_click_type.get()
            self.engine.mouse_double = (t_click in [t("double"), "Double"])
        else:
            self.engine.mode = "keyboard"
            
        self.app.clear_warning()
        self.save_settings()
        self.engine.start()

    def disable_inputs(self, disable=True):
        state = "disabled" if disable else "normal"
        self.btn_segmented_mode.configure(state=state)
        self.combo_button.configure(state=state)
        self.combo_click_type.configure(state=state)
        self.btn_record_target_key.configure(state=state)
        self.entry_ms_min.configure(state=state)
        self.slider_ms_min.configure(state=state)
        self.entry_cps_min.configure(state=state)
        self.entry_ms_max.configure(state=state)
        self.slider_ms_max.configure(state=state)
        self.entry_cps_max.configure(state=state)
        self.btn_segmented_rand.configure(state=state)
        self.slider_bias_split.configure(state=state)
        self.entry_bias_split.configure(state=state)
        self.entry_cps_split.configure(state=state)
        self.slider_bias_percent.configure(state=state)
        self.entry_bias_percent.configure(state=state)
        self.btn_segmented_dir.configure(state=state)
        self.btn_segmented_stop.configure(state=state)
        self.entry_cycles.configure(state=state)
        self.entry_hours.configure(state=state)
        self.entry_minutes.configure(state=state)
        self.entry_seconds.configure(state=state)

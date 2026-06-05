import tkinter as tk
import customtkinter as ctk
from settings import get_key_name

class ClickerFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.engine = app.engine
        
        self.recording_target_key = False
        
        self.create_widgets()
        self.refresh_texts()
        self.refresh_presets_combo()

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
        # Card 1.5: Presets (NEW FEATURE)
        # -----------------------------------------
        self.card_presets = ctk.CTkFrame(self)
        self.card_presets.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_presets = ctk.CTkLabel(self.card_presets, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_presets.grid(row=0, column=0, columnspan=3, padx=15, pady=(5, 2), sticky="w")
        
        self.lbl_preset_sel = ctk.CTkLabel(self.card_presets, text="Preset:")
        self.lbl_preset_sel.grid(row=1, column=0, padx=(15, 8), pady=4, sticky="w")
        
        self.combo_presets = ctk.CTkComboBox(self.card_presets, values=[], width=280, command=self.on_preset_selected)
        self.combo_presets.grid(row=1, column=1, columnspan=2, padx=5, pady=4, sticky="w")
        
        # New Inline Preset Input widgets (initially hidden)
        self.entry_preset_name = ctk.CTkEntry(self.card_presets, width=220, placeholder_text="Preset")
        self.btn_cancel_preset = ctk.CTkButton(self.card_presets, text="X", width=50, fg_color="#7f8c8d", hover_color="#5d6d7e", command=self.hide_new_preset_input)
        
        self.btn_save_preset = ctk.CTkButton(self.card_presets, text="Enregistrer", width=135, fg_color="#27ae60", hover_color="#219653", command=self.on_save_preset_clicked)
        self.btn_save_preset.grid(row=2, column=1, padx=5, pady=(0, 5), sticky="w")
        
        self.btn_del_preset = ctk.CTkButton(self.card_presets, text="Supprimer", width=135, fg_color="#c0392b", hover_color="#962d22", command=self.on_delete_preset_clicked)
        self.btn_del_preset.grid(row=2, column=2, padx=5, pady=(0, 5), sticky="w")

        # -----------------------------------------
        # Card 2: Intervalle en millisecondes
        # -----------------------------------------
        self.card_speed = ctk.CTkFrame(self)
        self.card_speed.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_interval = ctk.CTkLabel(self.card_speed, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_interval.grid(row=0, column=0, columnspan=5, padx=15, pady=(5, 2), sticky="w")
        
        self.slider_ms = ctk.CTkSlider(self.card_speed, from_=1.0, to=2000.0, number_of_steps=1999, width=220, command=self.on_slider_ms_changed)
        self.slider_ms.grid(row=1, column=0, padx=(15, 10), pady=5, sticky="w")
        
        self.entry_ms = ctk.CTkEntry(self.card_speed, width=70, placeholder_text="100")
        self.entry_ms.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_ms.bind("<KeyRelease>", self.on_entry_ms_changed)
        
        self.lbl_ms_unit = ctk.CTkLabel(self.card_speed, text="ms", text_color="gray")
        self.lbl_ms_unit.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        self.entry_cps = ctk.CTkEntry(self.card_speed, width=70, placeholder_text="CPS", text_color="#2ecc71", font=ctk.CTkFont(weight="bold"))
        self.entry_cps.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.entry_cps.bind("<KeyRelease>", self.on_entry_cps_changed)
        
        self.lbl_cps_unit = ctk.CTkLabel(self.card_speed, text="cps", text_color="gray")
        self.lbl_cps_unit.grid(row=1, column=4, padx=5, pady=5, sticky="w")
        
        self.lbl_speed_hint = ctk.CTkLabel(self.card_speed, text="", text_color="gray", font=ctk.CTkFont(size=11))
        self.lbl_speed_hint.grid(row=2, column=0, columnspan=5, padx=15, pady=(0, 4), sticky="w")

        # -----------------------------------------
        # Card 3: Conditions d'Arrêt (Infini / Cycles / Minuteur)
        # -----------------------------------------
        self.card_duration = ctk.CTkFrame(self)
        self.card_duration.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_stop = ctk.CTkLabel(self.card_duration, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_stop.grid(row=0, column=0, columnspan=3, padx=15, pady=(5, 2), sticky="w")
        
        self.btn_segmented_stop = ctk.CTkSegmentedButton(self.card_duration, values=["Infini", "Cycles", "Minuteur"], command=self.on_stop_mode_changed)
        self.btn_segmented_stop.grid(row=1, column=0, columnspan=3, padx=15, pady=5, sticky="ew")
        
        # Sub-frame 1: Cycles Frame (hidden by default)
        self.frame_stop_cycles = ctk.CTkFrame(self.card_duration, fg_color="transparent")
        self.lbl_cycles_title = ctk.CTkLabel(self.frame_stop_cycles, text="Répéter :")
        self.lbl_cycles_title.grid(row=0, column=0, padx=(0, 10), pady=3, sticky="w")
        self.entry_cycles = ctk.CTkEntry(self.frame_stop_cycles, width=90, placeholder_text="100")
        self.entry_cycles.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.lbl_cycles_unit = ctk.CTkLabel(self.frame_stop_cycles, text="fois", text_color="gray")
        self.lbl_cycles_unit.grid(row=0, column=2, padx=5, pady=3, sticky="w")
        
        # Sub-frame 2: Minuteur Frame (hidden by default)
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
        # Localize segment buttons and labels
        t = self.app.settings_manager.get_text
        
        self.lbl_sec_action.configure(text=t("sec_action"))
        
        # Segmented buttons need list updates
        current_mode = self.btn_segmented_mode.get()
        self.btn_segmented_mode.configure(values=[t("mouse"), t("keyboard")])
        self.btn_segmented_mode.set(t("mouse") if current_mode in ["Souris", "Mouse", "Ratón"] else t("keyboard"))
        
        self.lbl_btn.configure(text=t("button"))
        self.lbl_click_type.configure(text=t("click_type"))
        self.lbl_target_k.configure(text=t("key"))
        self.btn_record_target_key.configure(text=t("change_key"))
        
        # Combo boxes translation
        self.combo_button.configure(values=[t("left"), t("right"), t("middle")])
        self.combo_button.set(t(self.engine.mouse_button))
        
        self.combo_click_type.configure(values=[t("single"), t("double")])
        self.combo_click_type.set(t("double") if self.engine.mouse_double else t("single"))
        
        self.lbl_target_key_display.configure(text=get_key_name(self.engine.keyboard_vk))
        
        self.lbl_sec_presets.configure(text=t("sec_presets"))
        self.lbl_preset_sel.configure(text=t("lbl_preset"))
        self.btn_save_preset.configure(text=t("btn_save_preset"))
        self.btn_del_preset.configure(text=t("btn_del_preset"))
        
        self.lbl_sec_interval.configure(text=t("sec_interval"))
        self.lbl_speed_hint.configure(text=t("examples_ms"))
        
        self.lbl_sec_stop.configure(text=t("sec_stop"))
        
        current_stop = self.btn_segmented_stop.get()
        # Translate values
        stop_mapping_old = ["Infini", "Cycles", "Minuteur", "Infinite", "Timer", "Temporizador"]
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
        
        # Load values into UI inputs
        self.slider_ms.set(self.engine.interval_ms)
        self.entry_ms.delete(0, "end")
        self.entry_ms.insert(0, f"{self.engine.interval_ms:.1f}")
        
        # Populate cycles/timer inputs with default values if they are empty
        if not self.entry_cycles.get():
            self.entry_cycles.insert(0, "100")
        if not self.entry_hours.get():
            self.entry_hours.insert(0, "0")
        if not self.entry_minutes.get():
            self.entry_minutes.insert(0, "10")
        if not self.entry_seconds.get():
            self.entry_seconds.insert(0, "0")
            
        self.update_cps_display()

    # Presets management
    def refresh_presets_combo(self):
        presets = self.app.settings_manager.get_presets()
        names = [p["name"] for p in presets]
        t = self.app.settings_manager.get_text
        names.append(t("new_item"))
        self.combo_presets.configure(values=names)
        if presets:
            self.combo_presets.set(presets[0]["name"])
        else:
            self.combo_presets.set("")

    def on_preset_selected(self, name):
        t = self.app.settings_manager.get_text
        if name == t("new_item"):
            self.show_new_preset_input()
            return
            
        presets = self.app.settings_manager.get_presets()
        preset = next((p for p in presets if p["name"] == name), None)
        if preset:
            # Set interval
            self.engine.interval_ms = preset.get("interval_ms", 100.0)
            self.slider_ms.set(self.engine.interval_ms)
            self.entry_ms.delete(0, "end")
            self.entry_ms.insert(0, f"{self.engine.interval_ms:.1f}")
            
            # Set stop mode
            stop_mode = preset.get("stop_mode", "Infini")
            if stop_mode == "Infini":
                self.btn_segmented_stop.set(t("stop_infinite"))
            elif stop_mode == "Cycles":
                self.btn_segmented_stop.set(t("stop_cycles"))
                self.entry_cycles.delete(0, "end")
                self.entry_cycles.insert(0, str(preset.get("cycles", 100)))
            elif stop_mode == "Minuteur":
                self.btn_segmented_stop.set(t("stop_timer"))
                self.entry_hours.delete(0, "end")
                self.entry_hours.insert(0, str(preset.get("duration_h", 0)))
                self.entry_minutes.delete(0, "end")
                self.entry_minutes.insert(0, str(preset.get("duration_m", 10)))
                self.entry_seconds.delete(0, "end")
                self.entry_seconds.insert(0, str(preset.get("duration_s", 0)))
                
            self.on_stop_mode_changed(self.btn_segmented_stop.get())
            self.update_cps_display()

    def on_save_preset_clicked(self):
        t = self.app.settings_manager.get_text
        
        if self.entry_preset_name.winfo_viewable():
            name = self.entry_preset_name.get().strip()
            if not name or name == t("new_item"):
                self.app.lbl_warning.configure(text=t("macro_err_name_empty"))
                return
        else:
            name = self.combo_presets.get()
            if not name or name == t("new_item"):
                self.show_new_preset_input()
                return
                
        preset_dict = {
            "name": name,
            "interval_ms": self.engine.interval_ms,
        }
        # Add stop mode configurations
        stop_val = self.btn_segmented_stop.get()
        if stop_val in [t("stop_infinite"), "Infini", "Infinite", "Infinito"]:
            preset_dict["stop_mode"] = "Infini"
        elif stop_val in [t("stop_cycles"), "Cycles", "Ciclos"]:
            preset_dict["stop_mode"] = "Cycles"
            try:
                preset_dict["cycles"] = int(self.entry_cycles.get())
            except:
                preset_dict["cycles"] = 100
        else:
            preset_dict["stop_mode"] = "Minuteur"
            try:
                preset_dict["duration_h"] = int(self.entry_hours.get())
                preset_dict["duration_m"] = int(self.entry_minutes.get())
                preset_dict["duration_s"] = int(self.entry_seconds.get())
            except:
                preset_dict["duration_h"] = 0
                preset_dict["duration_m"] = 10
                preset_dict["duration_s"] = 0
                
        self.app.settings_manager.add_preset(preset_dict)
        self.app.clear_warning()
        self.refresh_presets_combo()
        self.combo_presets.set(name)
        
        if self.entry_preset_name.winfo_viewable():
            self.hide_new_preset_input()

    def on_delete_preset_clicked(self):
        name = self.combo_presets.get()
        if name:
            self.app.settings_manager.delete_preset(name)
            self.refresh_presets_combo()

    # Inputs handlers
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

    def on_slider_ms_changed(self, value):
        self.entry_ms.delete(0, "end")
        self.entry_ms.insert(0, f"{value:.1f}")
        self.engine.interval_ms = float(value)
        self.update_cps_display()

    def on_entry_ms_changed(self, event):
        val_str = self.entry_ms.get()
        try:
            val = float(val_str)
            if val > 0:
                self.slider_ms.set(min(2000.0, max(1.0, val)))
                self.engine.interval_ms = val
                self.update_cps_display()
        except ValueError:
            pass

    def on_stop_mode_changed(self, stop_text):
        t = self.app.settings_manager.get_text
        self.frame_stop_cycles.grid_forget()
        self.frame_stop_timer.grid_forget()
        
        if stop_text in [t("stop_cycles"), "Cycles", "Ciclos"]:
            self.frame_stop_cycles.grid(row=2, column=0, columnspan=3, padx=15, pady=(2, 5), sticky="ew")
        elif stop_text in [t("stop_timer"), "Minuteur", "Timer", "Temporizador"]:
            self.frame_stop_timer.grid(row=2, column=0, columnspan=3, padx=15, pady=(2, 5), sticky="ew")

    # Keyboard Capture
    def start_recording_target_key(self):
        if self.engine.active:
            return
        self.recording_target_key = True
        self.btn_record_target_key.configure(text=self.app.settings_manager.get_text("press_key"), fg_color="#2ecc71")
        self.app.clear_warning()

    def handle_key_press(self, vk):
        if self.recording_target_key:
            # Check for conflict with global activation hotkey
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
        
        # Infinite
        if stop_val in [t("stop_infinite"), "Infini", "Infinite", "Infinito"]:
            self.engine.max_clicks = None
            self.engine.duration_sec = None
            
        # Cycles
        elif stop_val in [t("stop_cycles"), "Cycles", "Ciclos"]:
            try:
                cycles_str = self.entry_cycles.get().strip()
                if not cycles_str:
                    raise ValueError()
                cycles = int(cycles_str)
                if cycles <= 0:
                    raise ValueError()
                self.engine.max_clicks = cycles
                self.engine.duration_sec = None
            except ValueError:
                self.app.lbl_warning.configure(text=t("err_cycles"))
                return
                
        # Timer
        else:
            try:
                h_str = self.entry_hours.get().strip() or "0"
                m_str = self.entry_minutes.get().strip() or "0"
                s_str = self.entry_seconds.get().strip() or "0"
                
                h = int(h_str)
                m = int(m_str)
                s = int(s_str)
                
                if h < 0 or m < 0 or s < 0:
                    raise ValueError()
                total_sec = h * 3600 + m * 60 + s
                if total_sec <= 0:
                    raise ValueError()
                self.engine.duration_sec = total_sec
                self.engine.max_clicks = None
            except ValueError:
                self.app.lbl_warning.configure(text=t("err_timer"))
                return
                
        self.app.clear_warning()
        self.engine.start()

    def disable_inputs(self, disable=True):
        state = "disabled" if disable else "normal"
        self.btn_segmented_mode.configure(state=state)
        self.combo_button.configure(state=state)
        self.combo_click_type.configure(state=state)
        self.btn_record_target_key.configure(state=state)
        self.combo_presets.configure(state=state)
        self.btn_save_preset.configure(state=state)
        self.btn_del_preset.configure(state=state)
        self.entry_ms.configure(state=state)
        self.slider_ms.configure(state=state)
        self.btn_segmented_stop.configure(state=state)
        self.entry_cycles.configure(state=state)
        self.entry_hours.configure(state=state)
        self.entry_minutes.configure(state=state)
        self.entry_seconds.configure(state=state)
        self.entry_preset_name.configure(state=state)
        self.btn_cancel_preset.configure(state=state)
        self.entry_cps.configure(state=state)

    def update_cps_display(self):
        try:
            val = self.engine.interval_ms
            if val > 0:
                cps = 1000.0 / val
                self.entry_cps.delete(0, "end")
                if cps >= 100:
                    self.entry_cps.insert(0, f"{cps:.1f}")
                else:
                    self.entry_cps.insert(0, f"{cps:.2f}")
            else:
                self.entry_cps.delete(0, "end")
        except:
            pass

    def show_new_preset_input(self):
        self.combo_presets.grid_forget()
        self.entry_preset_name.grid(row=1, column=1, padx=5, pady=4, sticky="w")
        self.btn_cancel_preset.grid(row=1, column=2, padx=5, pady=4, sticky="w")
        self.entry_preset_name.delete(0, "end")
        self.entry_preset_name.insert(0, "")
        self.entry_preset_name.focus()

    def hide_new_preset_input(self):
        self.entry_preset_name.grid_forget()
        self.btn_cancel_preset.grid_forget()
        self.combo_presets.grid(row=1, column=1, columnspan=2, padx=5, pady=4, sticky="w")
        presets = self.app.settings_manager.get_presets()
        if presets:
            self.combo_presets.set(presets[0]["name"])
        else:
            self.combo_presets.set("")

    def on_entry_cps_changed(self, event):
        val_str = self.entry_cps.get().strip().replace(",", ".")
        try:
            cps = float(val_str)
            if cps > 0:
                interval_ms = 1000.0 / cps
                self.engine.interval_ms = interval_ms
                self.slider_ms.set(min(2000.0, max(1.0, interval_ms)))
                self.entry_ms.delete(0, "end")
                self.entry_ms.insert(0, f"{interval_ms:.1f}")
                self.app.clear_warning()
        except ValueError:
            pass

import tkinter as tk
import customtkinter as ctk
import time
from settings import SettingsManager, get_key_name
from hotkey import GlobalHotkeyManager
from engine import ClickerEngine, MacroEngine
from ui_clicker import ClickerFrame
from ui_silent import SilentClickerFrame
from ui_macro import ui_macro_frame

class EveryClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Load configuration settings
        self.settings_manager = SettingsManager()
        
        # Configure global window
        self.title("EveryClicker | Mouse & Keyboard clicker")
        self.geometry("760x700")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Engine initializations
        self.engine = ClickerEngine(self.on_engine_state_change)
        self.macro_engine = MacroEngine(self.on_engine_state_change)
        
        # Hotkey Manager
        self.hotkey_manager = GlobalHotkeyManager(self.toggle_active_engine)
        self.hotkey_manager.set_hotkey(self.settings_manager.get_hotkey())
        
        # State indicators
        self.active_tab = "clicker"
        self.recording_hotkey = False
        
        # Build Interface
        self.create_layout()
        
        # Sync values from settings
        self.sync_settings_to_ui()
        
        self.update_status_loop()
        
    def create_layout(self):
        # -----------------------------------------
        # LEFT: Sidebar Panel (Menu + Langs + Status + Footer)
        # -----------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        
        # Language Dropdown Picker
        self.combo_lang = ctk.CTkComboBox(self.sidebar_frame, values=["Français", "English", "Español"], width=130, command=self.on_language_changed)
        self.combo_lang.pack(pady=(20, 10), padx=20)
        
        self.lbl_title = ctk.CTkLabel(self.sidebar_frame, text="EVERYCLICKER", font=ctk.CTkFont(family="Outfit", size=18, weight="bold"))
        self.lbl_title.pack(pady=(15, 2))
        
        self.lbl_subtitle = ctk.CTkLabel(self.sidebar_frame, text="Mouse & Keyboard clicker", text_color="gray", font=ctk.CTkFont(size=11))
        self.lbl_subtitle.pack(pady=(0, 25))
        
        self.btn_nav_clicker = ctk.CTkButton(self.sidebar_frame, text="Clicker", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=lambda: self.select_page("clicker"))
        self.btn_nav_clicker.pack(pady=6, padx=20, fill="x")
        
        self.btn_nav_silent = ctk.CTkButton(self.sidebar_frame, text="Silencieux", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=lambda: self.select_page("silent"))
        self.btn_nav_silent.pack(pady=6, padx=20, fill="x")
        
        self.btn_nav_macro = ctk.CTkButton(self.sidebar_frame, text="Macros", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=lambda: self.select_page("macro"))
        self.btn_nav_macro.pack(pady=6, padx=20, fill="x")
        
        # Author signature footer at the very bottom
        self.lbl_author = ctk.CTkLabel(self.sidebar_frame, text="@stala", text_color="#3498db", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_author.pack(side="bottom", pady=(5, 20))
        
        # Status Panel in Sidebar (moved here to save height)
        self.status_panel = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.status_panel.pack(side="bottom", pady=(15, 5))
        
        self.lbl_status_dot = ctk.CTkLabel(self.status_panel, text="●", text_color="#e74c3c", font=ctk.CTkFont(size=18))
        self.lbl_status_dot.pack(side="left", padx=(0, 6))
        
        self.lbl_status = ctk.CTkLabel(self.status_panel, text="Statut : INACTIF", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_status.pack(side="left")

        # -----------------------------------------
        # RIGHT: Main container
        # -----------------------------------------
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="right", fill="both", expand=True)
        
        # Bottom Panel (Toggle Button only)
        self.btn_toggle = ctk.CTkButton(self.main_container, text="DÉMARRER (Raccourci: F6)", font=ctk.CTkFont(size=16, weight="bold"), height=45, command=self.toggle_active_engine)
        self.btn_toggle.pack(side="bottom", pady=(4, 10), fill="x", padx=15)
        
        # Warning label
        self.lbl_warning = ctk.CTkLabel(self.main_container, text="", text_color="#e74c3c", font=ctk.CTkFont(size=11, weight="bold"))
        self.lbl_warning.pack(side="bottom", pady=2)

        # Shared Hotkey Card (Card 4)
        self.card_hotkey = ctk.CTkFrame(self.main_container)
        self.card_hotkey.pack(side="bottom", pady=4, fill="x", padx=15)
        
        self.lbl_sec_hotkey = ctk.CTkLabel(self.card_hotkey, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_hotkey.grid(row=0, column=0, columnspan=3, padx=15, pady=(8, 3), sticky="w")
        
        self.lbl_hk = ctk.CTkLabel(self.card_hotkey, text="Raccourci Global :")
        self.lbl_hk.grid(row=1, column=0, padx=(15, 10), pady=8, sticky="w")
        
        self.lbl_hotkey_display = ctk.CTkLabel(self.card_hotkey, text="F6", font=ctk.CTkFont(weight="bold"), text_color="#e74c3c")
        self.lbl_hotkey_display.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        
        self.btn_change_hotkey = ctk.CTkButton(self.card_hotkey, text="Changer le raccourci", command=self.start_recording_hotkey, width=150)
        self.btn_change_hotkey.grid(row=1, column=2, padx=20, pady=8, sticky="w")

        # Top pages frame switcher
        self.pages_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.pages_container.pack(side="top", fill="both", expand=True, pady=(5, 0))
        
        self.clicker_frame = ClickerFrame(self.pages_container, self)
        self.silent_frame = SilentClickerFrame(self.pages_container, self)
        self.macro_frame = ui_macro_frame(self.pages_container, self)
        
        # Default view
        self.clicker_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.active_tab = "clicker"
        
        # Key interception
        self.bind("<KeyPress>", self.on_window_key_pressed)

    # -------------------------------------------------------------
    # State synchronization & settings syncing
    # -------------------------------------------------------------
    def sync_settings_to_ui(self):
        # Language picker sync
        lang = self.settings_manager.get_language()
        if lang == "en":
            self.combo_lang.set("English")
        elif lang == "es":
            self.combo_lang.set("Español")
        else:
            self.combo_lang.set("Français")
            
        self.lbl_hotkey_display.configure(text=get_key_name(self.hotkey_manager.vk))
        
        # Restore clicker configs
        click_cfg = self.settings_manager.data.get("clicker", {})
        self.engine.interval_ms = click_cfg.get("interval_ms", 100.0)
        self.engine.mode = click_cfg.get("mode", "mouse")
        self.engine.mouse_button = click_cfg.get("button", "left")
        self.engine.mouse_double = click_cfg.get("double", False)
        self.engine.keyboard_vk = click_cfg.get("keyboard_vk", 0x20)
        
        # Refresh widgets visually
        self.refresh_texts()
        
    def select_page(self, page_name):
        if page_name == "clicker":
            self.btn_nav_clicker.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            self.btn_nav_silent.configure(fg_color="transparent")
            self.btn_nav_macro.configure(fg_color="transparent")
            self.macro_frame.pack_forget()
            self.silent_frame.pack_forget()
            self.clicker_frame.pack(fill="both", expand=True, padx=10, pady=5)
            self.active_tab = "clicker"
        elif page_name == "silent":
            self.btn_nav_clicker.configure(fg_color="transparent")
            self.btn_nav_silent.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            self.btn_nav_macro.configure(fg_color="transparent")
            self.clicker_frame.pack_forget()
            self.macro_frame.pack_forget()
            self.silent_frame.pack(fill="both", expand=True, padx=10, pady=5)
            self.active_tab = "silent"
        else:
            self.btn_nav_clicker.configure(fg_color="transparent")
            self.btn_nav_silent.configure(fg_color="transparent")
            self.btn_nav_macro.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            self.clicker_frame.pack_forget()
            self.silent_frame.pack_forget()
            self.macro_frame.pack(fill="both", expand=True, padx=10, pady=5)
            self.active_tab = "macro"
            
        self.clear_warning()
        self.refresh_texts()

    def on_language_changed(self, choice):
        if choice == "English":
            self.settings_manager.set_language("en")
        elif choice == "Español":
            self.settings_manager.set_language("es")
        else:
            self.settings_manager.set_language("fr")
            
        self.refresh_texts()
        self.clicker_frame.refresh_texts()
        self.silent_frame.refresh_texts()
        self.macro_frame.refresh_texts()

    def refresh_texts(self):
        t = self.settings_manager.get_text
        
        # Main labels
        self.lbl_subtitle.configure(text=t("subtitle"))
        self.btn_nav_clicker.configure(text=t("tab_clicker"))
        self.btn_nav_silent.configure(text=t("tab_silent"))
        self.btn_nav_macro.configure(text=t("tab_macro"))
        
        self.lbl_sec_hotkey.configure(text=t("sec_hotkey"))
        self.lbl_hk.configure(text=t("lbl_hotkey"))
        self.btn_change_hotkey.configure(text=t("btn_change_hotkey"))
        
        if self.recording_hotkey:
            self.btn_change_hotkey.configure(text=t("press_key"), fg_color="#e74c3c")
            
        self._sync_engine_state_ui(self.engine.active or self.macro_engine.active)

    # -------------------------------------------------------------
    # Keyboard Capture (Global Activation Hotkey)
    # -------------------------------------------------------------
    def start_recording_hotkey(self):
        if self.engine.active or self.macro_engine.active:
            return
        self.recording_hotkey = True
        self.clicker_frame.recording_target_key = False
        self.btn_change_hotkey.configure(text=self.settings_manager.get_text("press_key"), fg_color="#e74c3c")
        self.clear_warning()

    def on_window_key_pressed(self, event):
        vk = event.keycode
        
        # Route to clicker target recording if active
        if self.clicker_frame.handle_key_press(vk):
            return
            
        # Hook for shared activation hotkey recording
        if self.recording_hotkey:
            # Check for conflict
            if self.clicker_frame.engine.mode == "keyboard" and self.check_key_conflicts(self.clicker_frame.engine.keyboard_vk, vk):
                self.btn_change_hotkey.configure(text=self.settings_manager.get_text("btn_change_hotkey"), fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
                self.recording_hotkey = False
                return
                
            self.hotkey_manager.set_hotkey(vk)
            self.settings_manager.set_hotkey(vk)
            
            t = self.settings_manager.get_text
            self.lbl_hotkey_display.configure(text=get_key_name(vk))
            self.btn_change_hotkey.configure(text=t("btn_change_hotkey"), fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            self.btn_toggle.configure(text=f"{t('btn_start')} ({t('btn_raccourci')} {get_key_name(vk)})")
            self.recording_hotkey = False
            self.clear_warning()

    def check_key_conflicts(self, target_vk, hotkey_vk):
        t = self.settings_manager.get_text
        if self.active_tab == "clicker" and self.engine.mode == "keyboard" and target_vk == hotkey_vk:
            self.lbl_warning.configure(text=t("err_same_key", key=get_key_name(target_vk)))
            return True
        self.clear_warning()
        return False

    def clear_warning(self):
        self.lbl_warning.configure(text="")

    # -------------------------------------------------------------
    # Engines Execution Routing
    # -------------------------------------------------------------
    def toggle_active_engine(self):
        if self.active_tab == "clicker":
            if self.engine.active:
                self.engine.stop()
            else:
                self.clicker_frame.start_clicker()
        elif self.active_tab == "silent":
            if self.engine.active:
                self.engine.stop()
            else:
                self.silent_frame.start_clicker()
        else:
            if self.macro_engine.active:
                self.macro_engine.stop()
            else:
                self.start_macro_playback()

    def start_macro_playback(self):
        t = self.settings_manager.get_text
        if not self.macro_engine.actions:
            self.lbl_warning.configure(text=t("macro_err_no_actions"))
            return
            
        # Parse timing mode
        if self.macro_frame.timing_var.get() == "fixed":
            try:
                val = float(self.macro_frame.entry_fixed_ms.get())
                if val <= 0:
                    raise ValueError()
                self.macro_engine.fixed_delay_ms = val
            except ValueError:
                self.lbl_warning.configure(text=t("macro_err_fixed_delay"))
                return
                
        # Parse stops cycles
        stop_val = self.macro_frame.btn_segmented_stop.get()
        if stop_val in [t("stop_infinite"), "Infini", "Infinite", "Infinito"]:
            self.macro_engine.max_cycles = None
        else:
            try:
                cycles = int(self.macro_frame.entry_cycles.get())
                if cycles <= 0:
                    raise ValueError()
                self.macro_engine.max_cycles = cycles
            except ValueError:
                self.lbl_warning.configure(text=t("err_cycles"))
                return
                
        self.clear_warning()
        self.macro_engine.start()

    def on_engine_state_change(self, active):
        self.after(0, self._sync_engine_state_ui, active)

    def _sync_engine_state_ui(self, active):
        t = self.settings_manager.get_text
        if active:
            self.lbl_status_dot.configure(text_color="#2ecc71") # Green LED
            self.btn_toggle.configure(text=f"{t('btn_stop')} ({t('btn_raccourci')} {get_key_name(self.hotkey_manager.vk)})", fg_color="#e74c3c", hover_color="#c0392b")
            
            # Lock Navigation and main config options
            self.btn_nav_clicker.configure(state="disabled")
            self.btn_nav_silent.configure(state="disabled")
            self.btn_nav_macro.configure(state="disabled")
            self.combo_lang.configure(state="disabled")
            self.btn_change_hotkey.configure(state="disabled")
            
            if self.active_tab == "clicker":
                self.clicker_frame.disable_inputs(True)
            elif self.active_tab == "silent":
                self.silent_frame.disable_inputs(True)
            else:
                self.macro_frame.disable_inputs(True)
        else:
            self.lbl_status_dot.configure(text_color="#e74c3c") # Red LED
            self.btn_toggle.configure(text=f"{t('btn_start')} ({t('btn_raccourci')} {get_key_name(self.hotkey_manager.vk)})", fg_color="#3498db", hover_color="#2980b9")
            self.lbl_status.configure(text=t("status_inactive"))
            
            # Unlock Nav
            self.btn_nav_clicker.configure(state="normal")
            self.btn_nav_silent.configure(state="normal")
            self.btn_nav_macro.configure(state="normal")
            self.combo_lang.configure(state="normal")
            self.btn_change_hotkey.configure(state="normal")
            
            self.clicker_frame.disable_inputs(False)
            self.silent_frame.disable_inputs(False)
            self.macro_frame.disable_inputs(False)

    def _format_time(self, seconds):
        rem_h = int(seconds // 3600)
        rem_m = int((seconds % 3600) // 60)
        rem_s = int(seconds % 60)
        rem_ms = int((seconds * 10) % 10)
        
        if rem_h > 0:
            return f"{rem_h:02d}h {rem_m:02d}m {rem_s:02d}s"
        elif rem_m > 0:
            return f"{rem_m:02d}m {rem_s:02d}s"
        else:
            return f"{rem_s}.{rem_ms}s"

    def update_status_loop(self):
        t = self.settings_manager.get_text
        
        if self.active_tab == "clicker" or self.active_tab == "silent":
            if self.engine.active:
                if self.engine.duration_sec is not None:
                    elapsed = time.perf_counter() - self.engine.start_perf_time
                    remaining = max(0.0, self.engine.duration_sec - elapsed)
                    time_str = self._format_time(remaining)
                    self.lbl_status.configure(text=t("status_active_timer", time=time_str))
                elif self.engine.max_clicks is not None:
                    rem_clicks = max(0, self.engine.max_clicks - self.engine.click_count)
                    self.lbl_status.configure(text=t("status_active_cycles", cycles=rem_clicks))
                else:
                    if self.active_tab == "silent":
                        self.lbl_status.configure(text=t("status_active_silent"))
                    else:
                        self.lbl_status.configure(text=t("status_active_inf"))
            else:
                self.lbl_status.configure(text=t("status_inactive"))
                
        else: # active_tab == "macro"
            if self.macro_engine.active:
                if self.macro_engine.max_cycles is not None:
                    rem_cycles = max(0, self.macro_engine.max_cycles - self.macro_engine.cycles_executed)
                    self.lbl_status.configure(text=t("macro_lbl_status_active_cycles", cycles=rem_cycles))
                else:
                    self.lbl_status.configure(text=t("macro_lbl_status_active_inf"))
            elif self.macro_frame.recording:
                self.lbl_status.configure(text=t("macro_lbl_status_recording", hotkey=get_key_name(self.hotkey_manager.vk)))
            else:
                self.lbl_status.configure(text=t("status_inactive"))
                
        self.after(50, self.update_status_loop)

    def on_closing(self):
        # Save current config to settings.json
        click_cfg = {
            "interval_ms": self.engine.interval_ms,
            "mode": self.engine.mode,
            "button": self.engine.mouse_button,
            "double": self.engine.mouse_double,
            "keyboard_vk": self.engine.keyboard_vk
        }
        self.settings_manager.data["clicker"] = click_cfg
        
        # Save silent configs
        self.silent_frame.save_settings()
        
        self.settings_manager.save()
        
        self.engine.stop()
        self.macro_engine.stop()
        self.hotkey_manager.stop()
        self.destroy()

if __name__ == "__main__":
    app = EveryClickerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

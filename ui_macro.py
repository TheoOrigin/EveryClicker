import ctypes
from ctypes import wintypes
import threading
import time
import tkinter as tk
import customtkinter as ctk
from settings import get_key_name

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Win32 Hook Hookproc type
HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_longlong, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
WH_KEYBOARD_LL = 13

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong)
    ]

class ui_macro_frame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.engine = app.macro_engine
        
        self.recording = False
        self.recorded_events = []
        self.last_event_time = 0.0
        
        # Hook thread fields
        self.hook_thread = None
        self.hook_thread_id = None
        self.hook_id = None
        self.hook_proc = HOOKPROC(self._hook_callback)
        
        self.create_widgets()
        self.refresh_texts()
        self.refresh_macros_combo()

    def create_widgets(self):
        # -----------------------------------------
        # Card 1: Enregistrement et Contrôles
        # -----------------------------------------
        self.card_controls = ctk.CTkFrame(self)
        self.card_controls.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_controls = ctk.CTkLabel(self.card_controls, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_controls.grid(row=0, column=0, columnspan=4, padx=15, pady=(5, 2), sticky="w")
        
        self.btn_record = ctk.CTkButton(self.card_controls, text="Enregistrer", width=140, fg_color="#c0392b", hover_color="#962d22", command=self.toggle_recording)
        self.btn_record.grid(row=1, column=0, padx=15, pady=5, sticky="w")
        
        self.btn_clear = ctk.CTkButton(self.card_controls, text="Effacer", width=90, fg_color="#7f8c8d", hover_color="#5d6d7e", command=self.clear_recorded)
        self.btn_clear.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.lbl_actions_count = ctk.CTkLabel(self.card_controls, text="Actions: 0", font=ctk.CTkFont(weight="bold"))
        self.lbl_actions_count.grid(row=1, column=2, padx=15, pady=5, sticky="w")
        
        # CTkTextbox to list recorded keys
        self.txt_events = ctk.CTkTextbox(self.card_controls, height=100, width=420, font=ctk.CTkFont(family="Consolas", size=11))
        self.txt_events.grid(row=2, column=0, columnspan=4, padx=15, pady=(3, 5), sticky="ew")
        self.txt_events.configure(state="disabled")

        # -----------------------------------------
        # Card 1.5: Sauvegarde des macros
        # -----------------------------------------
        self.card_save = ctk.CTkFrame(self)
        self.card_save.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_save = ctk.CTkLabel(self.card_save, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_save.grid(row=0, column=0, columnspan=3, padx=15, pady=(5, 2), sticky="w")
        
        self.lbl_macro_name = ctk.CTkLabel(self.card_save, text="Macro :")
        self.lbl_macro_name.grid(row=1, column=0, padx=(15, 8), pady=4, sticky="w")
        
        self.combo_macros = ctk.CTkComboBox(self.card_save, values=[], width=280, command=self.on_macro_selected)
        self.combo_macros.grid(row=1, column=1, columnspan=2, padx=5, pady=4, sticky="w")
        
        self.btn_save_macro = ctk.CTkButton(self.card_save, text="Sauvegarder", width=135, fg_color="#27ae60", hover_color="#219653", command=self.on_save_macro_clicked)
        self.btn_save_macro.grid(row=2, column=1, padx=5, pady=(0, 5), sticky="w")
        
        self.btn_del_macro = ctk.CTkButton(self.card_save, text="Supprimer", width=135, fg_color="#c0392b", hover_color="#962d22", command=self.on_delete_macro_clicked)
        self.btn_del_macro.grid(row=2, column=2, padx=5, pady=(0, 5), sticky="w")

        # -----------------------------------------
        # Card 2: Gestion des Délais (Enregistré vs Fixe)
        # -----------------------------------------
        self.card_timing = ctk.CTkFrame(self)
        self.card_timing.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_timing = ctk.CTkLabel(self.card_timing, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_timing.grid(row=0, column=0, columnspan=2, padx=15, pady=(5, 2), sticky="w")
        
        self.timing_var = tk.StringVar(value="real")
        self.radio_real = ctk.CTkRadioButton(self.card_timing, text="Délai réel", value="real", variable=self.timing_var, command=self.on_timing_mode_changed)
        self.radio_real.grid(row=1, column=0, padx=15, pady=5, sticky="w")
        
        self.radio_fixed = ctk.CTkRadioButton(self.card_timing, text="Délai fixe (ms)", value="fixed", variable=self.timing_var, command=self.on_timing_mode_changed)
        self.radio_fixed.grid(row=1, column=1, padx=15, pady=5, sticky="w")
        self.radio_real.select()
        
        self.frame_fixed_val = ctk.CTkFrame(self.card_timing, fg_color="transparent")
        
        self.entry_fixed_ms = ctk.CTkEntry(self.frame_fixed_val, width=100, placeholder_text="100")
        self.entry_fixed_ms.grid(row=0, column=0, padx=(0, 10), pady=3, sticky="w")
        self.entry_fixed_ms.insert(0, "100.0")

        # -----------------------------------------
        # Card 3: Conditions d'arrêt Lecture (Infini / Cycles)
        # -----------------------------------------
        self.card_stop = ctk.CTkFrame(self)
        self.card_stop.pack(pady=4, fill="x", padx=15)
        
        self.lbl_sec_stop = ctk.CTkLabel(self.card_stop, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db")
        self.lbl_sec_stop.grid(row=0, column=0, columnspan=3, padx=15, pady=(5, 2), sticky="w")
        
        self.btn_segmented_stop = ctk.CTkSegmentedButton(self.card_stop, values=["Infini", "Cycles"], command=self.on_stop_mode_changed)
        self.btn_segmented_stop.grid(row=1, column=0, columnspan=3, padx=15, pady=5, sticky="ew")
        self.btn_segmented_stop.set("Infini")
        
        self.frame_stop_cycles = ctk.CTkFrame(self.card_stop, fg_color="transparent")
        self.lbl_cycles_title = ctk.CTkLabel(self.frame_stop_cycles, text="Répéter :")
        self.lbl_cycles_title.grid(row=0, column=0, padx=(0, 10), pady=3, sticky="w")
        self.entry_cycles = ctk.CTkEntry(self.frame_stop_cycles, width=100, placeholder_text="10")
        self.entry_cycles.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.entry_cycles.insert(0, "10")
        self.lbl_cycles_unit = ctk.CTkLabel(self.frame_stop_cycles, text="fois", text_color="gray")
        self.lbl_cycles_unit.grid(row=0, column=2, padx=5, pady=3, sticky="w")

    def refresh_texts(self):
        t = self.app.settings_manager.get_text
        self.lbl_sec_controls.configure(text=t("macro_sec_controls"))
        
        if self.recording:
            self.btn_record.configure(text=t("macro_btn_stop_record"), fg_color="#f39c12", hover_color="#d35400")
        else:
            self.btn_record.configure(text=t("macro_btn_record"), fg_color="#c0392b", hover_color="#962d22")
            
        self.btn_clear.configure(text=t("macro_btn_clear"))
        self.lbl_actions_count.configure(text=t("macro_lbl_actions", count=len(self.recorded_events)))
        
        self.lbl_sec_save.configure(text=t("macro_sec_save"))
        self.lbl_macro_name.configure(text=t("macro_lbl_macro_name"))
        self.btn_save_macro.configure(text=t("macro_btn_save_macro"))
        self.btn_del_macro.configure(text=t("macro_btn_del_macro"))
        
        self.lbl_sec_timing.configure(text=t("macro_sec_timing"))
        self.radio_real.configure(text=t("macro_radio_real"))
        self.radio_fixed.configure(text=t("macro_fixed_delay"))
        
        self.lbl_sec_stop.configure(text=t("macro_sec_stop"))
        
        current_stop = self.btn_segmented_stop.get()
        self.btn_segmented_stop.configure(values=[t("stop_infinite"), t("stop_cycles")])
        if current_stop in ["Infini", "Infinite", "Infinito"]:
            self.btn_segmented_stop.set(t("stop_infinite"))
        else:
            self.btn_segmented_stop.set(t("stop_cycles"))
            
        self.lbl_cycles_title.configure(text=t("lbl_cycles"))
        self.lbl_cycles_unit.configure(text=t("lbl_cycles_unit"))
        
        self.update_log_display()

    # Macros selection
    def refresh_macros_combo(self):
        macros = self.app.settings_manager.get_macros()
        names = list(macros.keys())
        self.combo_macros.configure(values=names)
        if names:
            self.combo_macros.set(names[0])
        else:
            self.combo_macros.set("")

    def on_macro_selected(self, name):
        macros = self.app.settings_manager.get_macros()
        macro = macros.get(name, [])
        if macro:
            self.recorded_events = macro
            self.engine.actions = macro
            self.refresh_texts()

    def on_save_macro_clicked(self):
        t = self.app.settings_manager.get_text
        if not self.recorded_events:
            self.app.lbl_warning.configure(text=t("macro_err_no_actions"))
            return
            
        dialog = ctk.CTkInputDialog(text=t("macro_lbl_macro_name"), title="Macro")
        name = dialog.get_input()
        if name:
            self.app.settings_manager.add_macro(name, self.recorded_events)
            self.app.clear_warning()
            self.refresh_macros_combo()
            self.combo_macros.set(name)

    def on_delete_macro_clicked(self):
        name = self.combo_macros.get()
        if name:
            self.app.settings_manager.delete_macro(name)
            self.recorded_events = []
            self.engine.actions = []
            self.refresh_macros_combo()
            self.refresh_texts()

    # Timing Mode
    def on_timing_mode_changed(self):
        if self.timing_var.get() == "real":
            self.frame_fixed_val.grid_forget()
            self.engine.timing_mode = "real"
        else:
            self.frame_fixed_val.grid(row=2, column=0, columnspan=2, padx=15, pady=(2, 5), sticky="w")
            self.engine.timing_mode = "fixed"

    # Stop Mode
    def on_stop_mode_changed(self, mode):
        t = self.app.settings_manager.get_text
        self.frame_stop_cycles.grid_forget()
        if mode in [t("stop_cycles"), "Cycles", "Ciclos"]:
            self.frame_stop_cycles.grid(row=2, column=0, columnspan=3, padx=15, pady=(2, 5), sticky="ew")

    # Global Hook Thread Logic
    def toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        if self.engine.active or self.app.engine.active:
            return
            
        self.recording = True
        self.recorded_events = []
        self.last_event_time = time.perf_counter()
        
        self.app.btn_toggle.configure(state="disabled")
        self.refresh_texts()
        
        # Start hook thread
        self.hook_thread = threading.Thread(target=self._run_hook, daemon=True)
        self.hook_thread.start()

    def stop_recording(self):
        if not self.recording:
            return
            
        self.recording = False
        
        # Signal hook thread to quit
        if self.hook_thread_id is not None:
            WM_QUIT = 0x0012
            user32.PostThreadMessageW(self.hook_thread_id, WM_QUIT, 0, 0)
            self.hook_thread_id = None
            
        self.app.btn_toggle.configure(state="normal")
        
        # Assign to engine
        self.engine.actions = self.recorded_events
        self.refresh_texts()

    def clear_recorded(self):
        self.recorded_events = []
        self.engine.actions = []
        self.refresh_texts()

    def _run_hook(self):
        self.hook_thread_id = kernel32.GetCurrentThreadId()
        self.hook_id = user32.SetWindowsHookExW(WH_KEYBOARD_LL, self.hook_proc, None, 0)
        if not self.hook_id:
            print("Failed to install low-level keyboard hook")
            return
            
        try:
            msg = wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        finally:
            user32.UnhookWindowsHookEx(self.hook_id)
            self.hook_id = None

    def _hook_callback(self, nCode, wParam, lParam):
        if nCode >= 0:
            kb = KBDLLHOOKSTRUCT.from_address(lParam)
            vk = kb.vkCode
            
            # Ignore the global activation hotkey to avoid recording the stop command!
            if vk != self.app.hotkey_manager.vk:
                is_down = wParam in [WM_KEYDOWN, WM_SYSKEYDOWN]
                is_up = wParam in [WM_KEYUP, WM_SYSKEYUP]
                
                if is_down or is_up:
                    now = time.perf_counter()
                    # Calculate delay
                    delay = now - self.last_event_time
                    self.last_event_time = now
                    
                    event_dict = {
                        "type": "down" if is_down else "up",
                        "vk": vk,
                        "delay": delay
                    }
                    self.recorded_events.append(event_dict)
                    
                    # Schedule UI update on main thread
                    self.after(0, self.update_log_display)
            else:
                # If hotkey pressed, stop recording
                is_down = wParam in [WM_KEYDOWN, WM_SYSKEYDOWN]
                if is_down:
                    self.after(0, self.stop_recording)
                    
        return user32.CallNextHookEx(None, nCode, wParam, lParam)

    def update_log_display(self):
        self.txt_events.configure(state="normal")
        self.txt_events.delete("1.0", "end")
        
        lines = []
        for i, ev in enumerate(self.recorded_events):
            t_str = "DOWN" if ev["type"] == "down" else "UP"
            key_name = get_key_name(ev["vk"])
            delay = ev["delay"]
            lines.append(f"#{i+1:03d} | {t_str:<4} | Key: {key_name:<12} | Delay: {delay:.3f}s")
            
        self.txt_events.insert("1.0", "\n".join(lines))
        self.txt_events.see("end")
        self.txt_events.configure(state="disabled")
        self.lbl_actions_count.configure(text=f"Actions: {len(self.recorded_events)}")

    def disable_inputs(self, disable=True):
        state = "disabled" if disable else "normal"
        self.btn_record.configure(state=state)
        self.btn_clear.configure(state=state)
        self.combo_macros.configure(state=state)
        self.btn_save_macro.configure(state=state)
        self.btn_del_macro.configure(state=state)
        self.radio_real.configure(state=state)
        self.radio_fixed.configure(state=state)
        self.entry_fixed_ms.configure(state=state)
        self.btn_segmented_stop.configure(state=state)
        self.entry_cycles.configure(state=state)

import threading
import time
import ctypes
import input_sim

winmm = ctypes.windll.winmm

class ClickerEngine:
    def __init__(self, state_change_callback):
        self.active = False
        self.thread = None
        
        # Configurations
        self.mode = "mouse"  # "mouse" or "keyboard"
        self.mouse_button = "left"  # "left", "right", "middle"
        self.mouse_double = False
        self.keyboard_vk = 0x20  # Space
        self.interval_ms = 100.0
        
        # Silent/Randomized Configurations
        self.random_mode = False
        self.min_interval_ms = 10.0
        self.max_interval_ms = 100.0
        self.bias_mode = "uniform"  # "uniform" or "biased"
        self.bias_split_ms = 70.0
        self.bias_percent = 70
        self.bias_direction = "above"  # "above" or "below"
        
        # Stopping conditions
        self.duration_sec = None
        self.max_clicks = None
        self.click_count = 0
        
        self.start_perf_time = 0.0
        self.state_change_callback = state_change_callback
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            if self.active:
                return
            self.active = True
            self.click_count = 0
            
            try:
                winmm.timeBeginPeriod(1)
            except:
                pass
                
            self.start_perf_time = time.perf_counter()
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()
            self.state_change_callback(True)

    def stop(self):
        with self.lock:
            if not self.active:
                return
            self.active = False
            try:
                winmm.timeEndPeriod(1)
            except:
                pass
            self.state_change_callback(False)

    def toggle(self):
        if self.active:
            self.stop()
        else:
            self.start()

    def _loop(self):
        import random
        end_time = (self.start_perf_time + self.duration_sec) if self.duration_sec is not None else None

        while self.active:
            now = time.perf_counter()
            
            # Check timer condition
            if end_time is not None and now >= end_time:
                self.active = False
                self.state_change_callback(False)
                try:
                    winmm.timeEndPeriod(1)
                except:
                    pass
                break

            # Check cycles condition
            if self.max_clicks is not None and self.click_count >= self.max_clicks:
                self.active = False
                self.state_change_callback(False)
                try:
                    winmm.timeEndPeriod(1)
                except:
                    pass
                break

            # Calculate interval for this click
            if self.random_mode:
                min_sec = self.min_interval_ms / 1000.0
                max_sec = self.max_interval_ms / 1000.0
                if min_sec > max_sec:
                    min_sec, max_sec = max_sec, min_sec
                
                if self.bias_mode == "biased":
                    split_sec = self.bias_split_ms / 1000.0
                    split_sec = max(min_sec, min(max_sec, split_sec))
                    
                    r = random.random()
                    percent_val = self.bias_percent / 100.0
                    
                    if r < percent_val:
                        if self.bias_direction == "above":
                            interval_sec = random.uniform(split_sec, max_sec)
                        else:
                            interval_sec = random.uniform(min_sec, split_sec)
                    else:
                        if self.bias_direction == "above":
                            interval_sec = random.uniform(min_sec, split_sec)
                        else:
                            interval_sec = random.uniform(split_sec, max_sec)
                else:
                    interval_sec = random.uniform(min_sec, max_sec)
            else:
                interval_sec = self.interval_ms / 1000.0

            loop_start = time.perf_counter()

            # Execute action
            if self.mode == "mouse":
                input_sim.perform_click(self.mouse_button, self.mouse_double, interval_sec)
                self.click_count += 1
            else:
                input_sim.perform_key_press(self.keyboard_vk, interval_sec)
                self.click_count += 1

            # High precision scheduler sleep calculation
            elapsed = time.perf_counter() - loop_start
            sleep_time = interval_sec - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)


class MacroEngine:
    def __init__(self, state_change_callback):
        self.active = False
        self.thread = None
        
        # Configurations
        self.actions = []  # List of dicts: {"type": "down"/"up", "vk": vk_code, "delay": delay_seconds}
        self.timing_mode = "real"  # "real" or "fixed"
        self.fixed_delay_ms = 100.0
        self.speed_multiplier = 1.0
        
        # Stopping conditions
        self.max_cycles = None  # None for infinite
        self.cycles_executed = 0
        
        self.state_change_callback = state_change_callback
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            if self.active:
                return
            if not self.actions:
                return
            self.active = True
            self.cycles_executed = 0
            
            try:
                winmm.timeBeginPeriod(1)
            except:
                pass
                
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()
            self.state_change_callback(True)

    def stop(self):
        with self.lock:
            if not self.active:
                return
            self.active = False
            try:
                winmm.timeEndPeriod(1)
            except:
                pass
            self.state_change_callback(False)

    def toggle(self):
        if self.active:
            self.stop()
        else:
            self.start()

    def _loop(self):
        cycles_count = 0
        
        while self.active:
            # Check cycle limits
            if self.max_cycles is not None and cycles_count >= self.max_cycles:
                self.active = False
                self.state_change_callback(False)
                try:
                    winmm.timeEndPeriod(1)
                except:
                    pass
                break
                
            # Play macro sequence once
            for event in self.actions:
                if not self.active:
                    break
                    
                # Delay calculation
                if self.timing_mode == "fixed":
                    delay = self.fixed_delay_ms / 1000.0
                else:
                    delay = event.get("delay", 0.0) / self.speed_multiplier
                    
                if delay > 0:
                    time.sleep(delay)
                    
                if not self.active:
                    break
                    
                # Execute action
                vk = event["vk"]
                is_down = (event["type"] == "down")
                try:
                    if is_down:
                        input_sim.send_key_down(vk)
                    else:
                        input_sim.send_key_up(vk)
                except:
                    pass
            
            cycles_count += 1
            self.cycles_executed = cycles_count
            
            # Avoid lockups if empty macro list is somehow executed
            if not self.actions:
                time.sleep(0.1)
                
        # Un-press any stuck keys on stop
        self._release_all_keys()
        
        self.active = False
        self.state_change_callback(False)

    def _release_all_keys(self):
        # Scan through recorded keys and ensure they are all released
        vks = set(event["vk"] for event in self.actions)
        for vk in vks:
            try:
                input_sim.send_key_up(vk)
            except:
                pass

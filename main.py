import customtkinter as ctk
from tkintermapview import TkinterMapView
from geopy.distance import geodesic
import datetime
import csv
import os
import shutil
from tkinter import filedialog, messagebox

# --- NASTAVENÍ BARVIČEK (Světlý/Tmavý režim ☀️🌑) ---
BG_COLOR = ("#F2F2F7", "#0D0E1A")        
PANEL_COLOR = ("#FFFFFF", "#15162B")     
ACCENT_COLOR = "#00A3FF"                 
TEXT_COLOR = ("#111111", "#E0E0FF")      
DANGER_COLOR = "#FF3366"                 

ctk.set_appearance_mode("Dark") 

def locator_to_latlon(locator):
    """ Převod Maidenhead lokátoru na souřadnice 🧭 """
    locator = locator.strip().upper()
    if len(locator) < 4: return None
    try:
        lon = (ord(locator[0]) - ord('A')) * 20 - 180
        lat = (ord(locator[1]) - ord('A')) * 10 - 90
        lon += int(locator[2]) * 2
        lat += int(locator[3])
        if len(locator) >= 6:
            lon += (ord(locator[4]) - ord('A') + 0.5) / 12
            lat += (ord(locator[5]) - ord('A') + 0.5) / 24
        else:
            lon += 1; lat += 0.5
        return lat, lon
    except Exception:
        return None

class CB_PMR_Logbook(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CB PMR Logbook – Celoroční Soutěžní Edice 2026/2027 📻💎")
        self.geometry("1450x880")
        self.configure(fg_color=BG_COLOR)

        # === KOMPLETNÍ KALENDÁŘ ZÁVODŮ NA ROK DOPŘEDU (2026 - 2027) === 🗓️🏆
        self.contest_details = {
            "Letní PMR Štafeta [PMR] (13.06.2026)": (
                "📟 Pásmo: PMR (446 MHz)\n"
                "🗓️ Přesné datum: 13. června 2026\n"
                "📜 Podrobnosti: Velká letní štafeta, kde signál putuje z jednoho konce republiky na druhý "
                "přes hřebeny hor. Perfektní prověření portablové techniky v teplém letním počasí! ☀️⛰️"
            ),
            "Letní Polní Den – LPD [PMR] (25.07. – 26.07.2026)": (
                "📟 Pásmo: PMR (446 MHz)\n"
                "🗓️ Přesné datum: 25. července – 26. července 2026\n"
                "📜 Podrobnosti: Legendární letní 24hodinový maraton. Vysílá se výhradně z přenosných "
                "stanic z kopečků, rozhleden a ptačích perspektiv. Hodnotí se kilometry i počet QSO! ☀️🏕️"
            ),
            "Srpnový PMR Sprint [PMR] (09.08.2026)": (
                "📟 Pásmo: PMR (446 MHz)\n"
                "🗓️ Přesné datum: 9. srpna 2026 (Neděle)\n"
                "📜 Podrobnosti: Rychlá nedělní soutěž zaměřená na maximální aktivaci domácích i portablových "
                "lokátorů. Ideální na vyhnání nudy z pásma! ⚡🏃‍♂️"
            ),
            "CB Maratón – 48 hodin [CB] (18.09. – 20.09.2026)": (
                "📟 Pásmo: CB (27 MHz, FM kanály)\n"
                "🗓️ Přesné datum: 18. září – 20. září 2026\n"
                "📜 Podrobnosti: Vytrvalostní závod, kde stanice jedou nonstop celý víkend. Počítají se "
                "dálková spojení napříč kraji a evropskými státy.🔋🌌"
            ),
            "Podzimní PMR Štafeta [PMR] (28.10.2026)": (
                "📟 Pásmo: PMR (446 MHz)\n"
                "🗓️ Přesné datum: 28. října 2026 (Státní svátek)\n"
                "📜 Podrobnosti: Pokus o kompletní řetězení signálu kolem dokola celé republiky z kopce na kopec. "
                "Zapisuje se přesný čas předání štafetového kolíku! 🍁⛰️"
            ),
            "Vánoční Závod éterem [CB + PMR] (26.12.2026)": (
                "📟 Pásmo: CB i PMR (Kombinovaný závod)\n"
                "🗓️ Přesné datum: 26. prosince 2026 (Štěpánské vysílání)\n"
                "📜 Podrobnosti: Tradiční sváteční setkání na pásmu. Všichni testují nové staničky a antény, "
                "které našli pod stromečkem! 🎄❄️"
            ),
            "Novoroční PMR Štafeta [PMR] (01.01.2027)": (
                "📟 Pásmo: PMR (446 MHz)\n"
                "🗓️ Přesné datum: 1. ledna 2027 (Nový rok)\n"
                "📜 Podrobnosti: První velký závod nového roku. Začíná se hned po obědě (14:00). Prověří tvou "
                "techniku v drsných zimních podmínkách! 🥶❄️"
            ),
            "Zimní PMR Kopec [PMR] (13.02.2027)": (
                "📟 Pásmo: PMR (446 MHz)\n"
                "🗓️ Přesné datum: 13. února 2027\n"
                "📜 Podrobnosti: Zimní pohár zaměřený na přežití a vysílání ze sněhem zapadaných vrcholů. "
                "Zde mají násobiče bodů stanice s vyšší nadmořskou výškou! 🏔️⛷️"
            ),
            "Jarní CB Sprint [CB] (21.03.2027)": (
                "📟 Pásmo: CB (27 MHz)\n"
                "🗓️ Přesné datum: 21. března 2027\n"
                "📜 Podrobnosti: Otevírání jarní CB sezóny. Krátký, dynamický závod zaměřený na odrazové "
                "vlny a lokální rychlospojení. 🌸📟"
            ),
            "Velikonoční éter [CB + PMR] (28.03.2027)": (
                "📟 Pásmo: CB i PMR (Dual band akce)\n"
                "🗓️ Přesné datum: 28. března 2027\n"
                "📜 Podrobnosti: Celodenní jarní výzva pro všechny mobilní i stacionární operátory. "
                "Loví se bonusové stanice s pomlázkou! 🥚🐣"
            ),
            "Čarodějnický DX Kontest [CB] (30.04.2027)": (
                "📟 Pásmo: CB (Všech 40 kanálů)\n"
                "🗓️ Přesné datum: 30. dubna 2027 (Noční provoz)\n"
                "📜 Podrobnosti: Magická noc plná dalekých DX spojení. Díky sníženému průmyslovému šumu v noci "
                "lze udělat rekordní vzdálenosti! 🔥🧹"
            ),
            "Éter Bez Hranic – EBH [CB] (22.05. – 23.05.2027)": (
                "📟 Pásmo: CB (Občanské stanice)\n"
                "🗓️ Přesné datum: 22. května – 23. května 2027\n"
                "📜 Podrobnosti: Král mezi českými a slovenskými CB závody! Desítky expedic na kótách po obou "
                "stranách hranice soutěží celou noc. Výstupy se posílají do CL6! 👑🇨🇿🇸🇰"
            )
        }

        # === AUTOMATICKÁ INTEGRACE DO DATABÁZE DENÍKŮ === 🗄️
        self.logbooks_data = {
            "Hlavní Deník": [],
            "Znojmo Portábl": []
        }
        for contest_key in self.contest_details.keys():
            self.logbooks_data[contest_key] = []

        self.current_log_name = "Hlavní Deník"

        self.my_marker = None
        self.contact_markers = []
        self.map_paths = []

        # --- HLAVNÍ ROZVRŽENÍ ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= 1. SIDEBAR (Boční Panel) 📱 =================
        self.sidebar = ctk.CTkFrame(self, fg_color=PANEL_COLOR, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="CB\nPMR", font=ctk.CTkFont(size=28, weight="bold"), text_color=ACCENT_COLOR)
        self.logo_label.pack(pady=30)

        menu_items = ["🏠 Dashboard", "📡 Live Log (Správce)", "🏆 Contests (Závody)", "⚙️ Settings"]
        self.menu_buttons = []
        
        for item in menu_items:
            btn = ctk.CTkButton(self.sidebar, text=item, fg_color="transparent", text_color=TEXT_COLOR, 
                                hover_color="#00A3FF", anchor="w", font=ctk.CTkFont(size=14),
                                command=lambda name=item: self.switch_frame(name))
            btn.pack(padx=15, pady=5, fill="x")
            self.menu_buttons.append(btn)

        # ================= HLAVNÍ CONTAINER PRO STRÁNKY =================
        self.main_container = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.frames = {
            "🏠 Dashboard": ctk.CTkFrame(self.main_container, fg_color="transparent"),
            "📡 Live Log (Správce)": ctk.CTkFrame(self.main_container, fg_color="transparent"),
            "🏆 Contests (Závody)": ctk.CTkFrame(self.main_container, fg_color="transparent"),
            "⚙️ Settings": ctk.CTkFrame(self.main_container, fg_color="transparent")
        }

        self.build_dashboard()
        self.build_live_log_manager()
        self.build_contests()
        self.build_settings()
        
        self.switch_frame("🏠 Dashboard")

    def switch_frame(self, frame_name):
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[frame_name].grid(row=0, column=0, sticky="nsew")
        if frame_name == "📡 Live Log (Správce)":
            self.refresh_log_manager_list()

    # ================= STAVBA OBSAHU OBRAZOVEK =================

    def build_dashboard(self):
        frame = self.frames["🏠 Dashboard"]
        frame.grid_columnconfigure(0, weight=2)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        # TOP PANEL 🏠
        self.top_panel = ctk.CTkFrame(frame, fg_color=PANEL_COLOR, height=60, corner_radius=12)
        self.top_panel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        ctk.CTkLabel(self.top_panel, text="Můj Lokátor (QTH):", font=ctk.CTkFont(weight="bold"), text_color=TEXT_COLOR).pack(side="left", padx=(20, 10))
        self.entry_my_locator = ctk.CTkEntry(self.top_panel, width=100, fg_color=BG_COLOR, border_color=ACCENT_COLOR)
        self.entry_my_locator.insert(0, "JN78XU")
        self.entry_my_locator.pack(side="left", padx=10)
        ctk.CTkButton(self.top_panel, text="Set QTH 🏠", width=80, command=self.update_my_qth, fg_color=ACCENT_COLOR).pack(side="left", padx=10)

        ctk.CTkLabel(self.top_panel, text="Aktivní Deník:", font=ctk.CTkFont(weight="bold"), text_color=ACCENT_COLOR).pack(side="left", padx=(40, 10))
        self.dropdown_active_log = ctk.CTkOptionMenu(self.top_panel, values=list(self.logbooks_data.keys()), command=self.change_active_log, fg_color=BG_COLOR, button_color=ACCENT_COLOR, text_color=TEXT_COLOR, width=320)
        self.dropdown_active_log.set(self.current_log_name)
        self.dropdown_active_log.pack(side="left", padx=10)

        # LEVÁ STRANA (Mapa + Tabulka spojení) 🗺️📊
        self.left_column = ctk.CTkFrame(frame, fg_color="transparent")
        self.left_column.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.left_column.grid_rowconfigure(0, weight=3)
        self.left_column.grid_rowconfigure(1, weight=2)
        self.left_column.grid_columnconfigure(0, weight=1)

        # MAPA S FIXACÍ PLÁTNA PROTI PROBLIKÁVÁNÍ BAREV 🗺️🛠️
        self.map_widget = TkinterMapView(
            self.left_column,
            corner_radius=15,
            bg_color=BG_COLOR[1] if ctk.get_appearance_mode() == "Dark" else BG_COLOR[0]
        )
        self.map_widget.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.map_widget.set_zoom(7)

        self.log_frame = ctk.CTkFrame(self.left_column, fg_color=PANEL_COLOR, corner_radius=15)
        self.log_frame.grid(row=1, column=0, sticky="nsew")
        
        header_frame = ctk.CTkFrame(self.log_frame, fg_color=BG_COLOR, corner_radius=5, height=30)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        headers = ["Čas (PC) ⏱️", "Volací znak 📡", "Lokátor 📍", "RST 📊", "Vzdálenost 📏"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(header_frame, text=h, font=ctk.CTkFont(size=11, weight="bold"), text_color="#888").place(relx=i*0.2, rely=0.5, anchor="w", x=10)

        self.log_scroll = ctk.CTkScrollableFrame(self.log_frame, fg_color="transparent")
        self.log_scroll.pack(fill="both", expand=True, padx=10, pady=5)
        self.drawn_qso_rows = []

        # PRAVÁ STRANA (Formulář zápisu) ⚡📝
        self.right_column = ctk.CTkFrame(frame, fg_color=PANEL_COLOR, corner_radius=15)
        self.right_column.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(self.right_column, text="QUICK LOG QSO 📡", font=ctk.CTkFont(size=16, weight="bold"), text_color=ACCENT_COLOR).pack(pady=20)
        self.entry_call = ctk.CTkEntry(self.right_column, placeholder_text="Volací znak protistanice", fg_color=BG_COLOR, text_color=TEXT_COLOR)
        self.entry_call.pack(pady=10, padx=25, fill="x")
        self.entry_loc = ctk.CTkEntry(self.right_column, placeholder_text="Lokátor (např. JN89AK)", fg_color=BG_COLOR, text_color=TEXT_COLOR)
        self.entry_loc.pack(pady=10, padx=25, fill="x")
        self.entry_rst = ctk.CTkEntry(self.right_column, placeholder_text="Report RST (např. 59)", fg_color=BG_COLOR, text_color=TEXT_COLOR)
        self.entry_rst.pack(pady=10, padx=25, fill="x")

        ctk.CTkButton(self.right_column, text="ZAPSAT DO DENÍKU ✍️💥", font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="#2ecc71", hover_color="#27ae60", height=45, command=self.log_qso).pack(pady=30, padx=25, fill="x")

        self.update_map_theme()
        self.update_my_qth()

    def build_live_log_manager(self):
        frame = self.frames["📡 Live Log (Správce)"]
        ctk.CTkLabel(frame, text="Správce Deníků CB / PMR 📂", font=ctk.CTkFont(size=24, weight="bold"), text_color=ACCENT_COLOR).pack(pady=20)
        
        add_frame = ctk.CTkFrame(frame, fg_color=PANEL_COLOR, corner_radius=10)
        add_frame.pack(pady=10, padx=50, fill="x")
        self.entry_new_log = ctk.CTkEntry(add_frame, placeholder_text="Vlastní název nového deníku...", width=350, fg_color=BG_COLOR)
        self.entry_new_log.pack(side="left", padx=20, pady=20)
        ctk.CTkButton(add_frame, text="Vytvořit vlastní deník ✨", command=self.create_new_log, fg_color=ACCENT_COLOR).pack(side="left", padx=10, pady=20)

        self.log_list_frame = ctk.CTkScrollableFrame(frame, fg_color=PANEL_COLOR, corner_radius=10)
        self.log_list_frame.pack(pady=20, padx=50, fill="both", expand=True)

    def build_contests(self):
        frame = self.frames["🏆 Contests (Závody)"]
        ctk.CTkLabel(frame, text="Kompletní Kalendář CB & PMR (Na rok dopředu) 🏆🗓️", font=ctk.CTkFont(size=22, weight="bold"), text_color=ACCENT_COLOR).pack(pady=20)
        
        scroll_contests = ctk.CTkScrollableFrame(frame, fg_color=PANEL_COLOR, corner_radius=15)
        scroll_contests.pack(fill="both", expand=True, padx=50, pady=20)
        
        for name, details in self.contest_details.items():
            row = ctk.CTkFrame(scroll_contests, fg_color=BG_COLOR, corner_radius=10)
            row.pack(fill="x", pady=6, padx=15)
            
            ctk.CTkLabel(row, text=name, font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_COLOR).pack(side="left", padx=15, pady=12)
            
            btn_info = ctk.CTkButton(row, text="Pravidla / Info 🔍", fg_color="#f39c12", hover_color="#d68910", width=130,
                                     command=lambda n=name, d=details: self.show_contest_info(n, d))
            btn_info.pack(side="right", padx=10, pady=10)
            
            btn_go = ctk.CTkButton(row, text="Otevřít deník 📖", fg_color=ACCENT_COLOR, width=110,
                                   command=lambda clg=name: self.open_log_in_dashboard(clg))
            btn_go.pack(side="right", padx=5, pady=10)

    def build_settings(self):
        frame = self.frames["⚙️ Settings"]
        ctk.CTkLabel(frame, text="Nastavení aplikace ⚙️", font=ctk.CTkFont(size=24, weight="bold"), text_color=ACCENT_COLOR).pack(pady=40)
        
        # Tlačítko pro vyčištění nakešovaných zmatených dlaždic 🧹
        ctk.CTkButton(frame, text="VYMAZAT MAPOVOU CACHE 🧹💾", fg_color=DANGER_COLOR, hover_color="#CC0033", 
                      font=ctk.CTkFont(weight="bold"), height=40, command=self.clear_map_cache_action).pack(pady=10)
        
        self.theme_switch = ctk.CTkSwitch(frame, text="Tmavý režim rozhraní (Dark Mode) 🌌☀️", button_color=ACCENT_COLOR, 
                                          progress_color=ACCENT_COLOR, text_color=TEXT_COLOR, command=self.toggle_theme)
        self.theme_switch.select() 
        self.theme_switch.pack(pady=30)

    # ================= AKCE A LOGIKA SYSTÉMU =================

    def show_contest_info(self, title, details):
        messagebox.showinfo("Propozice soutěže 🏆", f"{title}\n\n{details}")

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
        self.update_map_theme()

    def update_map_theme(self):
        """ 🔥 OPRAVENO: PLÁTNO MAPY SE TEĎ SLADÍ S THEMEM A NEBLIKÁ 🔥 """
        try:
            if ctk.get_appearance_mode() == "Dark":
                # Nastavení stabilního tmavého serveru bez omezovačů zoomu
                self.map_widget.set_tile_server("https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png")
                # Nastavení pozadí plátna na hlubokou tmavou modročernou, aby chybějící dlaždice neproblikávaly žlutě/bíle!
                self.map_widget.canvas.configure(bg="#15162B", highlightthickness=0)
            else:
                self.map_widget.set_tile_server("https://tile.openstreetmap.org/{z}/{x}/{y}.png")
                self.map_widget.canvas.configure(bg="#FFFFFF", highlightthickness=0)
        except Exception:
            pass

    def clear_map_cache_action(self):
        """ Akce pro úplné vymazání poškozené databáze stažených dlaždic na disku 🧹 """
        cache_dir = os.path.expanduser("~/.tkintermapview_tile_cache")
        try:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
            messagebox.showinfo("Hotovo! 🧹", "Mapová cache byla úspěšně vymazána!\nPři příštím pohybu na mapě se stáhnou zcela čisté, nové dlaždice. 🚀")
            self.update_map_theme()
        except Exception as e:
            messagebox.showerror("Chyba ⚠️", f"Nepodařilo se smazat složku cache, protože ji systém právě používá.\nZkus aplikaci restartovat a spustit mazání znova!\n{e}")

    def update_my_qth(self):
        coords = locator_to_latlon(self.entry_my_locator.get())
        if coords:
            if self.my_marker: self.my_marker.delete()
            self.my_marker = self.map_widget.set_marker(coords[0], coords[1], text="MÁ ZÁKLADNA 🏠", marker_color_circle=ACCENT_COLOR)
            self.map_widget.set_position(coords[0], coords[1])

    def change_active_log(self, selected_log):
        self.current_log_name = selected_log
        self.refresh_dashboard_view()

    def create_new_log(self):
        new_name = self.entry_new_log.get().strip()
        if new_name and new_name not in self.logbooks_data:
            self.logbooks_data[new_name] = []
            self.entry_new_log.delete(0, 'end')
            self.dropdown_active_log.configure(values=list(self.logbooks_data.keys()))
            self.refresh_log_manager_list()

    def delete_log(self, log_name):
        if len(self.logbooks_data) <= 1: return
        del self.logbooks_data[log_name]
        if self.current_log_name == log_name:
            self.current_log_name = list(self.logbooks_data.keys())[0]
            self.dropdown_active_log.set(self.current_log_name)
            self.change_active_log(self.current_log_name)
        self.dropdown_active_log.configure(values=list(self.logbooks_data.keys()))
        self.refresh_log_manager_list()

    def open_log_in_dashboard(self, log_name):
        self.dropdown_active_log.set(log_name)
        self.change_active_log(log_name)
        self.switch_frame("🏠 Dashboard")

    def export_log_file(self, log_name, file_format):
        qso_list = self.logbooks_data[log_name]
        if not qso_list:
            messagebox.showwarning("Prázdný log", "Tento deník neobsahuje žádná spojení pro export! ⚠️")
            return
            
        ext = file_format.strip().lower()
        file_path = filedialog.asksaveasfilename(defaultextension=ext, 
                                                 filetypes=[(f"{ext.upper()} soubory", f"*{ext}")],
                                                 initialfile=f"{log_name.replace(' ', '_')}_export{ext}")
        if file_path:
            with open(file_path, mode='w', encoding='utf-8', newline='') as file:
                if ext == ".c6v":
                    file.write(f"; Deník: {log_name} | Vygenerováno přes CB PMR Logbook\n")
                    file.write("; Čas;VolacíZnak;Lokátor;RST;Vzdálenost\n")
                    for qso in qso_list:
                        file.write(f"{qso['time']};{qso['call']};{qso['loc']};{qso['rst']};{qso['dist']}\n")
                else:
                    file.write(f"=== SOUTĚŽNÍ DENÍK: {log_name} ===\n")
                    file.write("-" * 65 + "\n")
                    file.write(f"{'ČAS':<10}{'VOLACÍ ZNAK':<20}{'LOKÁTOR':<12}{'RST':<8}{'VZDALENOST'}\n")
                    file.write("-" * 65 + "\n")
                    for qso in qso_list:
                        file.write(f"{qso['time']:<10}{qso['call']:<20}{qso['loc']:<12}{qso['rst']:<8}{qso['dist']} km\n")
            
            messagebox.showinfo("Export hotov! 🥳", f"Deník byl bezpečně uložen!\n📍 {file_path}")

    def refresh_log_manager_list(self):
        for widget in self.log_list_frame.winfo_children(): widget.destroy()

        for log_name, qso_list in self.logbooks_data.items():
            row = ctk.CTkFrame(self.log_list_frame, fg_color=BG_COLOR, corner_radius=8)
            row.pack(fill="x", pady=5, padx=10)
            
            ctk.CTkLabel(row, text=f"📂 {log_name}", font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT_COLOR).pack(side="left", padx=15, pady=10)
            ctk.CTkLabel(row, text=f"QSO: {len(qso_list)} 📡", text_color="#888").pack(side="left", padx=15)
            
            ctk.CTkButton(row, text="Smazat 🗑️", width=60, fg_color=DANGER_COLOR, hover_color="#CC0033", command=lambda n=log_name: self.delete_log(n)).pack(side="right", padx=5, pady=10)
            
            btn_exp = ctk.CTkButton(row, text="Export 💾", width=70, fg_color="#2ecc71", hover_color="#27ae60")
            btn_exp.pack(side="right", padx=5, pady=10)
            
            format_dropdown = ctk.CTkOptionMenu(row, values=[".txt", ".c6v"], width=75, fg_color=PANEL_COLOR, button_color=ACCENT_COLOR, text_color=TEXT_COLOR)
            format_dropdown.set(".txt")
            format_dropdown.pack(side="right", padx=5, pady=10)
            
            btn_exp.configure(command=lambda n=log_name, menu=format_dropdown: self.export_log_file(n, menu.get()))
            
            ctk.CTkButton(row, text="Otevřít a Upravit 📖", width=120, fg_color=ACCENT_COLOR, command=lambda n=log_name: self.open_log_in_dashboard(n)).pack(side="right", padx=5, pady=10)

    def refresh_dashboard_view(self):
        for m in self.contact_markers: m.delete()
        for p in self.map_paths: p.delete()
        for row in self.drawn_qso_rows: row.destroy()
        self.contact_markers.clear()
        self.map_paths.clear()
        self.drawn_qso_rows.clear()

        my_coords = locator_to_latlon(self.entry_my_locator.get())
        
        for qso in self.logbooks_data[self.current_log_name]:
            row = ctk.CTkFrame(self.log_scroll, fg_color=BG_COLOR, height=35, corner_radius=6)
            row.pack(fill="x", pady=3)
            self.drawn_qso_rows.append(row)
            
            data = [qso['time'], qso['call'], qso['loc'], qso['rst'], f"{qso['dist']} km"]
            for i, val in enumerate(data):
                ctk.CTkLabel(row, text=val, text_color=TEXT_COLOR, font=ctk.CTkFont(size=12)).place(relx=i*0.2, rely=0.5, anchor="w", x=10)

            if my_coords and qso['coords']:
                m = self.map_widget.set_marker(qso['coords'][0], qso['coords'][1], text=qso['call'], marker_color_circle="#e74c3c")
                p = self.map_widget.set_path([my_coords, qso['coords']], color=ACCENT_COLOR, width=3)
                self.contact_markers.append(m)
                self.map_paths.append(p)

    def log_qso(self):
        my_loc_str = self.entry_my_locator.get()
        his_call = self.entry_call.get().strip()
        his_loc_str = self.entry_loc.get().upper().strip()
        rst = self.entry_rst.get().strip()

        my_coords = locator_to_latlon(my_loc_str)
        his_coords = locator_to_latlon(his_loc_str)

        if not my_coords or not his_call or not his_coords: return

        distance_km = round(geodesic(my_coords, his_coords).km, 1)
        current_time = datetime.datetime.now().strftime("%H:%M:%S") 

        qso_record = {"time": current_time, "call": his_call, "loc": his_loc_str, "rst": rst, "dist": distance_km, "coords": his_coords}
        self.logbooks_data[self.current_log_name].append(qso_record)
        
        self.refresh_dashboard_view()
        self.entry_call.delete(0, 'end')
        self.entry_loc.delete(0, 'end')
        self.entry_rst.delete(0, 'end')

if __name__ == "__main__":
    app = CB_PMR_Logbook()
    app.mainloop()
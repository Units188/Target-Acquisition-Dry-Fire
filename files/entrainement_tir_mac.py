#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application d'entraînement au tir avec interface graphique
Version MAC OPTIMISÉE - Utilise la commande 'say' native
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
import subprocess
import sys

class EntrainementTirGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Entraînement au Tir")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.cibles = {}
        self.nb_essais = 0
        self.mode_jeu = tk.StringVar(value="unique")
        self.mode_identification = tk.StringVar(value="numero")
        self.essai_courant = 0
        self.session_active = False
        self.pause = False
        self.thread_session = None
        
        # ============================================
        # CONFIGURATION - Personnalisez ici !
        # ============================================
        self.delai_entre_cibles = 0.3  # Délai entre annonces (secondes)
        self.nb_cibles_min = 6         # Min de cibles par séquence
        self.nb_cibles_max = 13        # Max de cibles par séquence
        self.voice_rate = 200          # Vitesse de la voix (100-400)
        self.voice_name = "Thomas"     # Voix française Mac
        # ============================================
        
        # Configuration du style
        self.configurer_style()
        
        # Créer l'interface
        self.creer_interface()
        
        # Centrer la fenêtre
        self.centrer_fenetre()
    
    def configurer_style(self):
        """Configure le style de l'application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs
        accent_color = "#3498db"
        bg_color = "#2c3e50"
        
        style.configure('Title.TLabel', 
                       font=('Arial', 24, 'bold'),
                       foreground=accent_color,
                       background='white')
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 14),
                       foreground=bg_color,
                       background='white')
        
        style.configure('Target.TLabel',
                       font=('Arial', 32, 'bold'),
                       foreground=accent_color,
                       background='white',
                       padding=20)
        
        style.configure('Info.TLabel',
                       font=('Arial', 12),
                       foreground='#7f8c8d',
                       background='white')
        
        style.configure('Big.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=10)
    
    def centrer_fenetre(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def creer_interface(self):
        """Crée l'interface principale"""
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.page_accueil()
    
    def nettoyer_frame(self):
        """Nettoie le frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def page_accueil(self):
        """Page d'accueil"""
        self.nettoyer_frame()
        
        titre = ttk.Label(self.main_frame, 
                         text="🎯 Entraînement au Tir",
                         style='Title.TLabel')
        titre.pack(pady=(0, 10))
        
        sous_titre = ttk.Label(self.main_frame,
                              text="Système d'annonces vocales pour entraînement au tir",
                              style='Subtitle.TLabel')
        sous_titre.pack(pady=(0, 40))
        
        btn_start = ttk.Button(self.main_frame,
                              text="🚀 Commencer",
                              command=self.page_configuration_cibles,
                              style='Big.TButton')
        btn_start.pack(pady=10, ipadx=30, ipady=10)
        
        system_info = f"macOS | Python {sys.version.split()[0]} | Voix: {self.voice_name}"
        info_label = ttk.Label(self.main_frame,
                              text=system_info,
                              style='Info.TLabel')
        info_label.pack(side=tk.BOTTOM, pady=10)
    
    def page_configuration_cibles(self):
        """Page de configuration des cibles"""
        self.nettoyer_frame()
        
        titre = ttk.Label(self.main_frame,
                         text="📊 Configuration des Cibles",
                         style='Title.TLabel')
        titre.pack(pady=(0, 30))
        
        frame_nombre = ttk.Frame(self.main_frame)
        frame_nombre.pack(pady=20)
        
        ttk.Label(frame_nombre, 
                 text="Nombre de cibles:",
                 font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        
        self.spin_nb_cibles = ttk.Spinbox(frame_nombre,
                                          from_=1, to=20,
                                          width=10,
                                          font=('Arial', 12))
        self.spin_nb_cibles.set(5)
        self.spin_nb_cibles.pack(side=tk.LEFT, padx=5)
        
        btn_generer = ttk.Button(self.main_frame,
                                text="Générer les champs",
                                command=self.generer_champs_cibles)
        btn_generer.pack(pady=10)
        
        self.frame_cibles_container = ttk.Frame(self.main_frame)
        self.frame_cibles_container.pack(fill=tk.BOTH, expand=True, pady=20)
        
        frame_nav = ttk.Frame(self.main_frame)
        frame_nav.pack(pady=20)
        
        ttk.Button(frame_nav,
                  text="← Retour",
                  command=self.page_accueil).pack(side=tk.LEFT, padx=5)
        
        self.btn_suivant_cibles = ttk.Button(frame_nav,
                                            text="Suivant →",
                                            command=self.valider_cibles,
                                            state=tk.DISABLED)
        self.btn_suivant_cibles.pack(side=tk.LEFT, padx=5)
    
    def generer_champs_cibles(self):
        """Génère les champs de saisie pour les cibles"""
        for widget in self.frame_cibles_container.winfo_children():
            widget.destroy()
        
        try:
            nb_cibles = int(self.spin_nb_cibles.get())
        except ValueError:
            messagebox.showerror("Erreur", "Nombre invalide")
            return
        
        canvas = tk.Canvas(self.frame_cibles_container, height=300)
        scrollbar = ttk.Scrollbar(self.frame_cibles_container, 
                                 orient="vertical",
                                 command=canvas.yview)
        frame_cibles = ttk.Frame(canvas)
        
        frame_cibles.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_cibles, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.entries_cibles = {}
        
        for i in range(1, nb_cibles + 1):
            frame_ligne = ttk.Frame(frame_cibles)
            frame_ligne.pack(fill=tk.X, pady=5, padx=10)
            
            ttk.Label(frame_ligne,
                     text=f"Cible {i}:",
                     width=10,
                     font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
            
            entry = ttk.Entry(frame_ligne, width=40, font=('Arial', 10))
            entry.insert(0, f"Cible {i}")
            entry.pack(side=tk.LEFT, padx=5)
            
            self.entries_cibles[i] = entry
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.btn_suivant_cibles.config(state=tk.NORMAL)
    
    def valider_cibles(self):
        """Valide et enregistre les cibles"""
        self.cibles = {}
        
        for num, entry in self.entries_cibles.items():
            nom = entry.get().strip()
            if not nom:
                nom = f"Cible {num}"
            self.cibles[num] = nom
        
        if not self.cibles:
            messagebox.showerror("Erreur", "Aucune cible configurée")
            return
        
        self.page_configuration_session()
    
    def page_configuration_session(self):
        """Page de configuration de la session"""
        self.nettoyer_frame()
        
        titre = ttk.Label(self.main_frame,
                         text="⚙️ Configuration de la Session",
                         style='Title.TLabel')
        titre.pack(pady=(0, 30))
        
        frame_essais = ttk.LabelFrame(self.main_frame, 
                                     text="Nombre d'essais",
                                     padding=20)
        frame_essais.pack(fill=tk.X, padx=20, pady=10)
        
        self.spin_nb_essais = ttk.Spinbox(frame_essais,
                                         from_=1, to=100,
                                         width=10,
                                         font=('Arial', 12))
        self.spin_nb_essais.set(10)
        self.spin_nb_essais.pack()
        
        frame_mode = ttk.LabelFrame(self.main_frame,
                                   text="Mode de jeu",
                                   padding=20)
        frame_mode.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Radiobutton(frame_mode,
                       text="🎯 Tir unique (une cible par essai)",
                       variable=self.mode_jeu,
                       value="unique").pack(anchor=tk.W, pady=5)
        
        ttk.Radiobutton(frame_mode,
                       text="🎯🎯 Tir multiple (séquence de cibles)",
                       variable=self.mode_jeu,
                       value="multiple").pack(anchor=tk.W, pady=5)
        
        frame_id = ttk.LabelFrame(self.main_frame,
                                 text="Mode d'identification vocale",
                                 padding=20)
        frame_id.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Radiobutton(frame_id,
                       text="Par numéro (ex: '1')",
                       variable=self.mode_identification,
                       value="numero").pack(anchor=tk.W, pady=5)
        
        ttk.Radiobutton(frame_id,
                       text="Par nom (ex: 'Abat jour chevet')",
                       variable=self.mode_identification,
                       value="nom").pack(anchor=tk.W, pady=5)
        
        ttk.Radiobutton(frame_id,
                       text="Numéro et nom (ex: 'Cible 1, Abat jour chevet')",
                       variable=self.mode_identification,
                       value="numero_et_nom").pack(anchor=tk.W, pady=5)
        
        frame_nav = ttk.Frame(self.main_frame)
        frame_nav.pack(pady=20)
        
        ttk.Button(frame_nav,
                  text="← Retour",
                  command=self.page_configuration_cibles).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_nav,
                  text="🚀 Lancer la session",
                  command=self.demarrer_session,
                  style='Big.TButton').pack(side=tk.LEFT, padx=5)
    
    def demarrer_session(self):
        """Démarre la session d'entraînement"""
        try:
            self.nb_essais = int(self.spin_nb_essais.get())
        except ValueError:
            messagebox.showerror("Erreur", "Nombre d'essais invalide")
            return
        
        self.essai_courant = 0
        self.session_active = True
        self.pause = False
        
        self.page_session()
        
        self.thread_session = threading.Thread(target=self.executer_session, daemon=True)
        self.thread_session.start()
    
    def page_session(self):
        """Page de la session en cours"""
        self.nettoyer_frame()
        
        self.label_progression = ttk.Label(self.main_frame,
                                          text="🎯 Session en cours",
                                          style='Title.TLabel')
        self.label_progression.pack(pady=(0, 20))
        
        self.label_cible = ttk.Label(self.main_frame,
                                     text="",
                                     style='Target.TLabel')
        self.label_cible.pack(pady=40, fill=tk.BOTH, expand=True)
        
        frame_controles = ttk.Frame(self.main_frame)
        frame_controles.pack(pady=20)
        
        self.btn_pause = ttk.Button(frame_controles,
                                    text="⏸️ Pause",
                                    command=self.toggle_pause,
                                    style='Big.TButton')
        self.btn_pause.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(frame_controles,
                  text="⏹️ Arrêter",
                  command=self.arreter_session,
                  style='Big.TButton').pack(side=tk.LEFT, padx=10)
        
        self.label_timer = ttk.Label(self.main_frame,
                                    text="",
                                    style='Info.TLabel')
        self.label_timer.pack(pady=10)
    
    def toggle_pause(self):
        """Bascule pause/reprise"""
        self.pause = not self.pause
        if self.pause:
            self.btn_pause.config(text="▶️ Reprendre")
            self.label_timer.config(text="⏸️ EN PAUSE")
        else:
            self.btn_pause.config(text="⏸️ Pause")
    
    def arreter_session(self):
        """Arrête la session"""
        if messagebox.askyesno("Confirmer", "Voulez-vous vraiment arrêter la session ?"):
            self.session_active = False
            self.kill_all_say_processes()
            self.page_accueil()
    
    def executer_session(self):
        """Execute la session (dans un thread)"""
        self.parler("Début de la session")
        time.sleep(0.5)
        
        for i in range(1, self.nb_essais + 1):
            if not self.session_active:
                break
            
            self.essai_courant = i
            
            while self.pause and self.session_active:
                time.sleep(0.1)
            
            if not self.session_active:
                break
            
            self.root.after(0, self.label_progression.config,
                          {'text': f"🎯 Essai {i}/{self.nb_essais}"})
            
            if self.mode_jeu.get() == "unique":
                self.executer_tir_unique()
            else:
                self.executer_tir_multiple()
            
            for sec in range(10, 0, -1):
                if not self.session_active:
                    break
                while self.pause and self.session_active:
                    time.sleep(0.1)
                if not self.session_active:
                    break
                    
                self.root.after(0, self.label_timer.config,
                              {'text': f"⏱️ Prochain essai dans {sec}s..."})
                time.sleep(1)
        
        if self.session_active:
            self.parler("Session terminée")
            self.root.after(0, self.session_terminee)
    
    def executer_tir_unique(self):
        """Exécute un tir unique"""
        num_cible = random.choice(list(self.cibles.keys()))
        annonce = self.generer_annonce(num_cible)
        
        self.root.after(0, self.label_cible.config, {'text': annonce})
        self.parler(annonce)
    
    def executer_tir_multiple(self):
        """Exécute un tir multiple"""
        longueur = random.randint(self.nb_cibles_min, self.nb_cibles_max)
        sequence = [random.choice(list(self.cibles.keys())) for _ in range(longueur)]
        
        affichage = []
        for num_cible in sequence:
            annonce = self.generer_annonce(num_cible)
            affichage.append(annonce)
            
            texte_affichage = " • ".join(affichage)
            self.root.after(0, self.label_cible.config, {'text': texte_affichage})
            
            self.parler(annonce)
            time.sleep(self.delai_entre_cibles)
    
    def generer_annonce(self, num_cible):
        """Génère l'annonce selon le mode"""
        nom_cible = self.cibles[num_cible]
        mode = self.mode_identification.get()
        
        if mode == "numero":
            return f"{num_cible}"
        elif mode == "nom":
            return nom_cible
        else:
            return f"Cible {num_cible}, {nom_cible}"
    
    def parler(self, texte):
        """Synthèse vocale Mac native"""
        self.kill_all_say_processes()
        try:
            subprocess.Popen(
                ['say', '-v', self.voice_name, '-r', str(self.voice_rate), texte],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ).wait()
        except Exception as e:
            print(f"Erreur TTS: {e}")
    
    def kill_all_say_processes(self):
        """Tue les processus say sur Mac"""
        try:
            subprocess.run(['killall', 'say'],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            time.sleep(0.05)
        except:
            pass
    
    def session_terminee(self):
        """Affiche l'écran de fin de session"""
        self.nettoyer_frame()
        
        titre = ttk.Label(self.main_frame,
                         text="✅ Session Terminée !",
                         style='Title.TLabel')
        titre.pack(pady=(50, 30))
        
        message = ttk.Label(self.main_frame,
                           text=f"Vous avez complété {self.nb_essais} essais",
                           style='Subtitle.TLabel')
        message.pack(pady=20)
        
        ttk.Button(self.main_frame,
                  text="🏠 Retour à l'accueil",
                  command=self.page_accueil,
                  style='Big.TButton').pack(pady=20)
    
    def quitter(self):
        """Quitte l'application proprement"""
        if self.session_active:
            if not messagebox.askyesno("Confirmer", 
                                      "Une session est en cours. Voulez-vous vraiment quitter ?"):
                return
        
        self.session_active = False
        self.kill_all_say_processes()
        self.root.quit()


def main():
    root = tk.Tk()
    app = EntrainementTirGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.quitter)
    root.mainloop()


if __name__ == "__main__":
    main()

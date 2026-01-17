#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'entraînement au tir avec annonces vocales
VERSION MAC ULTRA-ROBUSTE - Tue les processus say avant chaque annonce
"""

import random
import time
import sys
import select
import termios
import tty
import subprocess
import os
import signal


class EntrainementTir:
    def __init__(self):
        self.cibles = {}
        self.nb_essais = 0
        self.mode_jeu = ""
        self.mode_identification = ""
        self.timer_actif = False
        self.pause = False
        self.current_process = None
        
        # ============================================
        # CONFIGURATION
        # ============================================
        
        # DÉLAI ENTRE LES ANNONCES (en secondes)
        # Ajustez cette valeur selon votre progression :
        # - Débutant : 0.5 (valeur par défaut)
        # - Intermédiaire : 0.3
        # - Avancé : 0.2
        # - Expert : 0.1 (minimum recommandé)
        self.delai_entre_cibles = 0.3
        
        # SÉQUENCE EN MODE MULTIPLE
        # Nombre minimum de cibles par séquence
        self.nb_cibles_min = 6
        # Nombre maximum de cibles par séquence  
        self.nb_cibles_max = 13
        
        # Configuration voix
        self.voice_rate = 200  # Vitesse de parole
        self.voice_name = "Thomas"  # Voix masculine française
        
        # ============================================
        
        print(f"✅ Voix : {self.voice_name} (vitesse: {self.voice_rate})")
        print(f"⏱️  Délai entre cibles : {self.delai_entre_cibles}s")
        print(f"🎯 Séquence : {self.nb_cibles_min} à {self.nb_cibles_max} cibles par essai")
    
    def kill_all_say_processes(self):
        """Tue tous les processus 'say' en cours"""
        try:
            subprocess.run(['killall', 'say'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
            time.sleep(0.05)  # Minimum pour que le kill soit effectif
        except:
            pass
    
    def parler(self, texte, afficher=True):
        """Énonce le texte à voix haute"""
        if afficher:
            print(f"🎯 {texte}")
        
        # TUER tous les processus say en cours
        self.kill_all_say_processes()
        
        try:
            # Créer un nouveau processus say
            self.current_process = subprocess.Popen(
                ['say', '-v', self.voice_name, '-r', str(self.voice_rate), texte],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # ATTENDRE que le processus se termine (bloquant)
            self.current_process.wait()
            self.current_process = None
            
        except Exception as e:
            print(f"⚠️  Erreur : {e}")
            self.current_process = None
    
    def attendre_espace_avec_timeout(self, timeout=10):
        """Attend la touche espace ou timeout"""
        print(f"\n⏱️  Timer de {timeout}s (ESPACE=pause | ÉCHAP=quitter)")
        
        debut = time.time()
        derniere_seconde = timeout
        
        old_settings = termios.tcgetattr(sys.stdin)
        
        try:
            tty.setcbreak(sys.stdin.fileno())
            
            while True:
                temps_ecoule = time.time() - debut
                temps_restant = timeout - temps_ecoule
                
                if temps_restant <= 0:
                    print("\n✅ Temps écoulé - Passage à la suite")
                    return True
                
                seconde_actuelle = int(temps_restant) + 1
                if seconde_actuelle != derniere_seconde:
                    print(f"⏱️  {seconde_actuelle}s...", end='\r', flush=True)
                    derniere_seconde = seconde_actuelle
                
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    touche = sys.stdin.read(1)
                    
                    # Échap pour quitter
                    if touche == '\x1b':
                        print("\n\n👋 Arrêt du programme...")
                        self.kill_all_say_processes()
                        sys.exit(0)
                    
                    # Espace pour pause
                    if touche == ' ':
                        print("\n⏸️  PAUSE - Appuyez sur ESPACE pour reprendre")
                        
                        while True:
                            if select.select([sys.stdin], [], [], 0.1)[0]:
                                touche = sys.stdin.read(1)
                                
                                # Échap pendant la pause
                                if touche == '\x1b':
                                    print("\n👋 Arrêt du programme...")
                                    self.kill_all_say_processes()
                                    sys.exit(0)
                                
                                # Espace pour reprendre
                                if touche == ' ':
                                    print("▶️  REPRISE - Nouveau timer de 10s")
                                    return self.attendre_espace_avec_timeout(timeout)
        
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
    def configurer_cibles(self):
        """Configure le nombre et les noms des cibles"""
        print("\n" + "="*60)
        print("🎯  CONFIGURATION DES CIBLES")
        print("="*60)
        
        while True:
            try:
                nb_cibles = int(input("\n📊 Nombre de cibles : "))
                if nb_cibles > 0:
                    break
                print("❌ Le nombre doit être supérieur à 0")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide")
        
        print(f"\n📝 Nommez vos {nb_cibles} cibles :")
        for i in range(1, nb_cibles + 1):
            nom = input(f"  Cible {i} : ").strip()
            if not nom:
                nom = f"Cible {i}"
            self.cibles[i] = nom
        
        print("\n✅ Cibles enregistrées :")
        for num, nom in self.cibles.items():
            print(f"   {num} : {nom}")
    
    def configurer_session(self):
        """Configure le nombre d'essais et le mode de jeu"""
        print("\n" + "="*60)
        print("⚙️  CONFIGURATION DE LA SESSION")
        print("="*60)
        
        while True:
            try:
                self.nb_essais = int(input("\n🔢 Nombre d'essais : "))
                if self.nb_essais > 0:
                    break
                print("❌ Le nombre doit être supérieur à 0")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide")
        
        print("\n🎮 Modes de jeu disponibles :")
        print("  1 - Tir unique (une cible par essai)")
        print("  2 - Tir multiple (séquence de cibles par essai)")
        
        while True:
            choix = input("\n➡️  Votre choix (1 ou 2) : ").strip()
            if choix == "1":
                self.mode_jeu = "unique"
                break
            elif choix == "2":
                self.mode_jeu = "multiple"
                break
            print("❌ Veuillez choisir 1 ou 2")
        
        print("\n🗣️  Mode d'identification vocale :")
        print("  1 - Par numéro (ex: '1')")
        print("  2 - Par nom (ex: 'Abat jour chevet')")
        print("  3 - Numéro et nom (ex: 'Cible 1, Abat jour chevet')")
        
        while True:
            choix = input("\n➡️  Votre choix (1, 2 ou 3) : ").strip()
            if choix == "1":
                self.mode_identification = "numero"
                break
            elif choix == "2":
                self.mode_identification = "nom"
                break
            elif choix == "3":
                self.mode_identification = "numero_et_nom"
                break
            print("❌ Veuillez choisir 1, 2 ou 3")
        
        mode_jeu_texte = "TIR UNIQUE" if self.mode_jeu == "unique" else "TIR MULTIPLE"
        mode_id_texte = {"numero": "Numéro", "nom": "Nom", "numero_et_nom": "Numéro et Nom"}[self.mode_identification]
        print(f"\n✅ Mode sélectionné : {mode_jeu_texte}")
        print(f"✅ Identification : {mode_id_texte}")
    
    def generer_annonce(self, num_cible):
        """Génère l'annonce en fonction du mode d'identification"""
        nom_cible = self.cibles[num_cible]
        
        if self.mode_identification == "numero":
            return f"{num_cible}"
        elif self.mode_identification == "nom":
            return f"{nom_cible}"
        else:
            return f"Cible {num_cible}, {nom_cible}"
    
    def tir_unique(self, num_essai):
        """Mode tir unique - une cible aléatoire"""
        num_cible = random.choice(list(self.cibles.keys()))
        nom_cible = self.cibles[num_cible]
        
        print(f"\n{'─'*60}")
        print(f"Essai {num_essai}/{self.nb_essais}")
        print(f"{'─'*60}")
        print(f"🎯 Cible {num_cible} : {nom_cible}")
        
        annonce = self.generer_annonce(num_cible)
        self.parler(annonce)
        
        self.attendre_espace_avec_timeout(10)
    
    def tir_multiple(self, num_essai):
        """Mode tir multiple - séquence de cibles aléatoires"""
        # Longueur aléatoire entre min et max configurables
        longueur_sequence = random.randint(self.nb_cibles_min, self.nb_cibles_max)
        
        # Générer la séquence
        sequence = [random.choice(list(self.cibles.keys())) 
                   for _ in range(longueur_sequence)]
        
        print(f"\n{'='*60}")
        print(f"Essai {num_essai}/{self.nb_essais} - Séquence de {longueur_sequence} cibles")
        print(f"{'='*60}\n")
        
        # Annoncer chaque cible
        for idx, num_cible in enumerate(sequence, 1):
            annonce = self.generer_annonce(num_cible)
            
            # Affichage simple : juste le mot
            print(f"{annonce}", end=' ', flush=True)
            
            # Annoncer
            self.parler(annonce, afficher=False)
            
            # Délai configurable entre les cibles
            if idx < longueur_sequence:
                time.sleep(self.delai_entre_cibles)
        
        print("\n")  # Retour à la ligne après la séquence
        
        self.attendre_espace_avec_timeout(10)
    
    def lancer_session(self):
        """Lance la session d'entraînement"""
        print("\n" + "="*60)
        print("🚀  DÉBUT DE LA SESSION")
        print("="*60)
        print("\n💡 ESPACE=pause | ÉCHAP=quitter")
        
        self.parler("Début de la session", afficher=False)
        
        for i in range(1, self.nb_essais + 1):
            if self.mode_jeu == "unique":
                self.tir_unique(i)
            else:
                self.tir_multiple(i)
        
        print("\n" + "="*60)
        print("🏁  SESSION TERMINÉE")
        print("="*60)
        self.parler("Session terminée", afficher=False)
    
    def demarrer(self):
        """Point d'entrée principal du programme"""
        print("\n")
        print("█"*60)
        print("█" + " "*58 + "█")
        print("█" + "  🎯  VERSION ULTRA-ROBUSTE - MAC NATIVE  🎯  ".center(58) + "█")
        print("█" + " "*58 + "█")
        print("█"*60)
        
        self.configurer_cibles()
        self.configurer_session()
        
        self.lancer_session()
        
        print("\n💪 Bon entraînement !\n")
    
    def __del__(self):
        """Nettoyer à la fin"""
        self.kill_all_say_processes()


if __name__ == "__main__":
    try:
        app = EntrainementTir()
        app.demarrer()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption - Nettoyage...")
        subprocess.run(['killall', 'say'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        print("✅ Terminé")
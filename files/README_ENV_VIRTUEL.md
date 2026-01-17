# 🍎 Build avec Environnement Virtuel

## 🎯 Trois Options Simples

Choisissez l'option qui vous convient :

---

## Option 1 : Conda (RECOMMANDÉ si vous utilisez conda)

### Build Automatique en 1 Commande

```bash
chmod +x build_with_conda.sh
./build_with_conda.sh
```

**C'est tout !** L'app sera dans `dist/EntrainementTir.app`

### Ou Manuellement

```bash
# 1. Créer l'environnement
conda create -n entrainement_tir python=3.11 -y

# 2. Activer
conda activate entrainement_tir

# 3. Installer PyInstaller
pip install pyinstaller

# 4. Builder
pyinstaller --clean build_mac.spec

# 5. Supprimer la quarantaine
xattr -cr dist/EntrainementTir.app

# 6. Lancer l'app
open dist/EntrainementTir.app

# 7. Désactiver quand c'est fini
conda deactivate
```

---

## Option 2 : venv (Python natif)

### Build Automatique en 1 Commande

```bash
chmod +x build_with_venv.sh
./build_with_venv.sh
```

**C'est tout !** L'app sera dans `dist/EntrainementTir.app`

### Ou Manuellement

```bash
# 1. Créer l'environnement
python3 -m venv venv

# 2. Activer
source venv/bin/activate

# 3. Installer PyInstaller
pip install pyinstaller

# 4. Builder
pyinstaller --clean build_mac.spec

# 5. Supprimer la quarantaine
xattr -cr dist/EntrainementTir.app

# 6. Lancer l'app
open dist/EntrainementTir.app

# 7. Désactiver quand c'est fini
deactivate
```

---

## Option 3 : Sans environnement virtuel

Si vous préférez installer directement :

```bash
chmod +x build_mac.sh
./build_mac.sh
```

---

## 📦 Fichiers Nécessaires

Quel que soit votre choix, vous avez besoin de :

1. **`entrainement_tir_mac.py`** - Le programme
2. **`build_mac.spec`** - Config PyInstaller
3. **Un script de build** :
   - `build_with_conda.sh` (pour conda)
   - `build_with_venv.sh` (pour venv)
   - `build_mac.sh` (sans env virtuel)

---

## ✅ Avantages de l'Environnement Virtuel

- ✅ **Isolation** : N'affecte pas votre installation Python
- ✅ **Propre** : Peut être supprimé après le build
- ✅ **Reproductible** : Même résultat à chaque fois

---

## 🧹 Nettoyer Après le Build

L'app finale (`EntrainementTir.app`) est **autonome** et ne dépend pas de l'environnement virtuel !

### Supprimer l'environnement conda

```bash
conda deactivate
conda remove -n entrainement_tir --all -y
```

### Supprimer l'environnement venv

```bash
deactivate
rm -rf venv
```

---

## 🧪 Tester Avant de Builder

Pour tester le script dans l'environnement virtuel :

### Avec conda

```bash
conda activate entrainement_tir
python entrainement_tir_mac.py
```

### Avec venv

```bash
source venv/bin/activate
python entrainement_tir_mac.py
```

Si ça marche → Le build marchera aussi !

---

## 🔧 Dépannage

### "conda: command not found"

Utilisez `build_with_venv.sh` à la place.

### "python3: command not found"

Installez Python depuis https://www.python.org/downloads/

### tkinter manquant

```bash
# Avec Homebrew
brew install python-tk@3.11

# Rebuild après installation
```

### Build échoue

1. **Testez d'abord le script** :
   ```bash
   conda activate entrainement_tir  # ou source venv/bin/activate
   python entrainement_tir_mac.py
   ```

2. **Si ça marche**, le problème vient de PyInstaller :
   ```bash
   pip install --upgrade pyinstaller
   pyinstaller --clean build_mac.spec
   ```

---

## 💡 Quelle Option Choisir ?

**Vous utilisez déjà conda** (miniconda/anaconda) ?
→ **Option 1** : `build_with_conda.sh`

**Python natif sans conda** ?
→ **Option 2** : `build_with_venv.sh`

**Vous vous en fichez** ?
→ **Option 3** : `build_mac.sh`

---

## 📋 Récapitulatif Ultra-Rapide

### Conda

```bash
chmod +x build_with_conda.sh && ./build_with_conda.sh
```

### venv

```bash
chmod +x build_with_venv.sh && ./build_with_venv.sh
```

### Sans env

```bash
chmod +x build_mac.sh && ./build_mac.sh
```

**Puis :**

```bash
open dist/EntrainementTir.app
```

---

**Bon build ! 🚀**

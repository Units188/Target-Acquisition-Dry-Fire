# Target Acquisition Dry Fire

Voice-guided dry-fire training tool for practicing multiple target transitions. Announces randomized target sequences with customizable target names.

## Features

- 🎯 Customizable target names
- 🔊 Text-to-speech announcements (macOS native)
- 🎮 Two modes: Single shot or multiple target sequences
- ⚙️ Configurable timing between targets
- ⏸️ Pause/resume during training
- 🎤 Three identification modes: number only, name only, or both

## Requirements

- macOS (uses native `say` command)
- Python 3.7+
- No external dependencies

## Installation
```bash
git clone https://github.com/YOUR_USERNAME/Target-Acquisition-Dry-Fire.git
cd Target-Acquisition-Dry-Fire
python3 entrainement_tir.py
```

## Usage

1. Run the script
2. Configure your targets (number and names)
3. Choose number of attempts and game mode
4. Select identification mode
5. Follow the vocal instructions

### Configuration

You can adjust these parameters in the code:

- `delai_entre_cibles`: Delay between announcements (0.1 to 0.5s)
- `nb_cibles_min/max`: Sequence length range
- `voice_name`: Text-to-speech voice (default: "Thomas" for French)
- `voice_rate`: Speech rate

### Controls

- **SPACE**: Pause/Resume
- **ESC**: Quit

## Example
```
🎯 CONFIGURATION DES CIBLES
📊 Nombre de cibles : 5

📝 Nommez vos 5 cibles :
  Cible 1 : Target Alpha
  Cible 2 : Target Bravo
  Cible 3 : Target Charlie
  Cible 4 : Target Delta
  Cible 5 : Target Echo
```

## Changing Voice Language

To use a different language, modify the `voice_name` parameter in the code:
- English: `"Alex"`, `"Samantha"`, `"Daniel"`
- Spanish: `"Jorge"`, `"Monica"`
- German: `"Anna"`, `"Stefan"`
- And many more...

Run `say -v ?` in terminal to see all available voices.

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License**.

You are free to:
- ✅ Share and use for personal/educational purposes
- ✅ Modify and adapt the code
- ✅ Distribute your modifications

Under these conditions:
- 📝 Give appropriate credit
- 🚫 No commercial use
- 🔄 Share modifications under the same license

See the [LICENSE](LICENSE) file for full details.

**For commercial licensing inquiries, please open an issue.**

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

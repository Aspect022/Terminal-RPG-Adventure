# 🎮 Python Text RPG Adventure

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-playable-success.svg)
![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)

A rich text-based RPG adventure game built in Python featuring dynamic combat, character progression, and an engaging quest system.

## ✨ Features

### Character System
- **Three Unique Classes**
  - 🗡️ **Warrior**: High health & strength (Perfect for beginners)
  - 🔮 **Mage**: Powerful magic abilities
  - 🏹 **Rogue**: Superior agility & balanced stats

- **Progression System**
  - Experience-based leveling
  - Stat improvements with each level
  - Equipment-based stat boosts

### Combat System
- **Dynamic Turn-Based Combat**
  - Strategic action choices
  - Multiple enemy types
  - Scaled difficulty based on player level

- **Combat Actions**
  - Basic attacks
  - Magic abilities
  - Item usage
  - Tactical retreat option

### Quest System
- **Multiple Quest Types**
  - Combat challenges
  - Collection objectives
  - Equipment goals
  - Story-driven missions

### Item System
- **Equipment**
  - Weapons with damage modifiers
  - Armor with defense bonuses
  - Accessories with special effects

- **Consumables**
  - Health potions
  - Status effect items
  - Quest items

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- No additional dependencies required

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/rpg-adventure.git
cd rpg-adventure
```

2. Run the game
```bash
# Option 1: Using Python directly
python game.py

# Option 2: Using the batch file (Windows)
start_game.bat
```

## 🎮 How to Play

### Starting Out
1. Create your character
   - Choose a name
   - Select a class (Warrior, Mage, or Rogue)
   - Each class has unique starting stats

### Main Menu Options
```
1. View Character  - Check stats and manage inventory
2. Explore        - Find enemies and loot
3. Quests         - Accept and track missions
4. Save Game      - Save your progress
5. Load Game      - Resume a saved game
6. Exit           - Quit the game
```

### Quick Tips
- 💪 Start with beginner quests to gain experience
- 🎒 Always check found equipment - it might be better than what you have
- ❤️ Keep healing items ready for tough battles
- 💰 Save gold for better equipment
- 💾 Save often to preserve progress

## 🎯 Game Features

### Enemy Types
| Enemy    | Difficulty | Best for           |
|----------|------------|-------------------|
| Goblin   | Easy       | New players       |
| Orc      | Medium     | Level 3+          |
| Troll    | Hard       | Level 5+          |
| Dragon   | Very Hard  | Level 8+          |

### Character Classes
| Class   | Health | Strength | Magic | Defense | Agility |
|---------|--------|----------|-------|---------|---------|
| Warrior | 120    | 15       | 5     | 12      | 8       |
| Mage    | 80     | 6        | 18    | 6       | 12      |
| Rogue   | 100    | 12       | 8     | 8       | 16      |

## 📁 Project Structure
```
rpg_adventure/
├── character.py    # Character class and stats system
├── combat.py       # Combat mechanics and enemy AI
├── quests.py       # Quest management system
├── game.py         # Main game loop and UI
├── README.md       # Documentation
└── start_game.bat  # Windows launcher
```

## 🛠️ Technical Details

### Save System
- JSON-based save files
- Multiple save slots supported
- Automatic save naming with character info
- Save files stored in `saves/` directory

### Combat System
- Turn-based mechanics
- Damage calculation based on stats and equipment
- Random elements for variety
- Scaled enemy difficulty

### Quest System
- Progressive difficulty
- Multiple quest types
- Dynamic reward scaling
- Quest state persistence

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

- Inspired by classic text RPGs
- Built with pure Python
- Developed for learning and entertainment

## 🐛 Known Issues

- None reported yet! Feel free to open an issue if you find any.

---
Made with ❤️ by [Jayesh RL]

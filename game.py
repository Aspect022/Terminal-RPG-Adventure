from character import Character
from combat import CombatSystem
from quests import QuestManager

import os
import sys
import random

class RPGGame:
    def __init__(self):
        self.player = None
        self.quest_manager = QuestManager()
        
    def start(self):
        print("Welcome to the Text-Based RPG Adventure!")
        self.create_character()
        self.main_menu()
        
    def create_character(self):
        print("\nCreate Your Character")
        name = input("Enter character name: ")
        print("Choose your class: Warrior, Mage, Rogue")
        character_class = input("Character class: ")
        
        self.player = Character(name, character_class)
        print(f"\nWelcome, {self.player.name} the {self.player.character_class}!")
        
    def main_menu(self):
        while True:
            print("\nMain Menu")
            print("1. View Character")
            print("2. Explore")
            print("3. Quests")
            print("4. Save Game")
            print("5. Load Game")
            print("6. Exit")
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self.view_character()
            elif choice == "2":
                self.explore_world()
            elif choice == "3":
                self.manage_quests()
            elif choice == "4":
                self.save_game()
            elif choice == "5":
                self.load_game()
            elif choice == "6":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Try again.")
                
    def view_character(self):
        self.player.display_stats()
        self.player.display_inventory()
        
        # Equipment management
        print("\n⚙️ Equipment Management:")
        print("1. Equip Weapon")
        print("2. Equip Armor")
        print("3. Use Item")
        print("4. Return to Main Menu")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            self.equip_weapon()
        elif choice == "2":
            self.equip_armor()
        elif choice == "3":
            self.use_item()
    
    def equip_weapon(self):
        weapons = [item for item in self.player.inventory if item.get('type') == 'weapon']
        if not weapons:
            print("❌ No weapons in inventory!")
            return
            
        print("\nAvailable Weapons:")
        for i, weapon in enumerate(weapons, 1):
            print(f"{i}. {weapon['name']} (+{weapon['damage']} damage) - {weapon['description']}")
            
        try:
            choice = int(input("Choose weapon to equip (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(weapons):
                weapon = weapons[choice - 1]
                self.player.inventory.remove(weapon)
                self.player.equip_weapon(weapon)
                print(f"⚔️ Equipped {weapon['name']}!")
                
                # Update quest progress
                self.quest_manager.update_quest_progress(self.player, "weapon_equipped")
        except ValueError:
            print("❌ Invalid choice!")
    
    def equip_armor(self):
        armors = [item for item in self.player.inventory if item.get('type') == 'armor']
        if not armors:
            print("❌ No armor in inventory!")
            return
            
        print("\nAvailable Armor:")
        for i, armor in enumerate(armors, 1):
            print(f"{i}. {armor['name']} (+{armor['defense']} defense) - {armor['description']}")
            
        try:
            choice = int(input("Choose armor to equip (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(armors):
                armor = armors[choice - 1]
                self.player.inventory.remove(armor)
                self.player.equip_armor(armor)
                print(f"🛡️ Equipped {armor['name']}!")
        except ValueError:
            print("❌ Invalid choice!")
    
    def use_item(self):
        consumables = [item for item in self.player.inventory if item.get('type') == 'consumable']
        if not consumables:
            print("❌ No consumable items!")
            return
            
        print("\nConsumable Items:")
        for i, item in enumerate(consumables, 1):
            print(f"{i}. {item['name']} - {item['description']}")
            
        try:
            choice = int(input("Choose item to use (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(consumables):
                item = consumables[choice - 1]
                if 'heal' in item:
                    healed = self.player.heal(item['heal'])
                    print(f"💚 Used {item['name']} and recovered {healed} HP!")
                    self.player.inventory.remove(item)
        except ValueError:
            print("❌ Invalid choice!")
        
    def explore_world(self):
        print("\n🌍 You venture into the wilderness...")
        
        # Random encounter chance
        if random.random() < 0.8:  # 80% chance for combat
            # Choose enemy based on player level
            if self.player.level <= 2:
                enemy_type = random.choice(['goblin', 'goblin', 'orc'])  # More goblins for beginners
            elif self.player.level <= 5:
                enemy_type = random.choice(['goblin', 'orc', 'orc', 'troll'])
            else:
                enemy_type = random.choice(['orc', 'troll', 'dragon'])
                
            enemy = CombatSystem.create_enemy(enemy_type, self.player.level)
            
            if CombatSystem.combat_encounter(self.player, enemy):
                # Update quest progress for kills
                self.quest_manager.update_quest_progress(self.player, "kill", enemy_type)
                
                # Check if player died
                if not self.player.is_alive():
                    print("\n💀 GAME OVER 💀")
                    print("Your adventure ends here...")
                    self.main_menu()
                    return
        else:
            # No combat encounter
            print("🌿 You explore peacefully and find some gold!")
            gold_found = random.randint(10, 30)
            self.player.gold += gold_found
            print(f"💰 Found {gold_found} gold!")
            
            # Update quest progress for gold
            self.quest_manager.update_quest_progress(self.player, "gold_gained", None, gold_found)
            
        input("\nPress Enter to continue...")
        
    def manage_quests(self):
        while True:
            print("\nQuest Management")
            print("1. View Available Quests")
            print("2. View Active Quests")
            print("3. View Completed Quests")
            print("4. Return to Main Menu")
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self.quest_manager.display_available_quests(self.player.level)
                quest_choice = input("Choose a quest to start or press Enter to cancel: ").strip()
                if quest_choice.isdigit():
                    index = int(quest_choice) - 1
                    if not self.quest_manager.assign_quest(self.player, index):
                        print("Invalid choice or quest already accepted.")
            elif choice == "2":
                self.quest_manager.display_active_quests(self.player)
            elif choice == "3":
                self.quest_manager.display_completed_quests(self.player)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Try again.")
        
    def save_game(self):
        if not os.path.exists('saves'):
            os.makedirs('saves')
        
        save_filename = f'saves/{self.player.name}_lvl{self.player.level}.sav'
        self.player.save_to_file(save_filename)
        print(f"Game saved as {save_filename}")
    
    def load_game(self):
        if not os.path.exists('saves'):
            print("No saved games found.")
            return
            
        files = [f for f in os.listdir('saves') if f.endswith('.sav')]
        if not files:
            print("No saved games found.")
            return
        
        print("Available Saves:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        
        choice = input("Enter save number to load or press Enter to cancel: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(files):
                filename = f'saves/{files[index]}'
                self.player = Character.load_from_file(filename)
                print(f"Loaded {filename}")
            else:
                print("Invalid choice.")
        else:
            print("Cancelled loading.")

if __name__ == '__main__':
    game = RPGGame()
    try:
        game.start()
    except KeyboardInterrupt:
        print("\nGame exited.")
        sys.exit(0)

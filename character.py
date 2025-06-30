import json
import random

class Character:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # Base stats based on class
        if character_class.lower() == "warrior":
            self.max_health = 120
            self.strength = 15
            self.magic = 5
            self.defense = 12
            self.agility = 8
        elif character_class.lower() == "mage":
            self.max_health = 80
            self.strength = 6
            self.magic = 18
            self.defense = 6
            self.agility = 12
        elif character_class.lower() == "rogue":
            self.max_health = 100
            self.strength = 12
            self.magic = 8
            self.defense = 8
            self.agility = 16
        else:  # Default balanced class
            self.max_health = 100
            self.strength = 10
            self.magic = 10
            self.defense = 10
            self.agility = 10
            
        self.current_health = self.max_health
        self.gold = 50
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.quests = []
        self.completed_quests = []
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.current_health = max(0, self.current_health - actual_damage)
        return actual_damage
        
    def heal(self, amount):
        old_health = self.current_health
        self.current_health = min(self.max_health, self.current_health + amount)
        return self.current_health - old_health
        
    def is_alive(self):
        return self.current_health > 0
        
    def add_experience(self, exp):
        self.experience += exp
        if self.experience >= self.experience_to_next_level:
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.experience = 0
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        
        # Stat increases
        self.max_health += 20
        self.current_health = self.max_health
        self.strength += 2
        self.magic += 2
        self.defense += 1
        self.agility += 1
        
        print(f"\n🎉 {self.name} leveled up to level {self.level}!")
        print(f"Health increased to {self.max_health}")
        print(f"All stats improved!")
        
    def add_item(self, item):
        self.inventory.append(item)
        
    def remove_item(self, item_name):
        for item in self.inventory:
            if item['name'].lower() == item_name.lower():
                self.inventory.remove(item)
                return item
        return None
        
    def equip_weapon(self, weapon):
        if self.equipped_weapon:
            self.inventory.append(self.equipped_weapon)
        self.equipped_weapon = weapon
        
    def equip_armor(self, armor):
        if self.equipped_armor:
            self.inventory.append(self.equipped_armor)
        self.equipped_armor = armor
        
    def get_attack_power(self):
        base_attack = self.strength
        if self.equipped_weapon:
            base_attack += self.equipped_weapon.get('damage', 0)
        return base_attack
        
    def get_defense_power(self):
        base_defense = self.defense
        if self.equipped_armor:
            base_defense += self.equipped_armor.get('defense', 0)
        return base_defense
        
    def display_stats(self):
        print(f"\n📊 {self.name} the {self.character_class}")
        print(f"Level: {self.level}")
        print(f"Health: {self.current_health}/{self.max_health}")
        print(f"Experience: {self.experience}/{self.experience_to_next_level}")
        print(f"Strength: {self.strength}")
        print(f"Magic: {self.magic}")
        print(f"Defense: {self.get_defense_power()}")
        print(f"Agility: {self.agility}")
        print(f"Gold: {self.gold}")
        
        if self.equipped_weapon:
            print(f"Weapon: {self.equipped_weapon['name']} (+{self.equipped_weapon['damage']} damage)")
        if self.equipped_armor:
            print(f"Armor: {self.equipped_armor['name']} (+{self.equipped_armor['defense']} defense)")
            
    def display_inventory(self):
        print(f"\n🎒 {self.name}'s Inventory:")
        if not self.inventory:
            print("Empty")
            return
            
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item['name']} - {item['description']}")
            
    def save_to_file(self, filename):
        data = {
            'name': self.name,
            'character_class': self.character_class,
            'level': self.level,
            'experience': self.experience,
            'experience_to_next_level': self.experience_to_next_level,
            'max_health': self.max_health,
            'current_health': self.current_health,
            'strength': self.strength,
            'magic': self.magic,
            'defense': self.defense,
            'agility': self.agility,
            'gold': self.gold,
            'inventory': self.inventory,
            'equipped_weapon': self.equipped_weapon,
            'equipped_armor': self.equipped_armor,
            'quests': self.quests,
            'completed_quests': self.completed_quests
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            
        character = cls(data['name'], data['character_class'])
        character.level = data['level']
        character.experience = data['experience']
        character.experience_to_next_level = data['experience_to_next_level']
        character.max_health = data['max_health']
        character.current_health = data['current_health']
        character.strength = data['strength']
        character.magic = data['magic']
        character.defense = data['defense']
        character.agility = data['agility']
        character.gold = data['gold']
        character.inventory = data['inventory']
        character.equipped_weapon = data['equipped_weapon']
        character.equipped_armor = data['equipped_armor']
        character.quests = data['quests']
        character.completed_quests = data['completed_quests']
        
        return character

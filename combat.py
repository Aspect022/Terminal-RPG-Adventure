import random
import time

class Enemy:
    def __init__(self, name, health, attack, defense, exp_reward, gold_reward, loot=None):
        self.name = name
        self.max_health = health
        self.current_health = health
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.loot = loot or []
        
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.current_health = max(0, self.current_health - actual_damage)
        return actual_damage
        
    def is_alive(self):
        return self.current_health > 0
        
    def attack_player(self, player):
        damage = random.randint(self.attack - 2, self.attack + 2)
        actual_damage = player.take_damage(damage)
        return actual_damage

class CombatSystem:
    @staticmethod
    def create_enemy(enemy_type, player_level):
        """Create enemies scaled to player level"""
        base_enemies = {
            'goblin': {
                'name': 'Goblin',
                'health': 30,
                'attack': 8,
                'defense': 2,
                'exp': 25,
                'gold': 15,
                'loot': [
                    {'name': 'Rusty Dagger', 'type': 'weapon', 'damage': 3, 'description': 'A worn dagger'},
                    {'name': 'Health Potion', 'type': 'consumable', 'heal': 30, 'description': 'Restores 30 HP'}
                ]
            },
            'orc': {
                'name': 'Orc Warrior',
                'health': 60,
                'attack': 12,
                'defense': 4,
                'exp': 50,
                'gold': 30,
                'loot': [
                    {'name': 'Iron Sword', 'type': 'weapon', 'damage': 8, 'description': 'A sturdy iron blade'},
                    {'name': 'Leather Armor', 'type': 'armor', 'defense': 5, 'description': 'Basic leather protection'}
                ]
            },
            'troll': {
                'name': 'Cave Troll',
                'health': 100,
                'attack': 15,
                'defense': 8,
                'exp': 100,
                'gold': 60,
                'loot': [
                    {'name': 'Troll Club', 'type': 'weapon', 'damage': 12, 'description': 'A massive wooden club'},
                    {'name': 'Greater Health Potion', 'type': 'consumable', 'heal': 60, 'description': 'Restores 60 HP'}
                ]
            },
            'dragon': {
                'name': 'Young Dragon',
                'health': 200,
                'attack': 25,
                'defense': 15,
                'exp': 300,
                'gold': 150,
                'loot': [
                    {'name': 'Dragon Scale Armor', 'type': 'armor', 'defense': 15, 'description': 'Armor made from dragon scales'},
                    {'name': 'Flame Sword', 'type': 'weapon', 'damage': 20, 'description': 'A sword imbued with dragon fire'}
                ]
            }
        }
        
        enemy_data = base_enemies.get(enemy_type, base_enemies['goblin'])
        
        # Scale enemy to player level
        level_multiplier = 1 + (player_level - 1) * 0.3
        
        enemy = Enemy(
            name=enemy_data['name'],
            health=int(enemy_data['health'] * level_multiplier),
            attack=int(enemy_data['attack'] * level_multiplier),
            defense=int(enemy_data['defense'] * level_multiplier),
            exp_reward=int(enemy_data['exp'] * level_multiplier),
            gold_reward=int(enemy_data['gold'] * level_multiplier),
            loot=enemy_data['loot'].copy()
        )
        
        return enemy
    
    @staticmethod
    def combat_encounter(player, enemy):
        print(f"\n⚔️ A wild {enemy.name} appears!")
        print(f"{enemy.name}: {enemy.current_health}/{enemy.max_health} HP")
        
        while player.is_alive() and enemy.is_alive():
            print(f"\n💖 Your Health: {player.current_health}/{player.max_health}")
            print(f"👹 {enemy.name} Health: {enemy.current_health}/{enemy.max_health}")
            
            action = CombatSystem.get_combat_action(player)
            
            if action == "attack":
                CombatSystem.player_attack(player, enemy)
            elif action == "magic":
                CombatSystem.player_magic_attack(player, enemy)
            elif action == "item":
                if not CombatSystem.use_item_in_combat(player):
                    continue  # Don't waste turn if no item used
            elif action == "flee":
                if CombatSystem.attempt_flee(player, enemy):
                    print("You successfully fled from battle!")
                    return False
                else:
                    print("You couldn't escape!")
            
            # Enemy's turn
            if enemy.is_alive():
                damage = enemy.attack_player(player)
                print(f"💥 {enemy.name} attacks you for {damage} damage!")
                
                if not player.is_alive():
                    print("💀 You have been defeated!")
                    return False
                    
            time.sleep(1)  # Pause for dramatic effect
        
        # Player won
        if player.is_alive():
            print(f"\n🎉 You defeated the {enemy.name}!")
            player.add_experience(enemy.exp_reward)
            player.gold += enemy.gold_reward
            print(f"💰 Gained {enemy.gold_reward} gold and {enemy.exp_reward} experience!")
            
            # Loot drop
            if enemy.loot and random.random() < 0.3:  # 30% chance for loot
                loot_item = random.choice(enemy.loot)
                player.add_item(loot_item)
                print(f"🎁 You found: {loot_item['name']}!")
            
            return True
        
        return False
    
    @staticmethod
    def get_combat_action(player):
        while True:
            print("\nWhat do you want to do?")
            print("1. Attack")
            print("2. Magic Attack")
            print("3. Use Item")
            print("4. Flee")
            
            choice = input("Choose your action (1-4): ").strip()
            
            if choice == "1":
                return "attack"
            elif choice == "2":
                return "magic"
            elif choice == "3":
                return "item"
            elif choice == "4":
                return "flee"
            else:
                print("Invalid choice. Please try again.")
    
    @staticmethod
    def player_attack(player, enemy):
        attack_power = player.get_attack_power()
        damage = random.randint(attack_power - 2, attack_power + 2)
        actual_damage = enemy.take_damage(damage)
        print(f"⚡ You attack for {actual_damage} damage!")
        
        if not enemy.is_alive():
            print(f"💀 {enemy.name} has been defeated!")
    
    @staticmethod
    def player_magic_attack(player, enemy):
        if player.magic < 5:
            print("❌ You don't have enough magic power!")
            return
            
        magic_damage = random.randint(player.magic, player.magic + 5)
        actual_damage = enemy.take_damage(magic_damage)
        print(f"✨ Your magic attack deals {actual_damage} damage!")
        
        if not enemy.is_alive():
            print(f"💀 {enemy.name} has been defeated!")
    
    @staticmethod
    def use_item_in_combat(player):
        consumables = [item for item in player.inventory if item.get('type') == 'consumable']
        
        if not consumables:
            print("❌ You have no consumable items!")
            return False
            
        print("\nConsumable Items:")
        for i, item in enumerate(consumables, 1):
            print(f"{i}. {item['name']} - {item['description']}")
        
        try:
            choice = int(input("Choose item to use (0 to cancel): "))
            if choice == 0:
                return False
            if 1 <= choice <= len(consumables):
                item = consumables[choice - 1]
                if 'heal' in item:
                    healed = player.heal(item['heal'])
                    print(f"💚 You used {item['name']} and recovered {healed} HP!")
                    player.inventory.remove(item)
                    return True
        except ValueError:
            pass
            
        print("❌ Invalid choice!")
        return False
    
    @staticmethod
    def attempt_flee(player, enemy):
        flee_chance = player.agility / (player.agility + enemy.attack)
        return random.random() < flee_chance

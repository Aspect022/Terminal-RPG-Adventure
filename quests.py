import random

class Quest:
    def __init__(self, name, description, quest_type, target=None, target_amount=1, reward_exp=0, reward_gold=0, reward_items=None):
        self.name = name
        self.description = description
        self.quest_type = quest_type  # 'kill', 'collect', 'explore', 'story'
        self.target = target
        self.target_amount = target_amount
        self.current_progress = 0
        self.reward_exp = reward_exp
        self.reward_gold = reward_gold
        self.reward_items = reward_items or []
        self.completed = False
        
    def update_progress(self, progress_type, amount=1):
        """Update quest progress based on player actions"""
        if self.completed:
            return False
            
        if self.quest_type == progress_type:
            self.current_progress += amount
            
        if self.current_progress >= self.target_amount:
            self.completed = True
            return True
        return False
        
    def display_progress(self):
        status = "✅ Complete" if self.completed else f"📋 Progress: {self.current_progress}/{self.target_amount}"
        print(f"{self.name}: {status}")
        print(f"   {self.description}")
        
    def get_reward_text(self):
        rewards = []
        if self.reward_exp > 0:
            rewards.append(f"{self.reward_exp} EXP")
        if self.reward_gold > 0:
            rewards.append(f"{self.reward_gold} Gold")
        if self.reward_items:
            for item in self.reward_items:
                rewards.append(item['name'])
        return ", ".join(rewards) if rewards else "None"

class QuestManager:
    def __init__(self):
        self.available_quests = []
        self.story_progress = 0
        self.init_quests()
        
    def init_quests(self):
        """Initialize all available quests"""
        
        # Starter quests
        starter_quests = [
            Quest(
                name="First Blood",
                description="Defeat 3 Goblins to prove your combat skills",
                quest_type="kill_goblin",
                target="goblin",
                target_amount=3,
                reward_exp=75,
                reward_gold=50,
                reward_items=[{'name': 'Health Potion', 'type': 'consumable', 'heal': 30, 'description': 'Restores 30 HP'}]
            ),
            Quest(
                name="Treasure Hunter",
                description="Collect 100 gold pieces",
                quest_type="collect_gold",
                target="gold",
                target_amount=100,
                reward_exp=50,
                reward_gold=25,
                reward_items=[{'name': 'Lucky Charm', 'type': 'accessory', 'description': 'Increases gold find chance'}]
            ),
            Quest(
                name="Equipment Upgrade",
                description="Find and equip a weapon",
                quest_type="equip_weapon",
                target="weapon",
                target_amount=1,
                reward_exp=40,
                reward_gold=30
            )
        ]
        
        # Intermediate quests
        intermediate_quests = [
            Quest(
                name="Orc Slayer",
                description="Eliminate 5 Orc Warriors threatening the village",
                quest_type="kill_orc",
                target="orc",
                target_amount=5,
                reward_exp=200,
                reward_gold=150,
                reward_items=[{'name': 'Silver Sword', 'type': 'weapon', 'damage': 15, 'description': 'A well-crafted silver blade'}]
            ),
            Quest(
                name="Cave Explorer",
                description="Defeat the Cave Troll in its lair",
                quest_type="kill_troll",
                target="troll",
                target_amount=1,
                reward_exp=300,
                reward_gold=200,
                reward_items=[{'name': 'Troll Hide Armor', 'type': 'armor', 'defense': 10, 'description': 'Tough armor made from troll hide'}]
            ),
            Quest(
                name="Merchant's Request",
                description="Collect rare items and sell them for 500 gold total",
                quest_type="collect_gold",
                target="gold",
                target_amount=500,
                reward_exp=150,
                reward_gold=100,
                reward_items=[{'name': 'Merchant Ring', 'type': 'accessory', 'description': 'Improves trading deals'}]
            )
        ]
        
        # Advanced quests
        advanced_quests = [
            Quest(
                name="Dragon Slayer",
                description="Face the Young Dragon and emerge victorious",
                quest_type="kill_dragon",
                target="dragon",
                target_amount=1,
                reward_exp=1000,
                reward_gold=500,
                reward_items=[
                    {'name': 'Dragon Slayer Title', 'type': 'achievement', 'description': 'Proof of your dragon-slaying prowess'},
                    {'name': 'Master Health Potion', 'type': 'consumable', 'heal': 100, 'description': 'Restores 100 HP'}
                ]
            ),
            Quest(
                name="Hero's Journey",
                description="Reach level 10 to become a true hero",
                quest_type="reach_level",
                target="level",
                target_amount=10,
                reward_exp=500,
                reward_gold=300,
                reward_items=[{'name': 'Hero\'s Cape', 'type': 'accessory', 'description': 'Symbol of your heroic status'}]
            )
        ]
        
        # Story quests
        story_quests = [
            Quest(
                name="The Mysterious Village",
                description="Investigate reports of strange happenings in the nearby village",
                quest_type="story",
                target="village_mystery",
                target_amount=1,
                reward_exp=100,
                reward_gold=75,
                reward_items=[{'name': 'Village Map', 'type': 'key_item', 'description': 'Shows hidden paths around the village'}]
            ),
            Quest(
                name="The Ancient Prophecy",
                description="Discover the truth behind the ancient prophecy",
                quest_type="story",
                target="prophecy",
                target_amount=1,
                reward_exp=200,
                reward_gold=150,
                reward_items=[{'name': 'Prophecy Scroll', 'type': 'key_item', 'description': 'Contains ancient wisdom'}]
            )
        ]
        
        self.all_quests = {
            'starter': starter_quests,
            'intermediate': intermediate_quests,
            'advanced': advanced_quests,
            'story': story_quests
        }
        
        # Start with starter quests
        self.available_quests = starter_quests.copy()
    
    def get_available_quests(self, player_level):
        """Get quests appropriate for player level"""
        available = []
        
        # Always show starter quests for low level players
        if player_level <= 3:
            available.extend([q for q in self.all_quests['starter'] if not q.completed])
            
        # Add intermediate quests for mid-level players
        if player_level >= 3:
            available.extend([q for q in self.all_quests['intermediate'] if not q.completed])
            
        # Add advanced quests for high-level players
        if player_level >= 6:
            available.extend([q for q in self.all_quests['advanced'] if not q.completed])
            
        # Story quests based on story progress
        if self.story_progress >= 0:
            available.extend([q for q in self.all_quests['story'] if not q.completed])
            
        return available
    
    def update_quest_progress(self, player, action_type, target=None, amount=1):
        """Update progress for all active quests"""
        completed_quests = []
        
        for quest in player.quests:
            if quest.completed:
                continue
                
            # Handle different quest types
            if quest.quest_type == f"kill_{target}" and action_type == "kill":
                if quest.update_progress("kill", amount):
                    completed_quests.append(quest)
                    
            elif quest.quest_type == "collect_gold" and action_type == "gold_gained":
                if quest.update_progress("collect_gold", amount):
                    completed_quests.append(quest)
                    
            elif quest.quest_type == "equip_weapon" and action_type == "weapon_equipped":
                if quest.update_progress("equip_weapon", amount):
                    completed_quests.append(quest)
                    
            elif quest.quest_type == "reach_level" and action_type == "level_up":
                quest.current_progress = player.level
                if quest.current_progress >= quest.target_amount:
                    quest.completed = True
                    completed_quests.append(quest)
        
        # Award rewards for completed quests
        for quest in completed_quests:
            self.complete_quest(player, quest)
            
        return completed_quests
    
    def complete_quest(self, player, quest):
        """Complete a quest and give rewards"""
        print(f"\n🎊 Quest Complete: {quest.name}!")
        print(f"📜 {quest.description}")
        
        # Give rewards
        if quest.reward_exp > 0:
            player.add_experience(quest.reward_exp)
            print(f"✨ Gained {quest.reward_exp} experience!")
            
        if quest.reward_gold > 0:
            player.gold += quest.reward_gold
            print(f"💰 Gained {quest.reward_gold} gold!")
            
        for item in quest.reward_items:
            player.add_item(item)
            print(f"🎁 Received: {item['name']}!")
            
        # Move to completed quests
        if quest in player.quests:
            player.quests.remove(quest)
        player.completed_quests.append(quest)
        
        # Update story progress for story quests
        if quest.quest_type == "story":
            self.story_progress += 1
    
    def assign_quest(self, player, quest_index):
        """Assign a quest to the player"""
        available = self.get_available_quests(player.level)
        
        if 0 <= quest_index < len(available):
            quest = available[quest_index]
            if quest not in player.quests:
                player.quests.append(quest)
                print(f"📋 Quest accepted: {quest.name}")
                print(f"📝 {quest.description}")
                print(f"🎁 Reward: {quest.get_reward_text()}")
                return True
        return False
    
    def display_available_quests(self, player_level):
        """Display all available quests"""
        available = self.get_available_quests(player_level)
        
        if not available:
            print("No quests available at your current level.")
            return
            
        print("\n📋 Available Quests:")
        for i, quest in enumerate(available):
            print(f"\n{i + 1}. {quest.name}")
            print(f"   📝 {quest.description}")
            print(f"   🎁 Reward: {quest.get_reward_text()}")
    
    def display_active_quests(self, player):
        """Display player's active quests"""
        if not player.quests:
            print("📋 No active quests.")
            return
            
        print("\n📋 Active Quests:")
        for quest in player.quests:
            quest.display_progress()
            print()
    
    def display_completed_quests(self, player):
        """Display player's completed quests"""
        if not player.completed_quests:
            print("📋 No completed quests yet.")
            return
            
        print("\n✅ Completed Quests:")
        for quest in player.completed_quests:
            print(f"✅ {quest.name}")

# Random quest generator for additional content
class RandomQuestGenerator:
    @staticmethod
    def generate_daily_quest(player_level):
        """Generate a random daily quest"""
        quest_templates = [
            {
                'name': 'Daily Hunt',
                'description': 'Defeat {amount} enemies',
                'type': 'kill_any',
                'amounts': [3, 5, 7],
                'rewards': {'exp': [30, 50, 80], 'gold': [20, 35, 60]}
            },
            {
                'name': 'Gold Rush',
                'description': 'Collect {amount} gold',
                'type': 'collect_gold',
                'amounts': [50, 100, 200],
                'rewards': {'exp': [25, 40, 70], 'gold': [10, 20, 40]}
            }
        ]
        
        template = random.choice(quest_templates)
        difficulty_index = min(player_level // 3, 2)  # 0, 1, or 2
        
        amount = template['amounts'][difficulty_index]
        exp_reward = template['rewards']['exp'][difficulty_index]
        gold_reward = template['rewards']['gold'][difficulty_index]
        
        return Quest(
            name=template['name'],
            description=template['description'].format(amount=amount),
            quest_type=template['type'],
            target_amount=amount,
            reward_exp=exp_reward,
            reward_gold=gold_reward
        )

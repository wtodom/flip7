from typing import List, Set
from .card import Card, CardType, ActionType

class Player:
    """Represents a player in the Flip 7 game."""
    
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        self.number_cards: Set[int] = set()  # Track unique numbers for quick bust checking
        self.bonus_cards: List[Card] = []
        self.has_second_chance = False
        self.is_frozen = False
        self.has_passed = False
        self.has_busted = False
    
    def receive_card(self, card: Card) -> bool:
        """
        Receive a card and handle its effects.
        Returns True if the player busts, False otherwise.
        """
        if self.is_frozen or self.has_passed or self.has_busted:
            if card.card_type == CardType.ACTION and card.action_type == ActionType.DEAL_THREE:
                return True  # Indicate bust to stop Deal Three sequence
            raise ValueError(f"Player {self.name} cannot receive cards")
        
        if card.card_type == CardType.NUMBER:
            if card.number_value in self.number_cards:
                return True  # Bust
            self.number_cards.add(card.number_value)
            self.hand.append(card)
        
        elif card.card_type == CardType.ACTION:
            if card.action_type == ActionType.FREEZE:
                self.is_frozen = True
            elif card.action_type == ActionType.SECOND_CHANCE:
                if self.has_second_chance:
                    return False  # Card will be handled by game logic (given to another player)
                self.has_second_chance = True
            self.hand.append(card)
        
        elif card.card_type == CardType.BONUS:
            self.bonus_cards.append(card)
        
        return False
    
    def use_second_chance(self) -> bool:
        """
        Attempt to use Second Chance.
        Returns True if successful, False if not available.
        """
        if not self.has_second_chance:
            return False
        self.has_second_chance = False
        # Remove the Second Chance card from hand
        self.hand = [card for card in self.hand 
                    if not (card.card_type == CardType.ACTION 
                           and card.action_type == ActionType.SECOND_CHANCE)]
        return True
    
    def calculate_score(self) -> int:
        """Calculate the player's score including bonuses."""
        if self.has_busted:
            return 0
        
        # Base score is sum of number cards
        score = sum(card.number_value for card in self.hand 
                   if card.card_type == CardType.NUMBER)
        
        # Add 15 points bonus for 7 unique numbers
        if len(self.number_cards) >= 7:
            score += 15
        
        # Apply bonus cards
        for bonus_card in self.bonus_cards:
            score = bonus_card.apply_bonus(score)
        
        return score
    
    def has_seven_numbers(self) -> bool:
        """Check if player has collected 7 unique number cards."""
        return len(self.number_cards) >= 7
    
    def __str__(self) -> str:
        return (f"Player {self.name}: "
                f"Numbers={sorted(list(self.number_cards))}, "
                f"Score={self.calculate_score()}") 
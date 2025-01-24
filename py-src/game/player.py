"""Player implementation for Flip 7."""
from typing import List, Dict, Optional
import random

from src.game.card import Card, CardType
from src.profiles.profile_loader import PlayerProfile
from src.profiles.strategy import ProfileStrategy

class Player:
    """Represents a player in the game."""
    
    def __init__(self, profile: Optional[PlayerProfile] = None):
        """Initialize a new player."""
        self.profile = profile
        self.strategy = ProfileStrategy(profile) if profile else None
        self.cards: List[Card] = []
        self.has_second_chance = False
        self.has_busted = False
        self.is_frozen = False
        self.has_passed = False
    
    def receive_card(self, card: Card) -> bool:
        """
        Add a card to the player's hand.
        Returns True if this would cause a bust (for number cards).
        Raises ValueError if player cannot receive cards.
        """
        if self.is_frozen or self.has_passed or self.has_busted:
            if card.card_type == CardType.ACTION:
                return True  # Indicate bust to stop Deal Three sequence
            raise ValueError("Player cannot receive cards")
            
        self.cards.append(card)
        
        if card.card_type == CardType.NUMBER:
            # Get all number cards in hand
            number_cards = [c.number_value for c in self.cards 
                          if c.card_type == CardType.NUMBER]
            # Check for duplicates
            if len(number_cards) != len(set(number_cards)):
                self.has_busted = True
                return True
        
        return False
    
    def get_score(self) -> int:
        """Calculate the player's current score."""
        score = 0
        unique_numbers = {c.number_value for c in self.cards 
                         if c.card_type == CardType.NUMBER}
        
        # Base score from unique numbers
        score = sum(unique_numbers)
        
        # Apply modifiers
        for card in self.cards:
            if card.card_type == CardType.MODIFIER:
                if card.is_multiplier:
                    score *= card.number_value
                else:
                    score += card.number_value
        
        return score
    
    def has_seven_numbers(self) -> bool:
        """Check if player has exactly seven unique numbers."""
        unique_numbers = {c.number_value for c in self.cards 
                         if c.card_type == CardType.NUMBER}
        return len(unique_numbers) == 7
    
    def should_draw_card(self, state: Dict) -> bool:
        """Decide whether to draw another card."""
        if self.strategy:
            return self.strategy.should_draw_card(state)
        
        # Default AI: Draw until we have 5 unique numbers
        unique_numbers = len({c.number_value for c in self.cards 
                            if c.card_type == CardType.NUMBER})
        return unique_numbers < 5
    
    def should_use_second_chance(self, state: Dict) -> bool:
        """Decide whether to use a Second Chance card."""
        if self.strategy:
            return self.strategy.should_use_second_chance(state)
            
        # Default AI: Always use Second Chance
        return True
    
    def end_game(self, won: bool) -> None:
        """Handle end of game tasks."""
        if self.strategy:
            self.strategy.end_game(won)
    
    def is_done(self) -> bool:
        """Check if player is done with their turn."""
        return self.has_busted or self.is_frozen or self.has_passed
    
    def status(self) -> str:
        """Get the player's current status."""
        if self.has_busted:
            return "busted"
        elif self.is_frozen:
            return "frozen"
        elif self.has_passed:
            return "passed"
        else:
            return "active" 
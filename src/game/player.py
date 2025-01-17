"""Player implementation for Flip 7."""
from dataclasses import dataclass, field
from typing import List, Optional
import random

from .card import Card, CardType, ActionType
from ..profiles.profile_loader import PlayerProfile
from ..profiles.strategy import ProfileStrategy, GameState

@dataclass
class Player:
    """Represents a player in the game."""
    name: str
    cards: List[Card] = field(default_factory=list)
    has_second_chance: bool = False
    is_frozen: bool = False
    has_passed: bool = False
    has_busted: bool = False
    profile: Optional[PlayerProfile] = None
    strategy: Optional[ProfileStrategy] = None
    
    def __post_init__(self):
        """Initialize strategy if profile is provided."""
        if self.profile:
            self.strategy = ProfileStrategy(self.profile)
    
    def receive_card(self, card: Card) -> bool:
        """Add a card to the player's hand. Returns True if this would cause a bust."""
        if self.is_frozen or self.has_passed or self.has_busted:
            if card.card_type == CardType.ACTION and card.action_type == ActionType.DEAL_THREE:
                return True  # Indicate bust to stop Deal Three sequence
            raise ValueError(f"Player {self.name} cannot receive cards")
        
        self.cards.append(card)
        
        if card.card_type == CardType.ACTION:
            if card.action_type == ActionType.SECOND_CHANCE:
                self.has_second_chance = True
            elif card.action_type == ActionType.FREEZE:
                self.is_frozen = True
        
        return self.would_bust()
    
    def get_score(self) -> int:
        """Get the player's current score."""
        number_cards = [c for c in self.cards if c.card_type == CardType.NUMBER]
        unique_numbers = len(set(c.number_value for c in number_cards))
        return unique_numbers
    
    def would_bust(self) -> bool:
        """Check if the player would bust with their current cards."""
        number_cards = [c for c in self.cards if c.card_type == CardType.NUMBER]
        unique_numbers = set(c.number_value for c in number_cards)
        return len(unique_numbers) > 7
    
    def has_seven_numbers(self) -> bool:
        """Check if the player has exactly seven unique numbers."""
        number_cards = [c for c in self.cards if c.card_type == CardType.NUMBER]
        unique_numbers = set(c.number_value for c in number_cards)
        return len(unique_numbers) == 7
    
    def should_draw_card(self, game_state: GameState) -> bool:
        """Decide whether to draw another card."""
        if self.strategy:
            return self.strategy.should_draw_card(game_state)
        
        # Default strategy if no profile
        if len(self.cards) <= 3:
            return True
        elif len(self.cards) == 4:
            return random.random() < 0.7
        elif len(self.cards) == 5:
            return random.random() < 0.5
        elif len(self.cards) == 6:
            return random.random() < 0.3
        return False
    
    def should_use_second_chance(self, game_state: GameState) -> bool:
        """Decide whether to use a Second Chance card."""
        if not self.has_second_chance:
            return False
            
        if self.strategy:
            return self.strategy.should_use_second_chance(game_state)
            
        # Default strategy: use it immediately
        return True
    
    def end_game(self, won: bool) -> None:
        """Handle end of game, update strategy if needed."""
        if self.strategy:
            self.strategy.end_game(won) 
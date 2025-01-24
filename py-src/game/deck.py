"""Deck implementation for Flip 7."""
import random
from typing import List, Optional

from src.game.card import Card, CardType, ActionType

class Deck:
    """Represents a deck of cards for Flip 7."""
    
    def __init__(self):
        """Initialize a new deck with all cards."""
        self.cards: List[Card] = []
        self.discard_pile: List[Card] = []
        
        # Add number cards (0-12, four of each)
        for value in range(13):
            for _ in range(4):
                self.cards.append(Card(CardType.NUMBER, value))
        
        # Add action cards
        for _ in range(4):
            self.cards.append(Card(CardType.ACTION, ActionType.FREEZE))
            self.cards.append(Card(CardType.ACTION, ActionType.DEAL_THREE))
            self.cards.append(Card(CardType.ACTION, ActionType.SECOND_CHANCE))
        
        # Add modifier cards
        for value in [2, 4, 6, 8, 10]:
            self.cards.append(Card(CardType.MODIFIER, value))
        self.cards.append(Card(CardType.MODIFIER, 2, is_multiplier=True))
    
    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)
    
    def draw(self) -> Optional[Card]:
        """Draw a card from the deck. Returns None if deck is empty."""
        if not self.cards:
            self._shuffle_discard_pile()
        
        if not self.cards:
            return None
            
        return self.cards.pop()
    
    def discard(self, card: Card) -> None:
        """Add a card to the discard pile."""
        self.discard_pile.append(card)
    
    def _shuffle_discard_pile(self) -> None:
        """Shuffle the discard pile back into the deck."""
        if not self.discard_pile:
            return
            
        self.cards.extend(self.discard_pile)
        self.discard_pile = []
        self.shuffle()
    
    def __len__(self) -> int:
        """Return the number of cards remaining in the deck."""
        return len(self.cards) 
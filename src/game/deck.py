import random
from typing import List
from .card import Card, CardType, ActionType, BonusType

class Deck:
    """Represents the deck of cards in Flip 7."""
    
    def __init__(self, seed: int = None):
        """Initialize a new deck with all cards."""
        if seed is not None:
            random.seed(seed)
        
        self.cards: List[Card] = []
        self._initialize_deck()
        self.shuffle()
    
    def _initialize_deck(self):
        """Create all cards for a fresh deck."""
        # Add number cards
        for num in range(13):
            count = num if 1 <= num <= 12 else 1  # 1 copy of 0, n copies of n for 1-12
            for _ in range(count):
                self.cards.append(Card(CardType.NUMBER, number_value=num))
        
        # Add action cards
        for action in ActionType:
            for _ in range(3):  # 3 copies of each action card
                self.cards.append(Card(CardType.ACTION, action_type=action))
        
        # Add bonus cards (one of each)
        for bonus in BonusType:
            self.cards.append(Card(CardType.BONUS, bonus_type=bonus))
    
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
    
    def draw(self) -> Card:
        """Draw a card from the deck."""
        if not self.cards:
            raise ValueError("No cards left in deck")
        return self.cards.pop()
    
    def __len__(self) -> int:
        return len(self.cards)
    
    @property
    def cards_remaining(self) -> int:
        """Number of cards remaining in the deck."""
        return len(self) 
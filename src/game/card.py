"""Card implementation for Flip 7."""
from enum import Enum, auto
from typing import Optional, Union

class CardType(Enum):
    """Types of cards in the game."""
    NUMBER = auto()
    ACTION = auto()
    MODIFIER = auto()

class ActionType(Enum):
    """Types of action cards."""
    FREEZE = auto()
    DEAL_THREE = auto()
    SECOND_CHANCE = auto()

class Card:
    """Represents a card in the game."""
    
    def __init__(self, card_type: CardType, value: Union[int, ActionType], is_multiplier: bool = False):
        """Initialize a new card."""
        self.card_type = card_type
        
        if card_type == CardType.NUMBER:
            if not isinstance(value, int) or value < 0 or value > 12:
                raise ValueError(f"Invalid number value: {value}")
            self.number_value = value
            self.action_type = None
            self.is_multiplier = False
        elif card_type == CardType.ACTION:
            if not isinstance(value, ActionType):
                raise ValueError(f"Invalid action type: {value}")
            self.number_value = None
            self.action_type = value
            self.is_multiplier = False
        elif card_type == CardType.MODIFIER:
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"Invalid modifier value: {value}")
            self.number_value = value
            self.action_type = None
            self.is_multiplier = is_multiplier
        else:
            raise ValueError(f"Invalid card type: {card_type}")
    
    def __str__(self) -> str:
        """Return a string representation of the card."""
        if self.card_type == CardType.NUMBER:
            return str(self.number_value)
        elif self.card_type == CardType.ACTION:
            return self.action_type.name
        else:  # MODIFIER
            return f"{'×' if self.is_multiplier else '+'}{self.number_value}"
    
    def __repr__(self) -> str:
        """Return a detailed string representation of the card."""
        return f"Card({self.card_type.name}, {self.number_value if self.number_value is not None else self.action_type.name if self.action_type is not None else 'None'}, is_multiplier={self.is_multiplier})" 
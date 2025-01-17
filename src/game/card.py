from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class CardType(Enum):
    """Types of cards in the game."""
    NUMBER = 1
    ACTION = 2
    BONUS = 3
    MODIFIER = 4  # Added MODIFIER type

class ActionType(Enum):
    FREEZE = auto()
    DEAL_THREE = auto()
    SECOND_CHANCE = auto()

class BonusType(Enum):
    PLUS_2 = 2
    PLUS_4 = 4
    PLUS_6 = 6
    PLUS_8 = 8
    PLUS_10 = 10
    MULTIPLY_2 = -2  # Using negative to indicate multiplication

@dataclass
class Card:
    """A card in the game."""
    card_type: CardType
    number_value: Optional[int] = None
    action_type: Optional[ActionType] = None
    bonus_type: Optional[BonusType] = None
    is_multiplier: bool = False  # Added for modifier cards

    def __post_init__(self):
        """Validate card configuration."""
        valid = False
        if self.card_type == CardType.NUMBER:
            valid = self.number_value is not None and 0 <= self.number_value <= 12
        elif self.card_type == CardType.ACTION:
            # For action cards, the action_type should be passed as the second argument
            if isinstance(self.number_value, ActionType):
                self.action_type = self.number_value
                self.number_value = None
            valid = self.action_type is not None
        elif self.card_type == CardType.BONUS:
            valid = self.bonus_type is not None
        elif self.card_type == CardType.MODIFIER:
            valid = self.number_value is not None and self.number_value in [2, 4, 6, 8, 10]

        if not valid:
            raise ValueError("Invalid card configuration")

    def __str__(self) -> str:
        if self.card_type == CardType.NUMBER:
            return str(self.number_value)
        elif self.card_type == CardType.ACTION:
            return self.action_type.name
        else:
            if self.bonus_type.value < 0:
                return "x2"
            return f"+{self.bonus_type.value}"

    def apply_bonus(self, score: int) -> int:
        """Apply bonus card effect to a score."""
        if self.card_type != CardType.BONUS:
            return score
        
        if self.bonus_type.value < 0:  # Multiply
            return score * 2
        return score + self.bonus_type.value 
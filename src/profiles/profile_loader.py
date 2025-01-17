"""Profile loading and validation for Flip 7 player profiles."""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union
import yaml

@dataclass
class RiskTolerance:
    base: float
    card_count_weights: List[float]
    score_sensitivity: float
    deck_awareness: float

    @classmethod
    def from_dict(cls, data: dict) -> 'RiskTolerance':
        return cls(
            base=data['base'],
            card_count_weights=data['card_count_weights'],
            score_sensitivity=data['score_sensitivity'],
            deck_awareness=data['deck_awareness']
        )

    def validate(self) -> None:
        """Validate risk tolerance configuration."""
        if not 0 <= self.base <= 1:
            raise ValueError(f"Base risk tolerance must be between 0 and 1, got {self.base}")
        if not all(0 <= w <= 1 for w in self.card_count_weights):
            raise ValueError("Card count weights must be between 0 and 1")
        if len(self.card_count_weights) != 7:
            raise ValueError(f"Expected 7 card count weights, got {len(self.card_count_weights)}")
        if not 0 <= self.score_sensitivity <= 1:
            raise ValueError(f"Score sensitivity must be between 0 and 1, got {self.score_sensitivity}")
        if not 0 <= self.deck_awareness <= 1:
            raise ValueError(f"Deck awareness must be between 0 and 1, got {self.deck_awareness}")

@dataclass
class LuckyCards:
    enabled: bool
    cards: List[Union[int, str]]

    @classmethod
    def from_dict(cls, data: dict) -> 'LuckyCards':
        return cls(
            enabled=data['enabled'],
            cards=data['cards']
        )

    def validate(self) -> None:
        """Validate lucky cards configuration."""
        if self.enabled and not self.cards:
            raise ValueError("Lucky cards enabled but no cards specified")
        for card in self.cards:
            if isinstance(card, int) and not 0 <= card <= 12:
                raise ValueError(f"Invalid lucky card number: {card}")
            elif isinstance(card, str) and card not in ["Second Chance", "Deal Three", "Freeze"]:
                raise ValueError(f"Invalid lucky card type: {card}")

@dataclass
class Superstitions:
    enabled: bool
    negative: List[Union[int, str]]
    threshold: float

    @classmethod
    def from_dict(cls, data: dict) -> 'Superstitions':
        return cls(
            enabled=data['enabled'],
            negative=data['negative'],
            threshold=data['threshold']
        )

    def validate(self) -> None:
        """Validate superstitions configuration."""
        if self.enabled and not self.negative:
            raise ValueError("Superstitions enabled but no cards specified")
        if not 0 <= self.threshold <= 1:
            raise ValueError(f"Threshold must be between 0 and 1, got {self.threshold}")
        for card in self.negative:
            if isinstance(card, int) and not 0 <= card <= 12:
                raise ValueError(f"Invalid superstition card number: {card}")
            elif isinstance(card, str) and card not in ["Second Chance", "Deal Three", "Freeze"]:
                raise ValueError(f"Invalid superstition card type: {card}")

@dataclass
class PlayerProfile:
    name: str
    description: str
    intelligence: float
    risk_tolerance: RiskTolerance
    target_score: int
    catch_up_aggression: float
    lucky_cards: LuckyCards
    superstitions: Superstitions

    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerProfile':
        return cls(
            name=data['name'],
            description=data['description'],
            intelligence=data['intelligence'],
            risk_tolerance=RiskTolerance.from_dict(data['risk_tolerance']),
            target_score=data['target_score'],
            catch_up_aggression=data['catch_up_aggression'],
            lucky_cards=LuckyCards.from_dict(data['lucky_cards']),
            superstitions=Superstitions.from_dict(data['superstitions'])
        )

    def validate(self) -> None:
        """Validate the complete profile configuration."""
        if not 0 <= self.intelligence <= 1:
            raise ValueError(f"Intelligence must be between 0 and 1, got {self.intelligence}")
        if not 0 <= self.catch_up_aggression <= 1:
            raise ValueError(f"Catch-up aggression must be between 0 and 1, got {self.catch_up_aggression}")
        if not 20 <= self.target_score <= 100:
            raise ValueError(f"Target score must be between 20 and 100, got {self.target_score}")
        
        self.risk_tolerance.validate()
        self.lucky_cards.validate()
        self.superstitions.validate()

def load_profile(profile_path: Union[str, Path]) -> PlayerProfile:
    """Load a player profile from a YAML file."""
    profile_path = Path(profile_path)
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {profile_path}")
    
    with open(profile_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in profile {profile_path}: {e}")
    
    try:
        profile = PlayerProfile.from_dict(data)
        profile.validate()
        return profile
    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid profile configuration in {profile_path}: {e}")

def load_all_profiles(profiles_dir: Union[str, Path]) -> List[PlayerProfile]:
    """Load all profiles from a directory."""
    profiles_dir = Path(profiles_dir)
    if not profiles_dir.exists():
        raise FileNotFoundError(f"Profiles directory not found: {profiles_dir}")
    
    profiles = []
    for profile_path in profiles_dir.glob("*.yaml"):
        try:
            profile = load_profile(profile_path)
            profiles.append(profile)
        except ValueError as e:
            print(f"Warning: Skipping invalid profile {profile_path}: {e}")
    
    return profiles 
"""Strategy implementation for player profiles."""
from dataclasses import dataclass
from typing import List, Dict, Optional
import random

from ..game.card import Card, CardType, ActionType
from .profile_loader import PlayerProfile

@dataclass
class GameState:
    """Current state of the game from a player's perspective."""
    current_score: int
    card_count: int
    cards_seen: List[Card]
    cards_in_hand: List[Card]  # The cards currently in the player's hand
    other_players_scores: List[int]
    max_score: int
    has_second_chance: bool

class ProfileStrategy:
    """Implements decision making based on player profiles."""
    
    def __init__(self, profile: PlayerProfile):
        self.profile = profile
        self.game_memory: List[Dict] = []  # Stores game outcomes for learning
        self.current_game_state: Dict = {
            'lucky_cards_seen': 0,
            'superstition_cards_seen': 0,
            'last_decision_risk': 0.5,  # Default risk level
            'successful_decisions': 0,  # Tracks good decisions for learning
            'total_decisions': 0
        }
    
    def calculate_base_risk(self, state: GameState) -> float:
        """Calculate the base risk level."""
        # Start with the base risk tolerance
        risk = self.profile.risk_tolerance.base * 1.1  # Increase base risk by 10%

        # Adjust based on card count
        if 0 <= state.card_count < len(self.profile.risk_tolerance.card_count_weights):
            risk *= self.profile.risk_tolerance.card_count_weights[state.card_count]

        # Adjust based on score sensitivity
        score_ratio = state.current_score / self.profile.target_score
        if score_ratio < 1.0:
            # Increase risk when below target score
            risk *= (1.0 + (1.0 - score_ratio) * self.profile.risk_tolerance.score_sensitivity * 0.5)
        else:
            # Decrease risk when above target score
            risk *= (1.0 - (score_ratio - 1.0) * self.profile.risk_tolerance.score_sensitivity)

        # Apply intelligence factor
        risk = risk * (0.7 + self.profile.intelligence * 0.3)

        return min(1.0, max(0.0, risk))
    
    def adjust_for_deck_awareness(self, base_risk: float, state: GameState) -> float:
        """Adjust risk based on cards seen and deck awareness."""
        if not state.cards_seen:
            return base_risk
        
        # More intelligent players make better use of deck information
        awareness = self.profile.risk_tolerance.deck_awareness * self.profile.intelligence
        
        # Count remaining high and low cards
        high_cards = sum(1 for card in state.cards_seen 
                        if card.card_type == CardType.NUMBER and card.number_value > 7)
        low_cards = sum(1 for card in state.cards_seen 
                       if card.card_type == CardType.NUMBER and card.number_value <= 7)
        
        # Adjust risk based on card distribution
        if high_cards > low_cards:
            base_risk *= (1.0 - 0.2 * awareness)  # Reduce risk if many high cards seen
        else:
            base_risk *= (1.0 + 0.2 * awareness)  # Increase risk if many low cards seen
            
        return min(max(base_risk, 0.0), 1.0)
    
    def adjust_for_personality(self, risk: float, state: GameState) -> float:
        """Adjust risk based on lucky cards and superstitions."""
        if self.profile.lucky_cards.enabled:
            for card in state.cards_in_hand:
                if (card.number_value is not None and card.number_value in self.profile.lucky_cards.cards) or \
                   (card.card_type == CardType.ACTION and str(card.action_type) in self.profile.lucky_cards.cards):
                    risk = min(1.0, risk * 1.6)  # Increase risk by 60% for lucky cards

        if self.profile.superstitions.enabled:
            for card in state.cards_in_hand:
                if (card.number_value is not None and card.number_value in self.profile.superstitions.negative) or \
                   (card.card_type == CardType.ACTION and str(card.action_type) in self.profile.superstitions.negative):
                    if random.random() < self.profile.superstitions.threshold:
                        risk *= 0.7  # Reduce risk by 30% for unlucky cards

        return min(1.0, max(0.0, risk))
    
    def adjust_for_catch_up(self, risk: float, state: GameState) -> float:
        """Adjust risk based on catch-up behavior."""
        if not state.other_players_scores:
            return risk

        max_other_score = max(state.other_players_scores)
        score_diff = max_other_score - state.current_score

        if score_diff > 0:
            # Increase risk when behind, scaled by catch_up_aggression
            catch_up_factor = 1.0 + (score_diff / state.max_score) * self.profile.catch_up_aggression * 1.2
            risk = min(1.0, risk * catch_up_factor)

        return risk
    
    def learn_from_outcome(self, success: bool) -> None:
        """Update strategy based on decision outcomes."""
        self.current_game_state['total_decisions'] += 1
        if success:
            self.current_game_state['successful_decisions'] += 1
            
        # Only adapt if intelligence is high enough
        if self.profile.intelligence > 0.7:
            success_rate = (self.current_game_state['successful_decisions'] / 
                          max(1, self.current_game_state['total_decisions']))
            
            # Adjust base risk tolerance based on success rate
            if success_rate > 0.6:
                self.profile.risk_tolerance.base = min(
                    1.0, 
                    self.profile.risk_tolerance.base * 1.1
                )
            elif success_rate < 0.4:
                self.profile.risk_tolerance.base = max(
                    0.0, 
                    self.profile.risk_tolerance.base * 0.9
                )
    
    def should_draw_card(self, state: GameState) -> bool:
        """Decide whether to draw another card based on profile and state."""
        # Always draw if we have too few cards
        if state.card_count < 3:
            return True
            
        # Calculate final risk threshold
        risk = self.calculate_base_risk(state)
        risk = self.adjust_for_deck_awareness(risk, state)
        risk = self.adjust_for_personality(risk, state)
        risk = self.adjust_for_catch_up(risk, state)
        
        # Store for learning
        self.current_game_state['last_decision_risk'] = risk
        
        # Compare against random threshold
        return random.random() < risk
    
    def should_use_second_chance(self, state: GameState) -> bool:
        """Decide whether to use a Second Chance card."""
        if not state.has_second_chance:
            return False
            
        # More intelligent players make better use of Second Chance
        if self.profile.intelligence > 0.8:
            # Save it if we're close to target score
            if state.current_score >= self.profile.target_score * 0.8:
                return False
        
        # Use based on risk tolerance
        return random.random() < self.profile.risk_tolerance.base
    
    def end_game(self, won: bool) -> None:
        """Handle end of game, store memory if needed."""
        self.game_memory.append({
            'won': won,
            **self.current_game_state
        })
        
        # Reset current game state
        self.current_game_state = {
            'lucky_cards_seen': 0,
            'superstition_cards_seen': 0,
            'last_decision_risk': 0.5,
            'successful_decisions': 0,
            'total_decisions': 0
        } 
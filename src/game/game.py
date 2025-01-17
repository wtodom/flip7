from typing import List, Optional, Dict
from loguru import logger
from .deck import Deck
from .player import Player
from .card import Card, CardType, ActionType

class Game:
    """Manages a game of Flip 7."""
    
    def __init__(self, player_names: List[str], seed: Optional[int] = None):
        """Initialize a new game with the given players."""
        if not 5 <= len(player_names) <= 12:
            raise ValueError("Game requires 5-12 players")
        
        self.deck = Deck(seed)
        self.players = [Player(name) for name in player_names]
        self.current_player_idx = 0
        self.round_number = 0
        self.game_over = False
        self.round_stats: List[Dict] = []  # Track statistics for visualization
    
    def start_round(self):
        """Start a new round."""
        self.round_number += 1
        logger.info(f"Starting round {self.round_number}")
        
        # Reset player states
        for player in self.players:
            player.hand.clear()
            player.number_cards.clear()
            player.bonus_cards.clear()
            player.has_second_chance = False
            player.is_frozen = False
            player.has_passed = False
            player.has_busted = False
        
        # Deal initial cards
        for player in self.players:
            card = self.deck.draw()
            self._handle_card_effects(player, card)
        
        self.current_player_idx = 0
    
    def _handle_card_effects(self, player: Player, card: Card) -> bool:
        """
        Handle effects of a card being given to a player.
        Returns True if the round should end (7 numbers achieved).
        """
        try:
            # Try to give the card to the player
            would_bust = player.receive_card(card)
            
            if would_bust:
                if player.has_second_chance:
                    # Player can use Second Chance
                    player.use_second_chance()
                    return False
                else:
                    player.has_busted = True
                    logger.info(f"{player.name} busted!")
                    return False
            
            # Handle Deal Three (only if player hasn't busted)
            if (not player.has_busted and 
                card.card_type == CardType.ACTION and 
                card.action_type == ActionType.DEAL_THREE):
                for _ in range(3):
                    if len(self.deck.cards) == 0:
                        break
                    new_card = self.deck.draw()
                    if self._handle_card_effects(player, new_card):
                        return True
                    if player.has_busted:  # Stop if player busted
                        break
            
            # Handle Second Chance redistribution
            if (card.card_type == CardType.ACTION and 
                card.action_type == ActionType.SECOND_CHANCE and 
                player.has_second_chance):
                # Try to give to another player
                for other_player in self.players:
                    if (other_player != player and 
                        not other_player.has_second_chance and
                        not other_player.is_frozen and
                        not other_player.has_passed and
                        not other_player.has_busted):
                        other_player.receive_card(card)
                        return False
                # No valid player found, discard the card
                logger.info("Second Chance discarded - no valid recipients")
            
            return player.has_seven_numbers()
            
        except ValueError:
            # Player cannot receive cards (frozen/passed/busted)
            return False
    
    def play_turn(self, should_flip: bool) -> bool:
        """
        Play a turn for the current player.
        Returns True if the round should end.
        """
        player = self.players[self.current_player_idx]
        
        if player.is_frozen or player.has_passed or player.has_busted:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            return False
        
        if not should_flip:
            player.has_passed = True
            logger.info(f"{player.name} passes with score {player.calculate_score()}")
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            return False
        
        # Draw and handle card
        card = self.deck.draw()
        logger.info(f"{player.name} drew {card}")
        if self._handle_card_effects(player, card):
            logger.info(f"{player.name} got 7 unique numbers!")
            return True
        
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        return False
    
    def is_round_over(self) -> bool:
        """Check if the current round is over."""
        return all(p.is_frozen or p.has_passed or p.has_busted 
                  for p in self.players)
    
    def get_round_results(self) -> Dict:
        """Get the results of the current round."""
        results = {
            'round': self.round_number,
            'scores': {},
            'status': {},
            'cards': {},
            'winner': None,
            'winning_score': 0
        }
        
        for player in self.players:
            score = player.calculate_score()
            results['scores'][player.name] = score
            results['cards'][player.name] = len(player.number_cards)
            
            if player.has_busted:
                status = 'Busted'
            elif player.is_frozen:
                status = 'Frozen'
            elif player.has_passed:
                status = 'Passed'
            else:
                status = 'Active'
            results['status'][player.name] = status
            
            if score > results['winning_score']:
                results['winning_score'] = score
                results['winner'] = player.name
        
        self.round_stats.append(results)
        return results 
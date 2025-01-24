"""Game logic for Flip 7."""
import random
from typing import List, Optional
from loguru import logger

from src.game.card import Card, CardType, ActionType
from src.game.player import Player
from src.game.deck import Deck
from src.profiles.strategy import GameState

class Game:
    """Represents a game of Flip 7."""
    
    def __init__(self, players: List[Player], seed: Optional[int] = None):
        """Initialize a new game."""
        self.players = players
        self.deck = Deck()
        self.current_player_idx = 0
        self.second_chance_available = True
        
        if seed is not None:
            random.seed(seed)
            
        # Shuffle the deck
        self.deck.shuffle()
        
        # Deal initial cards
        for player in self.players:
            for _ in range(3):
                card = self.deck.draw()
                if card:
                    self._handle_card(player, card)
    
    def _handle_card(self, player: Player, card: Card) -> bool:
        """Handle drawing a card for a player. Returns True if player has won."""
        logger.debug(f"Player drew {card}")
        
        # Handle action cards
        if card.card_type == CardType.ACTION:
            if card.action_type == ActionType.DEAL_THREE:
                logger.debug("Activating Deal Three")
                for _ in range(3):
                    next_card = self.deck.draw()
                    if next_card:
                        if self._handle_card(player, next_card):
                            return True
                        if player.has_busted:
                            break
            elif card.action_type == ActionType.SECOND_CHANCE:
                logger.debug("Received Second Chance")
                player.has_second_chance = True
        
        # Add card to player's hand
        try:
            would_bust = player.receive_card(card)
            return player.has_seven_numbers()
        except ValueError:
            return False
    
    def _handle_turn(self, player: Player) -> bool:
        """Handle a player's turn. Returns True if they've won."""
        logger.debug("\nPlayer's turn")
        logger.debug(f"Current score: {player.get_score()}")
        
        # Skip if player has passed, frozen, or busted
        if player.has_passed or player.is_frozen or player.has_busted:
            logger.debug(f"Player is {player.status()}")
            return False
        
        # Get game state for strategy
        other_scores = [p.get_score() for p in self.players if p != player]
        state = GameState(
            current_score=player.get_score(),
            card_count=len(player.cards),
            cards_seen=[c for p in self.players for c in p.cards],
            cards_in_hand=player.cards,
            other_players_scores=other_scores,
            max_score=max([player.get_score()] + other_scores),
            has_second_chance=player.has_second_chance
        )
        
        # Check if player wants to draw
        if not player.should_draw_card(state):
            logger.debug("Player chooses to pass")
            player.has_passed = True
            return False
        
        # Draw card
        card = self.deck.draw()
        if not card:
            logger.debug("Deck is empty")
            return False
            
        # Handle card
        won = self._handle_card(player, card)
        
        # Check if player busted
        if player.has_busted:
            logger.debug("Player busted!")
            # Check for Second Chance
            if player.has_second_chance and player.should_use_second_chance(state):
                logger.debug("Player uses Second Chance")
                player.has_busted = False
                player.has_second_chance = False
                player.is_frozen = True
        
        return won
    
    def play_game(self) -> int:
        """Play a complete game. Returns the winning player's index."""
        while True:
            player = self.players[self.current_player_idx]
            
            if self._handle_turn(player):
                logger.info(f"Player {self.current_player_idx} wins with score {player.get_score()}!")
                return self.current_player_idx
            
            # Move to next player
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            
            # Check if all players are done
            if all(p.is_done() for p in self.players):
                # Find winner
                active_players = [p for p in self.players if not p.has_busted]
                if active_players:
                    winner = max(active_players, key=lambda p: p.get_score())
                    winner_idx = self.players.index(winner)
                    logger.info(f"Player {winner_idx} wins with score {winner.get_score()}!")
                    return winner_idx
                else:
                    # Everyone busted, highest score wins
                    winner = max(self.players, key=lambda p: p.get_score())
                    winner_idx = self.players.index(winner)
                    logger.info(f"Player {winner_idx} wins with score {winner.get_score()} (all busted)!")
                    return winner_idx 
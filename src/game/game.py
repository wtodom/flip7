"""Game implementation for Flip 7."""
import random
from typing import List, Optional, Tuple
from .card import Card, CardType, ActionType
from .player import Player
from ..profiles.strategy import GameState

class Game:
    """Represents a single game of Flip 7."""
    
    def __init__(self, players: List[Player], seed: Optional[int] = None):
        """Initialize a new game with the given players."""
        self.players = players
        self.deck = self._create_deck()
        self.discard_pile: List[Card] = []
        self.current_player_idx = 0
        self.winner: Optional[Player] = None
        
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.deck)
    
    def _create_deck(self) -> List[Card]:
        """Create and return a new deck of cards."""
        deck = []
        
        # Number cards (0-12, four of each)
        for value in range(13):
            for _ in range(4):
                deck.append(Card(CardType.NUMBER, value))
        
        # Action cards
        for _ in range(4):
            deck.append(Card(CardType.ACTION, ActionType.FREEZE))
            deck.append(Card(CardType.ACTION, ActionType.DEAL_THREE))
            deck.append(Card(CardType.ACTION, ActionType.SECOND_CHANCE))
        
        # Modifier cards
        for value in [2, 4, 6, 8, 10]:
            deck.append(Card(CardType.MODIFIER, value))
        deck.append(Card(CardType.MODIFIER, 2, is_multiplier=True))
        
        return deck
    
    def _get_game_state(self, player: Player) -> GameState:
        """Create a GameState object for the current player."""
        return GameState(
            current_score=player.get_score(),
            card_count=len(player.cards),
            cards_seen=self.discard_pile.copy(),
            other_players_scores=[p.get_score() for p in self.players if p != player],
            max_score=100,  # Maximum possible score
            cards_in_hand=player.cards.copy(),
            has_second_chance=player.has_second_chance
        )
    
    def _handle_deal_three(self, player: Player) -> bool:
        """Handle a Deal Three card. Returns True if player busts."""
        for _ in range(3):
            if not self.deck:
                self._shuffle_discard_pile()
            if not self.deck:  # Still no cards after shuffle
                return False
                
            card = self.deck.pop()
            try:
                would_bust = player.receive_card(card)
                if would_bust:
                    player.has_busted = True
                    return True
            except ValueError:
                # Player can't receive cards (frozen/passed/busted)
                self.discard_pile.append(card)
                return False
                
        return False
    
    def _shuffle_discard_pile(self) -> None:
        """Shuffle the discard pile back into the deck."""
        if not self.discard_pile:
            return
            
        self.deck.extend(self.discard_pile)
        self.discard_pile = []
        random.shuffle(self.deck)
    
    def play_turn(self) -> Tuple[bool, Optional[Player]]:
        """
        Play one player's turn.
        Returns (game_over, winner) tuple.
        """
        player = self.players[self.current_player_idx]
        
        # Skip if player can't take actions
        if player.is_frozen or player.has_passed or player.has_busted:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            return False, None
        
        # Get game state for decision making
        game_state = self._get_game_state(player)
        
        # Player decides whether to draw
        if not player.should_draw_card(game_state):
            player.has_passed = True
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            return self._check_game_over()
        
        # Draw card
        if not self.deck:
            self._shuffle_discard_pile()
        if not self.deck:  # Still no cards after shuffle
            return True, self._determine_winner()
            
        card = self.deck.pop()
        
        # Handle card
        try:
            would_bust = player.receive_card(card)
            if would_bust:
                if player.has_second_chance and player.should_use_second_chance(game_state):
                    player.has_second_chance = False
                else:
                    player.has_busted = True
                    self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
                    return self._check_game_over()
            
            # Handle action cards
            if card.card_type == CardType.ACTION:
                if card.action_type == ActionType.DEAL_THREE:
                    if self._handle_deal_three(player):
                        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
                        return self._check_game_over()
                elif card.action_type == ActionType.FREEZE:
                    player.is_frozen = True
                    self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
                    return self._check_game_over()
            
            # Check for win condition
            if player.has_seven_numbers():
                self.winner = player
                return True, player
                
        except ValueError:
            # Player couldn't receive card
            self.discard_pile.append(card)
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            return self._check_game_over()
        
        # Move to next player if frozen or passed
        if player.is_frozen or player.has_passed:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            
        return self._check_game_over()
    
    def _check_game_over(self) -> Tuple[bool, Optional[Player]]:
        """Check if the game is over and determine winner if needed."""
        # Game continues if any player can still take actions
        for player in self.players:
            if not (player.is_frozen or player.has_passed or player.has_busted):
                return False, None
        
        return True, self._determine_winner()
    
    def _determine_winner(self) -> Optional[Player]:
        """Determine the winner of the game."""
        if self.winner:
            return self.winner
            
        # Find player with highest score
        max_score = -1
        winner = None
        
        for player in self.players:
            score = player.get_score()
            if score > max_score:
                max_score = score
                winner = player
        
        # Update player strategies with game outcome
        for player in self.players:
            player.end_game(player == winner)
        
        return winner
    
    def play(self) -> Player:
        """Play the game until completion and return the winner."""
        game_over = False
        winner = None
        
        while not game_over:
            game_over, winner = self.play_turn()
        
        return winner 
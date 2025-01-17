"""Tests for the player profile system."""
import os
from pathlib import Path
import pytest
import yaml

from src.profiles.profile_loader import (
    PlayerProfile, RiskTolerance, LuckyCards, Superstitions,
    load_profile, load_all_profiles
)
from src.profiles.strategy import ProfileStrategy, GameState
from src.game.card import Card, CardType, ActionType
from src.game.player import Player
from src.game.game import Game
from src.simulation.simulator import (
    Simulator, SimulationConfig, PlayerConfig
)

@pytest.fixture
def test_profile_dir(tmp_path):
    """Create a temporary directory with test profiles."""
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()

    # Create test profile 1
    profile1 = {
        "name": "Test Profile 1",
        "description": "A test profile",
        "intelligence": 0.7,
        "risk_tolerance": {
            "base": 0.6,
            "card_count_weights": [1.0, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
            "score_sensitivity": 0.6,
            "deck_awareness": 0.7
        },
        "target_score": 55,
        "catch_up_aggression": 0.6,
        "lucky_cards": {
            "enabled": True,
            "cards": [7]
        },
        "superstitions": {
            "enabled": True,
            "negative": [4],
            "threshold": 0.5
        }
    }

    # Create test profile 2
    profile2 = {
        "name": "Test Profile 2",
        "description": "Another test profile",
        "intelligence": 0.8,
        "risk_tolerance": {
            "base": 0.7,
            "card_count_weights": [1.0, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
            "score_sensitivity": 0.7,
            "deck_awareness": 0.8
        },
        "target_score": 60,
        "catch_up_aggression": 0.7,
        "lucky_cards": {
            "enabled": False,
            "cards": []
        },
        "superstitions": {
            "enabled": False,
            "negative": [],
            "threshold": 0.5
        }
    }

    # Write profiles to files
    with open(profiles_dir / "profile_1.yaml", "w") as f:
        yaml.dump(profile1, f)
    with open(profiles_dir / "profile_2.yaml", "w") as f:
        yaml.dump(profile2, f)

    return profiles_dir

def test_load_profile(test_profile_dir):
    """Test loading a single profile."""
    profile = load_profile(test_profile_dir / "profile_1.yaml")
    
    assert isinstance(profile, PlayerProfile)
    assert profile.name == "Test Profile 1"
    assert profile.intelligence == 0.7
    assert profile.risk_tolerance.base == 0.6
    assert profile.target_score == 55
    assert profile.catch_up_aggression == 0.6
    assert profile.lucky_cards.enabled
    assert 7 in profile.lucky_cards.cards
    assert profile.superstitions.enabled
    assert 4 in profile.superstitions.negative

def test_load_all_profiles(test_profile_dir):
    """Test loading all profiles from a directory."""
    profiles = load_all_profiles(test_profile_dir)
    
    assert len(profiles) == 2
    assert all(isinstance(p, PlayerProfile) for p in profiles)
    assert {p.name for p in profiles} == {"Test Profile 1", "Test Profile 2"}

def test_profile_validation():
    """Test profile validation."""
    with pytest.raises(ValueError):
        RiskTolerance(
            base=1.5,  # Invalid: > 1
            card_count_weights=[1.0] * 7,
            score_sensitivity=0.5,
            deck_awareness=0.5
        ).validate()
    
    with pytest.raises(ValueError):
        LuckyCards(
            enabled=True,
            cards=[]  # Invalid: enabled but no cards
        ).validate()
    
    with pytest.raises(ValueError):
        Superstitions(
            enabled=True,
            negative=[20],  # Invalid card number
            threshold=0.5
        ).validate()

def test_strategy_decision_making():
    """Test strategy decision making."""
    profile = PlayerProfile(
        name="Test Profile",
        description="Test profile for strategy decisions",
        intelligence=0.7,
        risk_tolerance=RiskTolerance(
            base=0.6,
            card_count_weights=[1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
            score_sensitivity=0.6,
            deck_awareness=0.7
        ),
        target_score=50,
        catch_up_aggression=0.6,
        lucky_cards=LuckyCards(
            enabled=True,
            cards=[7]
        ),
        superstitions=Superstitions(
            enabled=True,
            negative=[4],
            threshold=0.4
        )
    )
    
    strategy = ProfileStrategy(profile)
    
    # Test basic decision making
    state = GameState(
        current_score=30,
        card_count=4,
        cards_seen=[],
        other_players_scores=[35, 40],
        max_score=100,
        cards_in_hand=[Card(CardType.NUMBER, 7)],  # Lucky number
        has_second_chance=True
    )
    
    # Run multiple decisions to test consistency
    decisions = [strategy.should_draw_card(state) for _ in range(100)]
    true_ratio = sum(decisions) / len(decisions)
    
    # Risk should be increased due to:
    # 1. Lucky card (7) present
    # 2. Behind other players (catch-up behavior)
    # Base risk is 0.6, increased by lucky card and catch-up
    assert 0.6 < true_ratio < 0.95  # Adjusted range based on new base risk

def test_game_with_profiles(test_profile_dir):
    """Test running a game with profiled players."""
    profiles = load_all_profiles(test_profile_dir)
    
    players = [
        Player(name=f"Player_{i+1}", profile=profile)
        for i, profile in enumerate(profiles)
    ]
    # Add some default players
    while len(players) < 6:
        players.append(Player(name=f"Player_{len(players)+1}"))
    
    game = Game(players=players, seed=42)
    winner = game.play()
    
    assert winner is not None
    assert isinstance(winner, Player)

def test_simulation_with_profiles(test_profile_dir):
    """Test running a simulation with profiles."""
    config = SimulationConfig(
        num_games=10,
        num_players=6,
        base_seed=42,
        profiles_dir=test_profile_dir,
        player_configs=[
            PlayerConfig(position=0, profile_name="Test Profile 1"),
            PlayerConfig(position=1, profile_name="Test Profile 2")
        ]
    )
    
    simulator = Simulator(config)
    results = simulator.run()
    
    assert results.total_games == 10
    assert len(results.profile_stats) == 3  # 2 profiles + default
    assert "Test Profile 1" in results.profile_stats
    assert "Test Profile 2" in results.profile_stats
    assert "default" in results.profile_stats 
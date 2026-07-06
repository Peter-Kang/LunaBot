
import pytest
from unittest.mock import patch, MagicMock
from Services.DnDServices.DnDService import DnD
from Services.DnDServices.Monsters.DnDMonsters import DnDEnvironments


class TestDnDRoll:
    """Test suite for DnD.roll() method"""

    def setup_method(self):
        """Initialize DnD instance before each test"""
        self.dnd = DnD()

    def test_roll_valid_simple_format(self):
        """Test rolling with valid simple format (XdY)"""
        with patch('random.randrange', return_value=5):
            result = self.dnd.roll("2d8")
            assert "You Rolled 2d8" in result
            assert "Total:" in result

    def test_roll_valid_format_with_addition(self):
        """Test rolling with valid format including addition (XdY+Z)"""
        with patch('random.randrange', return_value=5):
            result = self.dnd.roll("2d8+3")
            assert "You Rolled 2d8+3" in result
            assert "Total:" in result

    def test_roll_with_spaces(self):
        """Test rolling with spaces in input"""
        with patch('random.randrange', return_value=5):
            result = self.dnd.roll("2 d 8")
            assert "You Rolled 2d8" in result

    def test_roll_case_insensitive(self):
        """Test rolling is case insensitive"""
        with patch('random.randrange', return_value=5):
            result = self.dnd.roll("2D8")
            assert "You Rolled 2d8" in result

    def test_roll_invalid_format_no_d(self):
        """Test rolling with invalid format (no 'd')"""
        result = self.dnd.roll("28")
        assert "Please enter valid dice format" in result

    def test_roll_invalid_format_zero_dice_count(self):
        """Test rolling with zero dice count"""
        result = self.dnd.roll("0d8")
        assert "Please enter valid dice format" in result

    def test_roll_invalid_format_negative_dice_count(self):
        """Test rolling with negative dice count"""
        result = self.dnd.roll("-2d8")
        assert "Please enter valid dice format" in result

    def test_roll_invalid_format_non_numeric_count(self):
        """Test rolling with non-numeric dice count"""
        result = self.dnd.roll("xd8")
        assert "Please enter valid dice format" in result

    def test_roll_invalid_format_zero_dice_sides(self):
        """Test rolling with zero dice sides"""
        result = self.dnd.roll("2d0")
        assert "Please enter valid dice format" in result

    def test_roll_invalid_format_non_numeric_sides(self):
        """Test rolling with non-numeric dice sides"""
        result = self.dnd.roll("2dx")
        assert "Please enter valid dice format" in result

    def test_roll_invalid_format_non_numeric_addition(self):
        """Test rolling with non-numeric addition"""
        result = self.dnd.roll("2d8+x")
        assert "Please enter valid dice format" in result

    def test_roll_invalid_format_zero_addition(self):
        """Test rolling with zero addition (invalid)"""
        result = self.dnd.roll("2d8+0")
        assert "Total:" in result

    def test_roll_multiple_additions(self):
        """Test rolling with multiple plus signs"""
        result = self.dnd.roll("2d8+3+5")
        assert "Please enter valid dice format" in result

    @patch('random.randrange')
    def test_roll_total_calculation(self, mock_randrange):
        """Test that total is correctly calculated"""
        mock_randrange.side_effect = [3, 5]
        result = self.dnd.roll("2d8")
        assert "Total:8" in result

    @patch('random.randrange')
    def test_roll_total_with_addition(self, mock_randrange):
        """Test that total includes the flat addition"""
        mock_randrange.side_effect = [3, 5]
        result = self.dnd.roll("2d8+2")
        assert "Total:" in result

    @patch('random.randrange')
    def test_roll_results_displayed(self, mock_randrange):
        """Test that individual roll results are displayed"""
        mock_randrange.side_effect = [3, 5]
        result = self.dnd.roll("2d8")
        assert "[" in result and "]" in result

    @patch('random.randrange')
    def test_roll_long_results_truncated(self, mock_randrange):
        """Test that very long results are truncated"""
        mock_randrange.return_value = 500
        result = self.dnd.roll("10d20")
        # If results string exceeds 1900 chars, it should be empty
        assert "Total:" in result

    def test_roll_single_die(self):
        """Test rolling a single die"""
        with patch('random.randrange', return_value=4):
            result = self.dnd.roll("1d20")
            assert "You Rolled 1d20" in result
            assert "Total:" in result

    def test_encounter_no_result(self):
        """When the monsters provider returns None, Encounter should return a 'No result' embed"""
        mock_monsters = MagicMock()
        mock_monsters.Encounter.return_value = None
        dnd = DnD(argsDnDMonsters=mock_monsters)
        embed = dnd.Encounter(ChallengeRating=1.0, Environment=DnDEnvironments.All)
        assert hasattr(embed, 'title')
        assert getattr(embed, 'title') == "No result"

    def test_encounter_returns_embedding(self):
        """When the monsters provider returns a DnDMonster, its embedding is returned"""
        mock_monster = MagicMock()
        fake_embed = MagicMock()
        mock_monster.getEmbedding.return_value = fake_embed

        mock_monsters = MagicMock()
        mock_monsters.Encounter.return_value = mock_monster

        dnd = DnD(argsDnDMonsters=mock_monsters)
        embed = dnd.Encounter(ChallengeRating=2.0, Environment=DnDEnvironments.Forest)
        # Should be the exact object returned by getEmbedding
        assert embed is fake_embed

            
import unittest
from unittest.mock import patch
from io import StringIO

from main import main, load_data, menu, change_aspect_ratio


class MainTestCase(unittest.TestCase):
    @patch("your_module.load_data")
    @patch("your_module.menu")
    @patch("your_module.change_aspect_ratio")
    def test_main(self, mock_change_aspect_ratio, mock_menu, mock_load_data):
        # Test that main calls load_data, menu, and change_aspect_ratio
        main()
        mock_load_data.assert_called_once()
        mock_menu.assert_called_once()
        mock_change_aspect_ratio.assert_called_once()

        # Test that "VThang - 2023" is printed to stdout
        with patch("sys.stdout", new=StringIO()) as fake_out:
            main()
            self.assertEqual(fake_out.getvalue().strip(), "VThang - 2023")


if __name__ == "__main__":
    unittest.main()

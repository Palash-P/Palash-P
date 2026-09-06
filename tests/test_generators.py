import os, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]/"scripts"))
from svg_utils import finish, svg_open
class TestSVG(unittest.TestCase):
    def test_document(self):
        value=finish(svg_open(10,10,"test")); self.assertTrue(value.startswith("<svg")); self.assertTrue(value.endswith("</svg>\n"))
if __name__ == "__main__": unittest.main()

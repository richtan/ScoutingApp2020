import unittest
from flask import Flask, request, Blueprint, render_template
from ..util import DatabaseUtil

bp = Blueprint('tester', __name__)

class TestUM(unittest.TestCase):

    def setUp(self):
        DatabaseUtil.DatabaseUtil
        print("GOT DE DATABASE HHEHEHEHEHE")

    def test_False(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

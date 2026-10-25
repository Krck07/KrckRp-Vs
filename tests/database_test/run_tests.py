#!/usr/bin/env python3
"""
Simple test runner for database tests.
"""

import unittest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

if __name__ == '__main__':
    # Discover and run all tests in this directory
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with error code if tests failed
    sys.exit(not result.wasSuccessful())
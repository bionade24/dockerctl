#!/usr/bin/env python3
"""
Quick validation script to verify all tests can be imported and run.
"""
import sys
import unittest

# Add workspace to path
sys.path.insert(0, '/workspaces/dockerctl')

# Import test module
import test_parser

# Create test suite
loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(test_parser)

# Run tests
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Exit with appropriate code
sys.exit(0 if result.wasSuccessful() else 1)

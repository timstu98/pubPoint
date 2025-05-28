import unittest
from algorithms.bayesian_emulation.bayesian_emulator import BayesianEmulator

class TestBayesianEmulator(unittest.TestCase):

    def test_given_one_dimension__when_emulated__then_matches_known_values(self):
        # Input data
        x_train = [[1], [2], [3], [4], [5], [6], [7], [8]]
        D = [1, 2, 3, 4, 4, 3, 2, 1]

        # Initialize BayesianEmulator
        be = BayesianEmulator(2.5, 1, 1, x_train, D)

        # Compute M
        be.compute_M()

        # Check if emulated values match true values
        for i in range(len(x_train)):
            x_j = x_train[i]
            emulated = be.emulate(x_j)
            true_value = D[i]
            self.assertAlmostEqual(emulated, true_value, places=5, msg=f"Emulated value {emulated} does not match true value {true_value} for input {x_j}")
    
    def test_given_three_dimensions__when_emulated__then_matches_known_values(self):
        # Input data
        x_train = [[1,2], [2,1], [1,1], [3,3]]
        D = [2, 2, 1, 5]

        # Initialize BayesianEmulator
        be = BayesianEmulator(2.5, 1, 1, x_train, D)

        # Compute M
        be.compute_M()

        # Check if emulated values match true values
        for i in range(len(x_train)):
            x_j = x_train[i]
            emulated = be.emulate(x_j)
            true_value = D[i]
            self.assertAlmostEqual(emulated, true_value, places=5, msg=f"Emulated value {emulated} does not match true value {true_value} for input {x_j}")
    
    def test_given_five_dimensions__when_emulated__then_matches_known_values(self):
        # Input data
        x_train = [[1,2,3,4,5], [2,1,4,3,2], [1,1,1,1,1], [3,3,3,3,2]]
        D = [2, 2, 1, 5]

        # Initialize BayesianEmulator
        be = BayesianEmulator(2.5, 1, 1, x_train, D)

        # Compute M
        be.compute_M()

        # Check if emulated values match true values
        for i in range(len(x_train)):
            x_j = x_train[i]
            emulated = be.emulate(x_j)
            true_value = D[i]
            self.assertAlmostEqual(emulated, true_value, places=5, msg=f"Emulated value {emulated} does not match true value {true_value} for input {x_j}")

if __name__ == '__main__':
    unittest.main()
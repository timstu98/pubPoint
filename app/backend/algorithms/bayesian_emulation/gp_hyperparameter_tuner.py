import numpy as np
from scipy.optimize import minimize

class GPHyperparameterTuner:
    def __init__(self, x_train, D, beta):
        """
        Class to tune GP hyperparameters theta and sigma by maximizing
        the log marginal likelihood.

        Parameters:
        x_train : ndarray of shape (n_samples, n_features)
            Training input data.
        D : ndarray of shape (n_samples,)
            Training output data.
        beta : float
            GP prior mean.
        """
        self.x_train = np.array(x_train, dtype=np.float64)
        self.D = np.array(D, dtype=np.float64)
        self.beta = float(beta)
        self.noise_var = 1e-6

    def _kernel(self, X1, X2, theta, sigma):
        sq_dists = np.sum((X1[:, None, :] - X2[None, :, :])**2, axis=-1)
        return sigma**2 * np.exp(-sq_dists / theta**2)

    def _negative_log_marginal_likelihood(self, log_params):
        log_theta, log_sigma = log_params
        theta = np.exp(log_theta)
        sigma = np.exp(log_sigma)
        X = self.x_train
        y = self.D - self.beta
        n = len(y)

        K = self._kernel(X, X, theta, sigma)
        K[np.diag_indices_from(K)] += self.noise_var

        try:
            L = np.linalg.cholesky(K)
            alpha = np.linalg.solve(L.T, np.linalg.solve(L, y))
            logdetK = 2.0 * np.sum(np.log(np.diag(L)))
            nll = 0.5 * y.T @ alpha + 0.5 * logdetK + 0.5 * n * np.log(2 * np.pi)
            return nll
        except np.linalg.LinAlgError:
            return np.inf

    def tune(self, initial_theta=0.2, initial_sigma=1.0):
        """
        Returns optimal theta and sigma by minimizing negative log marginal likelihood.
        """
        initial_log_params = [np.log(initial_theta), np.log(initial_sigma)]
        bounds = [(np.log(1e-3), np.log(1.0)), (np.log(1e-3), np.log(1000.0))]

        result = minimize(self._negative_log_marginal_likelihood,
                          initial_log_params, method='L-BFGS-B', bounds=bounds)

        if not result.success:
            raise RuntimeError("Hyperparameter tuning failed.")

        theta_opt = np.round(np.exp(result.x[0]),5)
        sigma_opt = np.round(np.exp(result.x[1]),5)
        return theta_opt, sigma_opt

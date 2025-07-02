import numpy as np

class BayesianEmulator:
    def __init__(self, beta, sigma, theta, x_train, D, M=None):
        '''
        Creates a Bayesian Emulator for predicting the results of an expensive simulator (such as a Maps API)

        Parameters:
        beta : float
            The mean of the Gaussian Process, representing the expected value of the simulation output, E[f(x)].
            This is a constant value that shifts the entire Gaussian Process.

        sigma : float
            The standard deviation of the Gaussian Process, controlling the overall scale of the covariance.
            This determines how much the function values can deviate from the mean.

        theta : float
            The correlation-length parameter of the Gaussian Process, controlling the smoothness of the function.
            Smaller values of theta allow for more rapid changes in the function, while larger values result in smoother functions.

        x_train: (array-like)
            The active inputs chosen for each output of the true function to obtain the n known outputs, D
            shape (n_samples, n_dimensions)

        D: (array-like)
            The known outputs obtained from running the true function for x_train
            shape (n_samples,)

        M: (array-like)
            Precomputed value of Matrix M = Var[D]^{-1} (D - E[D])
            shape (n_samples, n_samples)
        '''
        self.beta = np.array(beta, dtype=np.float64)
        self.sigma = np.array(sigma, dtype=np.float64)
        self.theta = np.array(theta, dtype=np.float64)
        self.x_train = np.array(x_train, dtype=np.float64)
        self.D = np.array(D, dtype=np.float64)
        self.M = np.array(M, dtype=np.float64)
        self.noise_var = 1e-12

    def compute_M(self):
        """
        Computes the matrix M = Var[D]^{-1} (D - E[D])
        """
        self.x_train = np.array(self.x_train)
        self.D = np.array(self.D)
        X = self.x_train
        n = len(X)
        
        # Compute pairwise squared (Euclidean) distances, ||x^(j)-x^(k)||^2
        sq_dists = np.sum((X[:, np.newaxis, :] - X[np.newaxis, :, :])**2, axis=-1)
        
        # Compute covariance matrix K, Var[D] = sigma^2 e^{||x^(j)-x^(k)||^2 / theta^2}
        K = (self.sigma ** 2) * np.exp(-sq_dists / (self.theta ** 2))

        # don't use nugget for now
        # nugget: either user‑provided noise_var or tiny jitter
        # nugget = self.noise_var #+ 1e-10 * np.var(self.D)
        # K[np.diag_indices(n)] += nugget

        # Cholesky factor
        L = np.linalg.cholesky(K)
        
        # Center the outputs D by subtracting beta, D - E[D]
        y = self.D - self.beta
        
        # # Solve for M = K^{-1} y
        # self.M = np.linalg.solve(K, y)

        # Solve for M = K^{-1} y using L Lᵀ M = y
        z = np.linalg.solve(L, y)
        self.M = np.linalg.solve(L.T, z)
            
        return self.M

    def emulate(self, x):
        """
        Predicts the emulated value E_D[f(x)] using the precomputed M
        
        Parameters:
        x (array-like): New input point to emulate, shape (n_dimensions,)
        """
        if self.M is None:
            raise ValueError("M has not been computed. Run compute_M first or provide M.")
    
        x = np.array(x, dtype=np.float64)
        
        # Compute squared distances between x and each training point, ||x-x^(j)||^2
        sq_dists = np.sum((x-self.x_train)**2, axis=1)
        
        # Compute covariance vector k, Cov[f(x),D]_j = sigma^2 exp{-||x-x^(j)||^2/theta^2}
        k = (self.sigma ** 2) * np.exp(-sq_dists / (self.theta ** 2))
        
        # Calculate the emulated mean, E_D[f(x)] = E[f(x)] + Cov[f(x),D] Var[D]^-1(D - E[D])
        return self.beta + np.dot(k, self.M)
import numpy as np

class BayesianEmulator:
    def __init__(self, beta, sigma, theta, x_train, D=None, M=None):
        self.beta = beta
        self.sigma = sigma
        self.theta = theta
        self.x_train = x_train
        self.D = D
        self.M = M

    def compute_M(self, x_train, D):
        """
        Computes the matrix M = Var[D]^{-1} (D - E[D])
        
        Parameters:
        x_train (array-like): Training input points, shape (n_samples, n_dimensions)
        D (array-like): Observed outputs at x_train, shape (n_samples,)
        """
        self.x_train = np.array(x_train)
        self.D = np.array(D)
        
        # Compute pairwise squared (Euclidean) distances, ||x^(j)-x^(k)||^2
        X = self.x_train
        sq_dists = np.sum((X[:, np.newaxis, :] - X[np.newaxis, :, :])**2, axis=-1)
        
        # Compute covariance matrix K, Var[D] = sigma^2 e^{||x^(j)-x^(k)||^2 / theta^2}
        K = (self.sigma ** 2) * np.exp(-sq_dists / (self.theta ** 2))
        
        # Center the outputs D by subtracting beta, D - E[D]
        y = self.D - self.beta
        
        # Solve for M = K^{-1} y
        self.M = np.linalg.solve(K, y)
        
        return self.M

    def emulate(self, x):
        """
        Predicts the emulated value E_D[f(x)] using the precomputed M
        
        Parameters:
        x (array-like): New input point to emulate, shape (n_dimensions,)
        M (array-like, optional): Precomputed M matrix. If None, uses self.M
        """
        if self.M is None:
            raise ValueError("M has not been computed. Run compute_M first or provide M.")
    
        x = np.array(x)
        
        # Compute squared distances between x and each training point, ||x-x^(j)||^2
        sq_dists = np.sum((x-self.x_train)**2, axis=1)
        
        # Compute covariance vector k, Cov[f(x),D]_j = sigma^2 exp{-||x-x^(j)||^2/theta^2}
        k = (self.sigma ** 2) * np.exp(-sq_dists / (self.theta ** 2))
        
        # Calculate the emulated mean, E_D[f(x)] = E[f(x)] + Cov[f(x),D] Var[D]^-1(D - E[D])
        return self.beta + np.dot(k, self.M)
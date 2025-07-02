import numpy as np

class Scaler:
    """
    Static utility class for fixed-range scaling of 2D coordinate pairs.
    """

    x_min, x_max = -15000.0, 10000.0
    y_min, y_max = -8000.0, 8000.0

    @staticmethod
    def scale(x):
        """
        Scales either:
        - A list of shape (4,) => [x1, y1, x2, y2]
        - A list of shape (2,) => [x1, y1]
        - A list of points of shape (n_samples, 4)

        All coordinates are scaled to [0, 1] based on fixed grid bounds.
        Input values can be floats or Decimals.

        Returns:
            NumPy array of same shape as input.
        """
        x = np.asarray(x, dtype=np.float64)

        if x.ndim == 1:
            if x.shape[0] == 4:
                return np.array([
                    (x[0] - Scaler.x_min) / (Scaler.x_max - Scaler.x_min),
                    (x[1] - Scaler.y_min) / (Scaler.y_max - Scaler.y_min),
                    (x[2] - Scaler.x_min) / (Scaler.x_max - Scaler.x_min),
                    (x[3] - Scaler.y_min) / (Scaler.y_max - Scaler.y_min),
                ])
            elif x.shape[0] == 2:
                return np.array([
                    (x[0] - Scaler.x_min) / (Scaler.x_max - Scaler.x_min),
                    (x[1] - Scaler.y_min) / (Scaler.y_max - Scaler.y_min),
                ])
            else:
                raise ValueError("Expected a 4-element vector: [x1, y1, x2, y2] or 2-element vector: [x1, y1]")
                
        elif x.ndim == 2 and x.shape[1] == 4:
            x = x.astype(np.float64)
            scaled = np.empty_like(x)
            scaled[:, 0] = (x[:, 0] - Scaler.x_min) / (Scaler.x_max - Scaler.x_min)
            scaled[:, 1] = (x[:, 1] - Scaler.y_min) / (Scaler.y_max - Scaler.y_min)
            scaled[:, 2] = (x[:, 2] - Scaler.x_min) / (Scaler.x_max - Scaler.x_min)
            scaled[:, 3] = (x[:, 3] - Scaler.y_min) / (Scaler.y_max - Scaler.y_min)
            return scaled
        else:
            raise ValueError("Input must be shape (4,) or (n_samples, 4)")
        
    def scale_x(x):
        """
        Scales either:
        - A list of x points of shape (1, nsamples)

        All coordinates are scaled to [0, 1] based on fixed grid bounds.
        Input values can be floats or Decimals.

        Returns:
            NumPy array of same shape as input.
        """
        x = np.asarray(x, dtype=np.float64)

        if x.ndim == 1:
            scaled = np.empty_like(x)
            scaled[:] = (x[:] - Scaler.x_min) / (Scaler.x_max - Scaler.x_min)
            return scaled

        raise ValueError("Expected a list of x points of shape (1, nsamples)")
        
    def scale_y(y):
        """
        Scales either:
        - A list of y points of shape (1, nsamples)

        All coordinates are scaled to [0, 1] based on fixed grid bounds.
        Input values can be floats or Decimals.

        Returns:
            NumPy array of same shape as input.
        """
        y = np.asarray(y, dtype=np.float64)

        if y.ndim == 1:
            scaled = np.empty_like(y)
            scaled[:] = (y[:] - Scaler.y_min) / (Scaler.y_max - Scaler.y_min)
            return scaled

        raise ValueError("Expected a list of y points of shape (1, nsamples)")
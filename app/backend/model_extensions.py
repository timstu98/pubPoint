from decimal import Decimal
from models import BayesianModel, DElement, XTrainElement, MVectorElement, db

from decimal import Decimal

class BayesianModelExtensions:
    @staticmethod
    def insert_bayesian_model(name, m_vector, x_train, d_vector, beta, sigma, theta, commit=True):
        """
        Insert a BayesianModel into the database.
        
        Args:
            name (str): Name of the BayesianModel.
            m_vector (list of Decimal or float): The M vector.
            x_train (list of Decimal or float): The X_train vector.
            d_vector (list of Decimal or float): The D vector.
            beta (Decimal or float): The beta value.
            sigma (Decimal or float): The sigma value.
            theta (Decimal or float): The theta value.
            commit (bool): Whether to commit the transaction immediately.
        
        Returns:
            BayesianModel: The created BayesianModel object.
        """
        # Convert inputs to Decimal for precision
        m_vector = [Decimal(str(v)) for v in m_vector]
        x_train = [[Decimal(str(v)) for v in row] for row in x_train]
        d_vector = [Decimal(str(v)) for v in d_vector]
        beta = Decimal(str(beta))
        sigma = Decimal(str(sigma))
        theta = Decimal(str(theta))

        # Create the BayesianModel entry
        new_emulation = BayesianModel(
            name=name,
            m_length=len(m_vector),
            d_length=len(d_vector),
            beta=beta,
            sigma=sigma,
            theta=theta
        )
        db.session.add(new_emulation)

        if commit:
            db.session.commit()

        # Insert M vector elements
        for i, value in enumerate(m_vector):
            element = MVectorElement(bayesian_model_id=new_emulation.id, index=i, value=value)
            db.session.add(element)

        # Insert X_train elements
        for i, row in enumerate(x_train):
            for j, val in enumerate(row):
                db.session.add(XTrainElement(bayesian_model_id=new_emulation.id,row=i,col=j,value=val))

        # Insert D vector elements
        for i, value in enumerate(d_vector):
            element = DElement(bayesian_model_id=new_emulation.id, index=i, value=value)
            db.session.add(element)

        if commit:
            db.session.commit()

        return new_emulation

    @staticmethod
    def get_bayesian_model_by_name(name):
        """
        Retrieve a BayesianModel by its name.
        
        Args:
            name (str): Name of the BayesianModel.
            commit (bool): Whether to commit the transaction immediately.
        
        Returns:
            dict: A dictionary containing the BayesianModel data, or None if not found.
        """
        emulation = BayesianModel.query.filter_by(name=name).first()
        if not emulation:
            return None

        return emulation

    @staticmethod
    def update_bayesian_model(name, m_vector=None, x_train=None, d_vector=None, beta=None, sigma=None, theta=None, commit=True):
        """
        Update a BayesianModel in the database.
        
        Args:
            name (str): Name of the BayesianModel.
            m_vector (list of Decimal or float): The new M vector (optional).
            x_train (list of Decimal or float): The new X_train vector (optional).
            d_vector (list of Decimal or float): The new D vector (optional).
            beta (Decimal or float): The new beta value (optional).
            sigma (Decimal or float): The new sigma value (optional).
            theta (Decimal or float): The new theta value (optional).
            commit (bool): Whether to commit the transaction immediately.
        
        Returns:
            bool: True if the BayesianModel was updated, False if not found.
        """
        emulation = BayesianModel.query.filter_by(name=name).first()
        if not emulation:
            return False

        # Update scalar fields if provided
        if beta is not None:
            emulation.beta = Decimal(str(beta))
        if sigma is not None:
            emulation.sigma = Decimal(str(sigma))
        if theta is not None:
            emulation.theta = Decimal(str(theta))

        # Update M vector if provided
        if m_vector is not None:
            MVectorElement.query.filter_by(bayesian_model_id=emulation.id).delete()
            m_vector = [Decimal(str(v)) for v in m_vector]
            emulation.m_length = len(m_vector)
            for i, value in enumerate(m_vector):
                element = MVectorElement(bayesian_model_id=emulation.id, index=i, value=value)
                db.session.add(element)

        # Update X_train if provided
        if x_train is not None:
            XTrainElement.query.filter_by(bayesian_model_id=emulation.id).delete()
            x_train = [Decimal(str(v)) for v in x_train]
            for i, value in enumerate(x_train):
                element = XTrainElement(bayesian_model_id=emulation.id, index=i, value=value)
                db.session.add(element)

        # Update D vector if provided
        if d_vector is not None:
            DElement.query.filter_by(bayesian_model_id=emulation.id).delete()
            d_vector = [Decimal(str(v)) for v in d_vector]
            emulation.d_length = len(d_vector)
            for i, value in enumerate(d_vector):
                element = DElement(bayesian_model_id=emulation.id, index=i, value=value)
                db.session.add(element)

        if commit:
            db.session.commit()

        return True

    @staticmethod
    def delete_bayesian_model(name, commit=True):
        """
        Delete a BayesianModel from the database.
        
        Args:
            name (str): Name of the BayesianModel.
            commit (bool): Whether to commit the transaction immediately.
        
        Returns:
            bool: True if the BayesianModel was deleted, False if not found.
        """
        emulation = BayesianModel.query.filter_by(name=name).first()
        if not emulation:
            return False

        # Delete all associated elements
        MVectorElement.query.filter_by(bayesian_model_id=emulation.id).delete()
        XTrainElement.query.filter_by(bayesian_model_id=emulation.id).delete()
        DElement.query.filter_by(bayesian_model_id=emulation.id).delete()

        # Delete the BayesianModel entry
        db.session.delete(emulation)

        if commit:
            db.session.commit()

        return True
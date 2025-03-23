from decimal import Decimal
from models import db, Vector, VectorElement
import numpy as np

class VectorExtensions:
    @staticmethod
    def insert_vector(name, vector, commit=True):
        """
        Insert a vector into the database.
        
        Args:
            name (str): Name of the vector.
            vector (np.ndarray or list of float): The vector to store.
            commit (bool): Whether to commit the transaction immediately.
        
        Returns:
            Vector: The created Vector object.
        """
        if isinstance(vector, list):
            vector = [Decimal(str(v)) for v in vector]  # Convert to Decimal

        length = len(vector)
        new_vector = Vector(name=name, length=length)
        db.session.add(new_vector)

        if commit:
            db.session.commit()

        for i, value in enumerate(vector):
            element = VectorElement(vector_id=new_vector.id, index=i, value=value)
            db.session.add(element)
        
        if commit:
            db.session.commit()

        return new_vector

    @staticmethod
    def get_vector_by_name(name):
        """
        Retrieve a vector by its name.
        
        Args:
            name (str): Name of the vector.
            commit (bool): Whether to commit the transaction immediately.
        
        Returns:
            np.ndarray: The vector, or None if not found.
        """
        vector = Vector.query.filter_by(name=name).first()
        if not vector:
            return None

        elements = VectorElement.query.filter_by(vector_id=vector.id).order_by(VectorElement.index).all()
        vector_data = np.zeros(vector.length) 

        for element in elements:
            vector_data[element.index] = element.value

        return vector_data

    @staticmethod
    def update_vector(name, new_vector, commit=True):
        """
        Update a vector in the database.
        
        Args:
            name (str): Name of the vector.
            new_vector (np.ndarray or list of float): The new vector data.
            commit (bool): Whether to commit the transaction immediately.
        
        Returns:
            bool: True if the vector was updated, False if not found.
        """
        if isinstance(new_vector, list):
            vector = [Decimal(str(v)) for v in vector]  # Convert to Decimal

        vector = Vector.query.filter_by(name=name).first()
        if not vector:
            return False

        # Delete existing elements
        VectorElement.query.filter_by(vector_id=vector.id).delete()

        # Update vector length
        length = len(new_vector)
        vector.length = length

        # Insert new elements
        for i, value in enumerate(new_vector):
            element = VectorElement(vector_id=vector.id, index=i, value=value)
            db.session.add(element)
        
        if commit:
            db.session.commit()

        return True
    
    @staticmethod
    def delete_vector(name, commit=True):
        """
        Delete a vector from the database.
        
        Args:
            name (str): Name of the vector.
            commit (bool): Whether to commit the transaction immediately.
        
        Returns:
            bool: True if the vector was deleted, False if not found.
        """
        vector = Vector.query.filter_by(name=name).first()
        if not vector:
            return False

        # Delete all elements associated with the vector
        VectorElement.query.filter_by(vector_id=vector.id).delete()

        # Delete the vector entry
        db.session.delete(vector)

        if commit:
            db.session.commit()

        return True
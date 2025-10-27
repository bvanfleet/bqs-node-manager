import pickle
import os
import sys
from typing import Optional

from lib.rpc import bqs_lease_pb2


class LeaseSerializer:
    """Utility class for serializing and deserializing Lease objects."""

    @classmethod
    def serialize_lease(cls, lease: bqs_lease_pb2.Lease, filename: str):
        """
        Serialize a Lease object to a file.
        
        Args:
            lease (bqs_lease_pb2.Lease): The Lease object to serialize.
            filename (str): The path to the file where the lease will be saved.
        """
        sys.modules['bqs_lease_pb2'] = bqs_lease_pb2
        with open(filename, "wb") as f:
            pickle.dump(lease, f)

        del sys.modules['bqs_lease_pb2']


    @classmethod
    def deserialize_lease(cls, filename: str) -> Optional[bqs_lease_pb2.Lease]:
        """
        Deserialize a Lease object from a file.

        Args:
            filename (str): The path to the file from which the lease will be loaded.
        """
        sys.modules['bqs_lease_pb2'] = bqs_lease_pb2
        if not os.path.exists(filename):
            return None
        
        with open(filename, "rb") as f:
            return pickle.load(f)
        
        del sys.modules['bqs_lease_pb2']

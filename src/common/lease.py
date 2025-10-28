from datetime import datetime, timezone
from typing import Optional
from .model import Model


class Lease(Model):
    """
    Represents a lease for a radio node, including node identification, lease expiration, and callsign.

    Attributes:
        node_id (int): Unique identifier for the radio node.
        lease (int): Lease expiration time as a Unix timestamp.
        callsign (str): Callsign associated with the node.
    """

    node_id: int
    expiry: int
    callsign: str

    def __init__(self, node_id: int, expiry: int, callsign: str,
                 created_at: datetime, created_by: str,
                 updated_at: datetime, updated_by: str,
                 deleted_at: Optional[datetime], deleted_by: Optional[str]):
        """
        Initialize a Lease object.

        Args:
            node_id (int): The unique identifier for the node.
            expiry (int): The lease expiration or value associated with the node.
            callsign (str): The callsign or name associated with the node.
        """
        super().__init__(created_at, created_by,
                         updated_at, updated_by,
                         deleted_at, deleted_by)
        self.node_id = node_id
        self.expiry = expiry
        self.callsign = callsign


    def is_expired(self, threshold: int) -> bool:
        """
        Checks if the lease has expired based on the current time.

        Returns:
            bool: True if the lease has expired, False otherwise.
        """
        lim = datetime.now(tz=timezone.utc).timestamp() + threshold
        return self.expiry < lim


    def __eq__(self, other):
        if not isinstance(other, Lease):
            return False
        
        return self.node_id == other.node_id and self.callsign == other.callsign

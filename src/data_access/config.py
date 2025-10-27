from typing import Optional

class Config:
    db_name: str
    node_id_range_start: int
    node_id_range_end: Optional[int]

    def __init__(self, db_name: str, node_id_range_start: int, node_id_range_end: Optional[int] = None):
        """
        Initialize configuration for the repository.
        
        Args:
            db_name: Name of the database to connect to
            node_id_range_start: Start of node ID allocation range (inclusive)
            node_id_range_end: End of node ID allocation range (inclusive). Set to 0 to disable range allocation.
        """
        self.db_name = db_name
        self.node_id_range_start = node_id_range_start
        self.node_id_range_end = node_id_range_end

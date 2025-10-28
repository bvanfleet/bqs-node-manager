from datetime import datetime
from typing import Optional

class Model:
    """
    Base model class with common attributes for tracking creation, updates, and deletion.

    Attributes:
        created_at (datetime): Timestamp when the record was created.
        created_by (str): Identifier of the user who created the record.
        updated_at (datetime): Timestamp when the record was last updated.
        updated_by (str): Identifier of the user who last updated the record.
        deleted_at (datetime): Timestamp when the record was deleted.
        deleted_by (str): Identifier of the user who deleted the record.
    """

    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    deleted_at: Optional[datetime]
    deleted_by: Optional[str]

    def __init__(self, created_at: datetime, created_by: str,
                 updated_at: datetime, updated_by: str,
                 deleted_at: Optional[datetime], deleted_by: Optional[str]):
        """
        Initialize a Model object.
        """
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.deleted_at = deleted_at
        self.deleted_by = deleted_by
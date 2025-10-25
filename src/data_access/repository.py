import sqlite3 as sql

from ..common import lease as l
from .config import Config


class BaseRepository:
    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def _get_connection(self):
        return sql.connect(self._config.db_name)


class LeaseRepository(BaseRepository):
    table_name = "leases"

    def get_lease(self, node_id: int) -> l.Lease | None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE node_id = ? and is_active = 1", (node_id,))
            row = cursor.fetchone()

        return l.Lease(node_id=row[0], callsign=row[1], expiry=row[2], created_at=row[3], created_by=row[4],
                       updated_at=row[5], updated_by=row[6], deleted_at=row[7], deleted_by=row[8],
                       row_version=row[9], is_active=row[10]) if row else None
    

    def create_lease(self, node_id: int, callsign: str, expiry: int) -> l.Lease:
        if node_id == 0:
            # Generate next node_id from allocatable range or next in sequence
            node_id = self.__get_next_node_id()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.table_name} (node_id, callsign, expiry) "
                        f"VALUES (?, ?, ?)",
                        (node_id, callsign, expiry))
            conn.commit()

        lease = self.get_lease(node_id)
        if lease is None:
            raise Exception("Failed to create lease.")
        return lease


    def __get_next_node_id(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # If range end is 0, range allocation is disabled
            if self._config.node_id_range_end == 0 or self._config.node_id_range_end is None:
                # When range allocation is disabled, get max node_id + 1 or start at 1
                cursor.execute(f"""
                    SELECT COALESCE(MAX(node_id) + 1, 1)
                    FROM {self.table_name}
                    WHERE is_active = 1
                """)
                return cursor.fetchone()[0]
                
            # Find first available ID in range that isn't actively leased
            cursor.execute(f"""
                WITH RECURSIVE numbers(n) AS (
                    SELECT ?
                    UNION ALL
                    SELECT n + 1 FROM numbers 
                    WHERE n < ?
                )
                SELECT n FROM numbers 
                WHERE n NOT IN (
                    SELECT node_id 
                    FROM {self.table_name} 
                    WHERE is_active = 1
                )
                LIMIT 1
            """, (self._config.node_id_range_start, self._config.node_id_range_end))
            
            row = cursor.fetchone()
            if row:
                return row[0]
                
            raise ValueError(
                f"No available node IDs in configured range ({self._config.node_id_range_start}"
                f"-{self._config.node_id_range_end})"
            )

from datetime import datetime, timezone
import pytest

from bqs_node_manager.common.lease import Lease

class TestLease:

    @pytest.mark.parametrize("threshold, expected", [(100, True), (-100, False)])
    def test_lease_expiry(self, threshold: int, expected: bool):
        lease = TestLease.__create_lease(
            node_id=1,
            callsign="TEST",
        )

        assert lease.is_expired(threshold=threshold) is expected

    def test_lease_equality(self):
        lease1 = TestLease.__create_lease(
            node_id=1,
            callsign="TEST",
        )

        lease2 = TestLease.__create_lease(
            node_id=1,
            callsign="TEST",
        )

        assert lease1 == lease2


    def test_lease_inequality(self):
        lease1 = TestLease.__create_lease(
            node_id=1,
            callsign="TEST",
        )

        lease2 = TestLease.__create_lease(
            node_id=2,
            callsign="TEST-2",
        )

        assert lease1 != lease2


    @classmethod
    def __create_lease(cls, node_id: int, callsign: str) -> Lease:
        return Lease(
            node_id=id,
            callsign=callsign,
            expiry=datetime.now(tz=timezone.utc).timestamp(),
            created_at=datetime.now(tz=timezone.utc),
            created_by="tester",
            updated_at=datetime.now(tz=timezone.utc),
            updated_by="tester",
            deleted_at=None,
            deleted_by=None
        )

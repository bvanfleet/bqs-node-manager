from lib.rpc import Lease as RpcLease

from bqs_node_manager.common.lease import Lease as DataLease
from bqs_node_manager.mapper.lease_mapper import LeaseMapper

class TestLeaseMapper:
    def test_to_rpc(self):
        data_lease = DataLease(
            node_id=1, callsign="TEST", expiry=1625097600,
            created_at=None, created_by="",
            updated_at=None, updated_by="",
            deleted_at=None, deleted_by=None)
        rpc_lease = LeaseMapper.to_rpc(data_lease)

        assert rpc_lease.nodeId == 1
        assert rpc_lease.callsign == "TEST"
        assert rpc_lease.expiry == 1625097600

    def test_from_rpc(self):
        rpc_lease = RpcLease(nodeId=2, callsign="NODE2", expiry=1625184000)
        data_lease = LeaseMapper.from_rpc(rpc_lease)

        assert data_lease.node_id == 2
        assert data_lease.callsign == "NODE2"
        assert data_lease.expiry == 1625184000
        assert data_lease.created_at is not None
        assert data_lease.created_by == "system"
        assert data_lease.updated_at is not None
        assert data_lease.updated_by == "system"
        assert data_lease.deleted_at is None
        assert data_lease.deleted_by is None

from datetime import datetime, timezone

from lib.rpc import Lease as RpcLease

from ..common.lease import Lease as DataLease


class LeaseMapper:
    @classmethod
    def to_rpc(cls, data_lease: DataLease) -> RpcLease:
        return RpcLease(
            nodeId=data_lease.node_id,
            callsign=data_lease.callsign,
            expiry=data_lease.expiry
        )

    @classmethod
    def from_rpc(cls, rpc_lease: RpcLease) -> DataLease:
        return DataLease(
            node_id=rpc_lease.nodeId,
            callsign=rpc_lease.callsign,
            expiry=rpc_lease.expiry,
            created_at=datetime.now(timezone.utc),
            created_by="system",
            updated_at=datetime.now(timezone.utc),
            updated_by="system",
            deleted_at=None,
            deleted_by=None,
            is_active=True
        )
    
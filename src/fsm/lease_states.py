import grpc
import logging
from typing import Optional

from lib.rpc import LeaseRequest, NodeManagerStub

from ..common.lease import Lease
from ..mapper.lease_mapper import LeaseMapper
from . import States
from .state import State

class NewLeaseState(State):
    """
    State representing a new lease request. Requests a new lease if none exists; otherwise, transitions to Active or
    Expired state based on lease status.
    """
    def __init__(self):
        super().__init__(States.NEW)


    def process(self, lease: Optional[Lease], manager: NodeManagerStub, **config) -> State:
        logging.debug("Processing NewLeaseState")
        if lease is not None:
            threshold = config['node']['lease_renewal_threshold']
            return ExpiredLeaseState() if lease.is_expired(threshold) else ActiveLeaseState()

        try:
            callsign = config['node']['callsign']
            request = LeaseRequest(callsign=callsign)

            logging.info(f"Requesting lease for callsign: {callsign}")
            lease = LeaseMapper.from_rpc(manager.GetLease(request))
            logging.info(
                f"Obtained new lease: Node ID = {lease.node_id}, Callsign = {lease.callsign}, Expiration = {lease.expiry}")

            return ActiveLeaseState()
        except grpc.RpcError as e:
            logging.error(f"Error occurred while requesting lease: ({e.code()}) {e.details()}")
            return self


class ExpiredLeaseState(State):
    def __init__(self):
        super().__init__(States.EXPIRED)


    def process(self, lease: Optional[Lease], manager: NodeManagerStub, **config) -> State:
        logging.debug("Processing ExpiredLeaseState")
        if lease is None:
            return NewLeaseState()
        
        if not lease.is_expired(config['node']['lease_renewal_threshold']):
            return ActiveLeaseState()

        # Attempt to renew the lease
        # Success: active lease state
        # Failure: remain in expired state
        logging.info(
            f"Renewed lease: Node ID = {lease.node_id}, Callsign = {lease.callsign}, Expiration = {lease.expiry}")
        return self


class ActiveLeaseState(State):
    def __init__(self):
        super().__init__(States.ACTIVE)


    def process(self, lease: Optional[Lease], manager: NodeManagerStub, **config) -> State:
        logging.debug("Processing ActiveLeaseState")
        if lease is None:
            return NewLeaseState()

        if lease.is_expired(config['node']['lease_renewal_threshold']):
            return ExpiredLeaseState()
        
        return self

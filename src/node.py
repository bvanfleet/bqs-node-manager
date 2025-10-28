import logging
import time
from typing import Optional
import grpc

from lib.rpc import NodeManagerStub, LeaseRequest, Lease as RpcLease

from . import utilities as utils
from .fsm.lease_states import NewLeaseState
from .mapper.lease_mapper import LeaseMapper
from .serialization import LeaseSerializer


def process(callsign: str, manager: NodeManagerStub) -> Optional[RpcLease]:
    try:
        request = LeaseRequest(callsign=callsign)
        logging.info(f"Requesting lease for callsign: {callsign}")
        lease = manager.GetLease(request)
        return lease
    except grpc.RpcError as e:
        logging.error(f"Error occurred while requesting lease: ({e.code()}) {e.details()}")
        return None


def main():
    utils.register_interrupts()
    utils.initialize_logging()
    logging.info("Starting Node Manager client...")

    _, config = utils.initialize_config()
    lease_path = config['node'].get('lease_path', 'node.lease')

    state = NewLeaseState()
    lease = LeaseSerializer.deserialize_lease(lease_path)

    while True:
        with grpc.insecure_channel(f"{config['rpc']['host']}:{config['rpc']['port']}") as channel:
            manager = NodeManagerStub(channel)
            lease = LeaseMapper.from_rpc(lease) if lease else None
            state = state.process(lease, manager, **config)

            if lease:
                lease = LeaseMapper.to_rpc(lease)
                LeaseSerializer.serialize_lease(lease, lease_path)

        time.sleep(config['node']['lease_refresh_interval'])
        

if __name__ == "__main__":
    main()

from datetime import datetime, timezone
import logging
import time
from typing import Optional, TypeGuard
import grpc

from lib.rpc import NodeManagerStub, LeaseRequest, Lease

from . import utilities as utils
from .serialization import LeaseSerializer
    

def is_lease_valid(lease: Optional[Lease], threshold: int) -> TypeGuard[Lease]:
    if lease is None:
        return False
    
    lim = datetime.now(tz=timezone.utc).timestamp() + threshold
    return lease.expiry > lim


def process(callsign: str, manager: NodeManagerStub) -> Optional[Lease]:
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

    while True:
        lease = LeaseSerializer.deserialize_lease(lease_path)
        if not is_lease_valid(lease, config['node']['lease_renewal_threshold']):
            with grpc.insecure_channel(f"{config['rpc']['host']}:{config['rpc']['port']}") as channel:
                manager = NodeManagerStub(channel)
                lease = process(config['node']['callsign'], manager)

                if lease:
                    logging.info(f"Obtained lease: Node ID = {lease.nodeId}, Callsign = {lease.callsign}, Expiration = {lease.expiry}")
                    LeaseSerializer.serialize_lease(lease, lease_path)
                else:
                    logging.error("Failed to obtain lease.")
        else:
            logging.debug(f"Existing valid lease found: Node ID = {lease.nodeId}, Callsign = {lease.callsign}, Expiration = {lease.expiry}")

        time.sleep(config['node']['lease_refresh_interval'])
        

if __name__ == "__main__":
    main()

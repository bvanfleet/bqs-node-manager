import logging
import grpc

from lib.rpc import NodeManagerStub, LeaseRequest, Lease

from . import utilities as utils


def process(callsign: str, manager: NodeManagerStub) -> Lease | None:
    try:
        request = LeaseRequest(callsign=callsign)
        logging.info(f"Requesting lease for callsign: {callsign}")
        lease = manager.GetLease(request)
        return lease
    except grpc.RpcError as e:
        logging.error(f"Error occurred while requesting lease: ({e.code()}) {e.details()}")
        return None

def main():
    utils.initialize_logging()
    logging.info("Starting Node Manager client...")

    _, config = utils.initialize_config()
    
    with grpc.insecure_channel(f"{config['rpc']['host']}:{config['rpc']['port']}") as channel:
        manager = NodeManagerStub(channel)

        lease = process(config['node']['callsign'], manager)

        if lease:
            logging.info(f"Obtained lease: Node ID = {lease.nodeId}, Callsign = {lease.callsign}, Expiration = {lease.expiry}")
        

if __name__ == "__main__":
    main()

from concurrent import futures
import grpc
import logging

from lib.rpc import LeaseRequest, Lease, NodeManagerServicer, add_NodeManagerServicer_to_server

from . import utilities as utils
from .common import lease as l
from .mapper.lease_mapper import LeaseMapper
from .data_access.repository import LeaseRepository


class NodeManager(NodeManagerServicer):

    __repository: LeaseRepository

    def __init__(self, repository: LeaseRepository):
        self.__repository = repository

    def GetLease(self, request: LeaseRequest, context) -> Lease:
        logging.info(f"Received lease request for callsign: {request.callsign} with node ID: {request.nodeId}")
        # Check if lease exists and return it
        lease = self.__repository.get_lease(request.nodeId)
        if lease is not None:
            return LeaseMapper.to_rpc(lease)
        
        # Create a new lease if it does not exist
        logging.info(f"Requesting new lease for callsign: {request.callsign} with node ID: {request.nodeId}")
        lease = self.__repository.create_lease(request.nodeId, request.callsign, 0)
        return LeaseMapper.to_rpc(lease)

    def RenewLease(self, request: LeaseRequest, context) -> Lease:
        raise NotImplementedError("RenewLease is not implemented.")

    def ReleaseLease(self, request: Lease, context) -> Lease:
        raise NotImplementedError("ReleaseLease is not implemented.")


def serve(config, manager: NodeManager):
    logging.info("Initializing Node Manager gRPC server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_NodeManagerServicer_to_server(manager, server)

    address = f"[::]:{config['rpc']['port']}"
    server.add_insecure_port(address)

    logging.info(f"Starting Node Manager gRPC server on {address}")
    server.start()
    server.wait_for_termination()


def main():
    utils.initialize_logging()

    logging.info("Starting Node Manager...")
    dbConfig, config = utils.initialize_config()
    repo = LeaseRepository(dbConfig)
    manager = NodeManager(repo)

    try:
        serve(config, manager)
    except KeyboardInterrupt:
        logging.debug("Shutting down Node Manager.")


if __name__ == "__main__":
    main()

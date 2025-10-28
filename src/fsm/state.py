from abc import ABCMeta, abstractmethod
from typing import Optional

from lib.rpc import NodeManagerStub

from ..common.lease import Lease
from . import States

class State(metaclass=ABCMeta):
    """
    Abstract base class for FSM states.
    
    Attributes:
        name (States): The name of the state.
    """
    name: States

    def __init__(self, name: States):
        """
        Initialize the state with a given name.
        
        Args:
            name (States): The name of the state.
        """
        self.name = name

    @abstractmethod
    def process(self, lease: Optional[Lease], manager: NodeManagerStub, **config) -> State:
        """
        Process the current state with the given lease and manager.
        
        Args:
            lease (Optional[Lease]): The current lease, if any.
            manager (NodeManagerStub): The gRPC stub for the Node Manager.
            **config: Additional configuration parameters.
        
        Returns:
            State: The next state after processing.
        """
        raise NotImplementedError("Subclasses must implement this method")

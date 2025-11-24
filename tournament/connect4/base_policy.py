"""Base Policy class for Connect 4 agents"""

class Policy:
    """Base class for Connect 4 policies/agents"""
    
    def mount(self, timeout=None):
        """Initialize the policy with optional timeout"""
        pass
    
    def act(self, state):
        """Choose an action given a state"""
        raise NotImplementedError("Subclasses must implement act method")
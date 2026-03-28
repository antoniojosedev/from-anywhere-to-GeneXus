"""Abstract base class for AI providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseProvider(ABC):
    """Abstract base class for all AI provider implementations."""

    @abstractmethod
    def generate_spec(self, file_name: str, program: str) -> Dict[str, Any]:
        """
        Generate a specification from source code.
        
        Args:
            file_name: Name of the source file
            program: Source code content
            
        Returns:
            Dictionary with spec data containing:
                - 'name': Procedure name
                - 'spec': YAML-formatted specification
                - 'file_name': Original file name
        """
        pass

    @abstractmethod
    def generate_procedure(self, name: str, spec: str) -> Dict[str, Any]:
        """
        Generate GeneXus procedure from specification.
        
        Args:
            name: Procedure name
            spec: Specification as string
            
        Returns:
            Dictionary with procedure data containing:
                - 'name': Procedure name
                - 'Parts': Dict with Source code and other parts
                - 'description': Spec description
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

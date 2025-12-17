"""
Project model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Project:
    """Project model"""
    id: int
    code: str
    name: str
    client_id: int
    client_name: str
    description: Optional[str] = None
    status: str = 'pending'  # pending, active, completed, on_hold
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'client_id': self.client_id,
            'client_name': self.client_name,
            'description': self.description,
            'status': self.status,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'estimated_cost': self.estimated_cost,
            'actual_cost': self.actual_cost,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


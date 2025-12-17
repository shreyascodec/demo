"""
Estimation model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Estimation:
    """Estimation model"""
    id: int
    rfq_id: int
    customer_id: int
    customer_name: str
    product: str
    test_types: List[str] = field(default_factory=list)
    total_cost: float = 0.0
    status: str = 'draft'  # draft, sent, approved, rejected
    created_at: datetime = field(default_factory=datetime.now)
    valid_until: Optional[datetime] = None
    notes: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'rfq_id': self.rfq_id,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'product': self.product,
            'test_types': self.test_types,
            'total_cost': self.total_cost,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'valid_until': self.valid_until.strftime('%Y-%m-%d') if self.valid_until else None,
            'notes': self.notes,
        }


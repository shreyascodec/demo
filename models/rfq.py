"""
RFQ (Request for Quotation) model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class RFQ:
    """RFQ model"""
    id: int
    customer_id: int
    customer_name: str
    product: str
    description: Optional[str] = None
    received_date: datetime = field(default_factory=datetime.now)
    status: str = 'pending'  # pending, approved, rejected
    notes: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'product': self.product,
            'description': self.description,
            'received_date': self.received_date.strftime('%Y-%m-%d'),
            'status': self.status,
            'notes': self.notes,
        }


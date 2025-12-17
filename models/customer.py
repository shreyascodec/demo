"""
Customer model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    """Customer/Client model"""
    id: int
    company_name: str
    email: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    gst_number: Optional[str] = None
    status: str = 'active'
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'company_name': self.company_name,
            'email': self.email,
            'contact_person': self.contact_person,
            'phone': self.phone,
            'address': self.address,
            'gst_number': self.gst_number,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


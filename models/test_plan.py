"""
Test Plan model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class TestPlan:
    """Test Plan model"""
    id: int
    project_id: int
    project_name: str
    name: str
    description: Optional[str] = None
    test_type: str = 'EMC'  # EMC, RF, Safety, Environmental
    status: str = 'Draft'  # Draft, InProgress, Completed, Approved
    assigned_engineer_id: Optional[int] = None
    assigned_engineer_name: Optional[str] = None
    planned_start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'project_name': self.project_name,
            'name': self.name,
            'description': self.description,
            'test_type': self.test_type,
            'status': self.status,
            'assigned_engineer_id': self.assigned_engineer_id,
            'assigned_engineer_name': self.assigned_engineer_name,
            'planned_start_date': self.planned_start_date.strftime('%Y-%m-%d') if self.planned_start_date else None,
            'planned_end_date': self.planned_end_date.strftime('%Y-%m-%d') if self.planned_end_date else None,
            'actual_start_date': self.actual_start_date.strftime('%Y-%m-%d') if self.actual_start_date else None,
            'actual_end_date': self.actual_end_date.strftime('%Y-%m-%d') if self.actual_end_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


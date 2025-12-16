from extensions import db

# Event Table

class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    allocations = db.relationship(
        'EventResourceAllocation',
        back_populates='event',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Event {self.title}>"

# Resource Table

class Resource(db.Model):
    __tablename__ = 'resources'

    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)

    allocations = db.relationship(
        'EventResourceAllocation',
        back_populates='resource',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Resource {self.resource_name}>"

#Junction Table: EventResourceAllocation
class EventResourceAllocation(db.Model):
    __tablename__ = 'event_resource_allocations'

    allocation_id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.event_id'),
        nullable=False
    )

    resource_id = db.Column(
        db.Integer,
        db.ForeignKey('resources.resource_id'),
        nullable=False
    )

    event = db.relationship('Event', back_populates='allocations')
    resource = db.relationship('Resource', back_populates='allocations')

    def __repr__(self):
        return f"<Allocation Event:{self.event_id} Resource:{self.resource_id}>"

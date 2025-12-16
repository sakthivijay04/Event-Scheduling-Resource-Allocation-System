from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

from extensions import db
from models import Event, Resource, EventResourceAllocation

app = Flask(__name__)
app.secret_key = "secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_scheduler.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    return redirect(url_for('view_events'))

#HELPER FUNCTIONS

def has_time_overlap(existing_start, existing_end, new_start, new_end):
    return (existing_start < new_end) and (new_start < existing_end)


def resource_has_conflict(resource_id, selected_event):
    existing_allocations = EventResourceAllocation.query.filter_by(
        resource_id=resource_id
    ).all()

    for allocation in existing_allocations:
        existing_event = Event.query.get(allocation.event_id)

        if has_time_overlap(
            existing_event.start_time,
            existing_event.end_time,
            selected_event.start_time,
            selected_event.end_time
        ):
            return True

    return False

#EVENT ROUTES

@app.route('/events')
def view_events():
    events = Event.query.all()
    return render_template('view_events.html', events=events)


@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        start_time = datetime.fromisoformat(request.form['start_time'])
        end_time = datetime.fromisoformat(request.form['end_time'])
        description = request.form['description']

        # Business rule: an event must start before it ends
        if start_time >= end_time:
            flash("Start time must be before end time")
            return redirect(url_for('add_event'))

        event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description
        )

        db.session.add(event)
        db.session.commit()
        return redirect(url_for('view_events'))

    return render_template('add_event.html')

#RESOURCE ROUTES

@app.route('/resources')
def view_resources():
    resources = Resource.query.all()
    return render_template('view_resources.html', resources=resources)


@app.route('/add-resource', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        resource = Resource(
            resource_name=request.form['resource_name'],
            resource_type=request.form['resource_type']
        )

        db.session.add(resource)
        db.session.commit()
        return redirect(url_for('view_resources'))

    return render_template('add_resource.html')

#RESOURCE ALLOCATION

@app.route('/allocate-resources', methods=['GET', 'POST'])
def allocate_resources():
    events = Event.query.all()
    resources = Resource.query.all()

    if request.method == 'POST':
        event_id = int(request.form['event_id'])
        selected_event = Event.query.get(event_id)
        selected_resource_ids = request.form.getlist('resource_ids')

        for resource_id in map(int, selected_resource_ids):
            resource = Resource.query.get(resource_id)

            # Conflict check extracted into helper function
            if resource_has_conflict(resource_id, selected_event):
                flash(
                    f"Resource '{resource.resource_name}' "
                    f"is already allocated during this time."
                )
                return redirect(url_for('allocate_resources'))

            allocation = EventResourceAllocation(
                event_id=event_id,
                resource_id=resource_id
            )
            db.session.add(allocation)

        db.session.commit()
        return redirect(url_for('view_events'))

    return render_template(
        'allocate_resources.html',
        events=events,
        resources=resources
    )

#RESOURCE UTILISATION REPORT

@app.route('/resource-utilization', methods=['GET', 'POST'])
def resource_utilization():
    report = []

    if request.method == 'POST':
        start_date = datetime.fromisoformat(request.form['start_date'])
        end_date = datetime.fromisoformat(request.form['end_date'])

        for resource in Resource.query.all():
            total_hours = 0
            upcoming_events = []

            allocations = EventResourceAllocation.query.filter_by(
                resource_id=resource.resource_id
            ).all()

            for allocation in allocations:
                event = Event.query.get(allocation.event_id)

                # Count only overlapping portion
                overlap_start = max(event.start_time, start_date)
                overlap_end = min(event.end_time, end_date)

                if overlap_start < overlap_end:
                    duration = overlap_end - overlap_start
                    total_hours += duration.total_seconds() / 3600

                if event.start_time > end_date:
                    upcoming_events.append(event)

            report.append({
                'resource_name': resource.resource_name,
                'total_hours': round(total_hours, 2),
                'upcoming_events': upcoming_events
            })

    return render_template('resource_utilization.html', report=report)

#App Runner
if __name__ == '__main__':
    app.run(debug=True)

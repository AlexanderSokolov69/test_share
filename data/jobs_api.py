import datetime

import flask
from flask import jsonify, request, make_response

from .db_init import db
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = db.session.query(Jobs).all()
    return jsonify({"jobs": [item.to_dict(only=("id", "job", "team_leader", "work_size",
                                                "collaborators", "start_date", "end_date",
                                                "is_finished")) for item in jobs]})

@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job_by_id(job_id):
    job = db.session.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({"error": f"Job {job_id} not found"})
    return jsonify(job.to_dict(only=("id", "job", "team_leader", "work_size",
                                    "collaborators", "start_date", "end_date",
                                    "is_finished")))

@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ["job", "team_leader", "work_size",
                  "collaborators", "start_date", "end_date", "is_finished"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    try:
        job = Jobs(
            job = request.json["job"],
            team_leader = request.json["team_leader"],
            work_size = request.json["work_size"],
            collaborators = request.json["collaborators"],
            start_date = datetime.date.fromisoformat(request.json["start_date"]),
            end_date = datetime.date.fromisoformat(request.json["end_date"]) if request.json["end_date"] else None,
            is_finished = request.json["is_finished"]
        )
        db.session.add(job)
        db.session.commit()
        return jsonify({'id': job.id})
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)

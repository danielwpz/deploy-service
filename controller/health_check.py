from flask import jsonify
import json


def health_check_factory(nomad_client):
    def health_check():
        try:
            nomad_client.jobs.get_jobs()

            result = {"health": "ok"}
            return jsonify(result)
        except Exception as e:
            print(str(e))
            result = {"health": "failed", "reason": "Failed to connect to nomad"}
            return json.dumps(result), 500, {"ContentType": "application/json"}

    return health_check

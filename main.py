import nomad
import boto3
import _thread
import json
from flask import Flask
from concurrent.futures import ThreadPoolExecutor

from controller.health_check import health_check_factory
from config import default

nomad_addr = "localhost"
app = Flask("Deploy Service")
sqs = boto3.client('sqs', 'us-east-1')

n = nomad.Nomad(host=nomad_addr, timeout=5)


def deploy_task(message):
    body = json.loads(message['Body'])
    task_action = body['action']

    if task_action == 'deploy':
        task_json = body['definition']
        task_name = task_json['Job']['ID']

        print(task_name, task_json)

        try:
            print('Submitting job: %s' % task_name)
            n.job.register_job(task_name, task_json)
            print('Submitted job: %s' % task_name)

            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(QueueUrl=default.DEPLOY_QUEUE_URL, ReceiptHandle=receipt_handle)
            print('Message deleted: %s' % task_name)
        except Exception as e:
            print('Failed to submit job %s' % task_name)
            print(e)
    else:
        print('Unknown task message')
        print(message['Body'])


def handle_deploy_queue():
    print('Start receiving queue messages ...')
    executor = ThreadPoolExecutor()
    while True:
        try:
            message = sqs.receive_message(QueueUrl=default.DEPLOY_QUEUE_URL)
            if 'Messages' in message:
                print('Got %d messages' % len(message['Messages']))
                for m in message['Messages']:
                    executor.submit(deploy_task, m)
            else:
                print('No message now, try again...')
        except Exception as err:
            print('Error receiving queue message')
            print(err)


# Flask health check endpoint
@app.route('/status/health')
def get_health():
    health_check_controller = health_check_factory(n)
    return health_check_controller()


def run():
    app.run(host='0.0.0.0', port=5400)


if __name__ == "__main__":
    _thread.start_new_thread(run, ())
    handle_deploy_queue()

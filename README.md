# deploy-service
A service that handles deployment of nomad jobs.

# Run locally
*You'll need a pair of AWS credentials that has access to your SQS deploy queue, and set them in environment variables*
- In another terminal window `nomad agent -dev`
- `pip3 install -r requirements.txt`
- `python3 -u main.py`

# How
This services keeps fetching messages from a AWS SQS queue for new deployment message.       
The message should be in the JSON form: `{ "action": "deploy", "definition": NOMAD_JSON_DEFINITION }` 
(you can get the `NOMAD_JSON_DEFINITION` by running `nomad run -output job.hcl`)       
Once a message is received, it will try to submit the job to local nomad cluster and delete the message from SQS.

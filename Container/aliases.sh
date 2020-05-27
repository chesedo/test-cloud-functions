# Local debugging
alias devel="start --debug"

# Deploy tasks
alias deploy="gcloud functions deploy $FUNCTION-test --trigger-resource eta-testing-bucket --trigger-event google.storage.object.finalize --memory 128MB --set-env-vars SENDGRID_API_KEY=$SENDGRID_API_KEY --max-instances 1 --region europe-west1 --entry-point $FUNCTION"
alias deploy_py37="deploy --runtime python37"
alias deploy_clean="gcloud functions delete $FUNCTION-test --region europe-west1"
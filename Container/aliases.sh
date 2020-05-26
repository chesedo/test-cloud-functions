# Development commands
alias test="pytest --doctest-modules --doctest-continue-on-failure --ignore=main.py --cov $FUNCTION"
alias lint_flake8="flake8"
alias lint_mypy="mypy ."
alias lint="lint_flake8 && lint_mypy"
alias format="black --line-length 119 ."

# Local debugging
alias start="functions-framework --target $FUNCTION --signature-type event"
alias devel="start --debug"

# Deploy tasks
alias deploy="gcloud functions deploy $FUNCTION-test --trigger-resource eta-testing-bucket --trigger-event google.storage.object.finalize --memory 128MB --set-env-vars SENDGRID_API_KEY=$SENDGRID_API_KEY --max-instances 1 --region europe-west1 --entry-point $FUNCTION"
alias deploy_py37="deploy --runtime python37"
alias deploy_clean="gcloud functions delete $FUNCTION-test --region europe-west1"
resource "google_cloudfunctions_function" "emailer" {
  name    = "py_emailer"
  runtime = "python37"

  available_memory_mb = 128
  entry_point         = "emailer"
  environment_variables = {
    "SENDGRID_API_KEY" = var.sendgrid.api_key
  }
  max_instances = 1
  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = google_storage_bucket.testing.name
  }
  source_repository {
    url = "https://source.developers.google.com/${google_sourcerepo_repository.test-cloud-functions.id}/moveable-aliases/master/paths/emailer/src/emailer/main.py"
  }
}

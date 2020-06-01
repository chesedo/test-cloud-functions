resource "google_project_iam_member" "cloudbuild-cloudfunctions-developer" {
  project = data.google_client_config.current.project
  role    = "roles/cloudfunctions.developer"
  member  = "serviceAccount:318987351169@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_member" "cloudbuild-secretManager-secretAccessor" {
  project = data.google_client_config.current.project
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:318987351169@cloudbuild.gserviceaccount.com"
}

resource "google_cloudbuild_trigger" "gcf-emailer-image" {
  provider    = google-beta

  description = "Rebuild GCF emailer image when needed"
  filename    = "cloudbuild.image.yaml"

  github {
    name  = "test-cloud-functions"
    owner = "pengelbrecht2627"

    push {
      tag = "^emailer\\.image\\..*"
    }
  }

  substitutions = {
    _FUNCTION = "emailer"
  }
}

resource "google_cloudbuild_trigger" "gcf-emailer-deploy" {
  provider    = google-beta

  description = "Deploy emailer GCF"
  filename    = "cloudbuild.deploy.yaml"

  github {
    name  = "test-cloud-functions"
    owner = "pengelbrecht2627"

    push {
      tag = "^emailer\\.deploy\\..*"
    }
  }

  substitutions = {
    _FUNCTION       = "emailer"
    _PYTHON_RUNTIME = "python37"
    _BUCKET         = "eta-testing-bucket"
    _MAX_INSTANCES  = 3
  }
}

resource "google_cloudbuild_trigger" "gcf-emailer-test" {
  provider    = google-beta

  description = "Auto test branches that made edits to the emailer GCF"
  filename    = "cloudbuild.test.yaml"
  included_files = [ "emailer/**" ]

  github {
    name  = "test-cloud-functions"
    owner = "pengelbrecht2627"

    pull_request {
      branch = ".*"
    }
  }

  substitutions = {
    _FUNCTION       = "emailer"
    _PYTHON_RUNTIME = "python37"
    _TEST_BUCKET    = "eta-testing-bucket"
  }
}

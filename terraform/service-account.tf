resource "google_service_account" "azure" {
  account_id   = "azure-1000"
  display_name = "Azure Pipeline testing"
}

resource "google_service_account" "appspot" {
  account_id = "eta-testing-239509"
  display_name = "App Engine default service account"
}

resource "google_project_iam_member" "azure-storage-objectAdmin" {
  project = "eta-testing-239509"
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.azure.email}"
}

resource "google_project_iam_member" "azure-cloudfunctions-developer" {
  project = "eta-testing-239509"
  role    = "roles/cloudfunctions.developer"
  member  = "serviceAccount:${google_service_account.azure.email}"
}

resource "google_service_account_iam_member" "azure-appspot-iam" {
  service_account_id = google_service_account.appspot.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.azure.email}"
}
resource "google_storage_bucket" "testing" {
  name          = "eta-testing-bucket"
  location      = var.gcp.region
  storage_class = "REGIONAL"
}

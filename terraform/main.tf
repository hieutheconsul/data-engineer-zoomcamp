terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.23.0"
    }
  }
}

provider "google" {
  credentials = "./keys/my-creds.json" #most important one
  project     = "laughwbari-sandbox"
  region      = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "laughwbari-sandbox-terra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }
}


resource "google_bigquery_dataset" "terraform-demo-dataset" {
  dataset_id    = "laughwbari_terra_dataset"
  friendly_name = "test"
  description   = "This is a test description"
}
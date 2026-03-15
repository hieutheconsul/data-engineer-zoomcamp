#This variable page to set default and use in main.tf

variable "location" {
  description = "Project Location"
  default = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default = "laughwbari_terra_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default = "laughwbari-sandbox-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default = "STANDARD"
}
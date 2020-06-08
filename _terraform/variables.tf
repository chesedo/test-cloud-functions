variable "gcp" {
  type = object({
    region = string
  })
}

variable "sendgrid" {
  type = object({
    api_key = string
  })
}

variable "network_name" {
  description = "Docker network name"
  type        = string
}

variable "db_user" {
  description = "PostgreSQL user"
  type        = string
}

variable "db_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
}

variable "db_port" {
  description = "PostgreSQL port"
  type        = number
  default     = 5432
}

variable "api_port" {
  description = "API port"
  type        = number
  default     = 8000
}

variable "dashboard_port" {
  description = "Dashboard port"
  type        = number
  default     = 5001
}

variable "image_tag" {
  description = "Docker image tag for the app services"
  type        = string
  default     = "8"
}

variable "db_user" {
  description = "PostgreSQL username"
  type        = string
  default     = "socuser"
}

variable "db_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "soc_db"
}

variable "db_port" {
  description = "PostgreSQL external port"
  type        = number
  default     = 5432
}

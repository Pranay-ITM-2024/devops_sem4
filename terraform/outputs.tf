output "network_name" {
  value = module.network.network_name
}

output "database_port" {
  value = var.db_port
}

output "api_port" {
  value = var.api_port
}

output "dashboard_port" {
  value = var.dashboard_port
}

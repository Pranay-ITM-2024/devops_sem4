output "database_host" {
  value = docker_container.postgres.name
}

output "database_port" {
  value = var.db_port
}

output "network_name" {
  value = docker_network.soc_network.name
}

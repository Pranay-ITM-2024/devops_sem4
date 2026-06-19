output "network_name" {
  description = "The name of the created Docker network"
  value       = docker_network.soc_network.name
}

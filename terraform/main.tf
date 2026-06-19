terraform {
  required_version = ">= 1.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# Pull PostgreSQL image
resource "docker_image" "postgres" {
  name         = "postgres:15-alpine"
  keep_locally = true
}

# Create Docker network
resource "docker_network" "soc_network" {
  name = "soc-network"
}

# Run PostgreSQL container
resource "docker_container" "postgres" {
  name  = "soc-postgres"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_USER=${var.db_user}",
    "POSTGRES_PASSWORD=${var.db_password}",
    "POSTGRES_DB=${var.db_name}"
  ]

  ports {
    internal = 5432
    external = var.db_port
  }

  networks_advanced {
    name = docker_network.soc_network.name
  }

  volumes {
    volume_name    = docker_volume.pgdata.name
    container_path = "/var/lib/postgresql/data"
  }
}

resource "docker_volume" "pgdata" {
  name = "soc-pgdata"
}

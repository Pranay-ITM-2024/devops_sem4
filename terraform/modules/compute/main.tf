terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# --- Database ---
resource "docker_image" "postgres" {
  name         = "postgres:15-alpine"
  keep_locally = true
}

resource "docker_volume" "pgdata" {
  name = "soc-pgdata-tf"
}

resource "docker_container" "postgres" {
  name  = "soc-postgres-tf"
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
    name = var.network_name
  }

  volumes {
    volume_name    = docker_volume.pgdata.name
    container_path = "/var/lib/postgresql/data"
  }
}

# --- API ---
resource "docker_image" "api" {
  name         = "yourusername/soc-api:${var.image_tag}"
  keep_locally = true
}

resource "docker_container" "api" {
  name  = "soc-api-tf"
  image = docker_image.api.image_id

  env = [
    "DATABASE_URL=postgresql://${var.db_user}:${var.db_password}@soc-postgres-tf:5432/${var.db_name}"
  ]

  ports {
    internal = 8000
    external = var.api_port
  }

  networks_advanced {
    name = var.network_name
  }

  depends_on = [docker_container.postgres]
}

# --- Dashboard ---
resource "docker_image" "dashboard" {
  name         = "yourusername/soc-dashboard:${var.image_tag}"
  keep_locally = true
}

resource "docker_container" "dashboard" {
  name  = "soc-dashboard-tf"
  image = docker_image.dashboard.image_id

  env = [
    "API_URL=http://soc-api-tf:8000",
    "FLASK_SECRET=dev-secret-key-change-me"
  ]

  ports {
    internal = 5000
    external = var.dashboard_port
  }

  networks_advanced {
    name = var.network_name
  }

  depends_on = [docker_container.api]
}

# --- Simulator ---
resource "docker_image" "simulator" {
  name         = "yourusername/soc-simulator:${var.image_tag}"
  keep_locally = true
}

resource "docker_container" "simulator" {
  name  = "soc-simulator-tf"
  image = docker_image.simulator.image_id

  env = [
    "API_URL=http://soc-api-tf:8000",
    "INTERVAL_SECONDS=30"
  ]

  networks_advanced {
    name = var.network_name
  }

  depends_on = [docker_container.api]
}

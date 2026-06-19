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

module "network" {
  source = "./modules/network"
}

module "compute" {
  source = "./modules/compute"

  network_name   = module.network.network_name
  db_user        = var.db_user
  db_password    = var.db_password
  db_name        = var.db_name
  db_port        = var.db_port
  api_port       = var.api_port
  dashboard_port = var.dashboard_port
  image_tag      = var.image_tag
}

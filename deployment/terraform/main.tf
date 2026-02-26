# OncoAgent Platform - Terraform per spec §8 infrastructure
# Configurable for EKS (AWS), GKE (GCP), AKS (Azure), or on-premise
# EU-region deployment required per GDPR data residency

terraform {
  required_version = ">= 1.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.25"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12"
    }
  }
  # backend "s3" {
  #   bucket = "oncoagent-terraform-state"
  #   key    = "production/terraform.tfstate"
  #   region = "eu-west-1"
  # }
}

variable "environment" {
  description = "Deployment environment (dev, staging, production)"
  type        = string
  default     = "dev"
}

variable "kubernetes_namespace" {
  type    = string
  default = "oncoagent"
}

# Namespace per spec: isolated for clinical, research, admin
resource "kubernetes_namespace" "oncoagent" {
  metadata {
    name = var.kubernetes_namespace
    labels = {
      app         = "oncoagent"
      environment = var.environment
    }
  }
}

# Deploy via Helm chart
resource "helm_release" "oncoagent" {
  name       = "oncoagent"
  chart      = "${path.module}/../helm/oncoagent"
  namespace  = kubernetes_namespace.oncoagent.metadata[0].name
  depends_on = [kubernetes_namespace.oncoagent]

  set {
    name  = "replicaCount"
    value = var.environment == "production" ? "3" : "1"
  }
}

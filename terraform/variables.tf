variable "aws_region" {
  description = "Região AWS onde a infraestrutura será criada"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "registro-despesas"
}

variable "image_tag" {
  description = "Tag da imagem Docker utilizada pelo ECS"
  type        = string
  default     = "latest"
}

variable "db_password" {
  description = "Senha do banco PostgreSQL"
  type        = string
  sensitive   = true
}

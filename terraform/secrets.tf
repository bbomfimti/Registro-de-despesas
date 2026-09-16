resource "aws_secretsmanager_secret" "db" {

  name = "${var.project_name}/database"

  recovery_window_in_days = 0

  tags = {

    Name = "${var.project_name}-database-secret"

    Project = var.project_name

  }

}

resource "aws_secretsmanager_secret_version" "db" {

  secret_id = aws_secretsmanager_secret.db.id

  secret_string = jsonencode({

    username = "registro_user"

    password = var.db_password

    dbname = "registro_despesas"

    host = aws_db_instance.main.address

    port = 5432

  })

}
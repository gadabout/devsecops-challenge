resource "aws_db_subnet_group" "bookings" {
  name       = "bookings-${var.environment}"
  subnet_ids = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

resource "aws_db_instance" "bookings" {
  identifier     = "bookings-${var.environment}"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class

  allocated_storage = 50
  storage_encrypted = false

  db_name  = "bookings"
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.bookings.name
  vpc_security_group_ids = [aws_security_group.database.id]
  publicly_accessible    = true

  backup_retention_period = 0
  skip_final_snapshot     = true
  deletion_protection     = false
}

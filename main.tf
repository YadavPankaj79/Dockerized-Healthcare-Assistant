resource "aws_instance" "healthcare_instance" {
  ami           = "ami-0f5ee92e2d63afc18"
  instance_type = "t3.micro"

  tags = {
    Name = "Healthcare-Terraform-Instance"
  }
}
say_hello:
	@echo "Hello, world!"

init:
	terraform init

plan:
	terraform validate
	terraform fmt
	terraform plan -out=tfplan

apply:
	@terraform validate
	@terraform fmt
	@terraform plan -out=tfplan
	terraform apply "tfplan"

destroy:
	terraform destroy

retry:
	make destroy
	make apply



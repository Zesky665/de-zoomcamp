## Week 1: Docker and Containerzation

#### Prerequisites

Make sure you have docker installed on your machine.

You can download it [here](https://www.docker.com/products/docker-desktop/).

## How to run the example

##### Generating the key pair
Let's start by opening the terminal, then navigate to the directory where the ssh keys are stored.

```Shell
cd ~/.ssh
```

Once in the ssh directory we can generate the keys, let's start by generating the private key using openssl.

```Shell
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out snowflake_tf_snow_key.p8 -nocrypt
```

What this command is doing is generating a 2048 bit private key, converting it to PKCS#8 (industry standard) format, saving it to a file called `snowflake_tf_snow_key.p8` and not encrypting the private key file with a passphrase.

After this is done we need to use the private key to generate the public key.
```Shell
openssl rsa -in snowflake_tf_snow_key.p8 -pubout -out snowflake_tf_snow_key.pub
```

This command takes the previously created private key as input and outputs the public key to a file named `snowflake_tf_snow_key.pub`.

##### Creating the Snowflake service account
The service account needs to be created in the Snowflake console, open a SQL worksheet set the user role to `ACCOUNTADMIN`.

To create a service account user enter and run the following script.

```SQL
CREATE USER "tf-snow" RSA_PUBLIC_KEY='RSA_PUBLIC_KEY_HERE' DEFAULT_ROLE=PUBLIC MUST_CHANGE_PASSWORD=FALSE;
```

Replace the `RSA_PUBLIC_KEY_HERE` with the contents of the `snowflake_tf_snow_key.pub` file we generated earlier.

After creating the service account user, we need to give it the roles it need to create and destroy Snowflake objects.
Run the following SQL commands to assign the `SYSADMIN` and `SECURITYADMIN` roles.

```SQL
GRANT ROLE SYSADMIN TO USER "tf-snow";
GRANT ROLE SECURITYADMIN TO USER "tf-snow";
```

The service account user is now done, the last set is to retrieve it's account_id and region, this will be needed for authentication and authorization.

The following script will output the account_id and region.
```SQL
SELECT current_account() as YOUR_ACCOUNT_LOCATOR, current_region() as YOUR_SNOWFLAKE_REGION_ID;
```

##### Setting Environmental Variables

To not have to hardcode auth information into the terraform script we need to set the values as environmental variables. We can easily do this in the terminal with the `export` command.
```Shell
export SNOWFLAKE_USER="tf-snow"
export SNOWFLAKE_AUTHENTICATOR=JWT
export SNOWFLAKE_PRIVATE_KEY=`cat ~/.ssh/snowflake_tf_snow_key.p8`
export SNOWFLAKE_ACCOUNT="YOUR_ACCOUNT_LOCATOR"
```

#### How to Run the Script

To run the terraform script we need to first initiate the terraform project, we do that running the `init` command in the directory where the `main.tf` file is located.

```Shell
terraform init
```

This will generate the `.terraform` directory, this is where terraform stores all the resources it needs to run the scripts. It also generates the `terraform.tfstate` file, this is where the state is stored. Make sure to add it to `.gitignore`, the state file contains all the used information including environmental variables and secrets, make sure it's private.

Before running the script we need to make sure it's correct, we do that by running the `plan` command.

```Shell
terraform plan
```

If everything works (the provider is under-development, the current code might not work), you can use the script by running the `apply`.

```Shell
terraform apply
```

After this command runs it course, go to the Snowflake console you will be able to see the newly created database and warehouse.

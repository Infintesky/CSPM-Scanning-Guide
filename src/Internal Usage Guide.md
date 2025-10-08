# Introduction

This guide provides setup guides and usage instructions for configuring Vulnerability Assessment (VA) scanning tools across AWS, Azure, and GCP environments.

# Tools Installation

### Python Version
- Python >3.9.1, <3.13 

### Dependency Management 

```bash
sudo apt update
sudo apt install -y python3-poetry

python3 -m pip install --upgrade pip
pip install virtualenv
```

### AWS CLI

```bash
# macOS
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Linux x86
sudo yum remove awscli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Linux ARM
sudo yum remove awscli
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Prowler

```bash
git clone https://github.com/prowler-cloud/prowler
cd prowler
poetry shell
poetry install
poetry run python ./prowler-cli.py --help
```

### ScoutSuite

```bash
git clone https://github.com/nccgroup/ScoutSuite
cd ScoutSuite
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python scout.py --help
```

### CloudSploit

```bash
git clone https://github.com/aquasecurity/cloudsploit.git
cd cloudsploit
npm install `aws-sdk@2.1680.0` @azure/identity
chmod +x ./index.js
./index.js
```

# AWS

## Setting up authentication

###  Configuring AWS CLI

For general use, the `aws configure` command is the fastest way to set up your AWS CLI installation. This configure wizard prompts you for each piece of information you need to get started. Unless otherwise specified by using the `--profile` option, the AWS CLI stores this information in the `default` profile.

The following example configures a `default` profile using sample values. Replace them with your own values as described in the following sections.

```bash
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```

The following example configures a profile named `userprod` using sample values. Replace them with your own values as described in the following sections.

```bash
$ aws configure --profile CSPM_<Client>_Role
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```

### Check that you have set up your credentials

```
aws configure list [--profile profile-name]

# Example Output
$ aws configure list
NAME       : VALUE                    : TYPE             : LOCATION
profile    : <not set>                : None             : None
access_key : ****************ABCD     : config_file      : ~/.aws/config
secret_key : ****************ABCD     : config_file      : ~/.aws/config
region     : us-west-2                : env              : AWS_DEFAULT_REGION

```

### Setting up credentials for `cloudsploit`

- First copy the example config file

```bash
cp config_example.js config.js
```

- Add your credentials into the following lines as shown below:

```json
<SNIP>
aws: {
            // OPTION 1: If using a credential JSON file, enter the path below
            // credential_file: '',
            // OPTION 2: If using hard-coded credentials, enter them below
            access_key: process.env.AWS_ACCESS_KEY_ID || 'AKIA<SNIP>VRZFBL',
            secret_access_key: process.env.AWS_SECRET_ACCESS_KEY || 'KBrw4km<SNIP>fa40JfOL',
            // session_token: process.env.AWS_SESSION_TOKEN || '',
            // plugins_remediate: ['bucketEncryptionInTransit']
        },
<SNIP>
```

## Steps

### Running Scans

```bash
# Prowler
# Default Run
poetry run python ./prowler-cli.py aws

# Execute checks based on requirements defined in compliance frameworks
poetry run python ./prowler-cli.py aws --list-compliance
poetry run python ./prowler-cli.py aws --compliance <compliance_framework>

# ScoutSuite
python scout.py aws

# CloudSploit
./index.js --config=./config.js --cloud=aws --compliance=cis --csv=cloudsploit_aws.csv --console=table
```

### Exporting Results

```bash
# Prowler
# Output saved to ./output/ in html, csv and json formats. Recommended to export html.

# ScoutSuite
# Output saved to ./scoutsuite-report/ in html format with various assets. Recommended to export whole folder

# CloudSploit
# Output saved to filename under csv field
```

# Azure

## Setting up authentication

### Setting up credentials for `cloudsploit`

- First copy the example config file

```bash
cp config_example.js config.js
```

- Add your credentials into the following lines as shown below:

```json
<SNIP>
azure: {
            // OPTION 1: If using a credential JSON file, enter the path below
            // credential_file: '/path/to/file.json',
            // OPTION 2: If using hard-coded credentials, enter them below
            application_id: process.env.AZURE_APPLICATION_ID || 'b73afeb4<SNIP>-276-8829-338dca105db3',      // Client ID
            key_value: process.env.AZURE_KEY_VALUE || 'dtA8Q~MYW.3nchsu<SNIP>Azn-lA8QovRdelIcuv',            // Password
            directory_id: process.env.AZURE_DIRECTORY_ID || 'bd146fad-35c5<SNIP>b1b2-ee634071b49e',          // Tenant ID
            subscription_id: process.env.AZURE_SUBSCRIPTION_ID || 'fa956b60<SNIP>4016-a330-65b21200374f',    // Subscription ID
            // storage_connection: process.env.AZURE_STORAGE_CONNECTION || '',
            // blob_container: process.env.AZURE_BLOB_CONTAINER || '',
            // govcloud: process.env.AZURE_GOV_CLOUD || ''
        },
<SNIP>
```

## Steps

### Running Scans

```bash
# Prowler
export AZURE_CLIENT_ID="b73afeb4<SNIP>338dca105db3"
export AZURE_TENANT_ID="bd146fad<SNIP>e634071b49e"
export AZURE_CLIENT_SECRET="dtA8Q<SNIP>lIcuv"
poetry run python ./prowler-cli.py azure --sp-env-auth

# ScoutSuite
python scout.py azure --tenant <tenant id> --service-principal                                                              
2025-10-06 10:24:19 <SNIP> scout[28193] INFO Launching Scout
2025-10-06 10:24:19 <SNIP> scout[28193] INFO Authenticating to cloud provider
Client ID: <application id>
Client secret: <application secret value>

# CloudSploit
./index.js --config=./config.js --cloud=azure --compliance=pci --csv=cloudsploit_azure.csv --console=table
```

### Exporting Results

```bash
# Prowler
# Output saved to ./output/ in html, csv and json formats. Recommended to export html.

# ScoutSuite
# Output saved to ./scoutsuite-report/ in html format with various assets. Recommended to export whole folder

# CloudSploit
# Output saved to filename under csv field
```

# GCP

## Setting up authentication

### Setting up credentials for `cloudsploit`

- First copy the example config file

```bash
cp config_example.js config.js
```

- Extract the relevant fields from the json file and fill in the fields in `config.js` as seen below

```json
<SNIP>
google: {
            // OPTION 1: If using a credential JSON file, enter the path below
            // credential_file: process.env.GOOGLE_APPLICATION_CREDENTIALS || '/path/to/file.json',
            // OPTION 2: If using hard-coded credentials, enter them below
            project: process.env.GOOGLE_PROJECT_ID || 'trusty-diorama-474500-h1',
            client_email: process.env.GOOGLE_CLIENT_EMAIL || 'cspmscanner@trusty-diorama-474500-h1.iam.gserviceaccount.com',
            private_key: process.env.GOOGLE_PRIVATE_KEY || '-----BEGIN PRIVATE KEY-----<SNIP>\n-----END PRIVATE KEY-----\n'
        },
<SNIP>
```

## Steps

### Running Scans

```bash
# Prowler
poetry run python ./prowler-cli.py gcp --project-ids <project id>

# ScoutSuite
python scout.py gcp --service-account </PATH/TO/KEY_FILE.JSON>

# CloudSploit
./index.js --config=./config.js --cloud=google --compliance=pci --csv=cloudsploit_gcp.csv --console=table
```

### Exporting Results

```bash
# Prowler
# Output saved to ./output/ in html, csv and json formats. Recommended to export html.

# ScoutSuite
# Output saved to ./scoutsuite-report/ in html format with various assets. Recommended to export whole folder

# CloudSploit
# Output saved to filename under csv field
```


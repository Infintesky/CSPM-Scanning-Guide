# 1. Introduction
This guide provides setup guides and usage instructions for configuring Vulnerability Assessment (VA) scanning tools across AWS, Azure, and GCP environments.
# 2. General Prerequisites 
## Tools Installation
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
### Azure CLI (Don't need for now)
```bash
# macOS
brew update && brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```
### GCP (Don't need for now)
#### Linux

| Platform                     | Package name                                                                                                                            | Size     | SHA256 Checksum                                                  |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------- |
| Linux 64-bit<br><br>(x86_64) | [google-cloud-cli-linux-x86_64.tar.gz](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz) | 150.4 MB | 1bd66d2f4bf45ebfcfdc98b109c262ad022af9d8ce9ebad8afa06faa48620e0e |
| Linux 64-bit<br><br>(Arm)    | [google-cloud-cli-linux-arm.tar.gz](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-arm.tar.gz)       | 57.0 MB  | 6882d3255f5cd78b2016665a9f251b94e75106432ff677d288e99e78470a1950 |
| Linux 32-bit<br><br>(x86)    | [google-cloud-cli-linux-x86.tar.gz](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86.tar.gz)       | 57.0 MB  | 68639e9fb28f5922a96a4137ef66dbd987714a51bbf8d985c36c4d69af85f331 |
```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh -y
./google-cloud-sdk/bin/gcloud init
```
#### macOS
| Platform                                   | Package                                                                                                                                   | Size    | SHA256 Checksum                                                  |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | ------- | ---------------------------------------------------------------- |
| macOS 64-bit<br><br>(x86_64)               | [google-cloud-cli-darwin-x86_64.tar.gz](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-x86_64.tar.gz) | 57.1 MB | e41964cb245ce447fce64ddc786cc40fbde29cfab5099a219f496398331b2e5d |
| macOS 64-bit<br><br>(ARM64, Apple silicon) | [google-cloud-cli-darwin-arm.tar.gz](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz)       | 57.0 MB | 9dcdd86a06c84c83043418224bf73ac2e63f2a89386ec32b9192707fd518a3c0 |
| macOS 32-bit<br><br>(x86)                  | [google-cloud-cli-darwin-x86.tar.gz](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-x86.tar.gz)       | 55.6 MB | f31859a49ea8f40947cd588f10f4d8615a0c0cadaff4dcc69cbc1834788ba8b0 |
```bash
wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz
tar -xf google-cloud-cli-darwin-arm.tar.gz
./google-cloud-sdk/install.sh
./google-cloud-sdk/bin/gcloud init
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
# 3. AWS Setup
## Authentication Setup
This section explains how to configure basic settings with an IAM user. These include your security credentials using the `config` and `credentials` files.
### Step 1: Create your IAM user
Create a user in AWS Identity and Access Management and assign a name.

![Screenshot 2025-10-03 at 2.52.51 PM.png](Screenshot%202025-10-03%20at%202.52.51%20PM.png)
### Step 2: Assign `SecurityAudit` Permission

![Screenshot 2025-10-03 at 2.53.23 PM.png](Screenshot%202025-10-03%20at%202.53.23%20PM.png)
### Step 3: Create User

![Screenshot 2025-10-03 at 2.55.15 PM.png](Screenshot%202025-10-03%20at%202.55.15%20PM.png)
### Step 4: Generating Access Keys

![Screenshot 2025-10-03 at 2.57.13 PM.png](Screenshot%202025-10-03%20at%202.57.13%20PM.png)
### Step 5

![Screenshot 2025-10-03 at 3.00.20 PM.png](Screenshot%202025-10-03%20at%203.00.20%20PM.png)
### Step 6

![Screenshot 2025-10-03 at 3.01.54 PM.png](Screenshot%202025-10-03%20at%203.01.54%20PM.png)
### Step 7

![Screenshot 2025-10-03 at 3.02.30 PM.png](Screenshot%202025-10-03%20at%203.02.30%20PM.png)
### Step 8: Configure the AWS CLI
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
### Step 9: Check that you have set up your credentials
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
### Step 10: Setting up credentials for `cloudsploit`
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
# 4. Azure Setup
## Authentication
### Setting up Service Principal
#### Step 1: Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com) as at least a [Cloud Application Administrator](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference#cloud-application-administrator).
#### Step 2: Browse to Entra ID > App registrations then select New registration

![Screenshot 2025-10-06 at 8.52.31 AM.png](Screenshot%202025-10-06%20at%208.52.31%20AM.png)
#### Step 3
- Give the application a name, such as `CSPMScanner`.
- Under Supported account types, select `Accounts in this organizational directory only`.
- Under Redirect URI, select Web for the type of application you want to create. Enter the URI where the access token is sent to. (**Optional**)
- Select Register

![Screenshot 2025-10-06 at 8.56.54 AM.png](Screenshot%202025-10-06%20at%208.56.54%20AM.png)

![Screenshot 2025-10-06 at 8.59.39 AM.png](Screenshot%202025-10-06%20at%208.59.39%20AM.png)
### Assign a role to the application 
#### Step 4
- Sign in to the [Azure portal](https://portal.azure.com).
- In the search bar at the top of the screen, search for and select **Subscriptions**.
- In the new window, select the subscription to want to modify. If you don't see the subscription you're looking for, select **global subscriptions filter**. Make sure the subscription you want is selected for the tenant.
- In the left pane, select Access control (IAM).
- Select Add, then select Add role assignment

![Screenshot 2025-10-06 at 9.07.53 AM.png](Screenshot%202025-10-06%20at%209.07.53%20AM.png)
#### Step 5
- In the Role tab, select the `Security Reader` role to assign to the application in the list, then select Next.

![Screenshot 2025-10-06 at 9.17.15 AM.png](Screenshot%202025-10-06%20at%209.17.15%20AM.png)
- On the Members tab, for Assign access to, select User, group, or service principal.
- Select Select members. By default, Microsoft Entra applications aren't displayed in the available options. To find your application, search for it by name and select it so it appears under `Selected members:` field.

![Screenshot 2025-10-06 at 9.11.50 AM.png](Screenshot%202025-10-06%20at%209.11.50%20AM.png)
- Select the Select button, then select Review + assign.

![Screenshot 2025-10-06 at 9.18.19 AM.png](Screenshot%202025-10-06%20at%209.18.19%20AM.png)
#### Step 6: Repeat the above steps for the roles `Log Analytics Reader` and `Reader`.
### Setting up access
#### Step 7: Create a new client secret
- Click `+ New client secret` then select add
- Note down the `value` field as it will not be shown again.

![Screenshot 2025-10-06 at 10.11.30 AM.png](Screenshot%202025-10-06%20at%2010.11.30%20AM.png)
#### Step 8: 
- Under `API permissions` select `Request API Permissions` and add `Directory.Read.All` and `Policy.Read.All` permissions.

![Screenshot 2025-10-06 at 10.18.18 AM.png](Screenshot%202025-10-06%20at%2010.18.18%20AM.png)
#### Step 9: Setting up credentials for `cloudsploit`

| Value           | Description                    |
| --------------- | ------------------------------ |
| Client ID       | Application ID                 |
| Client Secret   | Secret to Connect to the App   |
| Tenant ID       | Microsoft Entra Tenant ID      |
| Subscription ID | Microsoft subscription plan ID |

![Screenshot 2025-10-06 at 10.33.13 AM.png](Screenshot%202025-10-06%20at%2010.33.13%20AM.png)

![Screenshot 2025-10-06 at 10.34.52 AM.png](Screenshot%202025-10-06%20at%2010.34.52%20AM.png)

![Screenshot 2025-10-07 at 3.53.19 PM.png](Screenshot%202025-10-07%20at%203.53.19%20PM.png)
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
# 5. GCP Setup
## Authentication
### Creating Security Audit Role (CloudSploit)
#### Step 1: Activate "cloud" shell
- Select the top right terminal icon and activate cloud shell

![Screenshot 2025-10-08 at 8.44.10 AM.png](Screenshot%202025-10-08%20at%208.44.10%20AM.png)
#### Step 2
- Copy and paste the following code into a file `aqua-security-audit-role.yaml`, feel free to use vim/nano.
- Note! Exclude all rows starting with 'resourcemanager' if you do not use Organization.
```aqua-security-audit-role.yaml
name: roles/AquaCSPMSecurityAudit
title: Aqua CSPM Security Audit
includedPermissions:
  - cloudasset.assets.listResource
  - cloudkms.cryptoKeys.list
  - cloudkms.keyRings.list
  - cloudsql.instances.list
  - cloudsql.users.list
  - compute.autoscalers.list
  - compute.backendServices.list
  - compute.disks.list
  - compute.firewalls.list
  - compute.healthChecks.list
  - compute.instanceGroups.list
  - compute.instances.getIamPolicy
  - compute.instances.list
  - compute.networks.list
  - compute.projects.get
  - compute.securityPolicies.list
  - compute.subnetworks.list
  - compute.targetHttpProxies.list
  - container.clusters.list
  - dns.managedZones.list
  - iam.serviceAccountKeys.list
  - iam.serviceAccounts.list
  - logging.logMetrics.list
  - logging.sinks.list
  - monitoring.alertPolicies.list
  - resourcemanager.folders.get
  - resourcemanager.folders.getIamPolicy
  - resourcemanager.folders.list
  - resourcemanager.hierarchyNodes.listTagBindings
  - resourcemanager.organizations.get
  - resourcemanager.organizations.getIamPolicy
  - resourcemanager.projects.get
  - resourcemanager.projects.getIamPolicy
  - resourcemanager.projects.list
  - resourcemanager.resourceTagBindings.list
  - resourcemanager.tagKeys.get
  - resourcemanager.tagKeys.getIamPolicy
  - resourcemanager.tagKeys.list
  - resourcemanager.tagValues.get
  - resourcemanager.tagValues.getIamPolicy
  - resourcemanager.tagValues.list
  - storage.buckets.getIamPolicy
  - storage.buckets.list
  - deploymentmanager.deployments.list
  - dataproc.clusters.list
  - artifactregistry.repositories.list
  - composer.environments.list
stage: GA
```
#### Step 3
- Run the following command
```
gcloud iam roles create AquaCSPMSecurityAudit --organization=YOUR_ORGANIZATION_ID --file=aqua-security-audit-role.yaml
gcloud iam roles create AquaCSPMSecurityAudit --project=trusty<SNIP>h1 --file=aqua-security-audit-role.yaml
```
### Setting up Service Account
#### Step 4: Navigate to `IAM Admin > Service Accounts` and click on `Create Service Account`

![Screenshot 2025-10-08 at 8.38.43 AM.png](Screenshot%202025-10-08%20at%208.38.43%20AM.png)
#### Step 5 
- Fill in Service account name and description then select `Create and continue`

![Screenshot 2025-10-08 at 8.40.45 AM.png](Screenshot%202025-10-08%20at%208.40.45%20AM.png)
#### Step 6
- Add the following roles:
	- `Viewer`
	- `Security Reviewer`
	- `Stackdriver Accounts Viewer`
	- `Aqua CSPM Security Audit`
- Select `Done`

![Screenshot 2025-10-08 at 9.11.27 AM.png](Screenshot%202025-10-08%20at%209.11.27%20AM.png)
#### Step 7
- Next Navigate the `Keys` and click on `Create new key` and select `JSON`. The key will be downloaded onto your machine.

![Screenshot 2025-10-08 at 9.13.48 AM.png](Screenshot%202025-10-08%20at%209.13.48%20AM.png)
#### Step 8:
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
# 6. References
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Prowler](https://github.com/prowler-cloud/prowler.git)
- [Prowler CLI Basic Usage Documentation](https://docs.prowler.com/projects/prowler-open-source/en/latest/basic-usage/prowler-cli/)
- [Prowler Compliance Checks List](https://hub.prowler.com/compliance)
- [Prowler CLI Compliance Usage](https://docs.prowler.com/projects/prowler-open-source/en/latest/tutorials/compliance/)
- [ScoutSuite](https://github.com/nccgroup/ScoutSuite.git)
- [CloudSploit](https://github.com/aquasecurity/cloudsploit.git)
- [Authenticating using IAM user credentials for the AWS CLI](https://docs.aws.amazon.com/cli/v1/userguide/cli-authentication-user.html)
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Register Microsoft Entra app and create Service Principal](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-service-principal-portal)
- [ScoutSuite Azure ](https://github.com/nccgroup/ScoutSuite/wiki/Azure)
- [Creating Prowler Service Principal](https://docs.prowler.com/projects/prowler-open-source/en/latest/tutorials/azure/create-prowler-service-principal/)
- [GCP CLI](https://cloud.google.com/sdk/docs/install)
- [Setting up GCP Service Account](https://cloud.google.com/iam/docs/keys-create-delete)
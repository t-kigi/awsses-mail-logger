# awsses-mail-logger

This microservice provides the ability to save events for emails sent via SES to DynamoDB.

## Prerequisites

- `pipenv`, `pyenv`, and `cdk` commands must be available in the execution environment.
  - If pyenv is not available, make sure that Python 3.9 is available.
- An awscli profile is already configured (assumes `mail-logger` ).
- A verified SES ID is already registered and not using the default Configuration Set.

## Setup

```bash
$ pipenv install
$ pipenv install --dev
```

### awscdk

```bash
$ cd awscdk
$ pipenv run cdk bootstrap --profile mail-logger

# Check what operations will be performed with the following command
$ pipenv run cdk diff --profile mail-logger

# Deploy the required resources
$ pipenv run cdk deploy --all --profile mail-logger
```

### chalice

```bash
$ cd logger

# Reflect the results of executing awscdk
$ vim chalicelib/env/prod.yaml
$ vim .chalice/config.json
$ vim .chalice/policy-prod.json

# Deploy
$ pipenv run chalice deploy --stage prod --profile mail-logger
```

### To set up the verified SES ID

Use the Configuration Set that was created as the default set.


## License

Apache License 2.0

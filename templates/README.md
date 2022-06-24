# <% .Name %> Backend service

## Requirements

- Docker
- Kubectl
- terraform

## How to run :rocket:

```sh
make run
```

## Infrastructure provisioning:

### Terraform apply

> You should have configured the aws cli.

```sh
cd terraform
terraform apply
cd ..
```

### Update k8s configmap/aws-auth

```sh
kubectl edit -n kube-system configmap/aws-auth
```

```yaml
mapRoles: |
  - rolearn: arn:aws:iam::<% index .Params `accountId` %>:user/ci/ci
    username: ci
    groups:
    - system:masters
```

### Set github secrets AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

- Access the IAM dashboard on the AWS console;
- Users > ci > Security credentials;
- Create access key;
- Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in the github repo settings.
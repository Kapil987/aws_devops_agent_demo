### **1. On the AWS Side (IAM Setup)**

You need to tell AWS to trust GitHub as an "Identity Provider" and then create a role that GitHub is allowed to "assume."

#### **A. Create the Identity Provider**

1. Go to the **IAM Console** > **Identity Providers** > **Add provider**.
2. **Provider type:** OpenID Connect.
3. **Provider URL:** `https://token.actions.githubusercontent.com` (Click "Get thumbprint").
4. **Audience:** `sts.amazonaws.com`.

#### **B. Create the IAM Role (`GitHubLambdaRole`)**

1. Go to **Roles** > **Create role**.
2. **Trusted entity type:** Custom trust policy.
3. **Paste the Trust Policy below** (Replace the placeholders with your info):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_ORG/YOUR_REPO_NAME:*"
        }
      }
    }
  ]
}

```

4. **Add Permissions:** Attach a policy to this role that allows it to update Lambda code (e.g., `AWSLambda_FullAccess` or a custom policy with `lambda:UpdateFunctionCode`).
5. **Name it:** `GitHubLambdaRole`.

---

### **2. On the GitHub Side (Workflow Setup)**

GitHub doesn't need "Secret Keys" for OIDC, but it does need permission to request the token from AWS.

#### **A. Add Permissions to your YAML**

Your workflow file **must** have these permissions at the top of the job, or the `configure-aws-credentials` action will fail.

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write # This is required to request the OIDC JWT
      contents: read  # This is required for actions/checkout
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubLambdaRole
          aws-region: us-east-1

```

---

### **3. Verification Checklist**

* **Account ID:** Ensure the `123456789` in your YAML matches your actual AWS Account ID.
* **Thumbprint:** Ensure you clicked "Get thumbprint" when creating the OIDC provider in AWS.
* **Repo Path:** In the Trust Policy, ensure `repo:YOUR_GITHUB_ORG/YOUR_REPO_NAME:*` exactly matches your GitHub path (case-sensitive).


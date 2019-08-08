# Slack with Lambda Function

Build an Slack bot can use for manage Instances or Service on AWS

## Contents

- [Slack with Lambda Function](#slack-with-lambda-function)
  - [Contents](#contents)
  - [Create Slack App](#create-slack-app)
  - [Configure AWS intergrate with Slack Bot](#configure-aws-intergrate-with-slack-bot)
  - [Install App to Workspace](#install-app-to-workspace)
  - [Create Lambda Functions](#create-lambda-functions)
  - [Create API via API Gateway](#create-api-via-api-gateway)
  - [Develop function](#develop-function)
    - [Requirement](#requirement)


## Create Slack App
Login to your workspace on Slack and go to `https://api.slack.com`. In this page, click to button `Start Building` to start create new Slack App.

You will see an pop-up like below:

![popup-create-slack-app](docs/images/popup-create-slack-app.png)

Input the `App Name` and select the `Workspace` you will use the Slack App. After that, click `Create App` button

## Configure AWS intergrate with Slack Bot

- In app management page, Select `Slash Commands` in left menu and click `Create Slash` command

![slash command](docs/images/create-slash.png)

- You will see as below image:

![create new slash command](docs/images/create-new-slash-command.png)

- Input the command like below image:

![input information slash command](docs/images/create-new-slash-command.png)

- The result after create like below:

![result create slash](docs/images/result-create-slash.png)

## Install App to Workspace

- In API page click `Install App` in left menu and click to button `Install App to Workspace`

![install app](docs/images/install-app.png)

- Click `Install` button to install app to workspace

![confirm install app](docs/images/confirm-install-app.png)

- After that you will see as below:

![install success app](docs/images/install-app-success.png)

## Create Lambda Functions

- On Lambda page, click `Create function`

![create lambda page](docs/images/create-lambda-page.png)

- The page will display as below, you must create an role for lambda function

![create lambda](docs/images/create-lambda-function.png)

- After create successful you will see the result as below:

![create lambda result](docs/images/lambda-function-screen.png)

## Create API via API Gateway

- In API Gateway page click to `Create API` button

![create api page](docs/images/create-api-page.png)

- Input infomation for API and click `Create API` button

![create api](docs/images/create-api.png)

- Create `method` for API by click `Create Method` button as image below

![create api method](docs/images/create-api-method-page.png)

- Select `POST` method

![create post method](docs/images/create-api-select-post.png)

- You will see result as below

![create method api result](docs/images/create-api-method-result.png)

- You can also can see result in the `Design` block from Lambda like below

![lambda design](docs/images/desgin-in-lambda.png)

## Develop function

### Requirement

- Python 3.6
- AWS CLI

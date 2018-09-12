
# Alexa Serverless Comprehend Workshop: Building an Alexa Skill with AWS Serverless and ML Technologies

In this workshop, you will learn how to develop an Alexa Custom Skill, which queries Twitter for recent tweets relevant to your corporation.  A set of Twitter search criteria has already been created for the application but you will have the ability to change search criteria during the workshop.  In addition, we will be using a special hashtag, *#AWSSMAWS*, so as not to spam your company's tweet stream. 

**Note**: Text in **bold** indicates a critical instruction or reminder; usually asking you to confirm a setting so that your application deploys correctly.  Text in *italics* represents the literal name of a button, link, action, etc. that you should click, select, or enter when requested in the workshop instructions.  Text with `background` is for code, command line statements, or variables that you can copy directly from the workshop instructions and paste directly into the consoles.

**Note**:  AWS Services can either be Global or Regional.  Most of the services used today are intended to be used in the US East Region (aka N. Virginia).  When in the AWS Console, please, **always confirm you are in the US East Region** as indicated at the top right side of the screen.

**Note**:  Assuming you haven't been running other AWS resources in your account, (i.e. you're using a newly created AWS Account) as of the time this workshop was created, resources created will be in the free-tier. This assumes you delete all resources at the conclusion of the workshop as described in the step titled, *End of Workshop: Cleanup resources (optional)*

## Create an AWS Cloud9 Integrated Development Environment (IDE)

AWS Cloud9 is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser. It includes a code editor, debugger, and terminal. Cloud9 comes prepackaged with essential tools for popular programming languages.  AWS Cloud9 provides a seamless experience for developing serverless applications enabling you to easily define resources, debug, and switch between local and remote execution of serverless applications. With AWS Cloud9, you can quickly share your development environment with your team, enabling you to pair program and track each other's inputs in real time.

You can develop Lambda serverless applications, or any AWS Cloud application for that matter, with the IDE of your choice including popular IDEs such as Visual Studio, Eclipse and PyCharm.  Several of these IDEs have AWS plug-ins to assist with development and integration with AWS Cloud.  We’re using AWS Cloud9 as a standard for this workshop because it will provide a consistent environment across all students, which will help in providing consistent instruction as well as trouble shooting should any issues occur.  In addition, students don’t have to download and install software onto local machines, which could take additional time and require unique debugging.

**Note**: Cloud9 works with most popular browsers but AWS recommends Google for ease of cut-and-paste between environments. **If you use a browser other than Google, be sure to cut-and-paste between Cloud9 and other sources using the browser’s cut-and-paste feature, not Cloud9’s.**

### Create a Cloud9 Environment
- Login to the AWS console with a user with admin privileges.  **Note**: As a best practice, the **Root user is not recommended** but it can be used for this workshop if an IAM users of sufficient privilege is not available. 
- Either from within the menu of services under *Developer Tools*, or by typing *Cloud9* into the search field, select Cloud9.
- Now is a good time to verify you are in the *N. Virginia* Region.  Check the upper right hand corner of console to confirm.  If you’re not, click on the Region name and select *US East, N. Virginia.*  Always make sure you are in this Region when using the AWS Console.
- Click the orange button labeled, *Create Environment*.  
- Provide a name for your Cloud9 environment, e.g. Alexa Serverless Workshop.  Optionally, provide a description in the *Description* field. Click the *Next Step* button at the bottom right of the screen. (You may need to scroll down to see the button).
- On the next screen, accept all defaults and click the *Next Step* button at the bottom right of the screen.  The default configurations will deploy a T2.micro EC2 instance of Cloud9, which is sufficient for the purposes of this workshop.  The Cloud9 EC2 instance will be deployed into your Default VPC.  *If you experience connection issues, ask for assistance from your workshop leader.*
- Click *Create Environment* at the bottom right of the screen.

     **Note: Creating your Cloud9 environment takes a few minutes as it creates a new EC2 instance within your VPC in AWS.**

### Update Cloud9’s Python Path
Be default, Cloud9 assumes a Python developer will use Python 2.7 libraries.  The Python libraries we will use include Python 3.6 versions so we need to change the Python Path to include 3.6 libraries.

- From within the menu item labeled *AWS Cloud9* (bold upper-left corner of screen), select *Preferences*.  
- From Project Settings, select *Python Support*. 
- Replace the existing PYTHONPATH with: `/usr/local/lib/python2.7/site-packages:/usr/local/lib/python3.6/site-packages `
- Close the *Preferences* window by clicking on the *x* in the tab.

### Update the AWS Command Line Interface (CLI) in Cloud9
We will be using the AWS CLI to issue several commands to your AWS environment.  Cloud9 includes the AWS CLI but we need to confirm and, if necessary, update the CLI to the most recent version available.

- Close the *Welcome* window by clicking on the *x* in the tab.
- Open a new terminal window by clicking on the *+* icon near the top of the Cloud9 screen.  Select, *New Terminal*.
-  AWS offers the ability to create and manage infrastructure via the AWS Console (which you used to create a Cloud9 instance), several Software Development Kits (SDK), and a Command Line Interface (CLI).  Cloud9 includes the AWS CLI but we want to make sure we have the latest and greatest version.  Do so by entering into the Terminal Window (labeled, *bash - “ip-…*) and enter the following command and press return: ` pip install awscli --upgrade --user`  If needed, a download and install process will begin to update the AWS CLI.  This should take less than a minute to complete.

**Note**: If at any time in the Window Terminal (bash), you want to clear previous commands from the screen for better visibility, type `clear` and hit return. This will clear previous commands from the display and locate your cursor near the top of the window.

## Download project source code and templates

Code and infrastructure templates for this workshop are securely stored in AWS CodeCommit.  CodeCommit is a fully-managed source control service that makes it easy for companies to host secure and highly scalable private Git repositories. CodeCommit eliminates the need to operate your own source control system or worry about scaling its infrastructure. You can use CodeCommit to securely store anything from source code to binaries, and it works seamlessly with your existing Git tools.

Within the Cloud9 Terminal window, enter the following command:

`git clone https://github.com/mstockwell/Alexa-Serverless-Comprehend-Workshop.git`  This process, which should take less than a minute, will download and clone the repo to your Cloud9 environment.

Next, we will change the working directory to the local git repository you just cloned in your Cloud9 environment.  Within the Terminal window, type the following and hit return: `cd Alexa-Serverless-Comprehend-Workshop`

## Create an S3 bucket to store and deploy AWS Lambda functions 

S3 is AWS’ object storage service.  We will automatically be implementing most of the infrastructure and code using two AWS services, CloudFormation and SAM, described in detail later in the document.  SAM requires Lambda code to be stored in S3 so that CloudFormation can access it to deploy your lambda functions when it builds out infrastructure in AWS.  We will be creating your S3 bucket via the AWS command line.  

S3 buckets must be globally unique across all customers.  Therefore, a script has been created that will uniquely name and create your S3 bucket.  Confirm you are still in the *Alexa-Serverless-Comprehend-Workshop* directory and execute the following command in the Cloud9 terminal window: `. createbucket.sh` **(Don’t forget the leading period)**

In response, you will see *make_bucket:* followed by the unique name of your S3 bucket.  Go back to the AWS Console and select the S3 service, making sure you are in the US-East Region.  You will see your new S3 bucket listed in the console.


## Create AWS infrastructure and deploy Lambda functions

AWS CloudFormation provides a common language to describe and provision all the infrastructure resources in your cloud environment. CloudFormation allows you to use a simple text file to model and provision, in an automated and secure manner, all the resources needed for your applications across all regions and accounts. This file serves as the single source of truth for your cloud environment. 

The AWS Serverless Application Model (SAM) is a model to define serverless applications. SAM is natively supported by AWS CloudFormation and defines simplified syntax for expressing serverless resources.

### Create an AWS Secrets Manager Secret to store Twitter Developer credentials
Before executing our CloudFormation and SAM templates, we will need to create a secure and encrypted store to hold your unique Twitter developer credentials.  This secret will be programmatically accessed by your Lambda Poll Twitter function, which calls the Twitter API using your credentials.

- Return to the Cloud9 Console and enter back into the Terminal window.  You should still be in the `Alexa-Serverless-Comprehend-Workshop` directory.
- In the File Explorer pane on the left, expand the *Alexa-Serverless-Comprehend-Workshop* folder.  Within the folder, double click on the *twittercreds.json* file (which is located in /home/ec2-user/environment/Alexa-Serverless-Comprehend-Workshop).  This will open a new window with the contents of the file displayed.
- Modify the content with your specific Twitter Developer credentials.  Save the file and close the window.
-  At the Terminal Window, execute the following command: 
`aws secretsmanager create-secret --name twittercredentials --description "My Twitter Developer Credentials" --secret-string file://twittercreds.json`

### Run SAM and CloudFormation to create initial infrastructure and code
Within your Cloud9 Terminal window, verify you are still in the *Alexa-Serverless-Comprehend-Workshop* directory by typing `pwd` and hitting return.  You should see */home/ec2-user/environment/Alexa-Serverless-Comprehend-Workshop*. This is where your CloudFormation and SAM templates are located.  Now, enter the following command and press return:
`aws cloudformation package --template-file template.yaml  --output-template-file output.yaml --s3-bucket $S3_BUCKET_NAME  --s3-prefix WorkshopAppFunctions`  

The above command packages your lambda functions and puts them in your S3 bucket.  In addition, the SAM template will be transformed into a CloudFormation template to be used in the next step for creating your infrastructure stack.

Next, enter the following command and press return:
`aws cloudformation deploy --template-file output.yaml --stack-name Alexa-Workshop-App --capabilities CAPABILITY_NAMED_IAM`

You should see *Waiting for changeset to be created..* in Cloud9. The above command creates all the AWS infrastructure needed for the workshop.  In addition, it will access the Lambda code stored in your S3 bucket and deploy it into AWS.  Deploying the infrastructure will take approximately 3 minutes so feel free to take a short break.  If you like, the stack deployment can be monitored within the AWS Console by going to the CloudFormation Console and clicking on the stack named Alexa-Workshop-App.  Upon completion of the stack deployment, Cloud9 will show, *Successfully created/updated stack - Alexa-Workshop-App*

### Review artifacts automatically created and deployed using CloudFormation and SAM
We don’t have time to review everything the CloudFormation and SAM templates created, but let’s examine some of the major components created:

- Within the AWS Console, go to the DynamoDB service.  Click on *Tables*, located to the left side of the screen.  You will see two new tables created by your CloudFormation template: *Tweets_Table*, *Twitter_Stats_Table*.  Select a table and click on the *Items* tab.  Note that the table currently has no items.  Also, note that a Stream is enabled for the *Tweets_Table* and that a Trigger has been created to call the *Update_Twitter_Stats* Lambda function when a new record is placed on the DynamoDB Stream for the *Tweets_Table*.

- Let’s look at the Lambda functions created by CloudFormation. Within the AWS Console, go the the Lambda service.  There should be three Lambda functions created by this workshop.
	- Select the *Poll_Twitter* Lambda function.  
	- In the middle of the screen, is the name of the function in an orange box.  Notice just below and to left of the function name, it says *CloudWatch Events*  This indicates a CloudWatch Event triggers the execution of the function.  (We’ll, look at that event in a moment).
	- Scroll down further.  Notice there is a section for code runtime configuration and an area to upload, view and update code in the lambda browser.  However, when a code package gets too large, the code cannot be viewed directly in the Lambda console (instead it’s packaged into a compressed zip file).  If you wish to see the source code, go back to Cloud9 and double-click on the lambda_function.py within the Poll_Twitter folder to see the source code.  (Later in the workshop, you will create a new function and be able to see the code directly in the Lambda console.)
	- Go back the the AWS Console and scroll down a bit further to see the *Environment variables* this function uses.  Environment variables provide the ability to inject variables at runtime, allowing your functions to be much more flexible and dynamic.  Notice the variable named, *SEARCH_TEXT*  This variable contains a list of criteria to search for within Twitter.  If you like, you can modify this search string to change the criteria; Just be sure to save the function after making changes.  You save changes by clicking the orange save button located near the top right of the Lambda console.
	- Scroll a bit further down to see this function’s *Execution role* and *Basic settings*.  The Execution role is an AWS IAM role defining what access this Lambda function has to what AWS services.  It’s essentially used for assigning a service role to the Lambda. The Basic Settings dictate how much memory (and proportional CPU) is allocated to the Lambda function and how long the function is allowed to run before it times out.  Lambda is charged by the time it’s running (to the millisecond) and the amount of memory you provide it. 
- A CloudWatch Schedule Event was created by the CloudFormation template.  This event executes every minute, triggering the *Poll_Twitter* lambda function to retrieve any new tweets that meet your search criteria.  Within the AWS Console, go to the CloudWatch service and click on *Rules* on the left side. Click on the rule named *APP-Scheduled-Rule…*  You can see this rule executes on a fixed-rate of one minute and that it targets (executes/calls) the Lambda function *Poll_Twitter*.


### Initial Load of Historical Tweets (optional but if not performed see next section on seeding database)
To provide some initial data to work with, we have a JSON file containing historical tweets based on an Twitter Amazon search criteria string.  We will now load the Twitter data from this file into your DynamoDB database.

Within the terminal window of your Cloud9 environment, type the following command and hit return: `cd Import_Twitter_Table`.  This will change your working directory to the Lambda function that will import data into your DynamoDB table.

Next, we will use the SAM local service that’s already installed in your Cloud9 environment.  SAM local allows you to develop, test, debug, and deploy Lambda functions locally within your IDE before deploying into AWS.  We will be executing the *Import_Twitter_Table* Lambda function locally, within Cloud9, to update your DynamoDB tables within AWS.  Execute the following command within the Cloud9 Terminal window:

  `sam local invoke ImportTwitterTable -e lambda-payloads.json`

A return value of *null* indicates the Lambda function successfully loaded the data into DynamoDB with no errors.  Let’s confirm this by going into the AWS console and selecting the DynamoDB service.  Select *Tables* and select the *Tweets_Table* table.  Next, select the *Items* tab on the right-side.  You should see a list of tweets. 

### Seeding the DynamoDB database if historical tweets not available
- Using Twitter, find a recent tweet id for tweet you are interested in.  
- Add this tweet id to the Twitter_Stats_Table as an Item, `name` with string value of `LATEST` and add a field `sinceid` of type `number`
- Paste the tweet id into the sinceid field and save
- Now, add  tweet id to the Tweets_Table by creating a new Item, `tweetid` of type number and paste tweet id into the value and save.

## Deploy Alexa Skill 
Alexa is Amazon’s cloud-based voice service available on tens of millions of devices from Amazon and third-party device manufacturers. With Alexa, you can build natural voice experiences that offer customers and employees a more intuitive way to interact with the technology they use every day. Our collection of tools, APIs, reference solutions, and documentation make it easy for anyone to build with Alexa.

**Note**:  The Alexa Develop Console appears to have a short timeout period for user inactivity.  You may find that you’re required to log back into the console as we go through the workshop.

### Create an Alexa Skill
- Log into the Alexa Developer Console `https://developer.amazon.com/alexa`
- Click on *Your Alexa Consoles* near the top right of the screen, and select *Skills* from the dropdown.
- Click the *Create Skill* button, located to the left of the screen.
- For Skill Name, enter `my social media analytics`  (note: must be all lowercase)  **Note**: You may use a different name (e.g. `corp social media` ) for your skill but remember to use that name in future steps.
- In the upper-right hand corner, click the blue button named, *Create Skill*.
- On the next screen, make sure *Start from scratch* is selected with a blue triangle in the upper-right hand corner, and select the *Choose* button in the upper-right hand corner of the screen.
- Select *Invocation* (located on the left side of the screen) and enter `social analytics` for the Skill Invocation Name (This is the name speak/use to invoke the skill, it must be all lowercase).  
- Click on the *Save Model* button near the top of the screen to save your work.

### Create Intents using an Alexa JSON configuration file
- Near the bottom left side of the screen, select *JSON Editor*.  
- Replace the existing content (JSON located to the right) by copying and pasting the content of the file *Alexa Analytic Skill.json* within your Cloud9 environment.  This file is located in the Cloud9 file explorer located on the left-side of the screen.  The JSON file is located in the *Alexa-Serverless-Comprehend-Workshop* folder.  Double-clicking on the file *Alexa Analytics Skill.json* will open the content of the file in a new window to the right. Copy the entire content of the JSON file and paste into appropriate section of the Alexa Developer Console, replacing all the existing text.
- Click the *Save the Model* button in the upper section of the screen.

### Create a Lambda Endpoint for your Alexa Skill
- Select *Endpoint*, which is located below *JSON Editor* on the left side of screen.
- Select the *AWS Lambda ARN* radio button and copy the skill ID to the clipboard. **You will use the skill id in the Lambda Console in the next step below.** 
	- **Note**: An ARN is an Amazon Resource Name.  It’s often used to uniquely identify or reference a service or artifact in AWS.
- Go to AWS Lambda Console and select the *Alexa_Skill* Lambda.  
- Next, on the left hand side of the Lambda Console, under *Add Triggers*, select  *Alexa Skills Kit*.  Scroll down to *Configure Triggers* and paste the skill id into the *Skill ID* field
- Click the *Add* button located near the bottom right side of screen.
- Next, click the *Save* button near the upper right corner of screen.
- Located above the *Save* button is the Lambda ARN.  The ARN will start with, *arn:aws:lambda:us-east-1:*  Copy the Lambda ARN to the clipboard.  We will use the ARN to finish configuring our Alexa Endpoint in the Alexa Developer Console.
- Return to the Alexa Developer Console.
- Paste the copied Lambda ARN into the *Default Region* field and click the *Save Endpoints* button located near top of the screen.

### Build your Alexa Skill
- Staying in the Alexa Developer Console, click the *Build* link located near top left-side of the screen.
- On the right side of the screen, click the grayed out step, *3. Build Model >* .  You should receive a message indicating your model is being built and that you will be notified when it’s complete.  The build process will take approximately 2 minutes.  Once complete, the *Build Model* step will turn from gray to green.
- After a successful build notification, click the *Test* link located next to the *Build* link.  
     
## Test with live tweets!
The Alex Simulator offers you the capabilities to test your Alexa skill without the use of an Alexa device.  There are multiple ways to test your skill but the primary methods are either through your computer’s internal mic or by typing in your request.  

**Note**  You may need to enable your computer’s internal microphone and allow the Alexa Developer Console permission to the mic.  Alternatively, you can simply type your request into the test simulator without needing the internal mic.

- At the top of the Test screen, a message, *Test is disabled for this skill.*  will be displayed.  Click the slider bar to the left of the message to enable Alexa test mode.
- To test your Alexa skill, either click and hold on the microphone icon and speak your request, or type your request into the field to the left of the microphone icon.  You must first *Open* your skill to start testing it.  To open the skill, say *Alexa open social analytics*
- Now you can ask Alexa questions such as:

      *Alexa, what’s the most recent tweet?, Alexa, what’s the most favorited tweet?, Alexa, what’s the most retweeted tweet?*

- Add tweets in Twitter, using the `#AWSSMAWS` hashtag to see how real-time updates change the analytics.
- When you have finished testing, close your skill by saying, “Alexa, quit.” or simply click back to the *Build* link to leave testing.

## Create an Alexa Intent to report social media sentiment
Determining the current mood, or sentiment, of how customers or the general public feel about your corporation or it’s concerns can be valuable information.  For instance, understanding how aninvestment is trending, or current events, can provide insights into trading patterns and potentially predict investor behavior.  You are now going to create an Alexa Intent that will report back on the overall sentiment of recent tweets relevant to your corporation (based on the current *SEARCH_TEXT* being used in the *Poll_Twitter* Lambda function).  

### Create the backend Lambda function for calling Amazon Comprehend
First, we are going to create a Lambda function which reads and processes tweets within the DynamoDB using Amazon Comprehend.  Comprehend is a fully managed, Natural Language Processing (NLP) machine learning service, which, among many things, has the ability to determine the mood or emotions being conveyed within written text. 

- Within Cloud9 go to the File Explorer pane on the left.  Within the *Alexa-Serverless-Comprehend-Workshop* folder you will find a folder named *Sentiment-Analysis*.  Open the folder and double-click on the lambda_function.py file.  This will open the source code in a new window to the right of the file explorer. 
- Starting from the top of the Lambda source code file:
	- Notice how we import necessary python libraries, including some which integrate with AWS services.  
	- After the imports, we declare resource connections to DynamoDB and Comprehend.  
	- The def lambda\_handler(event, context):  statement denotes the beginning of code execution when a Lambda gets triggered.  
	- Within the handler, we see that we scan all tweets in the DynamoDB table where the tweet was created today (current_date).  
	- Next, for each tweet retrieved by the query, we ask Amazon Comprehend to detect the sentiment of the tweet.  Sentiment falls into four categories: Mixed, Neutral, Positive and Negative.  
	- The sentiment of all tweets are summed into each category and then written back to DynamoDB.  The category with the highest sentiment is considered prevailing.  **Note**: This is just one possible way of interpreting sentiment.  You may feel there are better methods for calculating overall sentiment.  The point of this simple algorithm is that you have flexibility to code how you want the overall sentiment analyzed based on the learnings of Comprehend. 
- Close the window containing the source code.  Now, double-click on the *template.yaml* file located in the same directory
- The template.yaml file is a SAM configuration file, which is the same type of file you used to deploy previous Lambda functions.  Recall that SAM template allows you to describe, configure, and deploy Lambda function.  As you can see, there are number of parameters within the SAM template; parameters for naming the function, declaring Environment Variables, assigning IAM roles for security, and declaring the memory size of the Lambda function.  This is just a subset of what can be configured using SAM. 
- Close the Window containing the SAM template.  
- On the far right side of the Cloud9 screen, click the *AWS Resources* tab.  Within the tab you will see a folder called *Local Functions*.  If necessary, click to expand the folder.
- Within the folder you we see another folder for the *Sentiment-Analysis* Lambda function, for which we just reviewed the source code and SAM template in the previous steps.
- Right click on the *Sentiment-Analysis* folder and click *Deploy*.  This will configure and deploy your source code into AWS as instructed by the SAM template.  The deployment process takes about one minute.
- After the deployment is complete, go to the AWS Lambda console and confirm the *Twitter_Sentiment_Analysis* function deployed.  Scroll down through the function details, notice the same source code you reviewed while in Cloud9.  See how the function is triggered when a new tweet record is added to DynamoDB.  See how it’s using the Lambda Role as defined in the SAM template along with the memory size of 128 as also described in the SAM template. 

### Test the sentiment Lambda function

Let’s test the sentiment analysis function before creating the Alexa Intent to trigger it.

- Click the *Test* button at the top right of the Lambda Console.
- Give the test a *Even name* of `test` and click the *Create* button in the lower right corner. 
- Now click the *Test* button again.  This will trigger the lambda function.  You should see a green box with *Execution result: succeeded* displayed.  Let’s see if it actually calculated sentiment scores…
- Within the AWS console, go to the DynamoDB service and select the *Twitter_Stats_Table*.  To the right, click on the *Items* tab.  You should see an item called *SENTIMENT* (if not, click the refresh icon to reload the table). 
- Scroll to the right to see the summary counts by each SENTIMENT category (i.e. MIXED, NEGATIVE, NEUTRAL, POSITIVE). 
- The current sentiment will probably show that a majority of tweets are *NEUTRAL* and therefore the overall sentiment in neutral.  Let’s attempt to change the overall sentiment by going to Twitter and creating several new tweets with a positive sentiment using the `#AWSSMAWS` hashtag.  Collectively, as a group, we should be able to quickly enter dozens of new tweets with a positive spin.  After a couple minutes, refresh the table in DyanmoDB and see if the SENTIMENT categories have changed.  Now let’s connect a new Alexa Intent to the sentiment functionality. 
 

### Create an Alexa Intent asking for the overall sentiment of recent tweets. 
In the previous step, we created the backend functionality for accessing our DynamoDB tables and processing records through Amazon Comprehend to determine and record the overall social media sentiment of the collective tweets.  Now we need to add an Intent to our Alexa Skill, which will trigger the function.  

- Go back to the Alexa Developer Console and return to the *Build* console.  **Note**: If you’re at the main page, under *Skill*, select the *social analytics* skill you previous created and this will bring you back to the *Build* console.
- On the left side of the console, to the right of *Intents*, click *Add*.
- Under *Create Custom Intent*, enter `Sentiment` and click *Create custom intent*.
- Let’s add some sample utterances to help Alexa understand when we are interested in the overall sentiment of recent tweets.  Enter the following utterances, after entering an utterance, click the *+* to the right to add another utterance:
	- `what's the overall mood on <your company>`
	- `how do people feel about <your company>`
	- `what is the overall sentiment`
	- `what's the sentiment`
- Click the *Save Model* button and then the *Build Model* button.  Within a minute or so, you should receive the *Build Successful* message.  We are ready to test the new Intention.
- Click the *Test* link. Test should already be enabled from our previous Alexa test session.  If it’s not, click the *Test is enabled for the skill* button.
- Click and hold the mic icon, or type in the request: *Alexa, open social analytics*.  
- Once the Skill is open, ask Alexa for the sentiment using one of the utterances you created. For example, *Alexa, how do people feel about <your company>?*
- If you’d like to try and change the sentiment in real-time, add more live tweets using the `#AWSSMAWS` hashtag and check back with Alexa on the sentiment.  

## End of Workshop: Cleanup resources *(optional)*
Recall earlier in the lab when we used CloudFormation and SAM to provision most of the infrastructure and code for the workshop.  We will now run CloudFormation again, but this time we will delete all the infrastructure provisioned during the lab.  Within AWS, you only pay for the resources you consume.  If you don’t plan to continue using the services created by this workshop, we recommend you execute the commands below to delete the infrastructure created during the workshop:

- At the Cloud9 Terminal window, type the following command and hit return: `aws cloudformation delete-stack --stack-name cloud9-Sentiment-Analysis`  This will instruct CloudFormation to delete the Sentiment-Analysis Lambda function you created.
- Next, type the following command and hit return: `aws cloudformation delete-stack --stack-name Alexa-Workshop-App`  This will instruct CloudFormation to delete all the resources created during the beginning of the workshop.
- Next, we need to delete the S3 bucket we created, which stored the Lambda code used by SAM and CloudFormation.  In the Cloud9 Terminal window, type the following command and hit return: `aws s3 rb s3://$S3_BUCKET_NAME --force`  This will delete the S3 bucket and all it’s content (Lambda code).
- Next, delete the secret store in AWS Secret Manager which held your Twitter Developer credentials: `aws secretsmanager delete-secret --secret-id twittercredentials`
-  Go to the AWS Console, Select the Cloud9 service.  Select your Cloud9 environment and click *Delete*.  A confirmation box will appear.  Type *Delete* into the entry field and click *Delete*.  This removes the Cloud9 EC2 instance. 
- Lastly, go to the Alexa Developer Console.  Select your Alexa Skill, *social analytics* and click *delete* to the right of the skill name.

# Congratulations! 
You just learned how to develop your first Alexa Skill using several AWS services:

- **AWS Cloud9**: You created an IDE in the Cloud, which allowed you to code, test, and deploy both code and infrastructure to AWS.
- **AWS CodeCommit**: You cloned the workshop project into your Cloud9 environment in order to build, test, and deploy artifacts to AWS.  In real-life usage, you would collaborate with team members by checking in and out code on a frequent basis and use a CI\CD pipeline to automatically test, integrate, deploy and deliver applications at a very rapid pace using DevOps practices.
- **Amazon S3**:  Using the AWS CLI, you created an S3 bucket (object store) to hold Lambda code for the project.  CloudFormation and SAM accessed this bucket to deploy your Lambda code into AWS.
- **AWS CloudFormation** and **SAM**:  Using CloudFormation and SAM templates, you created and deployed a Stack of infrastructure, automatically, into AWS.  This is also known as using Infrastructure as Code, and is a very powerful mechanism for consistently and quickly provisioning infrastructure into your AWS environment. 
- **Amazon DynamoDB**: Your Lambda functions accessed DynamoDB to return data and statistics on tweets relevant to your company.  DynamoDB is AWS’ fast and scalable NoSQL database.
- **AWS CloudWatch**:  Through CloudFormation, we created a CloudWatch event to execute a Lambda function that polled twitter for new tweets on a per minute schedule.  
- **AWS Lambda**:  Through SAM, we deployed several serverless functions using AWS Lambda.  You then coded a Lambda function to determine the overall sentiment (mood) of recent tweets concerning your company.  You created a trigger to execute the function using DynamoDB streams, which are created when data changes in a DynamoDB table.  In this case, the stream was created each time a new tweet was discovered.
- **Amazon Alexa**:  For the user interface, you created an Alexa skill using the skill template provided to you (JSON file).  You wired the skill to your Lambda Alexa function using a Lambda trigger.  

## Next Steps
Through this workshop, you gained hands-on experience and a general understanding of the AWS services available to you for developing and deploying an Alexa Skill.   Using just a handful of AWS services, you easily composed a fully functioning business application in a matter of hours.  Additional training and workshops are available for you to gain a deeper understanding of each service.  Perhaps you’re ready to POC some new application for your organization.  You could build upon this workshop to create a POC or look online for other CloudFormation and SAM templates and AWS quickstarts.  Your AWS Account team is here to help.  Thanks and Happy Building!
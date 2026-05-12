# Using CloudFront with Your EC2 Flask App
 
---
 
## Background
 
### Why CloudFront at All?
 
Right now, your setup looks like this:
 
```
User (anywhere in the world) ──────────────────→ EC2 instance (one physical location)
```
 
Every single request — whether the user is in Iowa or Tokyo — travels all the way to your EC2 server, waits for Flask to process it, and then the response travels all the way back. The further the user is, the slower it feels.
 
CloudFront fixes this by putting edge locations (AWS data centers) all over the world in between:
 
```
User (Tokyo) → CloudFront edge (Tokyo) → (maybe) EC2 origin (Iowa)
User (London) → CloudFront edge (London) → (maybe) EC2 origin (Iowa)
```
 
The key word is "maybe" — if the edge location already has a cached copy of what the user wants, it never bothers your EC2 at all. It just serves the response instantly from nearby.
 
---
 
### What is Caching and Why Does it Matter?
 
When CloudFront fetches something from your EC2 origin (a page, an image, a CSS file), it stores a copy at the edge location for a period of time. The next user who requests the same thing gets that copy — no round trip to EC2 needed.
 
This matters for three reasons:
 
- **Speed** — the edge location is physically closer to the user
- **Load** — your EC2 and Flask app handle far fewer requests
- **Cost** — CloudFront's outbound data rates are cheaper than EC2's
However, caching has a tradeoff: if your app returns different content per user (e.g. a logged-in dashboard, a personalized feed), you don't want CloudFront caching and serving one user's page to another. So it is important to ensure that dynamic content is not cached.
 
---
 
### What is an "Origin"?
 
In CloudFront terminology, your **origin** is the source of truth — the place CloudFront goes to fetch content when it doesn't have a cached copy. In your case, that's your EC2 instance on port 8080 or whichever port you are choosing to run it on.
 
CloudFront sits in front of your origin. Users never need to know your EC2 even exists.
 
---
 
### What About HTTPS?
 
CloudFront allows HTTPS to be used for free even if the origin is HTTP. The user gets a secure connection.
 
---
 
### What Will Actually Change for Your Flask App?
 
Honestly, very little on the EC2 side. Flask keeps running exactly as it is. The only changes are:
 
1. You create a CloudFront distribution pointing at your EC2
2. You (optionally) use the `*.cloudfront.net` URL instead of your EC2 URL
3. You think about which routes should be cached and which shouldn't
That last point is the most important one for a Flask app, and we'll tackle it carefully when we get to the cache settings.
 
---
 
## Step 1 — Set Up IAM Permissions
 
First, let's log into the AWS console on our root account and set up IAM permissions for our IAM user.
 
1. Go to **IAM → Users →** click your project's IAM user **→ Permissions tab → Add permissions**
2. Under the permissions options section choose **"Attach policies directly"**
    ![Screenshot 2026-05-11 124424](https://hackmd.io/_uploads/ryhj4-bJze.png)
3. Under the permission policies section search for **CloudFrontFullAccess** and select the checkbox
    - This will ensure that your IAM user has the permissions needed to set up CloudFront
4. Click **Next** to go to the review page and then click **Add permissions**
---
 
## Step 2 — Create the CloudFront Distribution
 
Now let's go make the CloudFront distribution.
 
1. First logout of the root account and into the IAM user you just gave CloudFront permissions to
2. At the top search bar type in **CloudFront** and select the option that appears
3. Go to the **Distributions** tab and select **Create distribution**
4. You'll be brought to step one of six. Make sure to click on the free plan for step one and then select **Next**
    ![Screenshot 2026-05-11 130729](https://hackmd.io/_uploads/S1o-rZbJfl.png)
5. Type in a name for your distribution (e.g. "CloudfrontDistribution-1") and then scroll down and select **Next**
### 2a — Configure Your Origin
 
Now you will be setting up your origin.
 
- For **Origin type** select **Other**
- Under **Custom origin** put your EC2's public DNS name (e.g. `ec2-XX-XX-XX-XX.compute-1.amazonaws.com`)
    - This is important because this is the address CloudFront uses to reach your EC2 instance when it needs to fetch new content
- Next select **Customize origin settings** under the Settings section. A number of items will then appear in a dropdown:
    - Select **HTTP only** because your Flask app has no HTTPS certificate. This is telling CloudFront that the origin is HTTP, but the endpoint that it spits out will still end up being HTTPS
    - For **HTTP port** type in the number of the port that your app is on (e.g. `8080`). Make sure it matches your application
    - Leave everything else as is
- You can now select **Next** to go on to the next part of the setup
### 2b — Configure Security (WAF)
 
Here you will see the **Web Application Firewall (WAF)** section. Make sure to turn on rate limiting to help protect against an excessive number of requests. You can leave the number at the default value.
 
![Screenshot 2026-05-11 162524](https://hackmd.io/_uploads/B1krHZ-yMl.png)
 
- Remember that this may block some IP addresses if requests exceed a certain amount. You can always go back and increase or decrease the limit from the default if necessary, but for most applications the default is more than enough
That's all you need for the security page, so go and click on the **Next** button to continue.
 
### 2c — Review and Create
 
Now you should be on the review page. Double check that all the settings match what you selected before and click **Create distribution** at the bottom.
 
You should be brought to the page for the distribution you just made. Make one last check that it shows the free plan under billing — you don't want surprise charges later. It might take a second for it to load.
 
![Screenshot 2026-05-11 163245](https://hackmd.io/_uploads/SJRtr--1zx.png)
 
Now at every CloudFront edge location available to the free tier, any requests to your distribution will send a signal back to your main EC2 address on the port you gave it!
 
Go back to the **Distributions** section on the sidebar and once the status says **Enabled** it is up. You can go copy the address under the domain name column and it should bring you to your web application, which is now HTTPS rather than HTTP — that means CloudFront handled the SSL certificate all on its own for you!
 
Try it out and make sure everything works the same as when you just use your EC2's public DNS directly.
 
---
 
## Step 3 — Verify CloudFront is Working
 
Now, let's look behind the hood a little to make sure it's working correctly rather than just passing requests all the way through to your EC2 every time.
 
1. Go into your browser's inspect mode on the CloudFront URL you just visited by either right clicking on the page and selecting **Inspect** or using **F12**
2. Then go to the **Network** tab and reload the page
    - Make sure the **"All"** tab is selected — if it is not then it might filter out what we are looking for
3. After you reload the page with the Network tab open you should see a number of items populate. Select the one that matches your domain name or is shown as `"/"`
4. Select the **Headers** tab and scroll down to the response headers section
5. You should see under `X-Cache` or `cf-cache-status` something like **"Miss from cloudfront"** — it means CloudFront didn't have a cached copy and forwarded the request to your main EC2 port
    - This is expected because Flask expects content to be dynamic and therefore won't cache it
6. Now look at your CSS or Bootstrap item in the Network tab. It should have something like **"Hit"** next to `X-Cache` or `cf-cache-status` because these are items not expected to be dynamic. If you see this, then it means CloudFront is working as expected (it's ok if you don't see this yet, we'll do a more thorough check next)
---
 
## Step 4 — Test Caching with a Static Image
 
Just to make sure it is working, let's add a static image to our Flask application to see if it caches it properly.
 
1. Start by making sure there is a `static` folder in your main directory with the image you want to use in it
2. When you implement the image make sure you reference it like this:
    ```html
    src="{{ url_for('static', filename='yourImage.jpg') }}"
    ```
    It needs that `static` label to be recognized properly and cached by CloudFront.
3. Here is a sample of how the image is implemented in my landing page:
    ```html
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Landing Page</title>
            <!-- Bootstrap CSS -->
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            <div class="container">
                <h1 class="mt-5">Welcome To The Shop</h1>
                <a href="/SignInPage" class="btn btn-primary">Sign In</a>
                <a href="/SignUpPage" class="btn btn-primary">Sign Up</a>
                <img src="{{ url_for('static', filename='kasaneTeto.jpg') }}" class="mt-4 d-block" alt="Kasane Teto" style="max-width: 100%;">
            </div>
        </body>
    </html>
    ```
    ![Screenshot 2026-05-11 180758](https://hackmd.io/_uploads/Hyiv_-ZJfe.png)
4. You will also have to add the following line right under where you have `app = Flask(__name__)` in your main Flask app file:
    ```python
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
    ```
    Here is an example of how that looks:
    ```python
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year in seconds
    ```
5. Once you have that, push it to your main repository and pull it to your EC2 to implement the changes
6. Now once you see the image on your CloudFront URL, open the Network tab again in inspect mode and select your static image from the items that appear
7. You may still see **"Miss from cloudfront"** under `X-Cache` or `cf-cache-status`. That's ok — just hard reload the page once or twice with **Ctrl+Shift+R** and it should change to **"Hit from cloudfront"**. That means it is successfully being cached in CloudFront. Congratulations!
---
 
## Step 5 — Cache Invalidations
 
Now, there are a few things to be wary of. Once an item is cached in CloudFront, CloudFront won't check the main EC2 for it until it reaches its cache-control expiration. But that could be an issue if those static items change within that time — the user would still see the old unchanged items until the expiration is reached, which could be quite a while.
 
To deal with this, we'll look at how to use **Invalidations** to ensure that CloudFront grabs the updated items.
 
1. First, let's change that picture. Replace your static image with a new one with the exact same name. Once you pull the change to your EC2 it should show up on your EC2 public DNS at the port your app is on (**make sure to hard refresh with Ctrl+Shift+R**), but on your CloudFront URL you will still see the old image
    ![Screenshot 2026-05-11 195342](https://hackmd.io/_uploads/rywQ2ZbyMe.png)
    *The EC2 URL*
    ![Screenshot 2026-05-11 195356](https://hackmd.io/_uploads/SkJW3-ZJMe.jpg)
    *The CloudFront URL*
2. You need to get CloudFront to wipe any local caches of this static file so that it has to grab it again from the main EC2 instance — this will lead to it grabbing the new updated file
3. To do this, go to your CloudFront distribution that you just made for this tutorial. Go over from your **General** tab and click on the **"Invalidations"** tab
    ![Screenshot 2026-05-11 200027](https://hackmd.io/_uploads/rkO3TW-Jfx.png)
4. Click on the **"Create invalidation"** button
5. In the **"Object paths to invalidate"** box type in the path to the file you want to wipe from any CloudFront caches:
    - For a single file: `/static/yourImage.jpg`
    - For everything in the static folder: `/static/*`
6. Once you have typed in the path simply click **"Create invalidation"** and it will wipe that path from local CloudFront caches. Once it shows that it has completed go and hard reload the page on your CloudFront URL and it should be up to date again with your EC2 instance
> **Remember:** This needs to be done each time you make changes to anything cached by CloudFront.
 
---
 
## Step 6 — Automate Invalidations with GitHub Actions
 
Last, we'll set up a GitHub Action that automatically runs an invalidation on any changed files. That way you don't have to worry about it and can just work on your application.
 
### 6a — Add GitHub Secrets
 
Go to your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**, and add:
 
| Secret | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | Your IAM user's access key |
| `AWS_SECRET_ACCESS_KEY` | Your IAM user's secret key |
| `CLOUDFRONT_DISTRIBUTION_ID` | Your distribution ID (found in the CloudFront console, looks like `EXXXXXXXXXXXX`) |
 
### 6b — Update Your deploy.yml
 
Now we just have to add some code to our `deploy.yml` file in our repository's `.github/workflows` folder. If it doesn't exist yet, add it. The full updated file looks like this:
 
```yaml
name: Deploy to EC2
 
on:
  push:
    branches:
      - main
 
jobs:
  deploy:
    runs-on: ubuntu-latest
 
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 2
 
      - name: Set up SSH key
        run: |
          mkdir -p ~/.ssh
          printf '%s\n' "${{ secrets.EC2_PRIVATE_KEY }}" > ~/.ssh/deploy_key
          chmod 600 ~/.ssh/deploy_key
          ssh-keyscan -H ${{ secrets.EC2_HOST }} >> ~/.ssh/known_hosts
 
      - name: Deploy to EC2
        env:
          HOST: ${{ secrets.EC2_HOST }}
          USER: ${{ secrets.EC2_USER }}
        run: |
          ssh -i ~/.ssh/deploy_key \
              -o StrictHostKeyChecking=no \
              -o ServerAliveInterval=60 \
              $USER@$HOST bash -s << 'REMOTE'
          cd ~/cs178-flask-app
          git pull origin main
          pkill -f "python3 flaskapp.py" || true
          sleep 2
          nohup python3 flaskapp.py > flask.log 2>&1 &
          sleep 1
          echo "Deploy complete. Flask restarted."
          REMOTE
 
      - name: Invalidate CloudFront cache
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: us-east-1
        run: |
          CHANGED=$(git diff --name-only HEAD~1 HEAD -- static/ | sed 's|^|/|' | tr '\n' ' ')
          if [ -n "$CHANGED" ]; then
            aws cloudfront create-invalidation \
              --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
              --paths $CHANGED
          else
            echo "No static files changed, skipping invalidation."
          fi
```
 
Here's what the new steps do:
 
- **Checkout code** — allows the action to check out the repo and look at the last two commits so it can see what has changed between the most recent commit and the one before it
- **Invalidate CloudFront cache** — invalidates only the static files that have changed, forcing CloudFront to fetch them again and grab the new changes
- The other two steps (**Set up SSH key** and **Deploy to EC2**) are what pull any new changes to EC2. You can remove them if you don't want automatic pulls to EC2
### 6c — Test It
 
Once you have implemented the code and pushed it to your repository, go ahead and try replacing your image with one that has the same name again.
 
If you go to your CloudFront distribution's URL now and hard reload the page (**Ctrl+Shift+R**) you should see the changed picture without having to manually invalidate the old image.
 
---
 
## Summary
 
And that's everything. Here's a recap of what we learned and did:
 
- **Why CloudFront** — instead of every user hitting your EC2 directly, CloudFront serves content from edge locations around the world, making your app faster, reducing load on your server, and lowering bandwidth costs
- **Caching** — CloudFront stores copies of static content at edge locations so it doesn't need to fetch it from your EC2 every time. Dynamic Flask routes are not cached since Flask marks them as such by default, but static files like images and CSS are
- **IAM Permissions** — we gave our IAM user the CloudFrontFullAccess policy so it has the permissions needed to create and manage CloudFront distributions without using the root account
- **Creating a Distribution** — we set up a CloudFront distribution pointing at our EC2 instance, configuring the origin protocol as HTTP on the correct port, enabling WAF with rate limiting for basic protection, and getting a free HTTPS endpoint in return
- **Verifying Caching** — we used the browser's Network tab to confirm CloudFront was working by checking the `cf-cache-status` header for Hit and Miss responses
- **Cache Invalidations** — when a cached static file is updated, CloudFront won't pick up the change until its cache expires. Invalidations let you manually force CloudFront to clear a cached file and fetch the updated version immediately
- **Automating Invalidations** — we updated our GitHub Actions workflow to automatically detect which static files changed in each push and run an invalidation for only those files, so deployments stay in sync with CloudFront without any manual steps
 
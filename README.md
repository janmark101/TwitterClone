
# Twitter Clone

The Twitter Clone is a project aimed at creating a simplified version of the Twitter social media platform. 
This project specifically involves creating a robust API for the following features.
The backend is implemented using Django Rest Framework to handle API requests and responses.


## Features
- login and registration system 
- account verification via email
- login via gmail
- change custom name or password
- adding and deleting tweets 
- adding and deleting likes 
- adding and deleting comments
- Retweeting tweets
- following other users
- getting tweets for different variations
(tweets from followed users, liked tweets, commented tweets, etc.)



## 🛠 Built With
- Django
- Rest Framework
- PostgreSQL
- Postman
- Docker



## Installation

1. Clone the repo
```bash
git clone https://github.com/janmark101/TwitterClone.git
```

2. Create virtual environment

```bash
python -m venv <name-of-your-enviroment> 
```

* Activate the virtual environment:
Windows
```bash
.\name-of-your-enviroment\Scripts\activate
```
macOS/Linux
```bash
source name-of-your-enviroment/bin/activate
```

3. Navigate to 'Backend' directory: 

```bash
cd code/Backend
```

4. Next install all necesary libraries with this command :

```bash
pip install -r requirements.txt
```

5. Prepare the database : 
```bash
python manage.py migrate
```

6. Start the server :
```bash
python manage.py runserver
```

Navigate to `http://localhost:8000/`.

## API Endpoints 

1. Authentication:
-'POST /auth/login/' - Log in the user
-'POST /auth/logout/' - Log out the user
-'POST /auth/register/' - Register a new user
-'POST /auth/verifyacc/' - Verify the user's account
-'POST /auth/changecustomname/' - Change the custom name of the user
-'GET /auth/users/' - Retrieve the list of all users
-'GET /auth/users/{id}/' - Retrieve details of a user by user.id
-'GET /auth/followersfollowinguser/' - Retrieve followers and following users of the logged-in user.
-'POST /auth/followuser/{id}/' - Follow or unfollow user by user.id
-'POST /auth/changepassword/' - Change password 

2. api:
-'GET /api/fullapi/' - Retrieve the list of all tweets with linked likes and comments
-'POST /api/retweet/{id}/' - Retweet tweet by logged-in user
-'GET /api/tweets/' - Retrieve the list of all tweets
-'POST /api/tweets/' - Creating a new tweet
-'GET /api/tweets/{id}/' - Retrieve details of tweet by tweet.id
-'DELETE /api/tweets/{id}/' - Delete tweet by tweet.id
-'GET /api/tweetslinkedwithfollowed/' - Retrieve the list of all tweets liked, commented, created or retweeted by followed users
-'GET /api/tweetsfromfollowed/' - Retrieve the list of tweets created by followed users
-'GET /api/userstweets/' - Retrieve the list of tweets created by logged-in user
-'GET /api/userretweetedtweets/' - Retrieve the list of tweets retweeted by logged-in user

3. apiComments:
-'GET /api/comments/allcomments/' - Retrieve the list of all comments
-'POST /api/comments/allcomments/' - Creating a comment
-'GET /api/comments/commentedtweetsfromfollowed/' - Retrieve the list of tweets commented by followed users
-'DELETE /api/comments/delete/{id}/' - Delete comment by comment.id
-'GET /api/comments/usercommentedtweets/' - Retrieve the list of tweets commented by logged-in user

4. apiLikes:
-'GET /api/likes/alllikes/' - Retrieve the list of all likes
-'GET /api/likes/likedtweetsfroomfollowed/' - Retrieve the list of tweets liked by followed users
-'POST /api/likes/liketweet/' - Like or unlike tweet
-'GET /api/likes/userlikedtweets/' - Retrieve the list of tweets liked by logged-in user

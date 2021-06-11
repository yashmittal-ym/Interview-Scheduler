# Interview-Scheduler [demo-website](https://www.google.com)
* #NOTE: Heroku does not provide SMTP services so Email notifications is not supported in this demo*

### The aim of the project is to easily schedule interviews.


#### Tech Used:
- Flask
- HTML
- Bootstrap
- Flask-SqlAlchemy (for the database)
- Flask-email (for sending email)


## Installation

clone the repo by :
```sh
git clone "https://github.com/yashmittal-ym/Interview-Scheduler.git"
cd Interview-Scheduler
```

Install dependencies: 

```sh
pip install -r requirements.txt
```
update email and password in app.py (line 14 and 15) for sending emails to the user via SMTP 
# Features

- ### Add candidates
>Can add the details of a new user and also view the already existing user.
Resumes for each user should be uploaded and they can also be downloaded from the table.
An Email is send to each user on successfull registration.
Clear all database feature is also provided
![Dashboard](https://github.com/yashmittal-ym/Interview-Scheduler/blob/main/assets/candidateRegistration.jpeg?raw=true)

- ### Slots Per User
>Upon Successfull registration 5 time slots from 8:00 to 13:00 are inserted for the user in the db which can be viewed on this page
>This is realtime page and is updated whenever an interview is scheduled or deleted time slot for that user is altered accordingly
![Dashboard](https://github.com/yashmittal-ym/Interview-Scheduler/blob/main/assets/slots.jpeg?raw=true)

- ### Schedule an intervier
>We can choose two candidates for the interview all the edge cases are taken under consideration(number of user should be greater than 1 and should be distinct) 
>upon choosing the available common slots for both the candidates are shown in a table
>now the admin is required to choose from the available slots and after selecting mail will be send to both the candidates with the mentioned time slot.
![Dashboard](https://github.com/yashmittal-ym/Interview-Scheduler/blob/main/assets/Schedule.jpeg?raw=true)

- ### Upcoming interviews
>shows the list of all upcoming interviews
>option for deleting the interview is also there
![Dashboard](https://github.com/yashmittal-ym/Interview-Scheduler/blob/main/assets/upcoming.jpeg?raw=true)

# Database
> There are three tables inside the database
- ### Candidate table
![](https://github.com/yashmittal-ym/Interview-Scheduler/blob/main/assets/candidate.jpeg?raw=true)

- ### Available slot for each User table
![](https://github.com/yashmittal-ym/Interview-Scheduler/blob/main/assets/user.jpeg?raw=true)

- ### Upcoming interviews table
![](https://github.com/yashmittal-ym/Interview-Scheduler/blob/main/assets/Upcomingdb.jpeg?raw=true)

# Email Notification
![](https://github.com/yashmittal-ym/Interview-Scheduler/blob/main/assets/email.jpeg?raw=true)






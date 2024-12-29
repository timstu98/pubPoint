Start Christmas new plan:

X add actual data to myswl db -> the jsons are not necessary if i can load it up to volume

X Work on the core algorithm - take current progress and build the required parts for pubs + graphs beign moved. On this, mayve just go for the graph thing, find a leetcode solution and just start from there. How does KNN even work?




# pubPoint
pubPoint app

So npm run dev
npm install 
within frontend

## Note on docker-compose
### Volumes
docker-compose down --volumes will delte all volumes, including mysql data 



So, shouldnt be pusghing up noide_modules. Deleted front-end. 
pkg-config \

clever clouud for db\
azimutt pop the uri in and then it works and can view data
https://azimutt.app/00000000-0000-0000-0000-000000000000/00000000-0000-0000-0000-000000000000

NEW AS OF NOVEMBER 2024

I have got lots of things set-up. I should create a main 

RUNNING CODE

I need to have docker desktop open. I click on the docker dektop link to access the port. 
I have hot reload on both front end and backend. I should do docker-compose up --build for rebuilding containers and docker-compose up for turning on without rebuild.
I can view my mysql db through Mysql workbench. I have got this successfully testing.
I had the front end and backend both successfully returning.

To do:
DONE - properly sety up .env 
change .env info for db.
DONE - properly hide all the info through .enc - currently with varying levels of success have some stuff hideen but others hard coded in.
DONE - Clean out the flask + react folders. -> create new branch when doing this to not rock boat.
DONE - Set up initial databse schemas in mysql
DONE - Work out how to add initial info to mysql
DONE - set up postman area
make plan for api
DONE - do i need to put api in one folder and then other non-api backend functions somewhere ekse? does this not make sense actually, you just put everything in the api is ideal
Go through other things like tsconfigs etc and check all good. Similar iwht node_modules shortcuts etc. Should i have node_modules in the frontend? Does that make sense? maybe not
.gitignores
clangd shit??

Actual plan:
1. DONE - Make a new git branch
2. DONE - Clear out folders
3. DONE - Add initial data to mysql (learn)
4. DONE -  Make mysql mock for backend sending back json addresses
5. DONE - get return centre working
....

PROPER WEBSITE PLAN

If I was doing it properly:

First think about whether doing app or website
I would wireframe the website
I would therefore decided on pages

I would then make tickets (troll/kanban thing somewhere)
I would get some data in my databse


An aside, treat for template

Which order of attack shall I go for? Backend first maybe, so I can serve it up. 

Core Features:
Get a landing page showing a map
Allow multiple peoples adfresses to be inputted
Have an api where I can send stuff -> plan this a bit first

Rough Architecture:

To dos:


Down the line:
Proper user data base
Proper 


So have an api call where you give multiple addresses, and it gives you the centre point of these people. 

	•	Core Features: What’s the one thing you want working first?
	•	Rough Architecture: High-level decisions like tech stack and basic data flow.
	•	Basic To-Dos: A simple list of tasks for the next few days or weeks.



Previous commands to run both together using concurrently
    "start": "concurrently \"npm run start:frontend\" \"npm run start:backend\"",
    "start:frontend": "cd frontend && npm run dev",
    "start:backend": "cd backend && source venv/bin/Activate && flask run --debug"



Routes Api:
IO have chosen to use the v2 routes api as updated. 
https://console.cloud.google.com/apis/library/routes.googleapis.com?project=eng-archery-442218-t3 -> go here to enable your api, maybe just for my accopunt or whatevcrtr 
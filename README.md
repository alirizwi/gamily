# Gamily - The ultimate framework for gamifying any web application in minutes. ;)

## Technologies used:
 - Python
 - Flask
 - Ember.js
 - MySQL
 - Nginx
 
 
### Work completed:
- Added functionality of Hooks, so that any user can now send a POST request to the Hooks API “/hooks” with data: {“hook_name”:__, “username”: __}. The API will first get all the events listening to the hooks and then for each event all the rules depending on that event will be found out. Then using parameters “gde_type”, “actions”, “value” and “username”, the action will be taken.
- Created Events and Hooks models, routes in the backend code and tables in the database.
- Added a form to the frontend to create rules for the GDE instances, which included creating events API in the backend to list all the events and action API’s for the GDE instances to list all the actions for that instance.
- Created Rules model and routes to handle CRUD requests in the backend. 
- Created and linked mySQL database to the code to be used by different components of the code.
- Linked frontend code which is written in Ember.js to the backend code and added functionality to do CRUD operations from the user interface.
- Created CRUD(Create, Read, Update and Delete) API’s for GDE and the modules badges and leaderboard. Linked frontend code which is written in Ember.js to the backend code and added functionality to do CRUD operations from the user interface.

### Work required to be done:
- Create GDE buckets based on the similarities of the GDE’s. GDES's include avatar, points, medals, levels, rewards, progress bar, etc.
- Convert all GDE elements into Ember components.
- Generalise the events in the rule engine to extend it to any application.
- Integrate with a fully fledged web application.


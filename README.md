## Toogethr Assignment - Parking Lot
#### ``A simple web application for handling reservation in a parking lot``

### Services
* #### Frontend application in `frontend` directory.
* #### Backend application in `backend` directory.
* #### Database in a docker container.

for frontend and backend applications you can find the README file in their directories.

### Stack
* ##### Frontend: React
* ##### Backend: Django, Django Rest Framework, PostgreSQL

### Running backend services in docker
Simply run `docker-compose up -d --build --force-recreate` in this directory!

### Improvements
* #### Frontend:
    *   Adding frontend to docker container
    *   Changing the UI based on a good design
    *   Better notifications for user
    *   Breaking the components to smaller components
    *   Adding slot management page
    *   Adding user profile page
    *   Adding sortBy feature to the tables
    *   Adding admin pages
* #### Backend:
    *   Adding more ordering, filtering and searching fields to the api endpoints
    *   Some endpoints for reporting the slots availability during the day
    *   Suggest time windows close to the user desired time window if there is no slot available
    *   Run backend behind `gunicorn`, `uWSGI` served by `Nginx` or `Apache`.
    *   Customize admin theme for `Django Rest Framework`
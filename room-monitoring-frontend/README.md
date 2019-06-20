# room-monitoring-frontend

This project was created to use alongside [room-monitoring-backend](https://github.com/heidinv12/room-monitoring-backend). The images below show what the frontend looks like:

![](/media/frontend_forms.PNG)
![](/media/frontend_tables.PNG)

In here ```createConfigData``` endpoint from [room-monitoring-backend](https://github.com/heidinv12/room-monitoring-backend) is used to create new temperature and humidity configurations. 

```createPhoneData``` is used for the Add Phone form.

The data in the tables are obtained by doing a GET request on ```getData``` also from [room-monitoring-backend](https://github.com/heidinv12/room-monitoring-backend)

**To run the frontend:**
- Download or copy repo
- In the root folder, run ```yarn install```
- Once al dpeendencies have been isntalled, run ```npm install```
- open a browser and go to ```http://localhost:9000/``` or ```http://127.0.0.1:9000/```

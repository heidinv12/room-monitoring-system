# room-monitoring-system

This repo contains all the components that define this project, along with their respective README files.

## Summary

- **room-monitoring-sys:** arduino component built in C++.

- **room-monitoring-serial-comm:** this script connects to a serial USB port to extract data outputted by the arduino board. Built with python.

- **room-monitoring-backend:** built a serie of Lambda functions and configuration files with python and Serverless Framework. Interfaces with both serial communicator and Frontend. Raw data acquired from the serial communicator is stored in S3, while the data 
obtained from the frontend is saved in DynamoDB.

- **room-monitoring-frontend:** built with Javascript. Displays sensor data and allows users for a way to register their phone number to receive alerts.

For a more detailed description, check the README file in each component's folder.

# HR Application
This project stores Company Employees and Designation related data into the Database (MySQL). This application is a network-based application built using a layered architecture.

## Layered Architecture
### Data-Layer
This layer automates the CRUD operations on the Database. The separate operations are treated as separate functional entities while maintaining the core structure of data.

### Business-Layer
This layer is for connecting the Data-Layer to the Server-side while connecting the CLI to the client-side. The Network Connection is also automated.

### Network-Layer
This layer deals with the transfer of data between server and client. Here requests and responses are dealt with using separate classes. The data transfer utilizes JSON format. Also, Wrapper classes transfer data within the network.


## How to run?
* Clone the repository
* Create a file named _dbconfig.xml_ which should consist of your Database credentials (An example file given in the repository).
* The Server Port Number is 5500
* Open a terminal, start the server by executing the command:
> python HRServer.py
* Now open separate terminals for each client and execute the program using the command:
> python HRApplication.py


## Output Expectations
Output is the CLI Menu used to perform specific operations and asks for desired inputs according to the operational needs.

### Language
* **Programming Language : Python 3.8.5**
* **Version Control : Git**

### Author
_Sarthak Kale_
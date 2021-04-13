# HR Application
The project is aimed to store a Company Employees' personal data and Designation related data into the Database (MySQL). This is a network application which is built using layered architecture.

# Layered Architecture
### Data-Layer
This is the layer which automates the CRUD operations on Database. The separate operations are treated as separate functional entities while maintaining the core structure of data.

### Business-Layer
This is the layer which is used for connecting the Data-Layer to the Server side while connecting the CLI to the client side. This is also done by automation of the Network Connection.

### Network-Layer
This is the architecture layer which deals with the transfer of data between server and client. Here requests and responses are dealed using separate classes and the data transfer utilize JSON format. Also special Wrappers are used to transfer data within the network.


# How to run?
* Clone the repository
* Create a file named "dbconfig.xml" which should consist your Database credentials (An example file is given in the repository).
* The Server Port Number is 5500, make sure it is not occupied.
* Open a terminal and execute HRServer.py, this starts the server. (python HRServer.py)
* Now open separate terminals for each client and execute HRApplication.py to execute the program. (python HRApplication.py)


## Output Expectations
Output is the CLI Menu which is used to perform specific operations and askes for desired inputs according to the specific operational needs.

### Language
Programming Language : Python 3.8.5
Version Control : Git

### Author
Sarthak Kale
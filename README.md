# CS_6400_Movie_Recommender_Project
###### Team Members: Jiecheng Lu (ML), Guanchen Meng (Frontend), Lifeng Tang (Backend)

##### Model Training README File:
https://github.gatech.edu/ltang62/CS_6400_Movie_Recommender_Project/blob/main/machine_learning/README.md

##### Project Goal:<br> 
- To experiment with the Milvus vector database<br>
- To compare the speed of storing data between Milvus and MySQL<br>
- To compare the speed of similarity search between Milvus and MySQL

##### Prerequisites
1. Install MySQL workbench
   1. https://dev.mysql.com/downloads/workbench/
2. Install Docker Desktop
   1. https://www.docker.com/products/docker-desktop/
3. Install Milvus
   1. https://milvus.io/docs/install_standalone-docker.md
4. Install Node Package Manager
   1. https://www.npmjs.com/package/npm
5. Install Python Flask
   1. https://flask.palletsprojects.com/en/2.2.x/installation/
   
##### Run the application
1. Navigate to the project folder
    ![navigate](https://github.gatech.edu/storage/user/37340/files/046470b6-af73-4d15-b653-39693146c792)<br><br><br>
2. Start Docker Desktop<br><br>
3. Go back to your terminal and run "docker-compose up -d" **to start Milvus.**
   1. **Note: this step assumes that you installed Milvus in the project folder. If you installed Milvus somewhere else, you need to navigate to that folder first.**
   ![image](https://github.gatech.edu/storage/user/37340/files/4941bda6-32df-46db-95f3-d02cf84f71cc)<br><br>
4. Now, it's time to store some user and movie feature data into both MySQL and Milvus. <br><br>
5. Before you can store data into MySQL, open the project using an IDE and find the "store_db_mysql.py" file.
![image](https://github.gatech.edu/storage/user/37340/files/6f928e15-0b51-4bc1-9aee-6f63d82db517)<br><br>
6. Go all the way to the bottom of the file and type in your MySQL localhost password.
![image](https://github.gatech.edu/storage/user/37340/files/ff209980-01ca-4675-91bd-2a732f8e2d09)<br><br>
7. Now, to store data into MySQL, run "python store_data/store_db_mysql.py," and **this will take some time.**
![image](https://github.gatech.edu/storage/user/37340/files/a625ff8a-635d-43fb-9142-741463602276)<br><br>
8. To store data into Milvus, run "python store_data/store_db_milvus.py." Again, this will take some time.
![image](https://github.gatech.edu/storage/user/37340/files/22f86730-f91e-4a7e-bdd7-80502b5aebe3)<br><br>
9. After the data has been stored, turn on the Flask backend by running "python server/app.py."
![image](https://github.gatech.edu/storage/user/37340/files/d579e2f2-98fa-4c9e-8e02-94478ed3fd93)<br><br>
10. To run the frontend, first, you need to install all the dependencies. Open another terminal to navigate to the "frontend" folder.
![image](https://github.gatech.edu/storage/user/37340/files/47aca69a-6fbf-4771-9daf-17d7614ecaa6)<br><br>
11. You need to install all the dependencies before running the frontend. To do that, run "npm install."
![image](https://github.gatech.edu/storage/user/37340/files/a2f2ba99-5d91-4839-880a-86107d50a7e8)<br><br>
12. Now we have to build the front end. Run "next build."
![image](https://github.gatech.edu/storage/user/37340/files/96cabee2-3990-4d36-84b1-17b5d3cf72da)<br><br>
13. Now, to turn on the front end, run "npm start."
![image](https://github.gatech.edu/storage/user/37340/files/71da30ba-4e22-4759-b7aa-89d68b0470c5)<br><br>
14. Open a browser and type the url "http://localhost:3000" to see the application.
![image](https://github.gatech.edu/storage/user/37340/files/9006d3d7-d140-4028-aad7-0286105e211c)<br><br>









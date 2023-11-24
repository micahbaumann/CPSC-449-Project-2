# CPSC 449 Project 2
* [Project Document](https://docs.google.com/document/d/1Dua9mpu3WIoa9oAZroRN0IWxMeS5wWCzW0SCJ0cQGHY/edit?usp=sharing)

## Updating the Databases
1. Write the SQL. For the enroll service, write it in `enroll/var/catalog.sql`. For the user service, write it in `users/var/users.sql`.
2. Go into the directory that the sql file is in:  
   For enroll:
   ```bash
   cd enroll/var
   ```
   For users:
   ```bash
   cd users/var
   ```
3. Run `updateDB.sh` for users service:
   ```bash
   ./updateDB.sh
   ```
   Run `catalog.py` for enroll service:
   ```bash
   python3 catalog.py  //Ensure dynamodb is running
   ```
4. When the SQLite CLI opens, enter `.quit`.

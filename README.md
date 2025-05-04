# User-Management-Database
A SQL database designed for managing user accounts, roles, and login history in web or enterprise applications. This project supports key authentication features such as role-based access control, account status tracking, and login activity logging, demonstrating secure and scalable database design.

# User Management Database

## Overview
This SQL project models a user management system commonly used in web applications or admin panels. It handles core functions like user registration, role assignment, account status, and login history. This database is designed with scalability and account security in mind.

## Database Schema
Key tables:
- **Users**: Stores user credentials and profile data.
- **Roles**: Defines user roles (e.g., admin, editor, viewer).
- **User_Roles**: Manages many-to-many relationships between users and roles.
- **Login_History**: Logs user login activity including timestamps and IP addresses.
- **Account_Status**: Tracks whether an account is active, suspended, or locked.

import cherrypy
import pymysql
import bcrypt

# Set up the MySQL connection
conn = pymysql.connect(
    host='localhost',      # Your MySQL host
    user='root',           # Your MySQL root user
    password='Kelsey2003!', # MySQL password
    database='user_management_db'  # The database name
)
cursor = conn.cursor()

# Define a CherryPy application class
class UserAuthApp:

    @cherrypy.expose
    def index(self):
        return """
            <h1>User Authentication System</h1>
            <h2>Register a New User</h2>
            <form method="post" action="register">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" required><br>
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="Register">
            </form>

            <h2>Log a Fake Action</h2>
            <form method="post" action="log_action">
                <label for="username_action">Username:</label><br>
                <input type="text" id="username_action" name="username" required><br>
                <label for="action_description">Action:</label><br>
                <input type="text" id="action_description" name="action_description" placeholder="Enter action here" required><br><br>
                <input type="submit" value="Log Action">
            </form>
            
            <p>Use <a href='/show_actions'>/show_actions</a> to view all logged user actions.</p>
        """

    @cherrypy.expose
    def register(self, username, password):
        try:
            query = "INSERT INTO userauthentication (username, password_hash) VALUES (%s, %s)"
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(query, (username, hashed_password))
            conn.commit()
            return "User registered successfully!"
        except Exception as e:
            conn.rollback()
            return f"Error: {e}"

    @cherrypy.expose
    def log_action(self, username, action_description):
        try:
            # Retrieve user ID based on username
            query = "SELECT user_id FROM userauthentication WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            
            if result:
                user_id = result[0]
                # Log the action in the UserActions table
                insert_action_query = "INSERT INTO useractions (user_id, action_description,action_timestamp) VALUES (%s, %s, NOW())"
                cursor.execute(insert_action_query, (user_id, action_description))
                conn.commit()
                return "Action logged successfully!"
            else:
                return "Error: User not found!"
        except Exception as e:
            conn.rollback()
            return f"Error: {e}"

    @cherrypy.expose
    def show_actions(self):
        try:
            query = "SELECT * FROM useractions"
            cursor.execute(query)
            actions = cursor.fetchall()
            action_list = "<br>".join(f"User ID: {row[1]}, Action: {row[2]}, Time: {row[3]}" for row in actions)
            return f"<h1>User Actions</h1><div>{action_list}</div>"
        except Exception as e:
            return f"Error: {e}"

# Close the cursor and connection when the app is stopped
def close_resources():
    if cursor:
        cursor.close()
    if conn:
        conn.close()

# Start the CherryPy server
if __name__ == '__main__':
    cherrypy.engine.subscribe('exit', close_resources)  # Ensure resources are closed on exit
    cherrypy.quickstart(
        UserAuthApp(), '/',  # Mount the UserAuthApp class as the root application
        {
            'global': {
                'server.socket_host': '0.0.0.0',  # Listen on all interfaces
                'server.socket_port': 8080,       # Or your desired port
            },
            '/': {
                'tools.sessions.on': True,        # Enable sessions if needed for authentication
            }
        }
    )

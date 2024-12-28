# Chat App
#### Video Demo:  
#### Description: 

The Chat App is a real-time messaging platform built using Flask, a lightweight web framework for Python, and Flask-SocketIO, which enables real-time communication between clients and the server. The application allows users to register, log in, send messages, and view online users in a chat room. It utilizes SQLite as the database for storing user credentials and messages, ensuring a lightweight and easy-to-manage data storage solution.

## Key Language/Framework Used

- **Flask**: A micro web framework for Python that provides the necessary tools to build web applications.
- **Flask-SocketIO**: An extension that enables real-time communication between clients and the server using WebSockets.
- **SQLite**: A lightweight, serverless database engine used for storing user data and chat messages.
- **HTML/CSS/JavaScript**: Standard web technologies for building the user interface and handling client-side interactions.
- **Werkzeug Security**: A library for securely hashing passwords and verifying user credentials.
- **Jinja**: A templating engine for generating HTML templates with dynamic content.

## Application Structure

The application is structured into several key components:

1. **Database Initialization**: The `init_db` function creates two tables in the SQLite database:
   - `users`: Stores user information, including a unique username, hashed password, online status, and a color identifier for message display.
   - `messages`: Stores chat messages, including the sender's ID, message content, and timestamp.

2. **User  Authentication**: The application provides user registration and login functionalities:
   - **Registration**: Users can create an account by providing a username and password. The username is sanitized to prevent XSS attacks, and the password is hashed before storage.
   - **Login**: Users can log in using their credentials. The application verifies the hashed password and sets session variables to track the logged-in user.

3. **Chat Functionality**: Once logged in, users can access the chat room:
   - **Message Sending**: Users can send messages that are stored in the database and broadcasted to all connected clients using SocketIO.
   - **Real-time Updates**: The application uses SocketIO to handle real-time message broadcasting and user connection updates.

4. **User  Interface**: The front-end is built using HTML templates rendered by Flask:
   - **Chat Room**: Displays messages with the sender's username and timestamp. Users can select a recipient from a dropdown menu to send direct messages.
   - **Online Users List**: Shows a list of users currently online, allowing for easy identification of active participants in the chat.

5. **Session Management**: The application uses Flask's session management to keep track of logged-in users.

## Security Measures

The application also implements several security measures to protect user data and prevent common web vulnerabilities:

- **Password Hashing**: User passwords are hashed using Werkzeug's security functions.
- **Input Sanitization**: User inputs are sanitized using the Bleach library to prevent XSS attacks.
- **Session Management**: The application checks for user authentication before allowing access to the chat room.

## Real-time Communication with SocketIO

Flask-SocketIO is a crucial component of the application, enabling real-time communication. Key features include:

- **Event Handling**: The application listens for various events, such as user connections, disconnections, and message sending.
- **Broadcasting Messages**: When a user sends a message, it is emitted to all connected clients.
- **Notification System**: The application includes a notification system that alerts users of new messages.

## User Experience

The user experience is designed to be intuitive and engaging:

- **Responsive Design**: The application uses Bootstrap for responsive design.
- **Notification Sounds**: Users receive audio notifications for new messages.
- **User  Customization**: Each user is assigned a unique color ID for message display.

## Future Enhancements

I plan to work on the following enhancements in the future:

- **Private Messaging**: Implementing a feature for private messaging between users.
- **User  Profiles**: Allowing users to customize their profiles with avatars and status messages.
- **Message History**: Storing and displaying message history for users to view past conversations.

## Conclusion

The Chat Application serves as a solid foundation for real-time messaging and can be expanded with additional features to enhance user engagement and functionality.
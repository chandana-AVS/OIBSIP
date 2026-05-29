# Oasis Secure Chat Application

## Overview

Oasis Secure Chat Application is a real-time desktop messaging system built using Python socket programming and Tkinter.

The application enables multiple clients to communicate simultaneously through a graphical user interface while ensuring secure encrypted communication using SSL. It also supports persistent chat history, allowing previous messages to be viewed even after the server is stopped and restarted.

---

## Features

### Graphical User Interface (GUI)

- User-friendly desktop interface built with Tkinter
- Simple chat window for sending and receiving messages
- Easy interaction without command-line complexity

### Multi-Client Communication

- Supports multiple clients connected to the server at the same time
- Real-time message exchange between all connected users

### Secure Communication

- End-to-end encrypted communication using Python SSL library
- Protects transmitted messages from interception

### Document Sharing

- Allows file/document sharing between connected clients

### Persistent Chat History

- Messages are stored locally
- Previous chat history remains accessible even after:
  - Server shutdown
  - Client disconnection
  - Server restart

### Message Notifications

- Users receive instant notifications when new messages are received
- Helps users stay updated even when not actively typing
- Improves real-time communication experience   

### Emoji Support

Includes limited emoji support for enhanced interaction.

Supported examples:

- 😊
- ❤️
- 👍
- 🔥
- 🎉

---

## Technologies Used

- Python
- Socket Programming
- Tkinter
- SSL Library
- SQLite
- Multithreading

---

## Project Structure

```plaintext
server.py
client.py
users.db
server.crt
server.key
README.md
```

---

## How to Run

### Start the Server

```bash
python server.py
```

### Start the Client

```bash
python client.py
```

Multiple clients can be launched simultaneously.

---

## Learning Outcomes

This project helped in understanding:

- Client-server architecture
- Socket programming
- SSL encryption implementation
- GUI development using Tkinter
- Database persistence
- Multithreading
- Secure communication systems

---

## Future Improvements

- Advanced emoji support
- File preview before sharing
- User authentication system
- Private messaging
- Improved chat customization

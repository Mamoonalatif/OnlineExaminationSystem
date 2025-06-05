import pandas as pd  
import socket       
import threading   
import json         
import os          

CSV_FILENAME = "questions.csv"       
SCORES_FILENAME = "student_scores.csv"  

def authenticate_user(username, password, user_type):
    filename = "Student.txt" if user_type == "Student" else "Admin.txt"
    print(f"Authenticating from file: {filename}")
    if not os.path.exists(filename):
        print("User file not found.")
        return False
    with open(filename, "r") as f:
        for line in f:
            stored_user, stored_pass = line.strip().split(",")
            if username == stored_user and password == stored_pass:
                print("Credentials matched.")
                return True
    return False  

def register_user(username, password, user_type):
    file_name = "Admin.txt" if user_type == "admin" else "Student.txt"
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            for line in f:
                existing_user, _ = line.strip().split(",", 1)
                if existing_user == username:
                    return False 
    with open(file_name, "a") as f:
        f.write(f"{username},{password}\n")
    return True

def load_data():
    if os.path.exists(CSV_FILENAME):
        return pd.read_csv(CSV_FILENAME)
    else:
        return pd.DataFrame(columns=["ID", "Text", "Options", "CorrectAnswer", "Concept", "Difficulty", "Course"])


def save_data(df):
    df.to_csv(CSV_FILENAME, index=False)

# Receive a full message from the client connection
# Handles partial TCP data packets by buffering until valid JSON is formed
def receive_full_message(conn):
    buffer = b""
    while True:
        part = conn.recv(4096)  # Receive up to 4096 bytes
        if not part:  # No more data, connection closed
            break
        buffer += part
        try:
            # Attempt to decode JSON to check if complete message received
            json.loads(buffer.decode())
            break  # Full message received
        except json.JSONDecodeError:
            continue  # Continue receiving if JSON incomplete
    return buffer.decode()

# Handles an individual client connection
def handle_client(conn):
    try:
        msg = receive_full_message(conn)
        if not msg:
            return
        try:
            request = json.loads(msg)  # Parse JSON request
        except json.JSONDecodeError:
            conn.sendall(b"ERROR: Invalid JSON format")
            return

        req_type = request.get("type")  # Get the type of request
        print(f"Received request: {req_type}")

        # Handle different request types from client
        if req_type == "get_questions":
            df = load_data()
            conn.sendall(df.to_json().encode())  # Send questions as JSON

        elif req_type == "save_questions":
            try:
                new_df = pd.read_json(request["data"])
                save_data(new_df)  # Save updated questions
                conn.sendall(b"success")
            except Exception as e:
                print("Error saving questions:", e)
                conn.sendall(b"ERROR: Failed to save questions")

        elif req_type == "save_score":
            try:
                # Load existing scores or create empty DataFrame
                scores_df = pd.read_csv(SCORES_FILENAME) if os.path.exists(SCORES_FILENAME) else pd.DataFrame(columns=["Student Name", "Score"])
                # Append new score data sent by client
                scores_df = pd.concat([scores_df, pd.DataFrame([request["data"]])], ignore_index=True)
                scores_df.to_csv(SCORES_FILENAME, index=False)  # Save updated scores
                conn.sendall(b"success")
            except Exception as e:
                print("Error saving score:", e)
                conn.sendall(b"ERROR: Failed to save score")

        elif req_type == "get_scores":
            try:
                scores_df = pd.read_csv(SCORES_FILENAME) if os.path.exists(SCORES_FILENAME) else pd.DataFrame(columns=["Student Name", "Score"])
                conn.sendall(scores_df.to_json().encode())  # Send scores as JSON
            except Exception as e:
                print("Error loading scores:", e)
                conn.sendall(b"ERROR: Failed to load scores")

        elif req_type == "login":
            username = request.get("username")
            password = request.get("password")
            user_type = request.get("user_type")
            if authenticate_user(username, password, user_type):
                conn.sendall(b"success")
            else:
                conn.sendall(b"failure")

        elif req_type == "register":
            username = request.get("username")
            password = request.get("password")
            user_type = request.get("user_type")
            if register_user(username, password, user_type):
                conn.sendall(b"success")
            else:
                conn.sendall(b"fail")

        else:
            conn.sendall(b"ERROR: Unknown request type")

    except Exception as e:
        print(f"Unexpected error: {e}")
        try:
            conn.sendall(b"ERROR: Server encountered an issue")
        except:
            pass
    finally:
        conn.close()  # Always close connection when done

# Starts the server and listens for incoming connections
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket
    server_socket.bind(("127.0.0.1", 8000))  # Bind to localhost and port 9999
    server_socket.listen()  # Listen for incoming connections
    print("Server listening on port 9999...")

    while True:
        client_conn, addr = server_socket.accept()  # Accept new client
        print(f"Connected by {addr}")
        # Start new thread to handle client so server can accept others
        thread = threading.Thread(target=handle_client, args=(client_conn,))
        thread.start()

# Main entry point to start the server
if __name__ == "__main__":
    start_server()

import socket
import time

host = "192.168.137.1"
port = 7777

s = socket.socket()
s.connect((host, port))

difficulty_prompt = s.recv(1024).decode().strip()
print(difficulty_prompt)

difficulty_choice = input().strip()
s.sendall(difficulty_choice.encode())
difficulty = int(difficulty_choice)

if difficulty == 1:  # easy
    min_val, max_val = 1, 10
elif difficulty == 2:  # medium
    min_val, max_val = 1, 50
else:  # hard
    min_val, max_val = 1, 100

banner = s.recv(1024).decode().strip()
print(banner)

print("Bot is playing the game...")
current_min = min_val
current_max = max_val
attempts = 0

while True:
    guess = (current_min + current_max) // 2
    attempts += 1
    
    print(f"Bot attempt #{attempts}: Guessing {guess}")
    
    try:
        s.sendall(str(guess).encode())
        reply = s.recv(1024).decode().strip()
        print(f"Server says: {reply}")
        
        if "CORRECT!" in reply:
            print(f"Bot found the correct number in {attempts} attempts!")
            break
        elif "Guess Lower" in reply:
            current_max = guess - 1
            print(f"Adjusting range to {current_min}-{current_max}")
        elif "Guess Higher" in reply:
            current_min = guess + 1
            print(f"Adjusting range to {current_min}-{current_max}")
            
        time.sleep(0.5)
        
    except ConnectionAbortedError:
        print("Connection was closed by the server")
        break

s.close()
print("Game ended. Connection closed.")
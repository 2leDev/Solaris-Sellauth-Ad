import requests
import time
import threading

content = input("Enter the message content to send: ")

# Ask user for the number of times to send per second
per_sec = int(input("Enter how many times to send the message per second: "))

# Ask user for how long to send the message (in seconds)
duration = int(input("Enter for how many seconds to send the message: "))

# Ask user where to send the messages
target = input("Do you want to send the messages to (1) Only General, (2) Only Advertising, or (3) Both? Enter 1, 2, or 3: ")

# Prepare the headers and data for the request
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Bearer no",
    "content-type": "application/json",
    "origin": "https://beta.sellauth.com",
    "priority": "u=1, i",
    "referer": "https://beta.sellauth.com/",
    "sec-ch-ua": '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0"
}
data = {
    "content": content
}

# Function to send messages to a specific URL
def send_messages(url, headers, data, per_sec, duration, channel_name):
    start_time = time.time()
    while time.time() - start_time < duration:
        for _ in range(per_sec):
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"[+] Message Sent to {channel_name}")
            else:
                print(f"[-] Failed to send message to {channel_name}: {response.status_code}")
            # Sleep for the appropriate fraction of a second to maintain the desired rate
            time.sleep(1 / per_sec)
    print(f"Finished sending messages to {channel_name}.")

# URLs to send messages to
urls = {
    "1": ("https://api-internal.sellauth.com/v1/chat/channels/1/messages", "General"),
    "2": ("https://api-internal.sellauth.com/v1/chat/channels/2/messages", "Advertising"),
}

# Determine which URLs to send messages to based on user input
selected_urls = []
if target == "1":
    selected_urls.append(urls["1"])
elif target == "2":
    selected_urls.append(urls["2"])
elif target == "3":
    selected_urls.append(urls["1"])
    selected_urls.append(urls["2"])
else:
    print("Invalid input. Exiting.")
    exit(1)

# Create and start threads for sending messages to selected URLs
threads = []
for url, channel_name in selected_urls:
    thread = threading.Thread(target=send_messages, args=(url, headers, data, per_sec, duration, channel_name))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("Finished sending messages to all selected channels.")

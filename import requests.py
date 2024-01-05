import requests

def get_all_group_messages(group_id, access_token):
    all_messages = []
    before_id = None

    while True:
        url = f"https://api.groupme.com/v3/groups/{group_id}/messages"
        headers = {"Content-Type": "application/json", "X-Access-Token": access_token}
        params = {"limit": 100, "before_id": before_id}  # Adjust the limit as needed

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            messages = response.json()["response"]["messages"]
            if not messages:
                break

            all_messages.extend(messages)
            before_id = messages[-1]["id"]
        else:
            print(f"Error retrieving messages. Status code: {response.status_code}")
            break

    return all_messages

def get_group_members(group_id, access_token):
    url = f"https://api.groupme.com/v3/groups/{group_id}"
    headers = {"Content-Type": "application/json", "X-Access-Token": access_token}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["response"]["members"]
    else:
        print(f"Error retrieving group members. Status code: {response.status_code}")
        return None

def calculate_likes_by_user(messages):
    likes_by_user = {}

    for message in messages:
        user_id = message["user_id"]
        likes = message["favorited_by"]

        if user_id not in likes_by_user:
            likes_by_user[user_id] = {"name": "", "likes": 0}

        likes_by_user[user_id]["likes"] += len(likes)

    return likes_by_user

def main():
    group_id = "..."  # Replace with your GroupMe group ID
    access_token = "ADD YOUR OWN"  # Replace with your GroupMe access token

    all_messages = get_all_group_messages(group_id, access_token)

    if all_messages:
        members = get_group_members(group_id, access_token)
        likes_by_user = calculate_likes_by_user(all_messages)

        print("Total Likes by User:")
        for user_id, data in likes_by_user.items():
            user_name = next((member["nickname"] for member in members if member["user_id"] == user_id), "Unknown")
            total_likes = data["likes"]
            print(f"User ID {user_id}, Name: {user_name}: {total_likes} likes")

if __name__ == "__main__":
    main()

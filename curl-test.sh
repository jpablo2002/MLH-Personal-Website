#!/bin/bash

NEW_POST=$(curl -s --request POST http://localhost:5000/api/timeline_post -d 'name=Juan Pablo Acosta&email=acosta.jp@icloud.com&content=Testing endpoints with curl.') && echo "Test post created. POST request successful."

if [ "$NEW_POST" ]
then
        echo "$NEW_POST"
else
        echo "Failed to create test post. POST request failed."
        exit 1
fi

NEW_ID=$(echo "$NEW_POST" | jq -r '.id')

printf "\nCurrent Timeline Posts: \n"
CURR_POSTS=$(curl -s http://localhost:5000/api/timeline_post)
echo "$CURR_POSTS"

FOUND_POST=$(echo "$CURR_POSTS" | jq -r --argjson new_id $NEW_ID '[.timeline_posts[] | .id == $new_id] | any')

if [ "$FOUND_POST" == "true" ]
then
        echo "New post found in created posts! Success!"
else
        echo "New post not found in created posts! Something went wrong!"
        exit 1
fi

if [ "$NEW_POST" ]
then
        POSTS_LEFT=$(curl -s --request DELETE http://localhost:5000/api/timeline_post) && printf "\nTest post deleted. DELETE request successful."
        printf "\nRemaining posts: "
        echo "$POSTS_LEFT"
else
        echo "Failed to delete test post. DELETE request failed."
        exit 1
fi

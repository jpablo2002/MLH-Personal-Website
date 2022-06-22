#!/bin/bash

echo "Test Timeline Post Added:"
curl --request POST http://localhost:3000/api/timeline_post -d 'name=Juan Pablo Acosta&email=acosta.jp@icloud.com&content=Testing endpoints with curl.'

echo "Current Timeline Posts: "
curl http://localhost:3000/api/timeline_post

echo "Test Timeline Post Deleted. Current Timeline Posts: "
curl --request DELETE http://localhost:3000/api/timeline_post

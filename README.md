
Clone signald first
```
git clone https://gitlab.com/signald/signald.git
cp signald/Containerfile signald/Dockerfile
```

The Signal bot operates as a Signal user with automation. Authenticated uses with known phone numbers can send end-to-end encrypted Signal messags to trigger automated actions. This prototype is deployed alongside our Starling Integrity Backend to receive authenticated captures, where the bot would pass the uploaded files along for verification, and subsequent registration and preservation.

Backend api written with flask to handle telegram bot requests

[https://game-telegram-bot-gules.vercel.app/](https://game-telegram-bot-gules.vercel.app/)

Unable to run package causewayCameras on vercel as it involves downloading webdriver which it has no permissions to do so.

```javascript
fetch("/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ test: true }),
});
```

# Widget Fix and Page Context Implementation

I have successfully updated the widget to resolve the connection issues and implement your requested features. Here is a summary of the changes made to `widget.js` and `relay.py`.

## What Was Changed

### 1. Fixed Connection Error
The reason the widget wasn't reaching the backend was due to a Javascript syntax error (a duplicated promise `.then()` chain). I removed the duplicate code, which allows the widget to successfully fetch from the `/message` route again.

### 2. Implemented Page Reading
Instead of passing the page text in the prompt string (which would consume a lot of context and risk hitting limits), I've implemented your suggestion:
- **Widget (`widget.js`)**: The widget now extracts up to 15,000 characters from `document.body.innerText` along with the current `window.location.href`. It sends this data in the JSON payload when a message is sent.
- **Relay (`relay.py`)**: The backend receives the text and saves it as a `.txt` file locally in `chat-page/contexts/<fingerprint>.txt`.
- **AI Prompt**: I added a system note to the prompt that tells the AI: *"The user is currently viewing the page: `<url>`. The text of this page has been saved to `/root/.openclaw/workspace/chat-page/contexts/<fingerprint>.txt`. Read this file if the user asks you to summarize the page or asks questions about it."*

### 3. Added "Summarise this page" Button
I updated the predefined buttons in the widget, replacing "Show me a finding" with **"Summarise this page"**.
When you click this button, the backend natively treats it as if you typed "Summarise this page", prompting the AI to read the text document it just saved and return a summary.

## Verification
You can now test the widget on any page. When you ask it to summarize the page or ask questions about the current page, it will correctly read the saved context file and answer.

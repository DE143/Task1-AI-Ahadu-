# 💬 Simple Chat Application

A professional and attractive real-time messaging application built with Python and Tkinter.

## Features

✅ Modern chat bubble interface (like WhatsApp/Messenger)
✅ Reply to specific messages
✅ Real-time messaging between users
✅ Auto-refresh every 3 seconds
✅ Message history with timestamps
✅ Persistent storage (saves to JSON file)
✅ Smooth scrolling chat window
✅ Username customization
✅ User-friendly interface with clear visual feedback

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)

## How to Run

1. Make sure you have Python installed
2. Run the application:
   ```bash
   python chat_gui.py
   ```

## How to Use

1. **Set Your Name**: Enter your username in the "You are:" field at the top right
2. **Send Messages**: Type your message in the input box and press Enter or click the ➤ button
3. **Reply to Messages**: Click "↩ Reply" on any message bubble to reply to it
4. **Cancel Reply**: Click the ✕ button on the yellow reply indicator to cancel
5. **Auto-Refresh**: Messages automatically refresh every 3 seconds
6. **Manual Refresh**: Click "🔄 Refresh" to reload messages immediately
7. **Clear Chat**: Click "🗑️ Clear" to delete all messages

## Key Features Explained

### Chat Bubbles
- Your messages appear in blue bubbles on the right
- Other users' messages appear in gray bubbles on the left
- Each bubble shows the timestamp and a reply button

### Reply Feature
- Click "↩ Reply" on any message to reply to it
- A yellow indicator shows which message you're replying to
- The reply context appears in the message bubble
- Cancel anytime by clicking the ✕ button

## File Structure

- `chat_gui.py` - Main GUI application
- `chat_manager.py` - Backend logic for message handling
- `chat_data.json` - Stores all chat messages (created automatically)

## Features Implemented

### Backend (chat_manager.py)
- Dictionary-based message storage (user: messages)
- Add messages with timestamps and reply references
- Display recent messages (last 50)
- Save chat to JSON file with reply data
- Load chat from JSON file
- Clear all messages

### GUI (chat_gui.py)
- Modern chat bubble design (blue for you, gray for others)
- Reply functionality with visual indicators
- Auto-refresh every 3 seconds
- Smooth scrolling with mouse wheel support
- Username editor in top bar
- Large, easy-to-use message input
- Prominent send button (➤)
- Refresh and Clear buttons
- Responsive layout that adapts to window size
- Professional color scheme matching popular chat apps

## Tips

- Change your username anytime in the top right field
- Messages automatically refresh - no need to click refresh constantly
- Click "↩ Reply" on any message to create threaded conversations
- Your messages appear on the right in blue, others on the left in gray
- Scroll with your mouse wheel for smooth navigation
- Press Enter to quickly send messages
- Chat history persists between sessions

Enjoy chatting! 🎉

# Ethiopian Equb System (Multi-Group ROSCA Manager)

A professional Rotating Savings and Credit Association (ROSCA) management system built with Python and Tkinter, implementing the traditional Ethiopian Equb system with support for multiple groups and lottery-based distribution.

## What is Equb?

Equb is a traditional Ethiopian financial system where:
- A group of people contribute a fixed amount regularly (daily, weekly, or monthly)
- Each round, the total collected amount goes to one member (selected by lottery or manually)
- This continues until every member has received the lump sum once
- After a complete cycle, a new cycle begins

### Example:
- 10 people contribute 1,000 birr each month
- Total collected = 10,000 birr per round
- Each month, one person receives the 10,000 birr (lottery winner)
- After 10 months, everyone has received their share
- Cycle repeats

## Features

### Multi-Group Support
- **Multiple Groups**: Create and manage multiple Equb groups simultaneously
- **Cross-Group Membership**: Members can participate in multiple groups
- **Independent Tracking**: Each group has its own cycles, rounds, and history

### Lottery System
- **🎲 Automatic Lottery**: Random selection from eligible members with animated display
- **Manual Selection**: Optional manual recipient selection
- **Fair Distribution**: Ensures everyone receives once per cycle

### Member Management
- **System-Wide Members**: Add members once, use in multiple groups
- **Group-Specific Tracking**: Track contributions and receipts per group
- **Contact Information**: Store phone and email for each member

### Round & Cycle Management
- **Automated Rounds**: Collect contributions and distribute to winner
- **Cycle Tracking**: Automatic new cycle when all members receive
- **Status Monitoring**: Real-time tracking of who has received

### History & Reporting
- **Multi-Group History**: View history for any group
- **Detailed Statistics**: Member summaries, round history, totals
- **Data Persistence**: Automatic save/load from JSON file

### Professional Design
- **Ethiopian Colors**: Green, Gold, and Red color scheme
- **Three-Panel Layout**: Groups, Rounds, and History
- **Intuitive Interface**: Easy navigation and clear information display

## Installation

1. Ensure Python 3.x is installed
2. No additional packages required (uses built-in tkinter)

## Usage

Run the application:
```bash
cd MiniEqubApplication
python equb_gui.py
```

## How to Use

### 1. Create Groups
1. Click "➕ New Group"
2. Enter:
   - Group name (e.g., "Family Equb", "Office Equb")
   - Fixed contribution amount (ETB)
   - Frequency (Daily/Weekly/Monthly)
3. Click "Create Group"

### 2. Add Members to Groups
1. Select a group from the dropdown
2. Enter member name and phone
3. Click "➕ Add to Group"
4. Repeat for all members
5. Same member can be added to multiple groups

### 3. Run Lottery Distribution
1. Select the group
2. Click "🎲 Run Lottery & Distribute"
3. Watch the animated lottery selection
4. Confirm the winner
5. System automatically:
   - Charges all members the fixed amount
   - Pays the winner the total pot
   - Updates all records

### 4. Manual Distribution (Optional)
1. Select a group
2. Choose recipient from "Manual Selection" dropdown
3. Click "Distribute to Selected"
4. Confirm the transaction

### 5. View History
1. Use the history panel on the right
2. Select any group to view its complete history
3. See member summaries and round details

### 6. Manage Cycles
- System automatically starts new cycle when all members receive
- Or manually start new cycle with "🔄 New Cycle" button
- Delete groups with "🗑️ Delete Group" button

## Data Storage

All data is automatically saved to `equb_data.json` in the same directory.

## Key Concepts

- **Group**: An independent Equb with its own members, amount, and cycles
- **Member**: A person who can participate in multiple groups
- **Round**: One distribution event where all contribute and one receives
- **Cycle**: Complete rotation where every member receives once
- **Lottery**: Random selection of the next recipient

## Color Scheme

Ethiopian flag inspired:
- Green (#1a5f3f) - Primary
- Gold/Yellow (#ffd700) - Secondary
- Red (#c8102e) - Accent
- Blue (#2980b9) - Info

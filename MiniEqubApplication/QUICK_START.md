# Quick Start Guide - Ethiopian Equb System

## Launch the Application

```bash
cd MiniEqubApplication
python equb_gui.py
```

## First Time Setup

### Step 1: Create Your First Group
1. Click "➕ New Group" button (top right)
2. Fill in:
   - **Group Name**: e.g., "Family Equb" or "Office Equb"
   - **Fixed Amount**: e.g., 1000 (ETB per member per round)
   - **Frequency**: Daily, Weekly, or Monthly
3. Click "Create Group"

### Step 2: Add Members
1. Make sure your new group is selected in the dropdown
2. In the left panel, enter:
   - **Name**: Member's full name
   - **Phone**: Contact number
3. Click "➕ Add to Group"
4. Repeat for all members (minimum 2 members recommended)

### Step 3: Run Your First Lottery
1. Once you have at least 2 members, go to the middle panel
2. Click "🎲 Run Lottery & Distribute"
3. Watch the animated lottery selection
4. Click "✅ Confirm & Distribute" when winner is shown
5. Done! The system automatically:
   - Charges each member the fixed amount
   - Pays the winner the total pot
   - Records everything

## Key Features

### Multiple Groups
- Create as many groups as you need
- Each group operates independently
- Switch between groups using the dropdown at the top

### Cross-Group Membership
- Same person can join multiple groups
- Just add them to each group separately
- Their contributions and receipts are tracked per group

### Lottery System
- **Automatic**: Click "Run Lottery" for random selection
- **Manual**: Use "Manual Selection" dropdown if you prefer to choose

### Cycle Management
- When all members receive once = 1 complete cycle
- System automatically starts new cycle
- Or manually start with "🔄 New Cycle" button

### History
- Right panel shows complete history
- Select any group to view its records
- See who paid what, who received when

## Example Scenario

**Family Equb with 5 members, 1000 ETB monthly:**

1. Create group: "Family Equb", 1000 ETB, Monthly
2. Add 5 members: Abebe, Tigist, Dawit, Sara, Meron
3. Round 1: Run lottery → Tigist wins → Gets 5,000 ETB (5 × 1000)
4. Round 2: Run lottery → Dawit wins → Gets 5,000 ETB
5. Continue until all 5 receive
6. Cycle 2 starts automatically
7. Everyone can win again!

## Tips

- **Start Small**: Test with 2-3 members first
- **Regular Schedule**: Stick to your frequency (daily/weekly/monthly)
- **Backup Data**: Copy `equb_data.json` file regularly
- **Multiple Groups**: Create separate groups for family, work, friends
- **Fair Play**: Lottery ensures everyone has equal chance

## Troubleshooting

**Can't remove a member?**
- Members who already received in current cycle cannot be removed
- Wait for new cycle or create a new group

**Lottery not working?**
- Make sure group has at least 2 members
- Check if all members already received (new cycle needed)

**Lost data?**
- Check for `equb_data.json` file in the same folder
- This file contains all your data

## Support

For issues or questions, check the README.md file for detailed documentation.

---

🇪🇹 **Enjoy your Equb!** 🇪🇹

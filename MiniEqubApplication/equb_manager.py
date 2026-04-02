import json
import os
import random
from datetime import datetime
from typing import List, Dict, Optional

class EqubManager:
    """Manages Ethiopian Equb (ROSCA) group savings system with multiple groups"""
    
    def __init__(self, data_file: str = "equb_data.json"):
        self.data_file = data_file
        self.equb_data = {
            'groups': {},  # Dictionary of group_id: group_data
            'members': {}  # Dictionary of member_id: member_data (can be in multiple groups)
        }
        self.load_data()
    
    def create_group(self, group_name: str, fixed_amount: float, frequency: str) -> str:
        """Create a new Equb group"""
        group_id = f"group_{len(self.equb_data['groups']) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.equb_data['groups'][group_id] = {
            'id': group_id,
            'name': group_name,
            'fixed_amount': fixed_amount,
            'frequency': frequency,
            'member_ids': [],
            'rounds': [],
            'current_round': 0,
            'cycle_number': 1,
            'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_data()
        return group_id
    
    def get_all_groups(self) -> List[Dict]:
        """Get all groups"""
        return list(self.equb_data['groups'].values())
    
    def get_group(self, group_id: str) -> Optional[Dict]:
        """Get group by ID"""
        return self.equb_data['groups'].get(group_id)
    
    def delete_group(self, group_id: str) -> bool:
        """Delete a group"""
        if group_id in self.equb_data['groups']:
            del self.equb_data['groups'][group_id]
            self.save_data()
            return True
        return False
    
    def add_member_to_system(self, name: str, phone: str = "", email: str = "") -> Optional[str]:
        """Add a member to the system (not to a specific group yet)"""
        # Check if member already exists
        for member_id, member in self.equb_data['members'].items():
            if member['name'].lower() == name.lower():
                return member_id
        
        member_id = f"member_{len(self.equb_data['members']) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.equb_data['members'][member_id] = {
            'id': member_id,
            'name': name,
            'phone': phone,
            'email': email,
            'group_memberships': {}  # group_id: membership_data
        }
        self.save_data()
        return member_id
    
    def add_member_to_group(self, group_id: str, member_id: str) -> bool:
        """Add an existing member to a specific group"""
        group = self.get_group(group_id)
        member = self.equb_data['members'].get(member_id)
        
        if not group or not member:
            return False
        
        if member_id in group['member_ids']:
            return False  # Already in group
        
        group['member_ids'].append(member_id)
        
        # Initialize member's group membership data
        member['group_memberships'][group_id] = {
            'has_received': False,
            'received_round': None,
            'total_contributed': 0.0,
            'total_received': 0.0,
            'joined_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.save_data()
        return True
    
    def remove_member_from_group(self, group_id: str, member_id: str) -> bool:
        """Remove a member from a specific group"""
        group = self.get_group(group_id)
        member = self.equb_data['members'].get(member_id)
        
        if not group or not member:
            return False
        
        membership = member['group_memberships'].get(group_id)
        if not membership or membership['has_received']:
            return False  # Can't remove if already received
        
        group['member_ids'].remove(member_id)
        del member['group_memberships'][group_id]
        
        self.save_data()
        return True
    
    def start_new_round_lottery(self, group_id: str) -> Optional[Dict]:
        """Start a new round with lottery selection for recipient"""
        group = self.get_group(group_id)
        if not group or not group['member_ids']:
            return None
        
        # Get members who haven't received yet
        available_members = []
        for member_id in group['member_ids']:
            member = self.equb_data['members'][member_id]
            membership = member['group_memberships'][group_id]
            if not membership['has_received']:
                available_members.append(member_id)
        
        if not available_members:
            # All members received, start new cycle
            self.start_new_cycle(group_id)
            available_members = group['member_ids'].copy()
        
        # Lottery selection
        winner_id = random.choice(available_members)
        winner = self.equb_data['members'][winner_id]
        
        return self.start_new_round(group_id, winner_id)
    
    def start_new_round(self, group_id: str, recipient_id: str) -> Optional[Dict]:
        """Start a new round with specified recipient"""
        group = self.get_group(group_id)
        recipient = self.equb_data['members'].get(recipient_id)
        
        if not group or not recipient:
            return None
        
        membership = recipient['group_memberships'].get(group_id)
        if not membership or membership['has_received']:
            return None
        
        round_number = group['current_round'] + 1
        total_amount = group['fixed_amount'] * len(group['member_ids'])
        
        round_data = {
            'round_number': round_number,
            'cycle_number': group['cycle_number'],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'recipient_id': recipient_id,
            'recipient_name': recipient['name'],
            'amount_per_member': group['fixed_amount'],
            'total_payout': total_amount,
            'contributions': [],
            'lottery_selected': False
        }
        
        # Record contributions from all members in the group
        for member_id in group['member_ids']:
            member = self.equb_data['members'][member_id]
            contribution = {
                'member_id': member_id,
                'member_name': member['name'],
                'amount': group['fixed_amount'],
                'paid': False
            }
            round_data['contributions'].append(contribution)
            member['group_memberships'][group_id]['total_contributed'] += group['fixed_amount']
        
        # Mark recipient
        membership['has_received'] = True
        membership['received_round'] = round_number
        membership['total_received'] += total_amount
        
        group['rounds'].append(round_data)
        group['current_round'] = round_number
        self.save_data()
        
        return round_data
    
    def start_new_cycle(self, group_id: str):
        """Start a new cycle after all members have received"""
        group = self.get_group(group_id)
        if not group:
            return
        
        group['cycle_number'] += 1
        group['current_round'] = 0
        
        # Reset all members' received status for this group
        for member_id in group['member_ids']:
            member = self.equb_data['members'][member_id]
            membership = member['group_memberships'][group_id]
            membership['has_received'] = False
            membership['received_round'] = None
        
        self.save_data()
    
    def get_group_members(self, group_id: str) -> List[Dict]:
        """Get all members in a specific group with their membership data"""
        group = self.get_group(group_id)
        if not group:
            return []
        
        members_data = []
        for member_id in group['member_ids']:
            member = self.equb_data['members'][member_id]
            membership = member['group_memberships'][group_id]
            
            members_data.append({
                'id': member_id,
                'name': member['name'],
                'phone': member['phone'],
                'email': member['email'],
                'has_received': membership['has_received'],
                'received_round': membership['received_round'],
                'total_contributed': membership['total_contributed'],
                'total_received': membership['total_received']
            })
        
        return members_data
    
    def get_available_recipients(self, group_id: str) -> List[Dict]:
        """Get members who haven't received in current cycle for a specific group"""
        members = self.get_group_members(group_id)
        return [m for m in members if not m['has_received']]
    
    def get_group_rounds(self, group_id: str) -> List[Dict]:
        """Get all rounds for a specific group"""
        group = self.get_group(group_id)
        if not group:
            return []
        return group['rounds']
    
    def get_group_cycle_info(self, group_id: str) -> Optional[Dict]:
        """Get current cycle information for a specific group"""
        group = self.get_group(group_id)
        if not group:
            return None
        
        members = self.get_group_members(group_id)
        total_members = len(members)
        received_count = sum(1 for m in members if m['has_received'])
        
        return {
            'group_id': group_id,
            'group_name': group['name'],
            'cycle_number': group['cycle_number'],
            'current_round': group['current_round'],
            'total_members': total_members,
            'received_count': received_count,
            'remaining': total_members - received_count,
            'fixed_amount': group['fixed_amount'],
            'frequency': group['frequency']
        }
    
    def get_all_members(self) -> List[Dict]:
        """Get all members in the system"""
        return list(self.equb_data['members'].values())
    
    def get_member_by_id(self, member_id: str) -> Optional[Dict]:
        """Get member by ID"""
        return self.equb_data['members'].get(member_id)
    
    def save_data(self):
        """Save Equb data to file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.equb_data, f, indent=2, ensure_ascii=False)
    
    def load_data(self):
        """Load Equb data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                    # Check if it's the new format (has 'groups' key)
                    if 'groups' in loaded_data and 'members' in loaded_data:
                        self.equb_data = loaded_data
                    else:
                        # Old format detected - initialize with default structure
                        print("Old data format detected. Starting fresh with new multi-group format.")
                        # Keep default structure
                        pass
            except Exception as e:
                print(f"Error loading data: {e}")
                pass

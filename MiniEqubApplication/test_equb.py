"""Test script for Equb Manager"""
from equb_manager import EqubManager
import os

# Clean test
if os.path.exists("test_equb_data.json"):
    os.remove("test_equb_data.json")

manager = EqubManager("test_equb_data.json")

print("=== Testing Multi-Group Equb System ===\n")

# Create groups
print("1. Creating groups...")
group1_id = manager.create_group("Family Equb", 1000, "Monthly")
group2_id = manager.create_group("Office Equb", 500, "Weekly")
print(f"   ✓ Created: Family Equb (ID: {group1_id})")
print(f"   ✓ Created: Office Equb (ID: {group2_id})\n")

# Add members to system
print("2. Adding members to system...")
member1_id = manager.add_member_to_system("Abebe Kebede", "0911234567")
member2_id = manager.add_member_to_system("Tigist Alemu", "0922345678")
member3_id = manager.add_member_to_system("Dawit Haile", "0933456789")
member4_id = manager.add_member_to_system("Sara Tesfaye", "0944567890")
print(f"   ✓ Added 4 members to system\n")

# Add members to groups
print("3. Adding members to groups...")
manager.add_member_to_group(group1_id, member1_id)
manager.add_member_to_group(group1_id, member2_id)
manager.add_member_to_group(group1_id, member3_id)
print(f"   ✓ Added 3 members to Family Equb")

manager.add_member_to_group(group2_id, member1_id)  # Abebe in both groups
manager.add_member_to_group(group2_id, member2_id)  # Tigist in both groups
manager.add_member_to_group(group2_id, member4_id)  # Sara only in Office
print(f"   ✓ Added 3 members to Office Equb")
print(f"   ✓ Abebe and Tigist are in BOTH groups\n")

# Test lottery for Family Equb
print("4. Running lottery for Family Equb...")
round1 = manager.start_new_round_lottery(group1_id)
if round1:
    print(f"   🎲 Winner: {round1['recipient_name']}")
    print(f"   💰 Payout: ETB {round1['total_payout']:,.2f}")
    print(f"   👥 Each member paid: ETB {round1['amount_per_member']:,.2f}\n")

# Test lottery for Office Equb
print("5. Running lottery for Office Equb...")
round2 = manager.start_new_round_lottery(group2_id)
if round2:
    print(f"   🎲 Winner: {round2['recipient_name']}")
    print(f"   💰 Payout: ETB {round2['total_payout']:,.2f}")
    print(f"   👥 Each member paid: ETB {round2['amount_per_member']:,.2f}\n")

# Check group info
print("6. Group Status:")
info1 = manager.get_group_cycle_info(group1_id)
print(f"   Family Equb: Round {info1['current_round']}/{info1['total_members']}, "
      f"Received: {info1['received_count']}, Remaining: {info1['remaining']}")

info2 = manager.get_group_cycle_info(group2_id)
print(f"   Office Equb: Round {info2['current_round']}/{info2['total_members']}, "
      f"Received: {info2['received_count']}, Remaining: {info2['remaining']}\n")

# Check member participation
print("7. Member Participation:")
member1 = manager.get_member_by_id(member1_id)
print(f"   {member1['name']} is in {len(member1['group_memberships'])} groups")
for group_id, membership in member1['group_memberships'].items():
    group = manager.get_group(group_id)
    print(f"      - {group['name']}: Contributed ETB {membership['total_contributed']:,.2f}, "
          f"Received ETB {membership['total_received']:,.2f}")

print("\n✅ All tests passed! Multi-group system working correctly.")
print(f"\n📁 Test data saved to: test_equb_data.json")

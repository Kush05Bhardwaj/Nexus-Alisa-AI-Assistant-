"""
View conversation history from the database
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from backend.app.db import SessionLocal
from backend.app.models import ConversationHistory

def view_history(limit=20):
    """View recent conversation history"""
    db = SessionLocal()
    
    print("=" * 80)
    print("💬 ALISA CONVERSATION HISTORY")
    print("=" * 80)
    print()
    
    rows = (
        db.query(ConversationHistory)
        .order_by(ConversationHistory.timestamp.desc())
        .limit(limit)
        .all()
    )
    
    if not rows:
        print("📭 No conversation history found.")
        return
    
    # Reverse to show chronological order
    for row in reversed(rows):
        timestamp = row.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        role_emoji = "👤" if row.role == "user" else "🤖"
        role_label = "You" if row.role == "user" else "Alisa"
        
        print(f"{role_emoji} {role_label} [{timestamp}]")
        print(f"   {row.content}")
        print()
    
    db.close()
    
    print("=" * 80)
    print(f"📊 Showing last {len(rows)} messages")
    print("=" * 80)

def clear_history():
    """Clear all conversation history from database"""
    response = input("⚠️  Are you sure you want to clear ALL conversation history? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Cancelled.")
        return
    
    db = SessionLocal()
    deleted = db.query(ConversationHistory).delete()
    db.commit()
    db.close()
    
    print(f"✅ Deleted {deleted} messages from history.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="View Alisa conversation history")
    parser.add_argument("-n", "--limit", type=int, default=20, help="Number of messages to show")
    parser.add_argument("--clear", action="store_true", help="Clear all conversation history")
    
    args = parser.parse_args()
    
    if args.clear:
        clear_history()
    else:
        view_history(args.limit)

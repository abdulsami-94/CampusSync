#!/usr/bin/env python3
"""
Database Viewer for CampusSync
Run this script to view all database contents in a readable format.
"""

from app import create_app, db
from app.models import User, Complaint

app = create_app()

def view_database():
    with app.app_context():
        print("=" * 60)
        print("CAMPUSSYNC DATABASE VIEWER")
        print("=" * 60)

        # Users
        print("\n👥 USERS:")
        print("-" * 40)
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id:2d} | {user.username:15} | {user.email:25} | {user.role}")

        # Complaints
        print("\n📋 COMPLAINTS:")
        print("-" * 40)
        complaints = Complaint.query.all()
        if not complaints:
            print("No complaints found.")
        else:
            for comp in complaints:
                assigned = comp.assignee.username if comp.assignee else 'Unassigned'
                status_icon = {'Pending': '⏳', 'In Progress': '🔄', 'Resolved': '✅'}.get(comp.status, '❓')
                print(f"ID: {comp.id:2d} | {comp.title[:14]:15} | {comp.category[:14]:15} | {status_icon} {comp.status[:11]:12} | {assigned[:12]:12} | {comp.is_deleted}")

        print("\n" + "=" * 60)

if __name__ == "__main__":
    view_database()
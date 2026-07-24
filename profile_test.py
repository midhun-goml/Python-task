import asyncio
import cProfile
import pstats
import io
import sys
import os
from pathlib import Path

# Add parent directory to path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))


from app.core.database import AsyncSessionLocal
from app.schemas.ticket_schema import TicketCreate, TicketUpdate
from app.services.ticket_service import ticket_service
 
 
async def test_crud():
 
    # Create database session
    async with AsyncSessionLocal() as db:
 
        # ==========================================
        # 1. CREATE TICKET
        # ==========================================
        print("\n1. Creating ticket...")
 
        create_data = TicketCreate(
            title="cProfile Test",
            description="Testing service performance",
            priority="high",
            assignee_email="midhun@test1.com"
        )
 
        created_ticket = await ticket_service.create_ticket(db, create_data)
 
        print("Created Ticket ID:", created_ticket.id)
 
        ticket_id = created_ticket.id
 
 
        # ==========================================
        # 2. GET ALL TICKETS
        # ==========================================
        print("\n2. Getting all tickets...")
 
        tickets = await ticket_service.get_all_tickets(db)
 
        print("Total tickets:", len(tickets))
 
 
        # ==========================================
        # 3. GET SINGLE TICKET
        # ==========================================
        print("\n3. Getting single ticket...")
 
        ticket = await ticket_service.get_ticket_by_id(db, ticket_id)
 
        print("Ticket ID:", ticket.id)
 
 
        # ==========================================
        # 4. UPDATE TICKET
        # ==========================================
        print("\n4. Updating ticket...")
 
        update_data = TicketUpdate(
            title="Updated cProfile Test"
        )
 
        updated_ticket = await ticket_service.update_ticket(
            db,
            ticket_id,
            update_data
        )
 
        print("Updated Ticket ID:", updated_ticket.id)
 
 
        # ==========================================
        # 5. DELETE TICKET
        # ==========================================
        print("\n5. Deleting ticket...")
 
        await ticket_service.delete_ticket(db, ticket_id)
 
        print("Ticket deleted successfully")
 
 
def main():
 
    # Create cProfile profiler
    profiler = cProfile.Profile()
 
    # Start profiling
    profiler.enable()
 
    # Run async CRUD operations
    asyncio.run(test_crud())
 
    # Stop profiling
    profiler.disable()
 
 
    # ==========================================
    # DISPLAY CPROFILE RESULTS
    # ==========================================
 
    stream = io.StringIO()
 
    stats = pstats.Stats(
        profiler,
        stream=stream
    )
 
    # Remove unnecessary directory paths
    stats.strip_dirs()
 
    # Sort by total cumulative execution time
    stats.sort_stats("cumulative")
 
    # Display top 30 functions
    stats.print_stats(30)
 
    print("\n")
    print("=" * 80)
    print("CPROFILE RESULTS")
    print("=" * 80)
 
    print(stream.getvalue())
 
 
if __name__ == "__main__":
    main()
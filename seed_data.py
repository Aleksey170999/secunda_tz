from app.db.base import SessionLocal
from app.models.organization import Organization
from app.models.building import Building
from app.models.activity import Activity

def create_test_data():
    db = SessionLocal()
    try:
        building1 = Building(
            address="123 Main St, City A",
            latitude=55.7558,
            longitude=37.6173
        )
        
        building2 = Building(
            address="456 Oak Ave, City B",
            latitude=55.7600,
            longitude=37.6200
        )
        
        db.add_all([building1, building2])
        db.flush()
        
        activity1 = Activity(name="IT Services", level=1)
        db.add(activity1)
        db.flush()
        
        activity2 = Activity(name="Web Development", level=2)
        activity2.parent_id = activity1.id
        activity3 = Activity(name="Mobile Development", level=2)
        activity3.parent_id = activity1.id
        
        activity4 = Activity(name="Design", level=1)
        db.add(activity4)
        db.flush()
        
        activity5 = Activity(name="UI/UX", level=2)
        activity5.parent_id = activity4.id
        
        db.add_all([activity2, activity3, activity5])
        db.flush()
        
        org1 = Organization(
            name="Tech Solutions Inc",
            phone_numbers=["+1234567890", "+1987654321"],
            building_id=building1.id
        )
        org1.activities = [activity2, activity5]
        
        org2 = Organization(
            name="Mobile Masters",
            phone_numbers=["+1122334455"],
            building_id=building2.id
        )
        org2.activities = [activity3]
        
        org3 = Organization(
            name="Design Hub",
            phone_numbers=["+5566778899"],
            building_id=building1.id
        )
        org3.activities = [activity4, activity5]
        
        db.add_all([org1, org2, org3])
        db.commit()
        print("✅ Test data created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
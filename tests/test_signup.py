"""
Tests for the signup endpoint
"""


def test_signup_for_activity_success(client):
    """Test successfully signing up for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity(client):
    """Test signing up for an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_participant(client):
    """Test that a student cannot sign up for the same activity twice"""
    email = "michael@mergington.edu"
    
    # This student is already signed up for Chess Club
    response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert response.status_code == 400
    
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_multiple_students(client):
    """Test signing up multiple students for the same activity"""
    students = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ]
    
    for student in students:
        response = client.post(
            f"/activities/Chess Club/signup?email={student}"
        )
        assert response.status_code == 200
    
    # Verify all students were added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    chess_participants = activities["Chess Club"]["participants"]
    
    for student in students:
        assert student in chess_participants


def test_signup_with_url_encoded_activity_name(client):
    """Test signing up for an activity with spaces in the name (URL encoded)"""
    response = client.post(
        "/activities/Programming%20Class/signup?email=newcoder@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newcoder@mergington.edu" in activities["Programming Class"]["participants"]


def test_signup_preserves_existing_participants(client):
    """Test that signing up a new student doesn't remove existing participants"""
    # Get initial participants
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()["Chess Club"]["participants"]
    initial_count = len(initial_participants)
    
    # Sign up a new student
    client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    
    # Verify all original participants are still there
    final_response = client.get("/activities")
    final_participants = final_response.json()["Chess Club"]["participants"]
    
    assert len(final_participants) == initial_count + 1
    for participant in initial_participants:
        assert participant in final_participants
    assert "newstudent@mergington.edu" in final_participants

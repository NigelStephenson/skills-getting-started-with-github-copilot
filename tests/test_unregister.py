"""
Tests for the unregister endpoint
"""


def test_unregister_participant_success(client):
    """Test successfully unregistering a participant from an activity"""
    # Verify participant exists first
    initial_response = client.get("/activities")
    initial_activities = initial_response.json()
    assert "michael@mergington.edu" in initial_activities["Chess Club"]["participants"]
    
    # Unregister the participant
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify the participant was removed
    final_response = client.get("/activities")
    final_activities = final_response.json()
    assert "michael@mergington.edu" not in final_activities["Chess Club"]["participants"]


def test_unregister_from_nonexistent_activity(client):
    """Test unregistering from an activity that doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
    )
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_nonexistent_participant(client):
    """Test unregistering a participant who is not signed up"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]


def test_unregister_preserves_other_participants(client):
    """Test that unregistering one participant doesn't affect others"""
    # Get initial participants
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()["Chess Club"]["participants"]
    initial_count = len(initial_participants)
    
    # Unregister one participant
    client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    
    # Verify other participants are still there
    final_response = client.get("/activities")
    final_participants = final_response.json()["Chess Club"]["participants"]
    
    assert len(final_participants) == initial_count - 1
    assert "michael@mergington.edu" not in final_participants
    assert "daniel@mergington.edu" in final_participants


def test_unregister_with_url_encoded_activity_name(client):
    """Test unregistering from an activity with spaces in the name (URL encoded)"""
    response = client.delete(
        "/activities/Programming%20Class/unregister?email=emma@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify the participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "emma@mergington.edu" not in activities["Programming Class"]["participants"]


def test_signup_and_unregister_workflow(client):
    """Test the complete workflow of signing up and then unregistering"""
    email = "workflow@mergington.edu"
    activity = "Chess Club"
    
    # Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Verify signup
    check_response = client.get("/activities")
    assert email in check_response.json()[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    
    # Verify unregistration
    final_response = client.get("/activities")
    assert email not in final_response.json()[activity]["participants"]


def test_unregister_all_participants(client):
    """Test unregistering all participants from an activity"""
    activity = "Chess Club"
    
    # Get initial participants
    initial_response = client.get("/activities")
    participants = initial_response.json()[activity]["participants"].copy()
    
    # Unregister all participants
    for participant in participants:
        response = client.delete(
            f"/activities/{activity}/unregister?email={participant}"
        )
        assert response.status_code == 200
    
    # Verify all participants were removed
    final_response = client.get("/activities")
    assert len(final_response.json()[activity]["participants"]) == 0


def test_unregister_and_signup_again(client):
    """Test that a participant can sign up again after unregistering"""
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Unregister (already signed up initially)
    unregister_response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    
    # Sign up again
    signup_response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Verify participant is back
    final_response = client.get("/activities")
    assert email in final_response.json()[activity]["participants"]

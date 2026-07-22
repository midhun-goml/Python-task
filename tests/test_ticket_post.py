def test_create_ticket_with_empty_title_returns_422(client):
    response = client.post(
        "/tickets",
        json={
            "title": "",
        }
    )
 
    assert response.status_code == 422
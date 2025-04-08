def test_read_main(test_client_one, test_client_two):
    """ Each user must see only its todos"""
    # Arrange
    test_client_one.post(
        "/todo",
        json={
          "title": "string",
          "description": "string",
          "expire_date": "2025-04-08",
          "status": "pendente"
        }
    )
    test_client_two.post(
        "/todo",
        json={
            "title": "string2",
            "description": "string2",
            "expire_date": "2025-04-08",
            "status": "pendente"
        }
    )
    test_client_two.post(
        "/todo",
        json={
            "title": "string3",
            "description": "string3",
            "expire_date": "2025-04-08",
            "status": "pendente"
        }
    )

    # Act
    response = test_client_one.get("/todo")
    response_two = test_client_two.get("/todo")

    # Assert
    assert len(response.json()) == 1
    assert response.json()[0].get("title") == "string"

    assert len(response_two.json()) == 2
    assert response_two.json()[0].get("title") == "string2"
    assert response_two.json()[1].get("title") == "string3"
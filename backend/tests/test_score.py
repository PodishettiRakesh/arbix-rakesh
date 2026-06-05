def test_score_happy_path(client):
    response = client.post(
        "/score",
        json={
            "land_area_acres": 6,
            "crop_type": "Rice",
            "repayment_history_score": 90,
            "annual_income_band": ">10L",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "reason_codes" in data
    assert len(data["reason_codes"]) == 3
    assert data["score"] == 94.0
    assert data["reason_codes"] == [
        "good_repayment",
        "large_landholding",
        "high_income_band",
    ]
    assert "request_id" in data
    assert "timestamp" in data

    stored = client.get(f"/scores/{data['request_id']}")
    assert stored.status_code == 200
    assert stored.json()["score"] == data["score"]
    assert stored.json()["reason_codes"] == data["reason_codes"]


def test_get_score_not_found(client):
    response = client.get("/scores/non-existent-id")
    assert response.status_code == 404


def test_score_validation_error_negative_land_area(client):
    response = client.post(
        "/score",
        json={
            "land_area_acres": -1,
            "crop_type": "Rice",
            "repayment_history_score": 90,
            "annual_income_band": ">10L",
        },
    )

    assert response.status_code == 422


def test_score_validation_error_empty_crop_type(client):
    response = client.post(
        "/score",
        json={
            "land_area_acres": 6,
            "crop_type": "",
            "repayment_history_score": 90,
            "annual_income_band": ">10L",
        },
    )

    assert response.status_code == 422

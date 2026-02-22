import pytest
from httpx import ASGITransport, AsyncClient

from models import Metric, Tag


@pytest.mark.asyncio
async def test_create_metric_record_success(client: AsyncClient, test_metric: Metric):
    """Успешное создание записи метрики."""
    response = await client.post(
        f"/v1/metrics/{test_metric.id}/records",
        json={
            "value": "150.5000",
            "timestamp": "2026-02-20T10:00:00",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["metric_id"] == test_metric.id
    assert data["value"] == "150.5000"
    assert data["tags"] == []
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_metric_record_with_tags(
    client: AsyncClient, test_metric: Metric, test_tags: list[Tag]
):
    """Создание записи метрики с тегами."""
    tag_ids = [tag.id for tag in test_tags]
    response = await client.post(
        f"/v1/metrics/{test_metric.id}/records",
        json={
            "value": "200.0000",
            "timestamp": "2026-02-20T12:00:00",
            "tag_ids": tag_ids,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data["tags"]) == 2
    response_tag_ids = {tag["id"] for tag in data["tags"]}
    assert response_tag_ids == set(tag_ids)


@pytest.mark.asyncio
async def test_create_metric_record_metric_not_found(client: AsyncClient):
    """Метрика не найдена — 404."""
    response = await client.post(
        "/v1/metrics/99999/records",
        json={
            "value": "100.0000",
            "timestamp": "2026-02-20T10:00:00",
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_metric_record_tags_not_found(
    client: AsyncClient, test_metric: Metric
):
    """Несуществующие теги — 404."""
    response = await client.post(
        f"/v1/metrics/{test_metric.id}/records",
        json={
            "value": "100.0000",
            "timestamp": "2026-02-20T10:00:00",
            "tag_ids": [99998, 99999],
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_metric_record_unauthorized():
    """Без авторизации — 403."""
    from api_app import app

    app.dependency_overrides.clear()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        response = await ac.post(
            "/v1/metrics/1/records",
            json={
                "value": "100.0000",
                "timestamp": "2026-02-20T10:00:00",
            },
        )
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_create_metric_record_invalid_data(
    client: AsyncClient, test_metric: Metric
):
    """Невалидные данные — 422."""
    response = await client.post(
        f"/v1/metrics/{test_metric.id}/records",
        json={
            "value": "not_a_number",
            "timestamp": "invalid_date",
        },
    )
    assert response.status_code == 422

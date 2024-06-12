from sqlmodel import SQLModel


class TaskRequest(SQLModel):
    url: str


class TaskResponse(SQLModel):
    id: str
    status: str = "PENDING"
    data: list[dict] | None = None

# Схема базы данных

## Описание

Для описания моделей для нашей базы данных была использована библиотека SQLModel.
SQLModel – это библиотека для работы с SQL-базами данных, представляющая собой
оболочку над ORM SQLAlchemy и Pydantic, основанная на аннотации типов.
Ниже представлены реализованные модели таблиц и схемы.

## Модели

### Пользователи

```python
class Gender(str, Enum):
    male = "male"
    female = "female"


class UserBase(SQLModel):
    email: str = Field(unique=True)
    first_name: str
    last_name: str
    gender: Gender
    birth_date: date
    description: str | None
    county: str
    language: str


class UserBaseUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    gender: Gender | None = None
    birth_date: date | None = None
    description: str | None = None
    county: str | None = None
    language: str | None = None


class UserBaseId(UserBase):
    id: int | None


class UserBaseCompanion(UserBaseId):
    companion_id: int
    status: str


class UserLogin(SQLModel):
    email: str = Field(unique=True)
    password: str


class UserPasswordUpdate(SQLModel):
    old_password: str
    new_password: str


class UserPasswordCreate(UserBase):
    password: str


class UserPassword(UserBase):
    password_hash: bytes


class User(UserPassword, table=True):
    id: int | None = Field(default=None, primary_key=True)
    favorite_trips: list['Trip'] = Relationship(
        back_populates='liked_by',
        sa_relationship_kwargs={"cascade": "all, delete"},
        link_model=FavoriuteTrip
    )
    reviews: list['Review'] = Relationship(
        back_populates='user',
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    created_trips: list['Trip'] = Relationship(
        back_populates='user',
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    trip_requests: list['Trip'] = Relationship(
        back_populates='companions',
        sa_relationship_kwargs={"cascade": "all, delete", "lazy": "selectin"}
    )
```

### Поездки

```python

class TripBase(SQLModel):
    start_location: str
    end_location: str
    start_date: datetime
    end_date: datetime
    description: str | None


class TripBasePartial(SQLModel):
    start_location: str | None = None
    end_location: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    description: str | None = None


class Trip(TripBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    user: 'User' = Relationship(
        back_populates='created_trips'
    )
    liked_by: list['User'] = Relationship(
        back_populates='favorite_trips',
        link_model=FavoriuteTrip
    )
    companions: list['User'] = Relationship(
        back_populates='trip_requests',
        link_model=Companion,
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class TripDetail(TripBase):
    id: int | None
    liked_by: list[UserBaseId] = []
```

### Компаньон

```python
class Status(str, Enum):
    approved = 'approved'
    rejected = 'rejected'
    pending = "pending"


class StatusScheme(SQLModel):
    status: Status | None = None


class CompanionBase(SQLModel):
    trip_id: int = Field(foreign_key='trip.id')
    status: Status = Field(default=Status.pending)


class CompanionBaseId(CompanionBase):
    id: int


class CompanionBaseDetail(CompanionBaseId):
    user: UserBaseId


class Companion(CompanionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
```

### Избранные поездки

```python
class FavoriuteTripBase(SQLModel):
    trip_id: int = Field(foreign_key='trip.id')


class FavoriuteTrip(FavoriuteTripBase, table=True):
    __tablename__ = 'favorite_trip'

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
```

### Отзывы

```python
class ReviewBase(SQLModel):
    trip_id: int = Field(foreign_key='trip.id')
    rate: int
    comment: str | None


class ReviewScheme(SQLModel):
    rate: int
    comment: str = ''


class ReviewBaseId(ReviewBase):
    id: int


class ReviewBaseList(ReviewBaseId):
    user_id: int


class ReviewBaseDetail(ReviewBaseId):
    user: UserBaseId


class Review(ReviewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    user: 'User' = Relationship(back_populates='reviews')
```
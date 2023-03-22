from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

# TODO возможно реализовать в одной таблице?

roles = Table(
    "folders",
    metadata,
    Column("type", String, nullable=False),
    Column("id", Integer, primary_key=True),
    Column("parent_id", Integer, nullable=True),
    Column("date", TIMESTAMP, default=datetime.utcnow),
)

users = Table(
    "files",
    metadata,
    Column("type", String, nullable=False),
    Column("id", Integer, primary_key=True),
    Column("size", Integer, nullable=False),
    Column("url", String, nullable=False),
    Column("date", TIMESTAMP, default=datetime.utcnow),
    Column("parent_id", Integer, ForeignKey("folders.id"), nullable=True),
)

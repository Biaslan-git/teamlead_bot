from sqlalchemy import delete, insert, select
from sqlalchemy.orm import selectinload

from db.models import Developer, Project, AuthKey, Status
from db.session import async_session


async def get_project_by_title(project_title: str) -> Project | None:
    async with async_session() as session:
        query = select(Project)\
        .where(Project.title == project_title)
        result = await session.execute(query)
        project = result.scalars().first()
        return project

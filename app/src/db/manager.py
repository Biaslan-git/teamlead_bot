from sqlalchemy import delete, func, insert, select
from sqlalchemy.orm import selectinload

from datetime import date 

from db.models import Developer, DeveloperSpecialties, Project, AuthKey, Status
from db.session import async_session
import uuid


async def add_developer(user_id: int, username: str | None, first_name: str):
    developer = Developer(user_id=user_id, username=username, first_name=first_name)
    async with async_session() as session:
        session.add(developer)
        await session.commit()
        await session.refresh(developer)

        return developer

async def delete_developer(id: int):
    async with async_session() as session:
        stmt = delete(Developer).where(Developer.id == id)
        await session.execute(stmt)
        await session.commit()

async def get_developers():
    async with async_session() as session:
        query = select(Developer)\
        .options(selectinload(Developer.projects))
        developers = await session.execute(query)
        return developers.scalars().all()

async def get_developer_by_user_id(user_id):
    async with async_session() as session:
        query = select(Developer).where(Developer.user_id == user_id)
        result = await session.execute(query)
        developer = result.scalars().first()
        return developer

async def get_developer_by_id(developer_id):
    async with async_session() as session:
        query = select(Developer)\
        .options(selectinload(Developer.projects))\
        .where(Developer.id == developer_id)
        result = await session.execute(query)
        developer = result.scalars().first()
        return developer

async def create_project(title: str, description: str, price: int, **kwargs):
    project = Project(title=title, description=description, price=price, **kwargs)
    async with async_session() as session:
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project

async def add_project_to_developer(project_id: int, developer_user_id: int) -> tuple[Project, Developer] | None:
    async with async_session() as session:
        developer_query = select(Developer)\
            .options(selectinload(Developer.projects))\
            .where(Developer.user_id == developer_user_id)
        project_query = select(Project)\
            .options(selectinload(Project.developers))\
            .where(Project.id == project_id)

        dev_res = await session.execute(developer_query)
        proj_res = await session.execute(project_query)

        developer = dev_res.scalars().first()
        project = proj_res.scalars().first()

        if developer and project:
            developer.projects.append(project)
            project.status = Status.in_progress
            if not project.taken_at:
                project.taken_at = date.today()
            await session.commit()
            await session.refresh(project)
            await session.refresh(developer)
            return project, developer



async def get_developers_to_take_project():
    async with async_session() as session:
        query = select(Developer)\
            .options(selectinload(Developer.projects))
        res = await session.execute(query)
        developers = res.scalars().all()

        developers = [x for x in developers if not x.projects]
        return developers

async def get_developer_projects_by_user_id(developer_user_id: int):
    async with async_session() as session:
        query = select(Developer)\
            .options(selectinload(Developer.projects))\
            .where(Developer.user_id == developer_user_id)
        res = await session.execute(query)
        developer = res.scalars().first()
        if developer:
            return developer.projects


async def change_developer_specialty(developer_id: int, 
                                     new_specialty: DeveloperSpecialties | None = None):
    async with async_session() as session:
        developer_query = select(Developer)\
        .options(selectinload(Developer.projects))\
        .where(Developer.id == developer_id)
        res = await session.execute(developer_query)
        developer = res.scalars().first()

        if developer:
            if not new_specialty:
                developer.specialty = developer.specialty.next()
            else:
                developer.specialty = new_specialty
            await session.commit()
            await session.refresh(developer)
            return developer


async def change_project_status(project_id: int, new_status: Status | None = None):
    async with async_session() as session:
        project_query = select(Project).where(Project.id == project_id)
        res = await session.execute(project_query)
        project = res.scalars().first()

        if project:
            if new_status:
                project.status = new_status
            else:
                project.status = project.status.next()
            await session.commit()
            await session.refresh(project)
            return project

async def get_developer_projects(developer_id: int):
    async with async_session() as session:
        query = select(Developer)\
            .options(selectinload(Developer.projects))\
            .where(Developer.id == developer_id)
        res = await session.execute(query)
        developer = res.scalars().first()
        if developer:
            return developer.projects

async def get_developer_current_projects(developer_id: int):
    async with async_session() as session:
        query = select(Developer)\
            .options(selectinload(Developer.projects))\
            .where(Developer.id == developer_id)
        res = await session.execute(query)
        developer = res.scalars().first()
        if developer:
            current_projs = [proj for proj in developer.projects if proj.status==Status.in_progress]
            return current_projs

async def get_developer_current_projects_by_user_id(developer_user_id: int):
    async with async_session() as session:
        query = select(Developer)\
            .options(selectinload(Developer.projects))\
            .where(Developer.user_id == developer_user_id)
        res = await session.execute(query)
        developer = res.scalars().first()
        if developer:
            current_projs = [proj for proj in developer.projects if proj.status==Status.in_progress]
            return current_projs

async def get_project_developers(project_id: int):
    async with async_session() as session:
        query = select(Project)\
            .options(selectinload(Project.developers))\
            .where(Project.id==project_id)
        res = await session.execute(query)
        project = res.scalars().first()
        if project:
            return project.developers

async def get_projects():
    async with async_session() as session:
        query = select(Project)
        projects = await session.execute(query)
        return projects.scalars().all()

async def get_projects_by_page(page: int):
    async with async_session() as session:
        page_size = 5
        offset = (page - 1) * page_size
        query = select(Project).limit(page_size).offset(offset)
        result = await session.execute(query)
        projects = result.scalars().all()
        return projects

async def get_developers_by_page(page: int):
    async with async_session() as session:
        page_size = 5
        offset = (page - 1) * page_size
        query = select(Developer).limit(page_size).offset(offset)
        result = await session.execute(query)
        projects = result.scalars().all()
        return projects

async def get_projects_count():
    async with async_session() as session:
        query = select(func.count(Project.id))
        result = await session.execute(query)
        return result.scalar_one()

async def get_project_by_id(id: int):
    async with async_session() as session:
        query = select(Project)\
        .options(selectinload(Project.developers))\
        .where(Project.id == id)
        result = await session.execute(query)
        project = result.scalars().first()
        return project

async def delete_project(id: int):
    async with async_session() as session:
        stmt = delete(Project).where(Project.id == id)
        await session.execute(stmt)
        await session.commit()

async def get_auth_key():
    async with async_session() as session:
        stmt = select(AuthKey)
        result = await session.execute(stmt)
        auth_key = result.scalars().first()

        if not auth_key:
            auth_key = await update_auth_key()
            return auth_key

        return auth_key.key


async def update_auth_key():
    async with async_session() as session:
        stmt = select(AuthKey)
        result = await session.execute(stmt)
        auth_key = result.scalars().first()

        new_key = str(uuid.uuid4())

        if not auth_key:
            stmt = insert(AuthKey).values(key=new_key)
            await session.execute(stmt)
            await session.commit()
            return new_key

        auth_key.key = new_key

        await session.commit()

        return new_key

        

        



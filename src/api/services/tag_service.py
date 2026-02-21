from fastapi import Depends
from api.repositories.tag_repository import TagRepository, get_tag_repository


class TagService:
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository


    async def get_tags_service(self):
        return await self.tag_repository.get_all()

def get_tag_service(tag_repository: TagRepository = Depends(get_tag_repository)) -> TagService:
    return TagService(tag_repository)
from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
from typing import List, Optional

from sqlalchemy import select, func, update, delete, and_, or_, desc
from sqlalchemy.orm import Session


from content.content_service.models.domain.source import Source
from src.content.content_service.database import database
from src.content.content_service.models.schemas.source import (
    SourceCreate, SourceResponse, SourceUpdate,
    # TagCreate, TagResponse, TagUpdate,
    # RatingCreate, RatingResponse, SourceWithRatingsResponse,
    # SourceTagCreate, SourceTagResponse,
    # PaginatedResponse
)

from src.content.content_service.api.dependencies import get_current_user


router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("")
async def get_tags(
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=100),
        name: Optional[str] = None,
        sort_by: Optional[str] = "usage_count",
        sort_order: Optional[str] = "desc",

):
    """
    Get a list of tags with optional filtering and pagination.
    """
    # tag_service = TagService(db)
    # tags, total = tag_service.get_tags(
    #     skip=skip,
    #     limit=limit,
    #     name=name,
    #     sort_by=sort_by,
    #     sort_order=sort_order
    # )
    #
    # return {
    #     "items": tags,
    #     "total": total,
    #     "page": skip // limit + 1,
    #     "pages": (total + limit - 1) // limit,
    #     "size": limit
    # }
    pass


@router.get("/{tag_id}")
async def get_tag(
        tag_id: int = Path(..., ge=1),
        # db: Session = Depends(get_db),
        # current_user: User = Depends(get_current_user)
):
    """
    Get a specific tag by ID.
    """
    # tag_service = TagService(db)
    # tag = tag_service.get_tag_by_id(tag_id)
    # if not tag:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Tag with ID {tag_id} not found"
    #     )
    # return tag
    pass


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_tag(
        # tag: TagCreate,
        # db: Session = Depends(get_db),
        # current_user: User = Depends(get_current_active_user)
):
    """
    Create a new tag.
    """
    # tag_service = TagService(db)
    #
    # # Check if tag with the same name already exists
    # existing_tag = tag_service.get_tag_by_name(tag.name)
    # if existing_tag:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Tag with name '{tag.name}' already exists"
    #     )
    #
    # return tag_service.create_tag(tag)
    pass


@router.put("/{tag_id}")
async def update_tag(
        # tag: TagUpdate,
        tag_id: int = Path(..., ge=1),
        # db: Session = Depends(get_db),
        # current_user: User = Depends(get_admin_user)  # Only admins can update tags
):
    """
    Update an existing tag (admin only).
    """
    # tag_service = TagService(db)
    # existing_tag = tag_service.get_tag_by_id(tag_id)
    #
    # if not existing_tag:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Tag with ID {tag_id} not found"
    #     )
    #
    # # If name is being updated, check for uniqueness
    # if tag.name and tag.name != existing_tag.name:
    #     name_exists = tag_service.get_tag_by_name(tag.name)
    #     if name_exists:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=f"Tag with name '{tag.name}' already exists"
    #         )
    #
    # return tag_service.update_tag(tag_id, tag)
    pass


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
        tag_id: int = Path(..., ge=1),
        # db: Session = Depends(get_db),
        # current_user: User = Depends(get_admin_user)  # Only admins can delete tags
):
    """
    Delete a tag (admin only).
    """
    # tag_service = TagService(db)
    # existing_tag = tag_service.get_tag_by_id(tag_id)
    #
    # if not existing_tag:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Tag with ID {tag_id} not found"
    #     )
    #
    # # Check if tag is being used
    # if tag_service.get_tag_usage_count(tag_id) > 0:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Cannot delete tag that is still in use. Remove tag from all sources first."
    #     )
    #
    # tag_service.delete_tag(tag_id)
    # return None
    pass
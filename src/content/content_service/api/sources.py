from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
from typing import List, Optional

from sqlalchemy import select, func, update, delete, and_, or_, desc
from sqlalchemy.orm import Session


from content.content_service.models.domain.source import Source
from src.content.content_service.models.schemas.source import (
    SourceCreate, SourceResponse, SourceUpdate,
    # TagCreate, TagResponse, TagUpdate,
    # RatingCreate, RatingResponse, SourceWithRatingsResponse,
    # SourceTagCreate, SourceTagResponse,
    # PaginatedResponse
)
from src.content.content_service.database import database
from src.content.content_service.api.dependencies import get_current_user
router = APIRouter(prefix="/sources", tags=["sources"])


# Source endpoints
@router.get("")
async def get_sources(
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        # filters: Optional[List[dict[str]]] = Query(None),
        content_type: Optional[str] = Query(None),
        tag_ids: Optional[List[int]] = Query(None),
        sort_by: Optional[str] = "added_date",
        order_desc: Optional[bool] = True,
        session=Depends(database.get_session)
):
    """
    Get a list of sources with optional filtering and pagination.
    """
    # source_service = SourceService(db)
    # sources, total = source_service.get_sources(
    #     skip=skip,
    #     limit=limit,
    #     title=title,
    #     content_type=content_type,
    #     is_verified=is_verified,
    #     is_recommended=is_recommended,
    #     tag_ids=tag_ids,
    #     sort_by=sort_by,
    #     sort_order=sort_order
    # )
    #
    # return {
    #     "items": sources,
    #     "total": total,
    #     "page": skip // limit + 1,
    #     "pages": (total + limit - 1) // limit,
    #     "size": limit
    # }
    query = select(Source)
    # Применяем фильтры
    # if filters:
    #     conditions = []
    #     if 'title' in filters and filters['title']:
    #         conditions.append(Source.title.ilike(f"%{filters['title']}%"))
    #     if 'content_type' in filters and filters['content_type']:
    #         conditions.append(Source.content_type == filters['content_type'])
    #     if 'added_by' in filters and filters['added_by']:
    #         conditions.append(Source.added_by == filters['added_by'])
    #     if 'is_verified' in filters:
    #         conditions.append(Source.is_verified == filters['is_verified'])
    #     if 'is_recommended' in filters:
    #         conditions.append(Source.is_recommended == filters['is_recommended'])
    #     if 'min_rating' in filters and filters['min_rating'] is not None:
    #         conditions.append(Source.avg_rating >= filters['min_rating'])
    #     if 'max_rating' in filters and filters['max_rating'] is not None:
    #         conditions.append(Source.avg_rating <= filters['max_rating'])
    #     if 'date_from' in filters and filters['date_from']:
    #         conditions.append(Source.publication_date >= filters['date_from'])
    #     if 'date_to' in filters and filters['date_to']:
    #         conditions.append(Source.publication_date <= filters['date_to'])

    if content_type is not None:
        query = query.where(and_(Source.content_type == content_type))

    # Применяем сортировку
    if sort_by is not None:
        column = getattr(Source, sort_by, None)
        if column is not None:
            query = query.order_by(desc(column) if order_desc else column)
    else:
        # По умолчанию сортируем по дате добавления (новые сначала)
        query = query.order_by(desc(Source.added_date))

    # Применяем пагинацию
    query = query.offset(skip).limit(limit)

    result = session.execute(query)
    sources = result.all()
    sources_response = list()
    if sources:
        for source in sources:
            # res = SourceResponse(
            #                      title=source.title,
            #                      url=source.url,
            #                      description=source.description,
            #                      thumbnail_url=source.thumbnail_url,
            #                      content_type=source.content_type,
            #                      publication_date=source.publication_date,
            #     source_id=source.source_id,
            #     added_date=source.added_date,
            #     added_by=source.added_by,
            #     is_verified=source.is_verified,
            #     is_recommended=source.is_recommended,
            #     avg_rating=source.avg_rating,
            #     tags=source.tags
            #                      )
            res = SourceResponse.model_validate(source[0])
            sources_response.append(res)

    # total = sources.count()
    return {
        "items": sources_response,
        # "total": total,
        "page": skip // limit + 1,
        # "pages": (total + limit - 1) // limit,
        "size": limit
    }


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(
        source_id: int = Path(..., ge=1),
        # db: Session = Depends(get_db),
        # current_user: User = Depends(get_current_user)
):
    """
    Get a specific source by ID.
    """
    # source_service = SourceService(db)
    # source = source_service.get_source_by_id(source_id)
    # if not source:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Source with ID {source_id} not found"
    #     )
    # return source
    pass


@router.post("", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def create_source(
        source: SourceCreate,
        # db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    """
    Create a new source.
    """
    # source_service = SourceService(db)
    # return source_service.create_source(source, current_user.id)


@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(
        source: SourceUpdate,
        source_id: int = Path(..., ge=1),
        current_user=Depends(get_current_user)
):
    """
    Update an existing source.
    """
    # source_service = SourceService(db)
    # existing_source = source_service.get_source_by_id(source_id)
    #
    # if not existing_source:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Source with ID {source_id} not found"
    #     )
    #
    # # Check if user is owner or admin
    # if existing_source.added_by != current_user.id and not current_user.is_admin:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to update this source"
    #     )
    #
    # return source_service.update_source(source_id, source)
    pass


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
        source_id: int = Path(..., ge=1),
        current_user = Depends(get_current_user)
):
    """
    Delete a source.
    """
    # source_service = SourceService(db)
    # existing_source = source_service.get_source_by_id(source_id)
    #
    # if not existing_source:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Source with ID {source_id} not found"
    #     )
    #
    # # Check if user is owner or admin
    # if existing_source.added_by != current_user.id and not current_user.is_admin:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to delete this source"
    #     )
    #
    # source_service.delete_source(source_id)
    # return None
    pass


# Source Ratings endpoints
@router.get("/{source_id}/ratings")
async def get_source_ratings(
        source_id: int = Path(..., ge=1),
        current_user=Depends(get_current_user)
):
    """
    Get all ratings for a specific source.
    """
    # source_service = SourceService(db)
    # rating_service = RatingService(db)
    #
    # source = source_service.get_source_by_id(source_id)
    # if not source:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Source with ID {source_id} not found"
    #     )
    #
    # return rating_service.get_ratings_by_source_id(source_id)
    pass


# @router.post("/{source_id}/ratings", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
# async def rate_source(
#         rating: RatingCreate,
#         source_id: int = Path(..., ge=1),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Add or update a rating for a source.
#     """
#     source_service = SourceService(db)
#     rating_service = RatingService(db)
#
#     source = source_service.get_source_by_id(source_id)
#     if not source:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Source with ID {source_id} not found"
#         )
#
#     # Check if user already rated this source
#     existing_rating = rating_service.get_user_rating_for_source(current_user.id, source_id)
#
#     if existing_rating:
#         # Update existing rating
#         return rating_service.update_rating(existing_rating.rating_id, rating.value)
#     else:
#         # Create new rating
#         return rating_service.create_rating(current_user.id, source_id, rating.value)
#
#
# # Source Tags endpoints
# @router.get("/{source_id}/tags", response_model=List[TagResponse])
# async def get_source_tags(
#         source_id: int = Path(..., ge=1),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ):
#     """
#     Get all tags for a specific source.
#     """
#     source_service = SourceService(db)
#     tag_service = TagService(db)
#
#     source = source_service.get_source_by_id(source_id)
#     if not source:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Source with ID {source_id} not found"
#         )
#
#     return tag_service.get_tags_by_source_id(source_id)
#
#
# @router.post("/{source_id}/tags", response_model=SourceTagResponse, status_code=status.HTTP_201_CREATED)
# async def add_tag_to_source(
#         tag_data: SourceTagCreate,
#         source_id: int = Path(..., ge=1),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Add a tag to a source.
#     """
#     source_service = SourceService(db)
#     tag_service = TagService(db)
#
#     source = source_service.get_source_by_id(source_id)
#     if not source:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Source with ID {source_id} not found"
#         )
#
#     # Check if user is owner or admin
#     if source.added_by != current_user.id and not current_user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to add tags to this source"
#         )
#
#     tag = tag_service.get_tag_by_id(tag_data.tag_id)
#     if not tag:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Tag with ID {tag_data.tag_id} not found"
#         )
#
#     # Check if tag is already linked to source
#     if tag_service.is_tag_linked_to_source(tag_data.tag_id, source_id):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Tag is already linked to this source"
#         )
#
#     return tag_service.link_tag_to_source(tag_data.tag_id, source_id)
#
#
# @router.delete("/{source_id}/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def remove_tag_from_source(
#         source_id: int = Path(..., ge=1),
#         tag_id: int = Path(..., ge=1),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_active_user)
# ):
#     """
#     Remove a tag from a source.
#     """
#     source_service = SourceService(db)
#     tag_service = TagService(db)
#
#     source = source_service.get_source_by_id(source_id)
#     if not source:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Source with ID {source_id} not found"
#         )
#
#     # Check if user is owner or admin
#     if source.added_by != current_user.id and not current_user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to remove tags from this source"
#         )
#
#     # Check if tag is linked to source
#     if not tag_service.is_tag_linked_to_source(tag_id, source_id):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Tag with ID {tag_id} is not linked to this source"
#         )
#
#     tag_service.unlink_tag_from_source(tag_id, source_id)
#     return None
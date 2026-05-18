from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.post import Post
from app.models.member import Member
from app.models.tag import Tag

router = APIRouter()


# 게시글 작성
@router.post("/post/upload")
async def create_post(
    title: str,
    content: str,
    tag_id: int,
    member_id: int,
    image_url: str = None,
    db: Session = Depends(get_db)
):

    member = db.query(Member).filter(Member.id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()

    if not tag:
        raise HTTPException(status_code=404, detail="태그를 찾을 수 없습니다.")

    new_post = Post(
        title=title,
        content=content,
        tag_id=tag_id,
        member_id=member_id,
        image_url=image_url
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "message": "게시글 작성 완료",
        "post_id": new_post.post_id
    }


# 게시글 전체 조회
@router.get("/post/list")
async def get_post_list(db: Session = Depends(get_db)):

    posts = (
        db.query(Post)
        .filter(Post.status == "ACTIVE")
        .order_by(Post.created_at.desc())
        .all()
    )

    result = []

    for post in posts:
        result.append({
            "post_id": post.post_id,
            "title": post.title,
            "content": post.content,
            "image_url": post.image_url,
            "created_at": post.created_at,
            "member_id": post.member_id,
            "tag_id": post.tag_id
        })

    return result


# 게시글 상세 조회
@router.get("/post/{post_id}")
async def get_post_detail(
    post_id: int,
    db: Session = Depends(get_db)
):

    post = (
        db.query(Post)
        .filter(
            Post.post_id == post_id,
            Post.status == "ACTIVE"
        )
        .first()
    )

    if not post:
        raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다.")

    return {
        "post_id": post.post_id,
        "title": post.title,
        "content": post.content,
        "image_url": post.image_url,
        "created_at": post.created_at,
        "member_id": post.member_id,
        "tag_id": post.tag_id
    }


# 게시글 수정
@router.put("/post/update/{post_id}")
async def update_post(
    post_id: int,
    title: str,
    content: str,
    tag_id: int,
    image_url: str = None,
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(Post.post_id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다.")

    post.title = title
    post.content = content
    post.tag_id = tag_id
    post.image_url = image_url

    db.commit()

    return {
        "message": "게시글 수정 완료"
    }


# 게시글 삭제
@router.delete("/post/delete/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(Post.post_id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="게시글이 존재하지 않습니다.")

    post.status = "DELETED"

    db.commit()

    return {
        "message": "게시글 삭제 완료"
    }
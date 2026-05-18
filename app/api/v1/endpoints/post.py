from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.post import Post
from app.models.member import Member
from app.models.tag import Tag
from app.models.comment import Comment

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
            "tag_id": post.tag_id,
            "nickname": post.member.nickname
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
        "tag_id": post.tag_id,
        "nickname": post.member.nickname
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


# 태그 리스트 조회
@router.get("/tag/list")
async def get_tag_list(db: Session = Depends(get_db)):

    tags = (
        db.query(Tag)
        .filter(Tag.status == "ACTIVE")
        .all()
    )

    result = []

    for tag in tags:
        result.append({
            "tag_id": tag.tag_id,
            "tag_name": tag.tag_name
        })

    return result

# 댓글 작성
@router.post("/comment/upload")
async def create_comment(
    content: str,
    post_id: int,
    member_id: int,
    parent_id: int | None = None,
    db: Session = Depends(get_db)
):

    member = db.query(Member).filter(Member.id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    post = db.query(Post).filter(Post.post_id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    # 부모 댓글 검증
    if parent_id:
        parent_comment = (
            db.query(Comment)
            .filter(Comment.comment_id == parent_id)
            .first()
        )

        if not parent_comment:
            raise HTTPException(
                status_code=404,
                detail="부모 댓글이 존재하지 않습니다."
            )

    new_comment = Comment(
        content=content,
        post_id=post_id,
        member_id=member_id,
        parent_id=parent_id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "message": "댓글 작성 완료",
        "comment_id": new_comment.comment_id
    }


# 댓글 리스트 조회
@router.get("/comment/list")
async def get_comment_list(db: Session = Depends(get_db)):

    comments = (
        db.query(Comment)
        .join(Post, Comment.post_id == Post.post_id)
        .filter(Post.status == "ACTIVE")
        .order_by(Comment.created_at.desc())
        .all()
    )

    result = []

    for comment in comments:
        result.append({
            "comment_id": comment.comment_id,
            "member_id": comment.member_id,
            "post_id": comment.post.post_id,
            "content": comment.content,
            "parent_id": comment.parent_id,
            "created_at": comment.created_at,
            "nickname": comment.member.nickname
        })

    return result
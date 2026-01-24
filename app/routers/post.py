# from app import oauth2
from ..import models, schemas, utils, oauth2
from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, cast
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
               limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print("Current user:", current_user.id)
    # print(limit)
    # db_posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()#.filter(models.Post.owner_id == current_user.id)

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
     models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results

@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""Insert into posts (title, content, published) values (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(current_user.email)
    new_post=models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id = %s""", (id,))
    # post=cursor.fetchone()
    # new_post=db.query(models.Post).filter(models.Post.id == id).first()

    new_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
     models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f" Sorry Post with id={id} Was Not Found")
    return new_post



"""CHATGPT CODE START HERE Need to be reviewed"""

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM Posts where id = %s returning *""",(id,))
    # d_post=cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post: Optional[models.Post] = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    print(type(post.owner_id), type(current_user.id))

    owner_id: int = cast(int, post.owner_id)
    if owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""CHATGPT CODE START HERE Need to be reviewed"""

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    db_post: Optional[models.Post] = post_query.first()

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sorry Post with id={id} Was Not Found"
        )

    owner_id: int = cast(int, db_post.owner_id)
    if owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are Not authorized to perform requested action")

    update_data = post.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)

    return db_post
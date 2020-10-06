from sqlalchemy import asc, desc, or_

from extensions import db


class Friendship(db.Model):
    __tablename__ = 'friendship'

    user_id_1 = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    user_id_2 = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean(), default=False)

    avatar_image = db.Column(db.String(100), default=None)

    friends = db.relationship('User', 
                              secondary='friendship', 
                              primaryjoin=id==Friendship.user_id_1,
                              secondaryjoin=id==Friendship.user_id_2,
                              lazy='dynamic')
    
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all(cls, q: str, page: int, per_page: int, sort: str, order: str):
        keyword = '%{keyword}%'.format(keyword=q)

        if order == 'asc':
            sort_logic = asc(getattr(cls, sort))
        else:
            sort_logic = desc(getattr(cls, sort))

        return cls.query.filter(cls.username.ilike(keyword)).order_by(sort_logic).paginate(page=page, per_page=per_page)

    def get_all_friends(self, q: str, page: int, per_page: int, sort: str, order: str):
        keyword = '%{keyword}%'.format(keyword=q)

        if order == 'asc':
            sort_logic = asc(getattr(User, sort))
        else:
            sort_logic = desc(getattr(User, sort))
        
        return self.friends.filter(or_(User.username.ilike(keyword), User.email.ilike(keyword))).order_by(sort_logic).paginate(page=page, per_page=per_page)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

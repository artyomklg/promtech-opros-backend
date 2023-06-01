oauth_account = Table(
    'oauth_account',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('oauth_name', String, index=True, nullable=False),
    Column('access_token', String, nullable=False),
    Column('idexpires_at', Integer, nullable=True),
    Column('refresh_token', String, nullable=True),
    Column('account_id', String, index=True, nullable=False),
    Column('account_email', String, nullable=False)
)

user = Table(
    'user',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
    Column("role_id", UUID, ForeignKey(oauth_account.c.id)),
)


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    id: uuid.UUID = Column(UUID, primary_key=True, default=uuid.uuid4)
    oauth_name: str = Column(String(length=100), index=True, nullable=False)
    access_token: str = Column(String(length=1024), nullable=False)
    expires_at: int | None = Column(Integer, nullable=True)
    refresh_token: str | None = Column(String(length=1024), nullable=True)
    account_id: str = Column(String(length=320), index=True, nullable=False)
    account_email: str = Column(String(length=320), nullable=False)
    user_id: uuid.UUID = Column(UUID, ForeignKey(
        'user.id', ondelete='cascade'), nullable=False)

    owner = relationship(
        'User', back_populates='oauth_accounts', uselist=False)


class User(SQLAlchemyBaseUserTableUUID, Base):
    id: uuid.UUID = Column(UUID, primary_key=True)
    email: str = Column(String(length=320), unique=True,
                        index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    oauth_accounts = relationship(
        'OAuthAccount', lazy='joined', back_populates='owner', uselist=True)

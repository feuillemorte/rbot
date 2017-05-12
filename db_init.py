from framework.base_user import Base, engine

Base.metadata.create_all(bind=engine)

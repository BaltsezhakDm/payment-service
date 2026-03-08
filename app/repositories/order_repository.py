from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import Order
 

class SqlAlchemyOrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, order_id: int) -> Order | None:
        return self.session.get(Order, order_id)

    def list(self) -> list[Order]:
        return list(self.session.scalars(select(Order)).all())

    def save(self, order: Order) -> Order:
        self.session.add(order)
        self.session.flush()
        self.session.refresh(order)
        return order
import reflex as rx
from sqlmodel import Field, func
from datetime import datetime, date, timezone
from NNProtect_new_website.utils.timezone_mx import get_mexico_now

class UserRankHistory(rx.Model, table=True):
    """
    Historial de rangos con timestamps México Central (UTC - 6h).
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    member_id: int = Field(index=True, foreign_key="users.member_id")
    rank_id: int = Field(default=None, index=True, foreign_key="ranks.id")
    
    # ✅ Timestamp México Central (UTC - 6 horas)
    achieved_on: datetime = Field(
        default_factory=get_mexico_now,
        sa_column_kwargs={
            "server_default": func.now() - func.interval('6 hours')
        }
    )

    period_id: int | None = Field(default=None, index=True, foreign_key="periods.id")
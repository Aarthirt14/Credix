from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api_server.api.deps import get_current_user
from api_server.db.session import get_db
from api_server.models.customer import Customer
from api_server.models.user import User
from api_server.schemas.customer import CustomerCreate, CustomerRead

router = APIRouter()


@router.post("", response_model=CustomerRead)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    existing = db.query(Customer).filter(Customer.phone == payload.phone).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone already exists")

    customer = Customer(name=payload.name, phone=payload.phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("", response_model=list[CustomerRead])
def list_customers(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Customer).order_by(Customer.created_at.desc()).all()


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer



 
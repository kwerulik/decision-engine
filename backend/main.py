from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Inbank Decision Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MIN_AMOUNT = 2000
MAX_AMOUNT = 10000
MIN_PERIOD = 12
MAX_PERIOD = 60

# Hard coded results
MOCK_REGISTRY = {
    "49002010965": {"debt": True, "modifier": 0},
    "49002010976": {"debt": False, "modifier": 100},
    "49002010987": {"debt": False, "modifier": 300},
    "49002010998": {"debt": False, "modifier": 1000},
}

class LoanApplication(BaseModel):
    loan_amount: int = Field(ge=MIN_AMOUNT, le=MAX_AMOUNT)
    loan_period: int = Field(ge=MIN_PERIOD, le=MAX_PERIOD)
    personal_code: str

class LoanResponse(BaseModel):
    approved: bool
    amount: int | None = None
    period: int | None = None
    message: str


def process_loan_application(application:LoanApplication) -> LoanResponse:
    '''
        Checks for debt, calculates the max possible amount, and tries to find 
        a longer period if the initial amount is below the 2000 minimum.
    '''
    user_data = MOCK_REGISTRY.get(application.personal_code)

    if not user_data:
        raise HTTPException(status_code=404, detail="Personal code not found")
    
    if user_data["debt"]:
        return LoanResponse(
            approved=False,
            message="Loan denied due to existing debt."
        )
    
    modifier = user_data["modifier"]

    def calc_max_amount(mod: int, period: int) -> int:
        ''' Calculates the maximum loan amount based on the modifier and period.'''
        return mod * period
    
    max_possible_amount = calc_max_amount(modifier, application.loan_period)
    approved_amount = min(max_possible_amount, MAX_AMOUNT)

    if approved_amount >= MIN_AMOUNT:
        return LoanResponse(
            approved=True,
            amount=approved_amount,
            period=application.loan_period,
            message="Loan approved"
        )
    
    for new_period in range(application.loan_period + 1, MAX_PERIOD + 1):
        new_max_amount = calc_max_amount(modifier, new_period)
        if new_max_amount >= MIN_AMOUNT:
            return LoanResponse(
                approved=True,
                amount=min(new_max_amount, MAX_AMOUNT),
                period=new_period,
                message="Requested period too short for minimum loan amount. Adjusted to a new suitable period"
            )
        
    return LoanResponse(
        approved=False,
        message="Application rejected: Credit score too low even for the maximum period."
    )

@app.post("/api/decision", response_model=LoanResponse)
def make_decision(application: LoanApplication):
    '''
    Main endpoint for loan decisions.
    '''
    return process_loan_application(application)

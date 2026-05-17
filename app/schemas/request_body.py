from pydantic import BaseModel, Field

class CustomerChurnInput(BaseModel):
    
    CustomerID: int = Field(..., description="Unique identifier for the customer", examples=[260758])
    Age: int = Field(..., description="Age of the customer", examples=[44])
    Gender: str = Field(..., description="Gender of the customer (Male/Female)", examples=["Female"])
    Tenure: int = Field(..., description="How many months the customer has been with the company", examples=[4])
    Usage_Frequency: int = Field(..., alias="Usage Frequency", description="Number of times customer uses the service per month", examples=[26])
    Support_Calls: int = Field(..., alias="Support Calls", description="Number of calls made to customer support", examples=[1])
    Payment_Delay: int = Field(..., alias="Payment Delay", description="Number of days payment has been delayed", examples=[7])
    Subscription_Type: str = Field(..., alias="Subscription Type", description="Type of subscription (Basic/Standard/Premium)", examples=["Premium"])
    Contract_Length: str = Field(..., alias="Contract Length", description="Duration of contract (Monthly/Quarterly/Annual)", examples=["Monthly"])
    Total_Spend: float = Field(..., alias="Total Spend", description="Total monetary amount spent by the customer", examples=[319.48])
    Last_Interaction: int = Field(..., alias="Last Interaction", description="Days since last interaction or activity", examples=[13])

from fastapi import APIRouter,Request, HTTPException
from app.schemas.SSL_schemas import CertificateInspectionResponse,ScoreResponse
from app.services.SSL.certificate_service import inspect_domain
from app.services.SSL.scores import calculate_scores

router = APIRouter(
    prefix="/certificates",
    tags=["Certificates"]
)




@router.get("/")
async def get_certtres():
    return  'tres'


@router.get("/inspect",response_model=CertificateInspectionResponse)
async def get_certdata(domain: str):
    try:
        return inspect_domain(domain)
    except Exception as e:
        # You can log e here if you want
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/score")
def score_domain(domain: str) -> ScoreResponse:
    try:
        cert_data = inspect_domain(domain)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    scores, explanations = calculate_scores(cert_data)
    overall = sum(scores.values()) / len(scores)

    return {
        "domain": domain,
        "scores": scores,
        "overall_score": round(overall, 2),
        "explanations": explanations,
        "raw_certificate": cert_data
    }



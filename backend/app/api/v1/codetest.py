from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_db, get_current_user, require_roles
from app.models.codetest import Test, Problem, Submission
from app.schemas.codetest import TestCreate, ProblemCreate, SubmissionCreate

router = APIRouter()

@router.post("/tests", dependencies=[Depends(require_roles("admin","superadmin"))])
async def create_test(data: TestCreate, db: AsyncSession = Depends(get_db)):
    test = Test(**data.dict())
    db.add(test)
    await db.commit()
    return {"status": "created"}

@router.post("/tests/{test_id}/problems", dependencies=[Depends(require_roles("admin","superadmin"))])
async def add_problem(test_id: int, data: ProblemCreate, db: AsyncSession = Depends(get_db)):
    prob = Problem(test_id=test_id, **data.dict())
    db.add(prob)
    await db.commit()
    return {"status": "problem added"}

@router.post("/problems/{problem_id}/submit")
async def submit(problem_id: int, data: SubmissionCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.execute(select(Problem).where(Problem.id == problem_id))
    problem = res.scalar_one()
    result = "correct" if data.code.strip() == problem.answer.strip() else "wrong"

    sub = Submission(
        problem_id=problem_id,
        user_id=user.id,
        code=data.code,
        result=result
    )
    db.add(sub)
    await db.commit()
    return {"result": result}

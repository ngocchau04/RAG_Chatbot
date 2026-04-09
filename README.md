# RAG Chatbot Monorepo (Next.js + FastAPI)

Kien truc theo SOLID, tach thanh:
- `apps/web`: UI chat (Next.js App Router)
- `apps/api`: RAG API (FastAPI)
- `packages/shared`: schema/tai lieu dung chung

## Run nhanh

### 1) Backend
```bash
cd apps/api
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend
```bash
cd apps/web
npm install
npm run dev
```

Mac dinh frontend goi `http://localhost:8000/api/v1/chat`.

## SOLID mapping
- **S**: Use case (`AnswerQuestionUseCase`) chi chua nghiep vu hoi/dap.
- **O**: Thay OpenAI bang provider khac chi can them adapter moi implement port.
- **L**: `RagProviderPort` co the thay the boi moi provider tuan thu contract.
- **I**: Port nho gon, chi chua hanh vi can thiet cho use case.
- **D**: Use case phu thuoc abstraction (`RagProviderPort`), khong phu thuoc SDK cu the.

## Hoi truc tiep tren 1 file PDF

Frontend da co nut upload PDF. Khi chon file, cau hoi se duoc gui den endpoint multipart:
- `POST /api/v1/chat/file`
- Form fields: `query` (text), `file` (pdf)

Backend tao vector store tam, nap file PDF vao OpenAI, goi `responses.create` voi `file_search`, tra ve cau tra loi + citation, sau do xoa tai nguyen tam.

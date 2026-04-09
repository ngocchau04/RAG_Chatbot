# RAG Chatbot Monorepo (Next.js + FastAPI)

Kien truc theo SOLID, tach thanh:
- `apps/web`: UI chat (Next.js App Router)
- `apps/api`: RAG API (FastAPI)
- `packages/shared`: schema/tai lieu dung chung

## Chay local (khong Docker)

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

UI chay o `http://localhost:3000`.
Frontend goi API qua `/backend/*` (Next rewrite sang `http://localhost:8000/*`).

## Docker Packaging + Deploy

### 1) Chuan bi env
```bash
cp .env.example .env
```
Cap nhat gia tri bat buoc trong `.env`:
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (mac dinh `gpt-4o-mini`)
- `OPENAI_VECTOR_STORE_ID` (neu dung kho tai lieu co san)
- `OPENAI_BASE_URL` (de trong neu goi truc tiep OpenAI)

### 2) Build va chay
```bash
docker compose up -d --build
```

### 3) Kiem tra health
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/chat/openai-health
```

### 4) Truy cap
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

## Deploy len VPS (Ubuntu)

1. Cai Docker + Docker Compose plugin tren VPS.
2. Clone source len VPS, tao `.env`.
3. Chay:
```bash
docker compose up -d --build
```
4. Mo firewall port `3000` (va `8000` neu can goi API truc tiep).
5. Khuyen nghi dung reverse proxy (Nginx/Caddy) + HTTPS cho production.

## SOLID mapping
- **S**: Use case (`AnswerQuestionUseCase`) chi chua nghiep vu hoi/dap.
- **O**: Thay OpenAI bang provider khac chi can them adapter moi implement port.
- **L**: `RagProviderPort` co the thay the boi moi provider tuan thu contract.
- **I**: Port nho gon, chi chua hanh vi can thiet cho use case.
- **D**: Use case phu thuoc abstraction (`RagProviderPort`), khong phu thuoc SDK cu the.

## Hoi truc tiep tren 1 file PDF

Frontend co nut upload PDF. Khi chon file, cau hoi se duoc gui den endpoint multipart:
- `POST /api/v1/chat/file`
- Form fields: `query` (text), `file` (pdf)

Backend tao vector store tam, nap file PDF vao OpenAI, goi `responses.create` voi `file_search`, tra ve cau tra loi + citation, sau do xoa tai nguyen tam.

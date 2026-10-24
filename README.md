# Claude-2026-everything

## 아침 뉴스 10선
매일 08:00 KST 기준으로 지난 24시간의 국내·해외 주요 뉴스 10개를 골라 `briefings/`에 누적한다.

- 생성 사양: [BRIEFING_SPEC.md](BRIEFING_SPEC.md)
- 아카이브: [briefings/](briefings/README.md)
- 실행: Claude Code Routine (매일 07:52 KST 정식 실행, 08:52 KST 재시도). 뉴스는 `scripts/collect_rss.py`로 언론사 RSS에서 모으고 검색으로 보충한다. 상세는 `ROUTINE_PROMPT.md` 참고

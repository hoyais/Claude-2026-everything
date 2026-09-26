# Routine 프롬프트 (등록된 원문)

매일 07:52 KST에 새 세션으로 실행된다. 원문 수정은 Routine(update_trigger)에서 한다.

---

오늘의 "아침 뉴스 10선" 브리핑을 만들어 레포에 커밋해줘.

1. hoyais/Claude-2026-everything 레포에서 `claude/morning-news-briefing-ld3gsq` 브랜치를 fetch하고 체크아웃해서 최신 상태로 맞춘다.
2. 레포 루트의 `BRIEFING_SPEC.md`를 읽고 수집 창, 범위, 수집 방법, 선정 기준, 출력 형식, 커밋 규칙을 **그대로** 따른다. 날짜는 `TZ=Asia/Seoul date`로 확인한다.
3. `briefings/YYYY/YYYY-MM-DD.md`를 작성하고, `briefings/README.md` 인덱스를 갱신한 뒤, 커밋하고 푸시한다.
4. 오늘 날짜 파일이 이미 있으면 새로 만들지 말고 종료한다.
5. PR은 만들지 않는다. 마지막에 파일 경로와 '오늘의 한 줄'만 출력한다.

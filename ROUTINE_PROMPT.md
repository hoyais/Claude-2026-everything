# Routine 프롬프트 (등록된 원문)

매일 07:52 KST에 새 세션으로 실행된다. 원문 수정은 Routine(update_trigger)에서 한다.
완료 알림: 폰 푸시 (마지막 응답의 세 줄이 알림 요약에 담긴다).

---

오늘의 "아침 뉴스 10선" 브리핑을 만들어 레포에 커밋해줘.

1. hoyais/Claude-2026-everything 레포에서 `claude/morning-news-briefing` 브랜치를 fetch하고 체크아웃해서 최신 상태로 맞춘다. 레포가 없으면 clone한다.
2. 레포 루트의 `BRIEFING_SPEC.md`를 읽고 수집 창, 범위, 수집 방법, 선정 기준, 출력 형식, 커밋 규칙을 **그대로** 따른다. 날짜는 `TZ=Asia/Seoul date +%F`로 확인한다.
3. `briefings/YYYY/YYYY-MM-DD.md`를 작성하고, `briefings/README.md` 인덱스를 갱신한 뒤, 커밋하고 `git push -u origin claude/morning-news-briefing`로 푸시한다. 푸시 후 `git ls-remote`로 원격에 커밋이 반영됐는지 확인한다.
4. 오늘 날짜 파일이 이미 원격에 있으면 새로 만들지 말고 5단계로 간다.
5. PR은 만들지 않는다. 마지막 응답은 아래 세 줄만 출력한다. **자리표시자를 그대로 쓰지 말고 실제 값으로 채운다.**
   - 1줄: `📰 아침 뉴스 10선 ` 뒤에 실제 날짜(예: 2026-09-28)
   - 2줄: 오늘 파일의 `**오늘의 한 줄**:` 뒤에 있는 문장을 그대로 옮긴다.
   - 3줄: 생략 없는 전체 URL `https://github.com/hoyais/Claude-2026-everything/blob/claude/morning-news-briefing/briefings/<연도>/<날짜>.md` (예: .../briefings/2026/2026-09-28.md). `...`로 줄이지 않는다.
   실패했으면 3줄 대신 `❌ 실패: <실제 원인 한 줄>`을 출력한다.

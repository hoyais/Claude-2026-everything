# Routine 프롬프트 (등록된 원문)

매일 07:52 KST에 새 세션으로 실행된다. 원문 수정은 Routine(update_trigger)에서 한다.
완료 알림: 폰 푸시 (마지막 응답의 세 줄이 알림 요약에 담긴다).
테스트: `briefings/_test/RUN_TEST`를 커밋해 두고 Routine을 수동 실행하면, 실제 경로 대신 `briefings/_test/`에 전체 흐름으로 생성·푸시한다(플래그는 같은 커밋에서 삭제).

---

오늘의 "아침 뉴스 10선" 브리핑을 만들어 레포에 커밋해줘.

1. hoyais/Claude-2026-everything 레포에서 `claude/morning-news-briefing` 브랜치를 fetch하고 체크아웃해서 최신 상태로 맞춘다. 레포가 없으면 clone한다.
2. 먼저 `D=$(TZ=Asia/Seoul date +%F); Y=${D:0:4}`로 오늘 날짜를 구한다. 이후 모든 날짜는 이 값만 사용한다.
   - **테스트 모드**: 브랜치에 `briefings/_test/RUN_TEST` 파일이 있으면 테스트 모드다. 이때 출력 파일 `OUT=briefings/_test/$D.md`, 인덱스(`briefings/README.md`)는 수정하지 않는다, 오늘 파일 존재 여부와 관계없이 3~4단계를 끝까지 수행한다, 같은 커밋에서 `git rm briefings/_test/RUN_TEST`로 플래그를 삭제한다, 커밋 메시지는 `test: $D E2E 테스트 브리핑`이다.
   - 테스트 모드가 아니면 `OUT=briefings/$Y/$D.md`이다.
3. 레포 루트의 `BRIEFING_SPEC.md`를 읽고 수집 창, 범위, 수집 방법, 선정 기준, 출력 형식, 커밋 규칙을 **그대로** 따른다.
4. `$OUT`을 작성하고, (테스트 모드가 아니면) `briefings/README.md` 인덱스를 갱신한 뒤, 커밋하고 `git push -u origin claude/morning-news-briefing`로 푸시한다. 푸시 후 `git ls-remote`로 원격에 커밋이 반영됐는지 확인한다.
   테스트 모드가 아니고 오늘 날짜 파일이 이미 원격에 있으면 새로 만들지 말고 5단계로 간다.
5. PR은 만들지 않는다. 마지막 응답은 아래 명령의 출력을 **그대로** 붙여서 세 줄만 출력한다. 직접 타이핑하지 않는다.
   ```
   echo "📰 아침 뉴스 10선 $D"
   grep -m1 '오늘의 한 줄' "$OUT" | sed 's/.*\*\*: *//'
   echo "https://github.com/hoyais/Claude-2026-everything/blob/claude/morning-news-briefing/$OUT"
   ```
   푸시를 포함해 어느 단계든 실패했으면 세 번째 줄 대신 `❌ 실패: <git 에러 원문 등 실제 원인 한 줄>`을 출력한다.

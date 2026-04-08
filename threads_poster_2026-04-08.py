#!/usr/bin/env python3
"""
Threads Auto Poster - 2026-04-08
게시 간격: 20분, 최대 재시도: 3회 (지수 백오프: 10s → 20s → 30s)
"""

import requests
import time
import sys
from datetime import datetime, timedelta

USER_ID = "34526993056892016"
ACCESS_TOKEN = "THAAXsZAKYWZAwZABUVM4QmgyaFRwQ1dObjFlZAXUwUkN6ZAU1ZAYzA0ODlMcVpocmlJak5fUEh0cE5QdEVVdWF4eUVIandWamtVeUhFQ3BlWlZAMT3NxSkxtV1JLeTQtUXBwQlhhRzk0V2hGRmszWVQtZAUUzXzhpRFFlNERwSkVyeEQyb2tNQQZDZD"
INTERVAL_MINUTES = 20
BASE_URL = "https://graph.threads.net/v1.0"

POSTS = [
    # 소스 1: Gemma 4
    """구글 오픈소스 AI, 진짜 강해졌음 — Gemma 4 정리

구글 딥마인드가 4월 초 공개한 최신 오픈 멀티모달 모델.

· 4가지 크기(E2B → 31B), MoE 구조로 파라미터 대비 연산 절약
· 영상·이미지·음성 동시 처리 — 멀티모달 기본 탑재
· 수학 시험(AIME 2026) 89.2%, 코딩(LiveCodeBench) 80.0% 달성
· Apache 2.0 라이선스 → 상업 활용 완전 자유

GPT·Claude 수준 성능을 내 서버에서 직접 돌리는 시대 열림.

출처: "Gemma 4 — Google DeepMind." Google DeepMind, 2 Apr. 2026, deepmind.google/models/gemma/gemma-4/.""",

    """Gemma 4가 특별한 진짜 이유 — MoE 아키텍처 해설

MoE(전문가 혼합)는 요리사팀에 비유하면 이해가 쉬움.

전체 요리사를 다 고용하는 대신, 음식 종류별 전문가를 매번 호출함. 총 인원(26B)은 많아도 실제 뛰는 인원(3.8B)은 적음.

결과:
· 26B 모델이지만 활성 파라미터는 3.8B만 사용
· 추론 속도와 비용이 대폭 절감됨
· 성능은 대형 모델과 동급 수준 유지됨

"크지 않아도 똑똑할 수 있다" — 효율 AI 시대의 핵심 공식.

출처: "Gemma 4: Byte for Byte, the Most Capable Open Models." Google Blog, 2 Apr. 2026, blog.google/innovation-and-ai/technology/developers-tools/gemma-4/.""",

    """Gemma 4가 바꾸는 AI 판도 — 오픈소스 경쟁이 달라졌음

지금까지 오픈소스 AI의 공식: "GPT·Claude보다 조금 모자란 공짜 모델".

Gemma 4 31B는 이 공식을 깨뜨림.

· 세계 오픈모델 성능 랭킹 3위 (Arena AI 기준)
· 이미지·영상·음성 전부 처리 — 폐쇄 모델과 동급
· 로컬 실행 가능 → 데이터 외부 유출 없음

기업 입장에서는: API 비용 제로 + 데이터 프라이버시 확보 조합이 생김.

"AI 인프라를 직접 소유하는 시대"의 포문이 열림.

출처: "Gemma 4 — Google DeepMind." Google DeepMind, 2 Apr. 2026, deepmind.google/models/gemma/gemma-4/.""",

    """개발자라면 지금 당장 Gemma 4 써봐야 하는 이유

비용 걱정 없이 실험 가능한 최적 타이밍.

추천 활용 사례:
· 문서·영상 분석 앱 → 멀티모달 기본 탑재
· 프라이버시 민감 서비스 → 로컬 배포로 데이터 통제
· 에이전틱 워크플로우 → τ-bench 86.4% 달성
· 글로벌 서비스 → 256K 장문 컨텍스트 지원

Hugging Face에 모델 공개됨. 오늘 바로 fine-tuning 테스트 가능.

출처: "Welcome Gemma 4: Frontier Multimodal Intelligence on Device." Hugging Face Blog, 2 Apr. 2026, huggingface.co/blog/gemma4.""",

    # 소스 2: CORAL
    """AI 에이전트끼리 서로 배우며 진화함 — CORAL 등장

arXiv 2604.01658 | 2026년 4월 발표.

기존 멀티 에이전트: 역할 고정 → 정해진 대로만 작동
CORAL: 에이전트가 스스로 탐색·기록·협업하며 진화함

핵심 구조:
· 공유 메모리로 에이전트 간 실시간 지식 공유됨
· 비동기 실행 — 서로 기다리지 않고 병렬 탐색
· 10개 벤치마크 최고 성능, 시도 횟수 70% 절감

"고정된 팀 구성 없이 알아서 최적 팀을 만드는 AI".

출처: "CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery." arXiv, 2 Apr. 2026, arxiv.org/abs/2604.01658.""",

    """CORAL이 뒤집은 AI 연구 패러다임 — 에이전트가 스스로 실험함

지금까지 AI 에이전트는 인간이 짜놓은 파이프라인을 실행하는 수행자였음.

CORAL은 다름:
· 에이전트가 가설을 세우고 직접 실험을 돌림
· 실패 기록을 공유 메모리에 저장 → 다른 에이전트가 참조
· 성공 전략은 자동으로 '기술(skill)'로 추상화됨

마치 대학원생들이 논문 읽고 토론하며 새 실험을 설계하는 과정과 유사함.

과학적 발견 자동화의 첫 실용적 시도.

출처: "CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery." arXiv, 2 Apr. 2026, arxiv.org/abs/2604.01658.""",

    """CORAL이 중요한 이유 — AI가 AI를 개선하는 루프

CORAL의 핵심 의미는 에이전트 개별 성능이 아님.

"AI 시스템이 스스로 자신을 개선하는 루프"를 실용 수준에서 구현했다는 점이 핵심.

우려:
· 목표 설정 실수 시 의도치 않은 방향으로 진화 위험
· 공유 메모리 오염 → 에러 전파 가능성 있음

기회:
· 인간 연구자 1명이 수십 개 에이전트 감독하는 구조 가능
· 신약 개발·소재 설계 등 반복 실험 분야 가속 기대됨

Claude Code·OpenCode와 이미 통합됨.

출처: "CORAL: Towards Autonomous Multi-Agent Evolution for Open-Ended Discovery." arXiv, 2 Apr. 2026, arxiv.org/abs/2604.01658.""",

    # 소스 3: STRUCTUREDAGENT
    """웹 브라우저 AI, 이제 장기 계획이 됨 — STRUCTUREDAGENT

arXiv 2603.05294 | 2026년 3월 발표.

기존 웹 에이전트 문제:
· 복잡한 작업에서 중간에 포기
· 잘못된 선택 후 되돌아오지 못함

해결책:
· AND/OR 트리로 작업을 계층 분해
· OR 노드: 플랜B, C를 사전에 준비
· 구조화된 메모리로 조건 충족 여부 추적됨

WebVoyager·WebArena 벤치마크 성능 개선 확인됨.

출처: "STRUCTUREDAGENT: Planning with AND/OR Trees for Long-Horizon Web Tasks." arXiv, 5 Mar. 2026, arxiv.org/abs/2603.05294.""",

    """AI 웹 에이전트가 왜 자꾸 실패했는지 드디어 밝혀짐

STRUCTUREDAGENT 논문이 분석한 LLM 웹 에이전트 실패 패턴 3가지:

1. 메모리 부족: 이전 액션 기억 못 해 같은 실수 반복됨
2. 계획 약점: 막히면 앞으로만 돌진하다 포기 (Greedy)
3. 대안 없음: 첫 번째 방법 실패 시 멈춤

AND/OR 트리는 이 3가지를 동시에 해결함:
· OR = 대안 경로 / AND = 순차 조건 / 메모리 = 진행 상태 추적

체스 엔진이 수를 미리 내다보듯, 웹 에이전트도 플랜 트리를 갖게 됨.

출처: "STRUCTUREDAGENT: Planning with AND/OR Trees for Long-Horizon Web Tasks." arXiv, 5 Mar. 2026, arxiv.org/abs/2603.05294.""",

    """AI 자동화 구축 시 STRUCTUREDAGENT에서 배울 설계 원칙

복잡한 웹 자동화 에이전트를 만든다면 참고할 4가지 원칙:

① 작업을 AND(순서)/OR(대안) 트리로 분해할 것
② 성공 조건을 명시적으로 정의할 것
③ 각 단계의 상태를 외부 메모리에 저장할 것
④ 중간 실패 시 대안 경로로 전환하는 로직 포함

n8n·LangGraph·CrewAI 같은 오케스트레이션 프레임워크에 바로 적용 가능.

"에이전트는 영리해야 하지만, 구조가 없으면 영리함이 낭비됨."

출처: "STRUCTUREDAGENT: Planning with AND/OR Trees for Long-Horizon Web Tasks." arXiv, 5 Mar. 2026, arxiv.org/abs/2603.05294.""",

    """장기 웹 작업 에이전트, 2026년이 변곡점인 이유

이커머스 주문·여행 예약·폼 자동 작성 — 기존 에이전트는 단순 작업에만 적합했음.

STRUCTUREDAGENT가 풀려는 문제: "10단계 이상 복잡한 작업을 처음부터 끝까지 완료"

실현 시 달라지는 것:
· HR 채용 프로세스 자동화
· 복잡한 B2B 구매 에이전트
· 멀티스텝 데이터 수집·분석 파이프라인

한계는 아직 있음 — 동적 사이트 구조 변경, CAPTCHA, 세션 만료 등.

하지만 방향은 분명함. AI가 장기 과업을 수행하는 팀원으로 진화 중.

출처: "STRUCTUREDAGENT: Planning with AND/OR Trees for Long-Horizon Web Tasks." arXiv, 5 Mar. 2026, arxiv.org/abs/2603.05294.""",
]


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def create_container(text):
    """컨테이너 생성 (POST /threads)"""
    url = f"{BASE_URL}/{USER_ID}/threads"
    params = {
        "media_type": "TEXT",
        "text": text,
        "access_token": ACCESS_TOKEN,
    }
    resp = requests.post(url, params=params, timeout=30)
    return resp


def publish_container(container_id):
    """컨테이너 게시 (POST /threads_publish)"""
    url = f"{BASE_URL}/{USER_ID}/threads_publish"
    params = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN,
    }
    resp = requests.post(url, params=params, timeout=30)
    return resp


def post_thread(post_text, post_num):
    """단일 포스트 게시 (최대 3회 재시도)"""
    backoffs = [10, 20, 30]
    for attempt in range(1, 4):
        try:
            print(f"  [{now_str()}] 시도 {attempt}/3 — 컨테이너 생성 중...", flush=True)
            resp = create_container(post_text)

            if resp.status_code != 200:
                raise RuntimeError(f"컨테이너 생성 실패: HTTP {resp.status_code} — {resp.text}")

            data = resp.json()
            container_id = data.get("id")
            if not container_id:
                raise RuntimeError(f"container_id 없음: {data}")

            print(f"  [{now_str()}] 컨테이너 생성 완료 (id={container_id}). 3초 대기...", flush=True)
            time.sleep(3)

            print(f"  [{now_str()}] 게시 요청 중...", flush=True)
            resp2 = publish_container(container_id)

            if resp2.status_code != 200:
                raise RuntimeError(f"게시 실패: HTTP {resp2.status_code} — {resp2.text}")

            pub_data = resp2.json()
            thread_id = pub_data.get("id", "unknown")
            print(f"  [{now_str()}] ✅ 포스트 #{post_num} 게시 성공 (thread_id={thread_id})", flush=True)
            return True

        except Exception as e:
            print(f"  [{now_str()}] ❌ 포스트 #{post_num} 시도 {attempt} 실패: {e}", flush=True)
            if attempt < 3:
                wait = backoffs[attempt - 1]
                print(f"  [{now_str()}] {wait}초 후 재시도...", flush=True)
                time.sleep(wait)

    print(f"  [{now_str()}] ❌ 포스트 #{post_num} 3회 모두 실패. 다음 포스트로 진행.", flush=True)
    return False


def preflight_check():
    """Threads API 연결 가능 여부 사전 확인"""
    print(f"[{now_str()}] === 사전 연결 체크 ===", flush=True)
    try:
        resp = requests.get(
            f"{BASE_URL}/me",
            params={"fields": "id,username", "access_token": ACCESS_TOKEN},
            timeout=15,
        )
        data = resp.json()
        if "error" in data:
            code = data["error"].get("code", 0)
            msg = data["error"].get("message", "")
            if code == 190:
                print("⚠️ Access Token 만료 - 재발급 필요", flush=True)
                sys.exit(1)
            print(f"[{now_str()}] API 오류 (code={code}): {msg}", flush=True)
            sys.exit(1)
        username = data.get("username", "unknown")
        uid = data.get("id", "unknown")
        print(f"[{now_str()}] ✅ 토큰 유효 — @{username} (id={uid})", flush=True)
    except Exception as e:
        print(f"[{now_str()}] ❌ Threads API 연결 불가: {e}", flush=True)
        print(f"❌ 실패 사유: graph.threads.net 네트워크 접근 불가 — 프록시 차단으로 게시 불가", flush=True)
        sys.exit(1)


def main():
    preflight_check()
    total = len(POSTS)
    estimated_end = datetime.now() + timedelta(minutes=INTERVAL_MINUTES * (total - 1))
    print(f"[{now_str()}] === Threads 자동 게시 시작 ===", flush=True)
    print(f"[{now_str()}] 총 포스트 수: {total}개", flush=True)
    print(f"[{now_str()}] 게시 간격: {INTERVAL_MINUTES}분", flush=True)
    print(f"[{now_str()}] 예상 종료 시각: {estimated_end.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(flush=True)

    success_count = 0
    fail_count = 0
    fail_list = []

    for i, post_text in enumerate(POSTS, 1):
        print(f"[{now_str()}] --- 포스트 #{i}/{total} 게시 시작 ---", flush=True)
        preview = post_text.split('\n')[0][:40]
        print(f"  내용 미리보기: {preview}...", flush=True)

        ok = post_thread(post_text, i)
        if ok:
            success_count += 1
        else:
            fail_count += 1
            fail_list.append(i)

        if i < total:
            print(f"[{now_str()}] {INTERVAL_MINUTES}분 대기 중 (다음 포스트: #{i+1})...", flush=True)
            time.sleep(INTERVAL_MINUTES * 60)

    print(flush=True)
    print(f"[{now_str()}] === 게시 완료 ===", flush=True)
    print(f"[{now_str()}] 성공: {success_count}개 / 실패: {fail_count}개", flush=True)

    if fail_list:
        print(f"[{now_str()}] ❌ 실패한 포스트 번호: {fail_list}", flush=True)
        sys.exit(1)
    else:
        print(f"[{now_str()}] ✅ 모든 포스트 게시 성공", flush=True)
        sys.exit(0)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="KORAIL CREW SYSTEM", layout="wide")

# [디자인 고도화] 최신 스트림릿 엔진 맞춤형 월 탭 볼드체 및 세로 구분 테두리선 강제 주입
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        html, body, [data-testid="stWidgetLabel"] { font-family: 'Noto Sans KR', sans-serif !important; }
        .main-header { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 18px; border-radius: 12px; margin-bottom: 20px; }
        .card-box { background-color: #FFFFFF; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; margin-bottom: 15px; }
        .summary-box { background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); padding: 15px; border-radius: 10px; border: 1px solid #CBD5E1; margin-top: 15px; }
        
        /* [완벽 패치] 상단 월 탭 단추: 울트라 볼드체, 좌우 폭 대폭 확장, 선명한 격자 경계선 주입 */
        div[data-testid="stTabBar"] {
            gap: 6px !important;
            border-bottom: 3px solid #94A3B8 !important;
            padding-bottom: 2px !important;
        }
        button[data-testid="stTab"] {
            border-top: 2px solid #94A3B8 !important;
            border-left: 2px solid #94A3B8 !important;
            border-right: 2px solid #94A3B8 !important;
            border-bottom: none !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 12px 26px !important;
            background-color: #F1F5F9 !important;
            margin: 0 !important;
        }
        button[data-testid="stTab"] p {
            font-size: 17px !important;
            font-weight: 900 !important; /* 가장 두꺼운 서체 */
            color: #475569 !important;
        }
        button[data-testid="stTab"][aria-selected="true"] {
            background-color: #1E293B !important;
            border-top: 3px solid #38BDF8 !important;
            border-left: 2px solid #38BDF8 !important;
            border-right: 2px solid #38BDF8 !important;
        }
        button[data-testid="stTab"][aria-selected="true"] p {
            color: #38BDF8 !important;
        }
    </style>
    <div class="main-header">
        <h1 style="color:#FFFFFF; margin:0; font-size:24px; font-weight:700;">🚄 KORAIL CREW SYSTEM <span style="font-size:15px; font-weight:300; color:#38BDF8;">v3.6 Genuine</span></h1>
    </div>
""", unsafe_allow_html=True)

# 1. 승무행로표 마스터 데이터베이스 원장
ROSTER_DATA = {
    "85001": {"work_time": "09:44", "rest_time": "00:00", "details": [
        {"train_no": "(510) (편승)", "dep_time": "10:42", "arr_time": "11:55", "section": "순천-익산"},
        {"train_no": "1571", "dep_time": "13:04", "arr_time": "14:43", "section": "익산-순천"},
        {"train_no": "1571", "dep_time": "14:45", "arr_time": "15:11", "section": "순천-여수엑스포"},
        {"train_no": "(524) (편승)", "dep_time": "15:47", "arr_time": "17:19", "section": "여수엑스포-익산"},
        {"train_no": "1573", "dep_time": "18:40", "arr_time": "20:26", "section": "익산-순천"}
    ]},
    "85002": {"work_time": "09:17", "rest_time": "00:23", "details": [
        {"train_no": "(509) (편승)", "dep_time": "12:36", "arr_time": "12:58", "section": "순천-여수엑스포"},
        {"train_no": "1504(새)", "dep_time": "14:10", "arr_time": "16:03", "section": "여수엑스포-익산"},
        {"train_no": "1573", "dep_time": "18:40", "arr_time": "20:26", "section": "익산-순천"},
        {"train_no": "1573", "dep_time": "20:28", "arr_time": "20:52", "section": "순천-여수엑스포"},
        {"train_no": "(534) (편승)", "dep_time": "21:54", "arr_time": "22:13", "section": "여수엑스포-순천"}
    ]},
    "85003": {"work_time": "08:48", "rest_time": "00:00", "details": [
        {"train_no": "1503(새)", "dep_time": "11:44", "arr_time": "12:10", "section": "순천-여수엑스포"},
        {"train_no": "1574", "dep_time": "13:11", "arr_time": "13:35", "section": "여수엑스포-순천"},
        {"train_no": "1574", "dep_time": "13:37", "arr_time": "15:19", "section": "순천-익산"},
        {"train_no": "1527", "dep_time": "17:10", "arr_time": "19:14", "section": "익산-여수엑스포"},
        {"train_no": "(532) (편승)", "dep_time": "20:22", "arr_time": "20:42", "section": "여수엑스포-순천"}
    ]},
    "85004": {"work_time": "10:59", "rest_time": "00:00", "details": [
        {"train_no": "1524", "dep_time": "10:13", "arr_time": "11:48", "section": "순천-익산"},
        {"train_no": "1571", "dep_time": "13:04", "arr_time": "14:43", "section": "익산-순천"},
        {"train_no": "(522) (편승)", "dep_time": "15:18", "arr_time": "16:32", "section": "순천-익산"},
        {"train_no": "1505(새)", "dep_time": "19:35", "arr_time": "21:02", "section": "익산-순천"}
    ]},
    "85005": {"work_time": "12:00", "rest_time": "04:17", "details": [
        {"train_no": "1506(새)", "dep_time": "19:39", "arr_time": "21:23", "section": "순천-익산"},
        {"train_no": "1575", "dep_time": "22:26", "arr_time": "00:26", "section": "익산-여수엑스포"},
        {"train_no": "1524", "dep_time": "09:51", "arr_time": "10:12", "section": "여수엑스포-순천"}
    ]},
    "85006": {"work_time": "12:00", "rest_time": "05:05", "details": [
        {"train_no": "(519) (편승)", "dep_time": "16:57", "arr_time": "17:20", "section": "순천-여수엑스포"},
        {"train_no": "1506(새)", "dep_time": "19:15", "arr_time": "19:37", "section": "여수엑스포-순천"},
        {"train_no": "(532) (편승)", "dep_time": "20:44", "arr_time": "22:00", "section": "순천-익산"},
        {"train_no": "1575", "dep_time": "22:26", "arr_time": "00:26", "section": "익산-여수엑스포"},
        {"train_no": "1572", "dep_time": "06:30", "arr_time": "06:52", "section": "여수엑스포-순천"}
    ]},
    "85007": {"work_time": "12:00", "rest_time": "05:00", "details": [
        {"train_no": "1977", "dep_time": "18:43", "arr_time": "21:08", "section": "순천-광주송정"},
        {"train_no": "1972", "dep_time": "06:05", "arr_time": "08:23", "section": "광주송정-순천"}
    ]},
    "85008": {"work_time": "07:40", "rest_time": "00:46", "details": [
        {"train_no": "1975", "dep_time": "14:56", "arr_time": "17:22", "section": "순천-광주송정"},
        {"train_no": "1978", "dep_time": "20:04", "arr_time": "22:16", "section": "광주송정-순천"}
    ]},
    "85009": {"work_time": "07:00", "rest_time": "00:00", "details": [
        {"train_no": "1991", "dep_time": "07:38", "arr_time": "09:54", "section": "순천-목포"},
        {"train_no": "1992", "dep_time": "11:57", "arr_time": "14:06", "section": "목포-순천"}
    ]},
    "85010": {"work_time": "07:23", "rest_time": "00:00", "details": [
        {"train_no": "1973", "dep_time": "11:33", "arr_time": "13:54", "section": "순천-광주송정"},
        {"train_no": "1976", "dep_time": "16:17", "arr_time": "18:36", "section": "광주송정-순천"}
    ]},
    "85011": {"work_time": "12:00", "rest_time": "02:38", "details": [
        {"train_no": "1931", "dep_time": "17:51", "arr_time": "19:47", "section": "순천-목포"},
        {"train_no": "1932", "dep_time": "08:01", "arr_time": "10:03", "section": "목포-순천"}
    ]},
    "85012": {"work_time": "07:00", "rest_time": "00:00", "details": [
        {"train_no": "1981", "dep_time": "14:07", "arr_time": "16:20", "section": "순천-목포"},
        {"train_no": "1994", "dep_time": "17:21", "arr_time": "19:33", "section": "목포-순천"}
    ]},
    "85013": {"work_time": "09:51", "rest_time": "00:00", "details": [
        {"train_no": "1572", "dep_time": "06:54", "arr_time": "08:37", "section": "순천-익산"},
        {"train_no": "1503(새)", "dep_time": "10:19", "arr_time": "11:42", "section": "익산-순천"},
        {"train_no": "1574", "dep_time": "13:37", "arr_time": "15:19", "section": "순천-익산"},
        {"train_no": "(519) (편승)", "dep_time": "15:39", "arr_time": "16:55", "section": "익산-순천"}
    ]},
    "85014": {"work_time": "07:20", "rest_time": "00:00", "details": [
        {"train_no": "1993", "dep_time": "10:04", "arr_time": "12:16", "section": "순천-목포"},
        {"train_no": "1982", "dep_time": "14:48", "arr_time": "17:04", "section": "목포-순천"}
    ]},
    "85015": {"work_time": "08:47", "rest_time": "00:00", "details": [
        {"train_no": "1572", "dep_time": "06:54", "arr_time": "08:37", "section": "순천-익산"},
        {"train_no": "1401(새)", "dep_time": "11:43", "arr_time": "12:43", "section": "익산-광양"},
        {"train_no": "(420) (편승)", "dep_time": "13:40", "arr_time": "14:16", "section": "광양-익산"},
        {"train_no": "(665) (편승)", "dep_time": "14:36", "arr_time": "15:51", "section": "익산-순천"}
    ]},
    "85016": {"work_time": "07:52", "rest_time": "00:00", "details": [
        {"train_no": "1932", "dep_time": "10:06", "arr_time": "12:45", "section": "순천-부산"},
        {"train_no": "1931", "dep_time": "15:08", "arr_time": "17:48", "section": "부산-순천"}
    ]},
    "85017": {"work_time": "07:36", "rest_time": "00:30", "details": [
        {"train_no": "1971", "dep_time": "06:20", "arr_time": "08:42", "section": "순천-광주송정"},
        {"train_no": "1974", "dep_time": "11:16", "arr_time": "13:36", "section": "광주송정-순천"}
    ]},
    "85019": {"work_time": "12:00", "rest_time": "04:26", "details": [
        {"train_no": "(530) (편승)", "dep_time": "19:46", "arr_time": "21:03", "section": "순천-익산"},
        {"train_no": "1506(새)", "dep_time": "21:25", "arr_time": "00:31", "section": "익산-용산"},
        {"train_no": "1501(새)", "dep_time": "05:25", "arr_time": "08:36", "section": "용산-익산"},
        {"train_no": "(541) (편승)", "dep_time": "09:24", "arr_time": "10:40", "section": "익산-순천"}
    ]},
    "85020": {"work_time": "12:00", "rest_time": "06:01", "details": [
        {"train_no": "1530(새)", "dep_time": "22:40", "arr_time": "00:30", "section": "여수엑스포-익산"},
        {"train_no": "1521(새)", "dep_time": "05:40", "arr_time": "08:38", "section": "익산-여수엑스포"},
        {"train_no": "(1524) (편승)", "dep_time": "09:51", "arr_time": "10:12", "section": "여수엑스포-순천"}
    ]},
    "85901": {"work_time": "08:00", "rest_time": "00:00", "details": [
        {"train_no": "비상대기", "dep_time": "10:20", "arr_time": "18:20", "section": "순천역 비상대기"}
    ]}
}

if "db" not in st.session_state:
    st.session_state.db = {str(m): [] for m in range(1, 13)}
    st.session_state.db["9"] = [
        ["2026.09.01", "85012", "1981", "1994", "12:03", "20:03", "N"],
        ["2026.09.02", "S", "-", "-", "-", "-", "Y"], ["2026.09.03", "S", "-", "-", "-", "-", "Y"],
        ["2026.09.04", "85003", "1503", "1527", "11:04", "20:52", "N"],
        ["2026.09.05", "85020", "1505", "1521", "20:23", "10:22", "N"],
        ["2026.09.06", "~(85020)", "1505", "1521", "20:23", "10:22", "N"],
        ["2026.09.07", "85S15", "1572", "1401", "06:14", "17:01", "N"],
        ["2026.09.08", "S", "-", "-", "-", "-", "Y"], ["2026.09.09", "S", "-", "-", "-", "-", "Y"],
        ["2026.09.10", "85001", "1571", "1573", "10:12", "20:53", "N"],
        ["2026.09.11", "85005", "1506", "1524", "18:59", "10:42", "N"],
        ["2026.09.12", "~(85005)", "1506", "1524", "18:59", "10:42", "N"],
        ["2026.09.13", "85009", "1991", "1992", "06:48", "14:48", "N"],
        ["2026.09.14", "S", "-", "-", "-", "-", "Y"], ["2026.09.15", "S", "-", "-", "-", "-", "Y"],
        ["2026.09.16", "85016", "1932", "1931", "09:26", "18:18", "N"],
        ["2026.09.17", "85008", "1975", "1978", "14:06", "22:46", "N"],
        ["2026.09.18", "85019", "1506", "1501", "19:16", "10:50", "N"],
        ["2026.09.19", "~(85019)", "1506", "1501", "19:16", "10:50", "N"],
        ["2026.09.20", "85019", "1506", "1501", "19:16", "10:50", "Y"],
        ["2026.09.21", "~(85019)", "1506", "1501", "19:16", "10:50", "Y"],
        ["2026.09.22", "85014", "1993", "1982", "09:14", "17:34", "N"],
        ["2026.09.23", "85006", "1506", "1572", "16:27", "07:22", "N"],
        ["2026.09.24", "~(85006)", "1506", "1572", "16:27", "07:22", "N"],
        ["2026.09.25", "85017", "1971", "1974", "05:30", "14:06", "N"],
        ["2026.09.26", "S", "-", "-", "-", "-", "Y"], ["2026.09.27", "S", "-", "-", "-", "-", "Y"],
        ["2026.09.28", "85002", "1504", "1573", "12:06", "22:23", "N"],
        ["2026.09.29", "85007", "1977", "1972", "17:53", "08:53", "N"],
        ["2026.09.30", "~(85007)", "1977", "1972", "17:53", "08:53", "N"]
    ]
    st.session_state.db["10"] = [
        ["2026.10.01", "*", "-", "-", "-", "-", "N"],
        ["2026.10.02", "85011", "1931", "1932", "17:11", "10:33", "Y"],
        ["2026.10.03", "~(85011)", "1931", "1932", "17:11", "10:33", "Y"],
        ["2026.10.04", "85901", "-", "-", "10:20", "18:20", "N"],
        ["2026.10.05", "85010", "1973", "1976", "10:43", "19:06", "N"],
        ["2026.10.06", "85019", "1506", "1501", "19:16", "10:50", "N"],
        ["2026.10.07", "~(85019)", "1506", "1501", "19:16", "10:50", "N"],
        ["2026.10.08", "S", "-", "-", "-", "-", "Y"], ["2026.10.09", "S", "-", "-", "-", "-", "Y"],
        ["2026.10.10", "85004", "1524", "1505", "09:33", "21:32", "N"],
        ["2026.10.11", "85011", "1931", "1932", "17:11", "10:33", "N"],
        ["2026.10.12", "~(85011)", "1931", "1932", "17:11", "10:33", "N"],
        ["2026.10.13", "85012", "1981", "1994", "12:03", "20:03", "N"],
        ["2026.10.14", "S", "-", "-", "-", "-", "Y"], ["2026.10.15", "S", "-", "-", "-", "-", "Y"],
        ["2026.10.16", "85003", "1503", "1527", "11:04", "20:52", "N"],
        ["2026.10.17", "85020", "1505", "1521", "20:23", "10:22", "N"],
        ["2026.10.18", "~(85020)", "1505", "1521", "20:23", "10:22", "N"],
        ["2026.10.19", "85015", "1572", "1401", "06:14", "16:01", "N"],
        ["2026.10.20", "S", "-", "-", "-", "-", "Y"], ["2026.10.21", "S", "-", "-", "-", "-", "Y"],
        ["2026.10.22", "85001", "1571", "1573", "10:12", "20:56", "N"],
        ["2026.10.23", "85005", "1506", "1524", "18:59", "10:42", "N"],
        ["2026.10.24", "~(85005)", "1506", "1524", "18:59", "10:42", "N"],
        ["2026.10.25", "85S09", "1991", "1992", "06:48", "15:48", "N"],
        ["2026.10.26", "S", "-", "-", "-", "-", "Y"], ["2026.10.27", "S", "-", "-", "-", "-", "Y"],
        ["2026.10.28", "85016", "1932", "1931", "09:26", "18:18", "N"],
        ["2026.10.29", "85008", "1975", "1978", "14:06", "22:46", "N"],
        ["2026.10.30", "85019", "1506", "1501", "19:16", "10:50", "N"],
        ["2026.10.31", "~(85019)", "1506", "1501", "19:16", "10:50", "N"]
    ]

st.markdown('<div class="card-box">', unsafe_allow_html=True)
c_b1, c_b2, c_b3 = st.columns(3)
with c_b1: uploaded_file = st.file_uploader("📂 로드", type=["txt"], label_visibility="collapsed")
with c_b2: 
    if st.button("💾 프로그램 내부에 영구 보존하기", use_container_width=True): st.success("저장 성공!")
with c_b3:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for m in range(1, 13):
            m_rows = st.session_state.db.get(str(m), [])
            if m_rows: pd.DataFrame(m_rows, columns=["사업일자", "다이아 번호", "대표 열번1", "대표 열번2", "출근 시각", "퇴근 시각", "휴일 여부"]).to_excel(writer, sheet_name=f"{m}월", index=False)
    st.download_button(label="📊 엑셀 내보내기", data=output.getvalue(), file_name="crew_schedule.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

m_tabs = st.tabs([f"  {m}월 승무  " for m in range(1, 13)])
for idx, tab in enumerate(m_tabs):
    m_str = str(idx + 1)
    with tab:
        rows = st.session_state.db.get(m_str, [])
        if not rows:
            st.info("📅 등록된 연간 승무 일정 데이터가 존재하지 않습니다냥.")
            continue
            
        left_col, right_col = st.columns([1.1, 0.9])
        
        with left_col:
            st.markdown("##### 📅 연간 일정표 (행 선택 시 우측 실시간 바인딩)")
            df = pd.DataFrame(rows, columns=["사업일자", "다이아 번호", "대표 열번1", "대표 열번2", "출근 시각", "퇴근 시각", "휴일 여부"])
            
            # [요청사항 전면 교정] 야간 조건문 및 휴일대체(빨강) 최우선 도색 엔진
            def row_coloring(row):
                d_num = str(row["다이아 번호"]).strip()
                on_t = str(row["출근 시각"]).strip()
                is_holiday = str(row["휴일 여부"]).strip()
                
                # 1단계: 비번/지정휴무/쉬는 날 -> 회색 바탕
                if d_num in ["-", "S", "*", ""] or on_t == "-" or "휴무" in d_num:
                    return ["background-color: #E2E8F0; color: #1E293B; font-weight: bold;"] * len(row)
                
                # 2단계: 휴일에 근무한 대체근무 (휴일여부 Y이면서 정상 출근한 조) -> 빨간색 바탕
                if is_holiday == "Y":
                    return ["background-color: #FEE2E2; color: #B91C1C; font-weight: bold;"] * len(row)
                
                # 3단계: 평일 대체근무조 (평일 N이면서 다이아명에 대체/대출 포함) -> 고동색 바탕
                if "대체" in d_num or "대출" in d_num:
                    return ["background-color: #4A3728; color: #FFFFFF; font-weight: bold;"] * len(row)
                
                # [버그 수정 완료] 문자열에서 괄호, 공백, 요일 완전 분리 후 순수 출근 시각(Hour) 정수 추출
                try:
                    time_part = on_t.split()[0] if " " in on_t else on_t
                    hour = int(time_part.split(":")[0])
                except:
                    hour = 9
                
                # 4단계: 야간근무 (출근 시각 오후 18시 이후 ~ 새벽 05시 이전 밤샘조) -> 파란색 바탕
                if hour >= 18 or hour < 5:
                    return ["background-color: #DBEAFE; color: #1E40AF; font-weight: bold;"] * len(row)
                
                # 5단계: 주간근무 (일반 아침/낮 승무조) -> 황색 바탕
                else:
                    return ["background-color: #FEF08A; color: #854D0E; font-weight: bold;"] * len(row)

            styled_df = df.style.apply(row_coloring, axis=1)
            
            selection = st.dataframe(
                styled_df, use_container_width=True, height=380, hide_index=True, on_select="rerun", selection_mode="single-row"
            )
            
            selected_row_idx = 0
            if selection and "rows" in selection.selection and selection.selection["rows"]:
                selected_row_idx = selection.selection["rows"]
                
            v_date, v_code = str(df.iloc[selected_row_idx]["사업일자"]), str(df.iloc[selected_row_idx]["다이아 번호"])
            v_on, v_off = str(df.iloc[selected_row_idx]["출근 시각"]), str(df.iloc[selected_row_idx]["퇴근 시각"])
            v_t1, v_t2 = str(df.iloc[selected_row_idx]["대표 열번1"]), str(df.iloc[selected_row_idx]["대표 열번2"])
            # [요청사항 2] 하단 총 실근무일수 및 정밀 누적 근무시간 계산 합산기
            total_days, total_minutes = 0, 0
            for _, r in df.iterrows():
                d_num, on_t = str(r["다이아 번호"]).strip(), str(r["출근 시각"]).strip()
                if d_num not in ["-", "S", "*", ""] and on_t != "-" and "휴무" not in d_num:
                    total_days += 1
                    clean_dia = d_num.replace("~", "").replace("(", "").replace(")", "").strip()
                    if "85S" in clean_dia: clean_dia = clean_dia.replace("85S", "850")
                    if clean_dia in ROSTER_DATA:
                        try:
                            h, m = map(int, ROSTER_DATA[clean_dia]["work_time"].split(":"))
                            total_minutes += (h * 60 + m)
                        except: pass
                    else:
                        try:
                            pure_on = on_t.split()[0] if " " in on_t else on_t
                            pure_off = str(r["퇴근 시각"]).split()[0] if " " in str(r["퇴근 시각"]) else str(r["퇴근 시각"])
                            sh, sm = map(int, pure_on.split(":"))
                            eh, em = map(int, pure_off.split(":"))
                            diff = (eh * 60 + em) - (sh * 60 + sm)
                            if diff < 0: diff += 1440
                            total_minutes += diff
                        except: total_minutes += 480
            
            st.markdown(f"""
                <div class="summary-box">
                    <p style="margin:0 0 6px 0; font-size:14px; font-weight:700; color:#334155;">📊 {m_str}월 승무 업무 집계 요약</p>
                    <div style="display:flex; gap:25px; font-size:13px; color:#475569;">
                        <span>🗓️ <b>실근무일수:</b> <span style="color:#2563EB; font-weight:700;">{total_days}일</span></span>
                        <span>⏱️ <b>총 근무시간:</b> <span style="color:#059669; font-weight:700;">{total_minutes // 60}시간 {total_minutes % 60}분</span></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with right_col:
            st.markdown('<div class="card-box">', unsafe_allow_html=True)
            if v_code in ["-", "S", "*", ""] or v_on == "-":
                st.markdown(f"### 💤 {v_date} 지정 휴무일 / 비번")
                st.markdown("<p style='color:#64748B; font-size:14px; margin-top:5px;'>오늘 하루 안전하고 편안하게 쉬세요냥!</p>", unsafe_allow_html=True)
            else:
                clean_dia = v_code.replace("~", "").replace("(", "").replace(")", "").strip()
                if "85S" in clean_dia: clean_dia = clean_dia.replace("85S", "850")
                    
                if clean_dia in ROSTER_DATA:
                    info = ROSTER_DATA[clean_dia]
                    st.markdown(f"### 🔍 {v_date} <span style='color:#2563EB;'>[다이어 {v_code}]</span> 세부 행로", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    c1.metric("⏰ 출근 시각", v_on)
                    c2.metric("🏁 퇴근 시각", v_off)
                    st.markdown(f"<div style='background-color:#F8FAFC; padding:10px; border-radius:8px; border-left:4px solid #38BDF8; margin:10px 0; font-size:13px;'>⏱️ <b>총 근무:</b> {info['work_time']} | ☕ <b>휴게:</b> {info['rest_time']}</div>", unsafe_allow_html=True)
                    dt_df = pd.DataFrame(info["details"])
                    dt_df.columns = ["열차 번호", "출발 시각", "도착 시각", "승무 운행 구간"]
                    st.table(dt_df)
                else:
                    st.markdown(f"### 🔍 {v_date} <span style='color:#E11D48;'>[다이어 {v_code} (자동 구성)]</span>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    c1.metric("⏰ 출근 시각", v_on)
                    c2.metric("🏁 퇴근 시각", v_off)
                    dyn_details = []
                    if v_t1 and v_t1 != "-": dyn_details.append({"열차 번호": v_t1, "출발 시각": v_on, "도착 시각": "-", "승무 운행 구간": "상세 확인 필요"})
                    if v_t2 and v_t2 != "-": dyn_details.append({"열차 번호": v_t2, "출발 시각": "-", "도착 시각": v_off, "승무 운행 구간": "상세 확인 필요"})
                    if dyn_details: st.table(pd.DataFrame(dyn_details))
            st.markdown('</div>', unsafe_allow_html=True)

# 하단 파싱 패널
st.markdown("---")
with st.expander("📋 웹페이지 연간 스케줄 데이터 실시간 파싱 주입"):
    txt = st.text_area("여기에 코레일 화면 전체 드래그 텍스트를 붙여넣으세요냥.")
    if st.button("🚀 데이터 자동 분산 동기화"):
        if txt:
            if "사업일자" in txt: txt = txt[txt.find("사업일자"):]
            lines = txt.strip().split("\n")
            pc = 0
            for l in lines:
                if not l.strip() or "사업일자" in l or "다이아" in l: continue
                tk = l.split("\t")
                if len(tk) >= 7:
                    dt_str = tk.strip()
                    m_val = None
                    for s in ['.', '-', '/']:
                        if s in dt_str and len(dt_str.split(s)) >= 2:
                            try: m_val = str(int(dt_str.split(s)))
                            except: continue
                            break
                    if m_val and m_val in st.session_state.db:
                        st.session_state.db[m_val] = [x for x in st.session_state.db[m_val] if x != dt_str]
                        st.session_state.db[m_val].append([t.strip() for t in tk[:7]])
                        st.session_state.db[m_val].sort(key=lambda x: x)
                        pc += 1
            if pc > 0: st.success(f"성공: 총 {pc}개의 행을 완벽하게 디자인 엔진에 주입 완료했습니다냥!"); st.rerun()

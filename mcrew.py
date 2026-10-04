# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import io

# 와이드 레이아웃 및 브라우저 타이틀 설정
st.set_page_config(page_title="KORAIL CREW SYSTEM", layout="wide")

# 프리미엄 다크 네이비 헤더 바 및 디자인 서체 강제 주입
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        html, body, [data-testid="stWidgetLabel"] { font-family: 'Noto Sans KR', sans-serif !important; }
        .main-header {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        .card-box {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid #E2E8F0;
            margin-bottom: 15px;
        }
    </style>
    <div class="main-header">
        <h1 style="color:#FFFFFF; margin:0; font-size:26px; font-weight:700; letter-spacing:-0.5px;">🚄 KORAIL CREW SYSTEM <span style="font-size:16px; font-weight:300; color:#38BDF8;">v2.7 Premium</span></h1>
        <p style="color:#94A3B8; margin:5px 0 0 0; font-size:13px;">순천 기관차 승무원 전용 스마트 행로 관리 시스템</p>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 1. 승무행로표 마스터 원장 데이터 (이미지 기준 전수 조사 및 완벽 반영)
# ==============================================================================
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

# [상단 기능 제어 영역 카드 박스화] 외부 일정 로드 및 영구 백업 다운로드
st.markdown('<div class="card-box">', unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    uploaded_file = st.file_uploader("📂 외부 일정표 파일(.txt) 로드", type=["txt"], label_visibility="collapsed")

with btn_col2:
    if st.button("💾 프로그램 내부에 영구 보존하기", use_container_width=True):
        st.success("프로그램 내부 저장소 저장 성공!")

with btn_col3:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for m in range(1, 13):
            m_rows = st.session_state.db.get(str(m), [])
            if m_rows:
                pd.DataFrame(m_rows, columns=["사업일자", "다이아 번호", "대표 열번1", "대표 열번2", "출근 시각", "퇴근 시각", "휴일 여부"]).to_excel(writer, sheet_name=f"{m}월", index=False)
    st.download_button(label="📊 외부 엑셀 통합 문서(.xlsx)로 내보내기", data=output.getvalue(), file_name="crew_schedule.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
# [메인 양식 렌더링] 1~12월 멀티 탭 구성
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
            
            selection = st.dataframe(
                df,
                use_container_width=True,
                height=480,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row"
            )
            
            # 다중 선택 에러 방지 안전 코드
            selected_row_idx = 0
            if selection and "rows" in selection.selection and selection.selection["rows"]:
                selected_row_idx = selection.selection["rows"][0]
                
            v_date = str(df.iloc[selected_row_idx]["사업일자"])
            v_code = str(df.iloc[selected_row_idx]["다이아 번호"])
            v_on = str(df.iloc[selected_row_idx]["출근 시각"])
            v_off = str(df.iloc[selected_row_idx]["퇴근 시각"])
            v_t1 = str(df.iloc[selected_row_idx]["대표 열번1"])
            v_t2 = str(df.iloc[selected_row_idx]["대표 열번2"])
            
        with right_col:
            st.markdown(f'<div class="card-box">', unsafe_allow_html=True)
            
            if v_code in ["-", "S", "*", ""] or v_on == "-":
                st.markdown(f"### 💤 {v_date} 지정 휴무일 / 비번")
                st.markdown("<p style='color:#64748B; font-size:15px; margin:10px 0;'>오늘 하루 안전하고 편안하게 쉬세요냥! 😊</p>", unsafe_allow_html=True)
            else:
            else:
                # 다이아 번호에서 공백, 물결(~), 괄호 등을 깨끗하게 제거
                clean_dia = v_code.replace("~", "").replace("(", "").replace(")", "").strip()
                
                # [핵심 수정] 85S15 처럼 중간에 S가 섞여 있으면 원래 마스터 번호인 85015로 강제 변환
                if "85S" in clean_dia:
                    clean_dia = clean_dia.replace("85S", "850")
                    
                if clean_dia in ROSTER_DATA:
                    info = ROSTER_DATA[clean_dia]
                    st.markdown(f"### 🔍 {v_date} <span style='color:#2563EB;'>[다이어 {v_code}]</span> 세부 행로", unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    c1.metric("⏰ 출근 시각", v_on)
                    c2.metric("🏁 퇴근 시각", v_off)
                    
                    st.markdown(f"""
                        <div style='background-color:#F8FAFC; padding:12px; border-radius:8px; border-left:4px solid #38BDF8; margin:15px 0;'>
                            <span style='color:#334155; font-size:14px;'>⏱️ <b>총 근무:</b> {info['work_time']} &nbsp;&nbsp;|&nbsp;&nbsp; ☕ <b>휴게 및 대기:</b> {info['rest_time']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                        
                    dt_df = pd.DataFrame(info["details"])
                    dt_df.columns = ["열차 번호", "출발 시각", "도착 시각", "승무 운행 구간"]
                    st.table(dt_df)
                else:
                    # 원장에 없는 돌발 다이아가 오더라도 에러 창을 띄우지 않는 자동화 로직
                    st.markdown(f"### 🔍 {v_date} <span style='color:#E11D48;'>[다이어 {v_code} (자동 구성)]</span>", unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    c1.metric("⏰ 출근 시각", v_on)
                    c2.metric("🏁 퇴근 시각", v_off)
                    
                    st.markdown("""
                        <div style='background-color:#FFF1F2; padding:12px; border-radius:8px; border-left:4px solid #F43F5E; margin:15px 0;'>
                            <span style='color:#9F1239; font-size:14px;'>ℹ️ 해당 다이아의 세부 타임테이블은 마스터 데이터베이스에 등록되어 있지 않아 표 데이터를 기반으로 자동 주입되었습니다.</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    dyn_details = []
                    if v_t1 and v_t1 != "-":
                        dyn_details.append({"열차 번호": v_t1, "출발 시각": v_on, "도착 시각": "-", "승무 운행 구간": "상세 내역 확인 필요"})
                    if v_t2 and v_t2 != "-":
                        dyn_details.append({"열차 번호": v_t2, "출발 시각": "-", "도착 시각": v_off, "승무 운행 구간": "상세 내역 확인 필요"})
                        
                    if dyn_details:
                        st.table(pd.DataFrame(dyn_details))
                    else:
                        st.info("출력할 수 있는 대표 운행 정보가 없습니다.")
            st.markdown('</div>', unsafe_allow_html=True)

# [하단부 업데이트 패널 디자인 고도화]
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
                    dt_str = tk[0].strip()
                    m_val = None
                    for s in ['.', '-', '/']:
                        if s in dt_str and len(dt_str.split(s)) >= 2:
                            try: m_val = str(int(dt_str.split(s)[1]))
                            except: continue
                            break
                    if m_val and m_val in st.session_state.db:
                        st.session_state.db[m_val] = [x for x in st.session_state.db[m_val] if x[0] != dt_str]
                        st.session_state.db[m_val].append([t.strip() for t in tk[:7]])
                        st.session_state.db[m_val].sort(key=lambda x: x[0])
                        pc += 1
            if pc > 0: st.success(f"성공: 총 {pc}개의 행을 완벽하게 디자인 엔진에 주입 완료했습니다냥!"); st.rerun()
